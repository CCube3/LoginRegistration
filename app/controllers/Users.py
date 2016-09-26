from system.core.controller import *
class Users(Controller):
    def __init__(self, action):
        super(Users, self).__init__(action)
        # Note that we have to load the model before using it in the methods below
        self.load_model('User')
    # method to display registration page
    def index(self):
        return self.load_view('index.html')

    def success(self):
        return self.load_view('success.html')

    # def new(self):
    #     return self.load_view('users/new.html')
    # method to create a user
    def create(self):
        # gather data posted to our create method and format it to pass it to the model
        user_info = {
             "firstname" : request.form['firstname'],
             "lastname" : request.form['lastname'],
             "alias" : request.form['alias'],
             "date_of_birth" : request.form['date_of_birth'],
             "email" : request.form['email'],
             "password" : request.form['password'],
             "pw_confirmation" : request.form['pw_confirmation']
        }
        # # call create_user method from model and write some logic based on the returned value
        # # notice how we passed the user_info to our model method
        create_status = self.models['User'].create_user(user_info)
        if create_status['status'] == True:
            # the user should have been created in the model
            # we can set the newly-created users id and name to session
            session['id'] = create_status['user']['id']
            session['firstname'] = create_status['user']['firstname']
            # we can redirect to the users profile page here
            return redirect('/success')
        else:
            # set flashed error messages here from the error messages we returned from the Model
            for message in create_status['errors']:   # message = key, create_status['errors'] = error hash object
                flash(create_status['errors'][message], message)
                #flash(flash_message_message, flash_message_category);   flhas-message-message is what I want to display, flash_message_category is where I want to display it.
            # redirect to the method that renders the form
        return redirect('/')

    def login(self):
        print "login working"

        user_info = {
            "email": request.form['email'],
            "password": request.form['password']
        }

        login_status = self.models['User'].login_user(user_info)
        if login_status['status'] == True:

            session['id'] = login_status['user']['id']
            session['firstname'] = login_status['user']['firstname']
            # we can redirect to the users profile page here
            return redirect('/success')
        else:
            # set flashed error messages here from the error messages we returned from the Model
            for message in login_status['errors']:   # message = key, create_status['errors'] = error hash object
                flash(login_status['errors'][message], message)
                #flash(flash_message_message, flash_message_category);   flhas-message-message is what I want to display, flash_message_category is where I want to display it.
            # redirect to the method that renders the form
        return redirect('/')
