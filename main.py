# main.py
import requests
from kivy.lang import Builder
from urllib.parse import quote, quote_plus
from kivymd.app import MDApp
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from firebase import firebase
from kivy.network.urlrequest import UrlRequest

Window.size = (310, 580)


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
        # Initialize Firebase
        self.firebase = firebase.FirebaseApplication(
            'https://loginforumic-default-rtdb.firebaseio.com/', None
        )

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
            # Clean the email by replacing special characters
            clean_email = email.replace('.', '_dot_').replace('@', '_at_')

            # Properly encode the email for the URL
            encoded_email = quote(email, safe='')

            # Your Firebase URL
            firebase_url = f'https://loginforumic-default-rtdb.firebaseio.com/users/{encoded_email}.json'

            # Check if the user already exists
            response = requests.get(firebase_url)
            if response.status_code == 200 and response.json() is not None:
                print("User already exists")
                return

            # If the user doesn't exist, create a new account
            user_data = {
                'username': username,
                'email': email,
                'password': password
            }

            response = requests.put(firebase_url, json=user_data)

            if response.status_code == 200:
                print("Signup successful!")
            else:
                print(f"An error occurred: {response.status_code}")
                print("Response content:", response.content.decode())

        except Exception as e:
            print(f"An error occurred: {e}")

    def signup(self, username, email, password):
        try:
            # Properly encode the email for the URL
            encoded_email = quote_plus(email)

            # Your Firebase URL
            firebase_url = f'https://loginforumic-default-rtdb.firebaseio.com/users/{encoded_email}.json'

            # Check if the user already exists
            response = requests.get(firebase_url)
            if response.status_code == 200 and response.json() is not None:
                print("User already exists")
                return

            # If the user doesn't exist, create a new account
            user_data = {
                'username': username,
                'email': email,
                'password': password
            }

            # Use UrlRequest to handle URL encoding
            UrlRequest(firebase_url, method='PUT', req_body=user_data)

            print("Signup successful!")

        except Exception as e:
            print(f"An error occurred during signup: {e}")
            import traceback
            traceback.print_exc()

    def handle_login(self, email, password):
        try:
            # Clean the email by replacing special characters
            clean_email = email.replace('.', '_dot_').replace('@', '_at_')

            # Your Firebase URL
            firebase_url = f'https://loginforumic-default-rtdb.firebaseio.com/users/{clean_email}.json'

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


if __name__ == "__main__":
    LabelBase.register(name="MPoppins", fn_regular="C:\\Users\\oiali\\PycharmProjects\login\\fonts\\Poppins-Medium.ttf")
    LabelBase.register(name="BPoppins",
                       fn_regular="C:\\Users\\oiali\\PycharmProjects\login\\fonts\\Poppins-SemiBold.ttf")

    DemoApp().run()
