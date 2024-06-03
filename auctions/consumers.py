import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from auctions.models import Bid, Auction
from chat.models import ChatRoom, ChatMessage

class UnifiedAuctionChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope.get('user')
        self.auction_id = self.scope["url_route"]["kwargs"]["auction_id"]
        self.room_group_name = f"auction_chat_{self.auction_id}"

        # Joining the group for both auction and chat
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leaving the group on disconnect
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get("type")

        if message_type == "chat.message":
            await self.handle_chat_message(text_data_json)
        elif message_type == "bid":
            await self.handle_bid(text_data_json)

    async def handle_chat_message(self, text_data_json):
        message = text_data_json.get("message")
        if message and not self.user.is_anonymous:
            auction = await database_sync_to_async(Auction.objects.get)(pk=self.auction_id)
            room, _ = await database_sync_to_async(ChatRoom.objects.get_or_create)(auction=auction)
            await database_sync_to_async(ChatMessage.objects.create)(
                room=room,
                user=self.user,
                message=message
            )

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message,
                    'user': self.user.first_name
                }
            )

    async def handle_bid(self, text_data_json):
        bid_amount = text_data_json.get("bid_amount")
        print("Received bid:", bid_amount)  # Debug statement
        if bid_amount and not self.user.is_anonymous:
            bid_amount = float(bid_amount)
            auction = await database_sync_to_async(Auction.objects.get)(pk=self.auction_id)
            
            # Check if auction is over
            if auction.end_time <= timezone.now():
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': 'The auction is over'
                }))
                return
            if bid_amount > auction.current_bid:
                await database_sync_to_async(Bid.objects.create)(
                    user=self.user,
                    auction=auction,
                    bid_amount=bid_amount
                )
                auction.current_bid = bid_amount
                await database_sync_to_async(auction.save)()

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'bid',
                        'new_bid': bid_amount,
                        'user': self.user.first_name
                    }
                )

    # Methods for handling real-time messages to clients
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'chat.message',
            'message': event['message'],
            'user': event['user']
        }))

    async def bid(self, event):
        await self.send(text_data=json.dumps({
            'type': 'bid',
            'new_bid': event['new_bid'],
            'user': event['user'],
            'message': 'Bid is updated'
        }))
