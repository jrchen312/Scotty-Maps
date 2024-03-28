
import json

from .models import Tag
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

class LocationConsumer(WebsocketConsumer):
    def connect(self):
        self.tag_id = self.scope["url_route"]["kwargs"]["tag_id"]
        self.tag_id_group_name = f"chat_{self.tag_id}"

        try:
            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.tag_id_group_name, self.channel_name
            )
        except Exception as e:
            print(e)
            
        self.accept()
    
    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.tag_id_group_name, self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)

        if (data["type"]) == "update":

            try:
                #tag = Tag.objects.get(id=data["tag_id"])
                msg = {
                    'x_pos': data["x_pos"], #tag.x_pos,
                    'y_pos': data["y_pos"], #tag.y_pos,
                    'rotation': data["rotation"], #tag.rotation,
                    'time': data["time"], #tag.last_update_time,
                }
            except:
                msg = {'error': 'Tag ID not found.'}

        else:
            msg = "huh"

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.tag_id_group_name, {"type": "location.update", "message": json.dumps(msg)}
        )

    # Receive message from room group
    def location_update(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))
