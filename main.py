# main.py
import requests
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.core.window import Window
import pyrebase

Window.size = (310, 580)

# Configurer votre configuration Firebase ici
firebase_config = {
    "apiKey": "AIzaSyATXmGkSdu4Nvp0kgdKRvgyL05XWDRiexs",
    "authDomain": "loginforumic.firebaseapp.com",
    "projectId": "loginforumic",
    "storageBucket": "loginforumic.appspot.com",
    "messagingSenderId": "536762153558",
    "appId": "1:536762153558:web:c50b0dc91dee0c29d259f7",
    "measurementId": "G-C2SXJHP3XH",
    "databaseURL": "https://loginforumic-default-rtdb.firebaseio.com",
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

    def handle_login(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        # Call the login method with the extracted data
        app = MDApp.get_running_app()
        app.handle_login(email, password)


class DemoApp(MDApp):
    def build(self):
        Builder.load_file("main.kv")
        Builder.load_file("login.kv")
        Builder.load_file("signup.kv")

        screen_manager = ScreenManager()

        # Add screens to the screen manager
        screen_manager.add_widget(LoginScreen(name="login"))
        screen_manager.add_widget(Builder.load_file("signup.kv"))
        screen_manager.add_widget(Builder.load_file("main.kv"))

        return screen_manager

    def handle_signup(self, username, email, password):
        try:
            # Remplacez les points dans l'e-mail par "_dot_"
            clean_email = email.replace('.', '_dot_').replace(" ", "")

            # Votre chemin Firebase
            firebase_path = f'/loginForumIC/Users/{clean_email}'

            # Vérifiez si l'utilisateur existe déjà
            user_data = db.child(firebase_path).get().val()
            if user_data is not None:
                print("User already exists")
                return

            # Si l'utilisateur n'existe pas, créez un nouveau compte
            user_data = {
                'username': username,
                'email': email,
                'password': password
            }

            # Utilisez push() pour générer une clé unique pour le nouvel utilisateur
            db.child(firebase_path).set(user_data)

            print("Signup successful!")

        except Exception as e:
            print(f"An error occurred during signup: {e}")
            import traceback
            traceback.print_exc()

    def handle_login(self, email, password):
        try:
            # Supprimer les espaces de l'email
            # Clean the email by replacing special characters
            clean_email = email.replace('.', '_dot_').replace(" ", "")

            # Your Firebase URL
            firebase_url = f'https://loginforumic-default-rtdb.firebaseio.com/loginForumIC/Users/{clean_email}.json'

            # Send a GET request to Firebase
            response = requests.get(firebase_url)

            if response.status_code == 200:
                try:
                    # Try to parse JSON data from the response
                    user_data = response.json()

                    if user_data is not None:
                        if isinstance(user_data, dict):
                            # Check if the response contains the 'password' key
                            if 'password' in user_data:
                                # User found, check password or perform other actions
                                if user_data['password'] == password:
                                    print("Login successful!")
                                else:
                                    print("Invalid email or password")
                            else:
                                print("Invalid response format from Firebase")
                                print("Response content:", response.content.decode())
                        else:
                            print("Invalid response format from Firebase")
                            print("Response content:", response.content.decode())
                    else:
                        # User not found
                        print("User not found")
                except ValueError:
                    print("Error parsing JSON from Firebase response")
                    print("Response content:", response.content.decode())
            elif response.status_code == 404:
                print("User not found")
            else:
                print(f"An error occurred: {response.status_code}")
                print("Response content:", response.content.decode())

        except Exception as e:
            print(f"An error occurred: {e}")

    def password_toggle(self, password_input):
        # Toggle password visibility when the eye icon button is pressed
        password_input.password = not password_input.password
        password_input.password_mask = '•' if password_input.password else ''
        password_input.focus = True  # Maintain focus on the input field after toggle


if __name__ == "__main__":
    LabelBase.register(name="MPoppins", fn_regular="C:\\Users\\oiali\\PycharmProjects\login\\fonts\\Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins",
                       fn_regular="C:\\Users\\oiali\\PycharmProjects\login\\fonts\\Poppins-SemiBold.ttf")

    DemoApp().run()
