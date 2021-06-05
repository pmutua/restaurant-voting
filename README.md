# Restaurant Menu Voting API

This is a REST API for voting restaurant menus.


## Getting Started


### Development

Uses the default Django development server.

1. Update the environment variables in the **docker-compose.yml** and **.env.dev**.

**.env.dev** Example



```
    DEBUG=1
    SECRET_KEY=foo
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=postgres
    SQL_USER=postgres
    SQL_PASSWORD=postgres
    SQL_HOST=db
    SQL_PORT=5432
    DATABASE=postgres
    EMAIL_HOST_PASSWORD=<Add sndgrid email host Here>
    LOGIN_REDIRECT_URL=<Add login redirect Here>
    CLOUDINARY_CLOUD_NAME=<Add Cloudinary Name Here>
    CLOUDINARY_API_KEY=<Add Cloudinary API Key Here>
    CLOUDINARY_API_SECRET=<Add Cloudinary API Secret Here>
```

2. Build the images and run the containers:

    `$ docker-compose up -d --build`


3. Create migrations and apply them into database. NOTE the containers must be running: 

    `$ docker-compose exec web python manage.py makemigrations`
    `$ docker-compose exec web python manage.py migrate`


4. Test it out at http://localhost:8000. The "app" folder is mounted into the container and your code changes apply automatically.

#### Running Tests in Development 

`$ docker-compose exec web python manage.py test`
    
NOTE: Before you execute the command above. The containers must me up an running.
    


### Production

Uses **gunicorn** and  **nginx**.

1. Update the environment variables in **.env.prod** and **.env.prod.db**


**.env.prod** Example
```
    DEBUG=0
    SECRET_KEY=foo
    DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
    SQL_ENGINE=django.db.backends.postgresql
    SQL_DATABASE=postgres
    SQL_USER=postgres
    SQL_PASSWORD=postgres
    SQL_HOST=db
    SQL_PORT=5432
    DATABASE=postgres
    EMAIL_HOST_PASSWORD=<Add sndgrid email host Here>
    LOGIN_REDIRECT_URL=<Add login redirect Here>
    CLOUDINARY_CLOUD_NAME=<Add Cloudinary Name Here>
    CLOUDINARY_API_KEY=<Add Cloudinary API Key Here>
    CLOUDINARY_API_SECRET=<Add Cloudinary API Secret Here>
```



**.env.prod.db** Example
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```

2. Build the images and run the containers:

    `$ docker-compose -f docker-compose.prod.yml up -d --build`
    
    
    Test it out at http://localhost:1337. No mounted folders. To apply changes, the image must be re-built.

    $ docker-compose -f docker-compose.prod.yml down -v


The API has been intergrated with third party services namely:

1. Sendgrid - Handles Emailing [Check out here how to intergrate sendgrid with Django](https://sendgrid.com/docs/for-developers/sending-email/django/)
2. Cloudinary - Handles File Storage [Check oout here how to intergrate Cloudinary with Django](https://cloudinary.com/documentation/django_integration)

## API Features

1. Authentication
2. Creating restaurant
3. Uploading menu for restaurant (There should be a menu for each day)
4. Creating employee
5. Getting current day menu
6. Voting for restaurant menu
7. Getting results for the current day. The winner restaurant should not be the winner for 3 consecutive working days
8. Logout


### Dependencies Used

1. Django==3.1.7
2. djangorestframework==3.12.4
3. Markdown==3.3.4
4. django-filter==2.4.0
5. djangorestframework-jwt==1.11.0
6. PyJWT==1.5.2
7. django-cors-headers==3.6.0
8. cloudinary==1.24.0
9. dj3-cloudinary-storage==0.0.3
10. gunicorn==19.9.0
11. Pillow >= 8.0
12. coverage==5.5
13. python-decouple==3.4
14. pycodestyle==2.7.0
15. autopep8==1.5.7
16. flake8
17. mock==4.0.3
18. psycopg2-binary>=2.8

[View all the other dependencies](./app/requirements.txt)

## API Endpoints

Some endpoints require a token for authentication. The API call should have the token in Authorization header.

    `{'Authorization': 'Bearer': <token>}`




| EndPoint                                        |                       Functionality |
| ------------------------------------------------|-----------------------------------: |
| POST /api/register_user/                        |                Register a user      |
| POST /api/create_employee/                      |         Creates a new employee      |
| POST /api/login/                                |                     User login      |
| GET /api/logout/                                |                    Logout user      |
| GET /api/restaurants/                           |            List all restaurants     |
| GET /api/menu_list/                             |   List all menus of current day     |
| GET /api/vote/:id/                              |                       Vote menu     |
| GET /api/results/                               |         Show results of the day     |


## Responses

The API responds with JSON data by default.


## Request examples

Request GET /api/results/

curl -H "Authorization: Bearer <your_token>" -H "Content-Type: application/json" https://localhost:8000/api/results/

















































