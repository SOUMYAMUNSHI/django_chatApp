#This is the views for the Django-channel

from channels.consumer import SyncConsumer, AsyncConsumer
import json
from .models import Chat
from django.contrib.auth.models import User
from asgiref.sync import async_to_sync


class MySyncChannel(SyncConsumer):


    def websocket_connect(self, event):
        print("Connected...", event)

        #retreving the chat_room_name from the websocket url (send from details.html)
        self.chat_room_name = self.scope['url_route']['kwargs']['username']

        #next 6 lines of code is to create an unique room id
        #spliting the username and user_id
        self.u_names = self.chat_room_name.split("_")

        #making the room id
        self.room_id = str(int(len(self.u_names[0])) + int(len(self.u_names[1])))

        #making a unique chat room name by adding substirng "cg_"
        self.new_chat_room_name = f"cg_{self.room_id}"

        print(self.new_chat_room_name)

        # creating a group using the channel name
        # we have to convert this function into a sync function
        async_to_sync (self.channel_layer.group_add)(self.new_chat_room_name, self.channel_name)

        self.send({
            'type': 'websocket.accept'
        })






    def websocket_receive(self, event):

        #receiving message in json format
        self.json_message = event['text']

        #retreving the username from the websocket url
        self.chat_room_name = self.scope['url_route']['kwargs']['username']

        #next 6 lines of code is to create an unique room id
        #spliting the username and user_id
        self.u_names = self.chat_room_name.split("_")

        #making the room id
        self.room_id = str(int(len(self.u_names[0])) + int(len(self.u_names[1])))

        #making a unique chat room name by adding substirng "cg_"
        self.new_chat_room_name = f"cg_{self.room_id}"
        
        #extracting sender user name
        self.sender_username = self.u_names[0]

        #converting message in dictionary format
        self.dict_message = json.loads(self.json_message)

        #retreving the current user
        self.current_user_id = self.dict_message['current_user_id']

        #reterving sender id from usernme
        self.sender_user_id = User.objects.get(username = self.sender_username).id

        #sending data to database
        Chat.objects.create(chat_msg = self.dict_message['message'], sender_id = self.current_user_id, receiver_id = self.sender_user_id, update_at = self.dict_message['timestamp'], user_id = self.current_user_id)

        #preparing the event to send the message to the group
        async_to_sync (self.channel_layer.group_send)(self.new_chat_room_name,{
            'type' : 'chat.message',
            'message' : self.dict_message['message']
        })

    #creating function (handler) to send the message to frontend (name is same as event name[chat.message])
    def chat_message(self, event):
        print("New message received.....................",event['message'])
        self.send({
            'type':'websocket.send',
            'text':event['message']
        })






    def websocket_disconnect(self, event):
        print("Disconnect...", event)

        #retreving the channel name
        self.chat_room_name = self.scope['url_route']['kwargs']['username']

        #next 6 lines of code is to create an unique room id
        #spliting the username and user_id
        self.u_names = self.chat_room_name.split("_")

        #making the room id
        self.room_id = str(int(len(self.u_names[0])) + int(len(self.u_names[1])))

        #making a unique chat room name by adding substirng "cg_"
        self.new_chat_room_name = f"cg_{self.room_id}"

        #disconnecting the channel name
        async_to_sync (self.channel_layer.group_discard)(self.new_chat_room_name, self.channel_name)










class MyAsyncChannel(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Connect")
    async def websocket_receive(self, event):
        print("Receive")
    async def websocket_disconnect(self, event):
        print("Disconnect")