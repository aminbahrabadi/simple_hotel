from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError

from rooms.models import Room

User = get_user_model()


class CreateUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=155, required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(max_length=255, required=True)
    last_name = serializers.CharField(max_length=255, required=True)
    password = serializers.CharField(required=True)
    roles = serializers.ListField(required=True)

    def validate(self, attrs):
        errors = {}
        password = attrs.get('password')
        if password:
            try:
                password_validation.validate_password(password)

            except ValidationError as e:
                errors['password'] = list(e.messages)

        username = attrs.get('username')
        if username:
            is_duplicated = User.objects.filter(username=username).exists()

            if is_duplicated:
                errors['username'] = 'username already exists'

        if errors:
            raise serializers.ValidationError(errors)

        return super(CreateUserSerializer, self).validate(attrs)


class RoomReserveSerializer(serializers.Serializer):
    room_id = serializers.IntegerField(required=True)
    reserve_from = serializers.DateTimeField(required=True)
    reserve_to = serializers.DateTimeField(required=True)


class RoomReserveListSerializer(serializers.Serializer):
    room_id = serializers.IntegerField(required=True)


class RoomReserveUpdateSerializer(serializers.Serializer):
    reserve_id = serializers.IntegerField(required=True)
    reserve_from = serializers.DateTimeField(required=True)
    reserve_to = serializers.DateTimeField(required=True)


class RoomCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['name', 'number_of_seats', 'time_of_availability']


class RoomReserveCancelSerializer(serializers.Serializer):
    reserve_id = serializers.IntegerField(required=True)
