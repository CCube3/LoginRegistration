from system.core.model import *
from flask import flash
import re # still need to import this module: we use regular expressions to validate email formats!

NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
PASSWORD_REGEX = re.compile(r'^.*[A-Z]+.*[0-9].*|.*[0-9]+.*[A-Z].*$')
EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')

class User(Model):
    def __init__(self):
        super(User, self).__init__()

    def create_user(self, info):
        password = info['password']
        # bcrypt is now an attribute of our model
        # we will call the bcrypt functions similarly to how we did before
        # here we use generate_password_hash() to generate an encrypted password
        # We write our validations in model functions.
        # They will look similar to those we wrote in Flask
        errors = {}
        # Some basic validation
        if not info['firstname']:
            errors['firstname'] = "Firstname cannot be blank"
        elif len(info['firstname']) < 2:
            errors['firstname'] = "Firstname must be at least 2 characters long"
        if not info['lastname']:
            errors['lastname'] = 'lastname cannot be blank'
        elif len(info['lastname']) < 2:
            errors['lastname'] = "Lastname must be at least 2 characters long"
        if not info['alias']:
            errors['alias'] = "Alias cannot be blank"
        if not info['date_of_birth']:
            errors['date_of_birth'] = "Date of birth cannot be blank"
        if not info['email']:
            errors['email'] = 'Email cannot be blank'
        elif not EMAIL_REGEX.match(info['email']):
            errors['email'] = 'Email format must be valid!'
        if not info['password']:
            errors['password'] = 'Password cannot be blank'
        elif len(info['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters long'
        if not info['pw_confirmation']:
            errors['pw_confirmation'] = 'Password confirmation cannot be blank!'
        elif info['password'] != info['pw_confirmation']:
            errors['pw_confirmation'] = 'Password and confirmation must match!'
        # If we hit errors, return them, else return True.
        if errors:
            return {"status": False, "errors": errors}
        else:
            hashed_pw = self.bcrypt.generate_password_hash(password)

            # Code to insert user goes here...
            create_query = "INSERT INTO users (firstname, lastname, alias, date_of_birth, password, created_at) VALUES (:firstname, :lastname, :alias, :date_of_birth, :pw_hash, NOW())"
            create_data = {'firstname': info['firstname'], 'lastname': info['lastname'], 'alias': info['alias'], 'date_of_birth': info['date_of_birth'], 'pw_hash': info['password']}
            self.db.query_db(create_query, create_data)

            # Then retrieve the last inserted user.
            get_user_query = "SELECT * FROM users ORDER BY id DESC LIMIT 1"
            users = self.db.query_db(get_user_query)
            return { "status": True, "user": users[0] }


    def login_user(self, info):
        password = info['password']
        errors = {}

        if not info['email']:
            errors['lg_email'] = 'Email cannot be blank'
        elif not EMAIL_REGEX.match(info['email']):
            errors['lg_email'] = 'Email format must be valid!'
        if not info['password']:
            errors['lg_password'] = 'Password cannot be blank'
        elif len(info['password']) < 8:
            errors['lg_password'] = 'Password must be at least 8 characters long'

        if errors:
            return {"status": False, "errors": errors}
        else:
            user_query = "SELECT * FROM users WHERE email = :email LIMIT 1"
            user_data = {'email': info['email']}
            user = self.db.get_one(user_query, user_data)
            if user:
                if self.bcrypt.check_password_hash(user.pw_hash, password):
                    return {"status": True, "user":user}
                errors['lg_password'] = 'Invalid password'
                return {"status": False, "errors": errors}
            errors['lg_email'] = 'Invalid email'
            return {"status": False, "errors": errors}

    # def get_all_users(self):
    #     return self.db.query_db("SELECT * FROM users")
    #
    # def get_user_by_id(self, user_id):
    #     # pass data to the query like so
    #     query = "SELECT * FROM users WHERE id = :user_id"
    #     data = { 'user_id': user_id}
    #     return self.db.query_db(query, data)

    # def add_user(self, user):
    #   # Build the query first and then the data that goes in the query
    #   query = "INSERT INTO users (title, description, created_at) VALUES (:title, :description, NOW())"
    #   data = { 'title': user['title'], 'description': user['description'] }
    #   return self.db.query_db(query, data)

    # def update_user(self, user):
    #   # Building the query for the update
    #   query = "UPDATE users SET title=:title, description=:description WHERE id = :user_id"
    #   # we need to pass the necessary data
    #   data = { 'title': user['title'], 'description': user['description'], 'user_id': user['id']}
    #   # run the update
    #   return self.db.query_db(query, data)
