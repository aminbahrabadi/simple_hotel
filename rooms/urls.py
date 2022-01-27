from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    # room
    path('create/', views.RoomCreateView.as_view(), name='room_create'),
    path('detail/<int:room_id>/', views.RoomDetailView.as_view(), name='room_detail'),

    # reserve
    path('reserve/create/<int:room_id>/', views.RoomReserveCreateView.as_view(),
         name='room_reserve_create'),
    path('reserve/edit/<int:reserve_id>/', views.RoomReserveUpdateView.as_view(),
         name='room_reserve_edit'),
    path('reserve/cancel/<int:room_id>/<int:reserve_id>/', views.RoomReserveCancelRedirectView.as_view(),
         name='room_reserve_cancel')

]
