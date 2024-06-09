from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import StringProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.lang import Builder
from kivy.core.window import Window
Window.clearcolor = (1, 1, 1, 1)
Window.size = (360, 640)

Window.minimum_width = 360
Window.minimum_height = 640

import json
import requests

KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex

<UserInput>:
    size_hint_y: None
    size_hint_x: 1
    height: self.minimum_height
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
    BoxLayout:
        size_hint_y: None
        height: max(user_response_label.texture_size[1] + dp(20), 100)
        canvas.before:
            Color:
                rgba: 0, 0.8, 1, 1  # Light blue background
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [25, 25, 25, 0]
        Label:
            id: user_response_label
            text: root.text
            color: 0, 0, 0, 1  # Set color to black (RGBA values)
            font_size: root.font_size
            size_hint: None, None
            size: self.texture_size
            padding: dp(10)  # Adjust padding as needed
            halign: 'left'
            valign: 'top'
            text_size: cm(9), None
            multiline: True

<BotResponse>:
    size_hint_y: None
    size_hint_x: 1
    height: max(response_label.texture_size[1] + dp(20), 100)  # Adjust padding, minimum height as needed
    BoxLayout:
        size_hint_y: None
        height: root.height
        canvas.before:
            Color:
                rgba: get_color_from_hex("#f29f80")  # New background color
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [25, 25, 0, 25]
        Label:
            id: response_label
            text: root.text
            color: 0, 0, 0, 1  # Set color to black (RGBA values)
            font_size: root.font_size
            size_hint: None, None
            size: self.texture_size
            padding: dp(10)  # Adjust padding as needed
            halign: 'left'
            valign: 'top'
            text_size: cm(9), None
            multiline: True

<ChatScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        BoxLayout:
            size_hint_y: None
            height: 40
            Label:
                text: "Story.AI"
                color: 0, 0, 0, .5
                halign: 'center'
                valign: 'middle'

        ScrollView:
            id: scroll_view
            do_scroll_x: False
            do_scroll_y: True
            BoxLayout:
                id: chat_area
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 10

        BoxLayout:
            size_hint_y: None
            height: 50
            TextInput:
                id: message
                hint_text: "Enter Stories Ideas Here!"
                size_hint_x: 0.85
                multiline: False
            Button:
                text: "Send"
                size_hint_x: 0.15
                on_press: root.send_message()
'''

class UserInput(BoxLayout):
    text = StringProperty()
    font_size = NumericProperty()

class BotResponse(BoxLayout):
    text = StringProperty()
    font_size = NumericProperty()

class ChatScreen(Screen):
    def send_message(self):
        user_input = self.ids.message.text
        self.ids.message.text = ""

        if user_input:
            # Log the user input
            print(f"User input: {user_input}")

            # Add user input to the chat area
            self.ids.chat_area.add_widget(UserInput(text=user_input, font_size=17))

            # Scroll to the bottom of the chat
            self.ids.scroll_view.scroll_y = 0

            # Send user input to the backend for AI response
            self.fetch_bot_response(user_input)

    def fetch_bot_response(self, user_input):
        url = "http://localhost:8501/"  # Update with your Streamlit app URL
        params = json.dumps({"user_input": user_input})  # Convert params to JSON string
        headers = {'Content-type': 'application/json'}
        r = requests.post("http://localhost:8000", json=params)
        self.ids.chat_area.add_widget(BotResponse(text=r.text, font_size=17))

        # def on_success(req, result):
        #     print("Request succeeded.")
        #     response = result.get('response', 'Sorry, I could not understand that.')
        #     print(f"Bot response: {response}")
        #     self.ids.chat_area.add_widget(BotResponse(text=response, font_size=17))

        #     # Scroll to the bottom of the chat
        #     self.ids.scroll_view.scroll_y = 0

        # def on_failure(req, result):
        #     print("Request failed.")
        #     print(f"Failure result: {result}")
        #     self.ids.chat_area.add_widget(BotResponse(text="Failed to get response from server", font_size=17))

        # def on_error(req, error):
        #     print(f"Error: {error}")
        #     self.ids.chat_area.add_widget(BotResponse(text="Error communicating with the server", font_size=17))

        # # Send the request
        # print(f"Sending request to {url} with params: {params}")
        # UrlRequest(url, on_success=on_success, on_failure=on_failure, on_error=on_error,
        #            req_body=params, method='POST', req_headers=headers)

class ChatApp(App):
    def build(self):
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(ChatScreen(name='chat'))
        return sm

if __name__ == '__main__':
    ChatApp().run()
