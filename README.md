# password_manager

# AuthApp

python version - 3.8.10
django version - 3.2.5


## Setup
  - Setup virtual environment
  ```sh
  virtualenv -p python3.8 venv
  ```

   ```sh
  source venv/bin/activate
  ```

  - start application
    ```sh
  pip install -r requirements.txt
  ```
  - migrate db
  ```sh
  python manage.py makemigrations
  ```
    ```sh
    python manage.py migrate
    ```
  - run application

    ```sh
    python manage.py runserver
    ```

# How it works

create a super admin in django using command
`python manage.py createsuperuser`
admin url endpoint: /admin
Use django admin panel for
1. creating `admin` group
2. assigning user to `admin` group.


API Functionalities

1. /apis/token/
user can login using this endpoint. User will get a JWT Bearer token after login
add that token in Authorization header

2. apis/orgainzation/
create organization
Only superadmin can create organization

3. apis/user/
any user can create account under selected organization
authorized users can view users under same organization using the same endpoing with get method
A user can view details of all the users under their own organization but can’t edit other user's details

4. apis/manage-user/<user-id>/ 
Only admin of same organization can delete user
admin of same organization can edit other users password current user can also update their own password

 
5. apis/token/refresh/
to generate a new access token using refresh token