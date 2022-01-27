from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


app_name = 'api'


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('create-user/', views.ApiUserCreate.as_view(), name='api_create_user'),

    path('rooms/list/', views.ApiRoomList.as_view(), name='api_rooms_list'),
    path('rooms/create/', views.ApiRoomCreate.as_view(), name='api_rooms_create'),

    path('reserve/create/', views.ApiReserveRoom.as_view(), name='api_reserve_create'),
    path('reserve/list/', views.ApiRoomReserveList.as_view(), name='api_reserve_list'),
    path('reserve/update/', views.ApiRoomReserveUpdate.as_view(), name='api_reserve_update'),
    path('reserve/cancel/', views.ApiRoomReserveCancel.as_view(), name='api_reserve_cancel'),
]
