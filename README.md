# Room Reservation / API
## Live demo
You can test live demo here: [Room Reservation / API](https://ResRoom.ir)
### Default user:
username: admin
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
<br />URL: ```create-user/```
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
