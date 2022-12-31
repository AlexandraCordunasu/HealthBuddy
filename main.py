import sys
sys.path.append("/".join(x for x in __file__.split("/")[:-1]))
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, NoTransition, CardTransition
from specialbuttons import ImageButton, LabelButton, ImageButtonSelectable
from kivy.properties import DictProperty
from workoutbanner import WorkoutBanner
from functools import partial
from os import walk
from myfirebase import MyFirebase
from datetime import datetime

import kivy.utils
from kivy.utils import platform
import requests
import json
import traceback
from kivy.graphics import Color, RoundedRectangle
import helperfunctions


class HomeScreen(Screen):
    pass

class AddWorkoutScreen(Screen):
    pass


class LoginScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass



#GUI =   # Make sure this is after all class definitions!
class MainApp(App):

    workout_image = None
    option_choice = None
    workout_image_widget = ""
    previous_workout_image_widget = None

    refresh_token_file = "refresh_token.txt"

    my_firebase = None  # Reference to class in myfirebase.py

    def build(self):
        print("BEFORE")
        self.my_firebase = MyFirebase()
        print(self.my_firebase)
        print("AFTER")
        if platform == 'ios':
            self.refresh_token_file = App.get_running_app().user_data_dir + self.refresh_token_file
        return Builder.load_file("main.kv")#GUI

    

    def update_workout_image(self, filename, widget_id):
        self.previous_workout_image_widget = self.workout_image_widget
        self.workout_image = filename
        self.workout_image_widget = widget_id
        # Clear the indication that the previous image was selected
        if self.previous_workout_image_widget:
            self.previous_workout_image_widget.canvas.before.clear()
        # Make sure the text color of the label above the scrollview is white (incase it was red from them earlier)
        select_workout_image_label = self.root.ids.add_workout_screen.ids.select_workout_image_label
        select_workout_image_label.color = (1, 1, 1, 1)

        # Indicate which image has been selected
        with self.workout_image_widget.canvas.before:
            Color(rgb=(kivy.utils.get_color_from_hex("#6C5B7B")))
            RoundedRectangle(size=self.workout_image_widget.size, pos=self.workout_image_widget.pos, radius = [5,])


    def on_start(self):
        # Display the ads
        if platform == 'ios':
            from pyobjus import autoclass
            self.banner_ad = autoclass('adSwitch').alloc().init()

        # Choose the correct time icon to show based on the current hour of day
        now = datetime.now()
        hour = now.hour
        if hour <= 6:
            self.root.ids['time_indicator1'].opacity = 1
        elif hour <= 12:
            self.root.ids['time_indicator2'].opacity = 1
        elif hour <= 18:
            self.root.ids['time_indicator3'].opacity = 1
        else:
            self.root.ids['time_indicator4'].opacity = 1

        # Set the current day, month, and year in the add workout section
        day, month, year = now.day, now.month, now.year
        self.root.ids.add_workout_screen.ids.month_input.text = str(month)
        self.root.ids.add_workout_screen.ids.day_input.text = str(day)
        self.root.ids.add_workout_screen.ids.year_input.text = str(year)


        # Populate workout image grid
        workout_image_grid = self.root.ids['add_workout_screen'].ids['workout_image_grid']
        for root_dir, folders, files in walk("icons/workouts"):
            for f in files:
                if '.png' in f:
                    img = ImageButton(source="icons/workouts/" + f, on_release=partial(self.update_workout_image, f))
                    workout_image_grid.add_widget(img)


        try:
            # Try to read the persistent signin credentials (refresh token)
            with open(self.refresh_token_file, 'r') as f:
                refresh_token = f.read()
            # Use refresh token to get a new idToken
            id_token, local_id = self.my_firebase.exchange_refresh_token(refresh_token)
            self.local_id = local_id
            self.id_token = id_token

            # Get database data
            print("LOCAL ID IS", local_id)
            print("https://friendly-fitness.firebaseio.com/" + local_id + ".json?auth=" + id_token)
            result = requests.get("https://friendly-fitness.firebaseio.com/" + local_id + ".json?auth=" + id_token)
            data = json.loads(result.content.decode())
            print("id token is", id_token)
            print(result.ok)
            print("DATA IS", data)
            
      
       
           
         
          
            # Get and update streak label
            streak_label = self.root.ids['home_screen'].ids['streak_label']
            #streak_label.text = str(data['streak']) + " Day Streak" # Thisis updated if there are workouts


            # Set the images in the add_workout_screen
            banner_grid = self.root.ids['home_screen'].ids['banner_grid']
            workouts = data['workouts']
            if workouts != "":
                workout_keys = list(workouts.keys())
                streak = helperfunctions.count_workout_streak(workouts)
                if str(streak) == 0:
                    streak_label.text = "Ziua 0 de activitate. Fă sport!"
                else:
                    streak_label.text = "Ziua " + str(streak) + " de activitate!"
                # Sort workouts by date then reverse (we want youngest dates at the start)
                workout_keys.sort(key=lambda value : datetime.strptime(workouts[value]['date'], "%m/%d/%Y"))
                workout_keys = workout_keys[::-1]
                for workout_key in workout_keys:
                    workout = workouts[workout_key]
                    # Populate workout grid in home screen
                    W = WorkoutBanner(workout_image=workout['workout_image'], description=workout['description'],
                                      type_image=workout['type_image'], number=workout['number'], units=workout['units'],
                                      likes=workout['likes'], date=workout['date'])
                    banner_grid.add_widget(W)

            self.change_screen("home_screen", "None")

        except Exception as e:
            traceback.print_exc()
            pass

   
    def sign_out_user(self):
        # User wants to log out
        with open(self.refresh_token_file, 'w') as f:
            f.write("")
        self.change_screen("login_screen", direction='down', mode='push')
        # Need to set the avatar to the default image
        avatar_image = self.root.ids['avatar_image']
        avatar_image.source = "icons/avatars/man.png"


        # Clear home screen
        self.root.ids.home_screen.ids.streak_label.text = "Ziua 0 de activitate. Fă sport!"

        # Clear login screen
        self.root.ids.login_screen.ids.login_email.text = ""
        self.root.ids.login_screen.ids.login_password.text = ""

        # Clear workout screen
        workout_screen = self.root.ids.add_workout_screen
        workout_screen.ids.description_input.text = ""
        workout_screen.ids.time_label.color = (0,0,0,1)
        workout_screen.ids.distance_label.color = (0,0,0,1)
        workout_screen.ids.sets_label.color = (0,0,0,1)
        workout_screen.ids.quantity_input.text = ""
        workout_screen.ids.quantity_input.background_color = (1,1,1,1)
        workout_screen.ids.units_input.text = ""
        workout_screen.ids.units_input.background_color = (1,1,1,1)
        now = datetime.now()
        day, month, year = now.day, now.month, now.year
        workout_screen.ids.month_input.text = str(month)
        workout_screen.ids.month_input.background_color = (1,1,1,1)
        workout_screen.ids.day_input.text = str(day)
        workout_screen.ids.day_input.background_color = (1,1,1,1)
        workout_screen.ids.year_input.text = str(year)
        workout_screen.ids.year_input.background_color = (1,1,1,1)


        self.workout_image = None
        self.option_choice = None
        # Clear the indication that the previous image was selected
        if self.workout_image_widget:
            self.workout_image_widget.canvas.before.clear()
        # Make sure the text color of the label above the scrollview is white (incase it was red from them earlier)
        select_workout_image_label = workout_screen.ids.select_workout_image_label
        select_workout_image_label.color = (1, 1, 1, 1)





   
    def add_workout(self):
        # Get data from all fields in add workout screen
        workout_ids = self.root.ids['add_workout_screen'].ids

        workout_image_grid = self.root.ids['add_workout_screen'].ids['workout_image_grid']
        select_workout_image_label = self.root.ids.add_workout_screen.ids.select_workout_image_label

        # Already have workout image in self.workout_image variable
        description_input = workout_ids['description_input'].text.replace("\n","")
        # Already have option choice in self.option_choice
        quantity_input = workout_ids['quantity_input'].text.replace("\n","")
        units_input = workout_ids['units_input'].text.replace("\n","")
        month_input = workout_ids['month_input'].text.replace("\n","")
        day_input = workout_ids['day_input'].text.replace("\n","")
        year_input = workout_ids['year_input'].text.replace("\n","")

        # Make sure fields aren't garbage
        if self.workout_image == None:
            select_workout_image_label.color = (1,0,0,1)
            return
        # They are allowed to leave no description
        if self.option_choice == None:
            workout_ids['time_label'].color = (1,0,0,1)
            workout_ids['distance_label'].color = (1,0,0,1)
            workout_ids['sets_label'].color = (1,0,0,1)
            return
        try:
            int_quantity = float(quantity_input)
        except:
            workout_ids['quantity_input'].background_color = (1,0,0,1)
            return
        if units_input == "":
            workout_ids['units_input'].background_color = (1,0,0,1)
            return
        try:
            int_month = int(month_input)
            if int_month > 12:
                workout_ids['month_input'].background_color = (1, 0, 0, 1)
                return
        except:
            workout_ids['month_input'].background_color = (1,0,0,1)
            return
        try:
            int_day = int(day_input)
            if int_day > 31:
                workout_ids['day_input'].background_color = (1, 0, 0, 1)
                return
        except:
            workout_ids['day_input'].background_color = (1,0,0,1)
            return
        try:
            if len(year_input) == 2:
                year_input = '20'+year_input
            int_year = int(year_input)
        except:
            workout_ids['year_input'].background_color = (1,0,0,1)
            return

        # If all data is ok, send the data to firebase real-time database
        workout_payload = {"workout_image": self.workout_image, "description": description_input, "likes": 0,
                           "number": float(quantity_input), "type_image": self.option_choice, "units": units_input,
                           "date": month_input + "/" + day_input + "/" + year_input}
        workout_request = requests.post("https://friendly-fitness.firebaseio.com/%s/workouts.json?auth=%s"
                                        %(self.local_id, self.id_token), data=json.dumps(workout_payload))
        # Add the workout to the banner grid in the home screen
        banner_grid = self.root.ids['home_screen'].ids['banner_grid']
        W = WorkoutBanner(workout_image=self.workout_image, description=description_input,
                          type_image=self.option_choice, number=float(quantity_input), units=units_input,
                          likes="0", date=month_input + "/" + day_input + "/" + year_input)
        banner_grid.add_widget(W, index=len(banner_grid.children))

        # Check if the new workout has made their streak increase
        streak_label = self.root.ids['home_screen'].ids['streak_label']
        result = requests.get("https://friendly-fitness.firebaseio.com/" + self.local_id + ".json?auth=" + self.id_token)
        data = json.loads(result.content.decode())
        workouts = data['workouts']
        streak = helperfunctions.count_workout_streak(workouts)
        if str(streak) == "0":
            streak_label.text = "Ziua" + str(streak) + " de activitate. Fă sport!"
        else:
            streak_label.text = "Ziua " + str(streak) + " de activitate!"


        # Go back to the home screen
        self.change_screen("home_screen", direction="backwards")


    
    
       

    def change_screen(self, screen_name, direction='forward', mode = ""):
        # Get the screen manager from the kv file
        screen_manager = self.root.ids['screen_manager']
        #print(direction, mode)
        # If going backward, change the transition. Else make it the default
        # Forward/backward between pages made more sense to me than left/right
        if direction == 'forward':
            mode = "push"
            direction = 'left'
        elif direction == 'backwards':
            direction = 'right'
            mode = 'pop'
        elif direction == "None":
            screen_manager.transition = NoTransition()
            screen_manager.current = screen_name
            return

        screen_manager.transition = CardTransition(direction=direction, mode=mode)

        screen_manager.current = screen_name

MainApp().run()
