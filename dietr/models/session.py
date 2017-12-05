class SessionModel:
    '''
    The session model.
    '''
    def generate_hash():
        pass

    def get_hash(password, salt):
        pass

    def get_salt():
        pass

    def add_user(user):
        pass

    def get_user(username):
        user = {
            'username': username,
            'hash': 0x00,
            'salt': 0x00,
            'email': 'example@domain.com',
            'name': {
                'first_name': 'John',
                'middle_name': None,
                'last_name': 'Doe'
            }
        }

        return user
