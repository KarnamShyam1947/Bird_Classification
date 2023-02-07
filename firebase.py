import pyrebase


firebaseConfig = {
  'apiKey': "AIzaSyCeQxUnLaVmiT1b-JUcQyrZRg1rk24yuWA",
  'authDomain': "fir-project-167c7.firebaseapp.com",
  'projectId': "fir-project-167c7",
  'storageBucket': "fir-project-167c7.appspot.com",
  'messagingSenderId': "652295302333",
  'appId': "1:652295302333:web:ab8cc8caecfa9ea2661bd4",
  'measurementId': "G-W9VNFPNFLR",
  'databaseURL' : ''
}

firebase = pyrebase.initialize_app(firebaseConfig)

auth = firebase.auth()

def create_user(email, password):
    result = ''
    try:
        user = auth.create_user_with_email_and_password(email, password)
        return user

    except:
        return None


def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return user

    except:
        return None

def main():
    pass

if __name__ == '__main__' : 
    main()
