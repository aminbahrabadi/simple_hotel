import pytz

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone

from accounts.constants import roles
from accounts.models import Role
from rooms.models import Room, Reserve
from rooms.functions import room_is_available
from .permissions import has_required_role
from .serializers import (CreateUserSerializer, RoomReserveSerializer,
                          RoomReserveListSerializer, RoomReserveUpdateSerializer,
                          RoomCreateSerializer, RoomReserveCancelSerializer)


User = get_user_model()


class ApiUserCreate(APIView):
    roles_required = [roles.get('admin')]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not has_required_role(request.user, self.roles_required):
            return Response('you do not have access to this Api',
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = CreateUserSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            first_name = serializer.validated_data.get('first_name')
            last_name = serializer.validated_data.get('last_name')
            password = serializer.validated_data.get('password')
            user_roles_list = serializer.validated_data.get('roles')

            user = User.objects.create(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name
            )

            user.set_password(password)
            user.save()

            for role in user_roles_list:
                if Role.objects.filter(name=role).exists():
                    user.profile.roles.add(Role.objects.get(name=role))
                    user.profile.save()

            return Response('{} is created!'.format(user.username), status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiRoomList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tehran_tz = pytz.timezone('Asia/Tehran')
        rooms = Room.objects.all()
        rooms_dict = {}

        for room in rooms:
            rooms_dict[room.name] = {}
            rooms_dict[room.name]['id'] = room.id
            rooms_dict[room.name]['name'] = room.name
            rooms_dict[room.name]['number_of_seats'] = room.number_of_seats
            rooms_dict[room.name]['available_from'] = room.time_of_availability.replace(tzinfo=tehran_tz)

        return Response(rooms_dict, status=status.HTTP_200_OK)


class ApiReserveRoom(APIView):
    roles_required = [roles.get('room_user')]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not has_required_role(request.user, self.roles_required):
            return Response('you do not have access to this Api',
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = RoomReserveSerializer(data=request.data)

        if serializer.is_valid():
            room_id = serializer.validated_data.get('room_id')
            reserve_from = serializer.validated_data.get('reserve_from')
            reserve_to = serializer.validated_data.get('reserve_to')

            room = Room.objects.filter(id=room_id)
            if room.exists():
                room = room.get()
            else:
                return Response('room not found', status=status.HTTP_404_NOT_FOUND)

            now = timezone.now()

            if reserve_from < now:
                return Response('your reservation start time can not be before now',
                                status=status.HTTP_400_BAD_REQUEST)

            if reserve_from < room.time_of_availability:
                return Response('room is not available at this time',
                                status=status.HTTP_400_BAD_REQUEST)

            if not room_is_available(room, reserve_from, reserve_to):
                return Response('Room is not Available in time range you have chosen',
                                status=status.HTTP_400_BAD_REQUEST)

            Reserve.objects.create(
                room_id=room.id,
                reserved_by_id=self.request.user.id,
                reserve_from=reserve_from,
                reserve_to=reserve_to
            )

            return Response('reserve is created!', status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiRoomReserveList(APIView):
    roles_required = [roles.get('room_user'), roles.get('room_manager')]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not has_required_role(request.user, self.roles_required):
            return Response('you do not have access to this Api',
                            status=status.HTTP_400_BAD_REQUEST)

        tehran_tz = pytz.timezone('Asia/Tehran')
        serializer = RoomReserveListSerializer(data=request.data)

        if serializer.is_valid():
            room_id = serializer.validated_data.get('room_id')

            reserves = Reserve.objects.filter(room_id=room_id)

            reserves_dict = {}
            if reserves:
                for reserve in reserves:
                    reserves_dict[reserve.id] = {}
                    reserves_dict[reserve.id]['id'] = reserve.id
                    reserves_dict[reserve.id]['reserver'] = reserve.reserved_by.username
                    reserves_dict[reserve.id]['from'] = reserve.reserve_from.replace(tzinfo=tehran_tz)
                    reserves_dict[reserve.id]['to'] = reserve.reserve_to.replace(tzinfo=tehran_tz)

            return Response(reserves_dict, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiRoomReserveUpdate(APIView):
    roles_required = [roles.get('room_user')]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not has_required_role(request.user, self.roles_required):
            return Response('you do not have access to this Api',
                            status=status.HTTP_400_BAD_REQUEST)

        now = timezone.now()
        serializer = RoomReserveUpdateSerializer(data=request.data)

        if serializer.is_valid():
            reserve_id = serializer.validated_data.get('reserve_id')
            reserve_from = serializer.validated_data.get('reserve_from')
            reserve_to = serializer.validated_data.get('reserve_to')

            reserve = Reserve.objects.filter(id=reserve_id,
                                             reserved_by_id=self.request.user.id,
                                             reserve_from__gt=now)
            if reserve.exists():
                reserve = reserve.get()
                room = reserve.room
            else:
                return Response('reserve not found', status=status.HTTP_404_NOT_FOUND)

            if reserve_from < now:
                return Response('your reservation start time can not be before now',
                                status=status.HTTP_400_BAD_REQUEST)

            if reserve_from < room.time_of_availability:
                return Response('room is not available at this time',
                                status=status.HTTP_400_BAD_REQUEST)

            if not room_is_available(room, reserve.reserve_from, reserve.reserve_to, reserve.id):
                return Response('Room is not Available in time range you have chosen',
                                status=status.HTTP_400_BAD_REQUEST)

            reserve.reserve_from = reserve_from
            reserve.reserve_to = reserve_to
            reserve.save()

            return Response('reserve is updated!', status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiRoomCreate(APIView):
    roles_required = [roles.get('room_manager')]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not has_required_role(request.user, self.roles_required):
            return Response('you do not have access to this Api',
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = RoomCreateSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            number_of_seats = serializer.validated_data.get('number_of_seats')
            time_of_availability = serializer.validated_data.get('time_of_availability')

            Room.objects.create(
                name=name,
                number_of_seats=number_of_seats,
                time_of_availability=time_of_availability
            )

            return Response('room is created!', status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiRoomReserveCancel(APIView):
    roles_required = [roles.get('room_manager')]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if not has_required_role(request.user, self.roles_required):
            return Response('you do not have access to this Api',
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = RoomReserveCancelSerializer(data=request.data)

        if serializer.is_valid():
            reserve_id = serializer.validated_data.get('reserve_id')

            reserve = Reserve.objects.filter(id=reserve_id)

            if reserve.exists():
                reserve = reserve.get()
            else:
                return Response('reserve not found', status=status.HTTP_404_NOT_FOUND)

            reserve.delete()

            return Response('reserve is canceled!', status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
