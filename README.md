# Room Reservation / API
## Live demo
You can test live demo here: [Room Reservation / API](https://RoomRes.ir)
### Users:
room_user:
username: test_1
password: adminadmin
room manager:
username: test_2
password: adminadmin
admin, room manager and room user:
username: test_3
password: adminadmin
## How to run
1. Clone the project
2. Open terminal and create a virtual environment:
<br />```virtualenv venv```
3. Activate virtual environment:
<br />```source venv/bin/activate```
4. Install packages:
<br />```pip install -r requirements.txt```
5. Migrate and create database:
<br />```python manage.py migrate```
6. Run server:
<br />```python manage.py runserver```
7. You can run tests:
<br />```python manage.py test```
8. Open the browser and browse this URL:
<br />```127.0.0.1:8000```
## Quickstart
1. Click on ```Create Roles``` button on the navbar to create desired rols.
2. Click on ```Admin``` button on the navbar and then click on ```Add Room``` to create a room.
3. Go to homepage and reserve room.
## Api
API links are as follow:
### Token (POST request):
<br />Before using each end-point, you should get a token by using this URL.
<br />URL: ```/api/token/```
### Create User (POST request):
<br />URL: ```/api/create-user/```
<br />Data load sample: ```{
   "username":"api_test_1",
   "email":"api_test_1@gmail.com",
   "first_name":"api_test_1",
   "last_name":"api_test_1",
   "password":"adminadmin",
   "roles":[
      "Admin",
      "Room User"
   ]
}```
### List of Rooms (GET request):
<br />URL: ```/api/rooms/list/```
### Create Room (POST request):
<br />URL: ```/api/rooms/create/```
<br />Data load sample: ```{
   "name":"api_room_1",
   "number_of_seats":20,
   "time_of_availability":"2022-01-30T17:30:00+03:30"
}```
### Create Room Reserve (POST request):
<br />URL: ```/api/reserve/create/```
<br />Data load sample: ```{
   "room_id":10,
   "reserve_from":"2022-01-30T15:30:00+03:30",
   "reserve_to":"2022-01-30T17:30:00+03:30"
}```
### List of reserves (POST request):
<br />URL: ```/api/reserve/list/```
<br />Data load sample: ```{
   "room_id":7
}```
### Update room reserve (POST request):
<br />URL: ```/api/reserve/update/```
<br />Data load sample: ```{
   "reserve_id":19,
   "reserve_from":"2022-01-30T15:30:00+03:30",
   "reserve_to":"2022-01-30T17:30:00+03:30"
}```

### Cancel room reserve (POST request):
<br />URL: ```/api/reserve/cancel/```
<br />Data load sample: ```{
   "reserve_id":19
}```

