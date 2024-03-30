
import json

from .models import Tag, Floor
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class LocationConsumer(WebsocketConsumer):
    # more security is nice. The current url format allows differentiation 
    # between different tag devices, and that tag device being on different 
    # floors. 
    def connect(self):
        # Parse the url route
        self.tag_id = self.scope["url_route"]["kwargs"]["tag_id"]
        self.floor_id = self.scope["url_route"]["kwargs"]["floor_id"]
        self.tag_id_group_name = f"nav_{self.floor_id}_{self.tag_id}"

        # Load some details about the floor to help translate provided position
        # to a pixel location to display on a map?
        # floor = Floor.objects.get(id=self.floor_id)

        try:
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.tag_id_group_name, self.channel_name
            )
        except Exception as e:
            print(e)
            
        self.accept()
    
    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.tag_id_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)

        if (("type" in data) and (data["type"]) == "update"):
            msg = {
                'type': "update",
                'x_pos': data["x_pos"], #tag.x_pos,
                'y_pos': data["y_pos"], #tag.y_pos,
                'rotation': data["rotation"], #tag.rotation,
                'time': data["time"], #tag.last_update_time,
            }
        else:
            msg = {
                "type": "error",
                "error": "An illegal data packet was received."
            }

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.tag_id_group_name, {"type": "location.update", "message": json.dumps(msg)}
        )

    # Receive message from room group
    def location_update(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
