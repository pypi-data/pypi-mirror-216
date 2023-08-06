import asyncio
import functools
import pyroherd

from ..utils import patch, patchable

loop = asyncio.get_event_loop()
    
class ListenerCanceled(Exception):
    pass

pyroherd.errors.ListenerCanceled = ListenerCanceled


@patch(pyroherd.client.Client)
class Client():
    @patchable
    def __init__(self, *args, **kwargs):
        self.listening = {}
        self.using_mod = True
        
        self.old__init__(*args, **kwargs)
    
    @patchable
    async def listen(self, chat_id, filters=None, timeout=None):
        if not isinstance(chat_id, int):
            chat = await self.get_chat(chat_id)
            chat_id = chat.id
        
        future = loop.create_future()
        future.add_done_callback(
            functools.partial(self.clear_listener, chat_id)
        )
        self.listening.update({
            chat_id: {"future": future, "filters": filters}
        })
        return await asyncio.wait_for(future, timeout)
    
    @patchable
    async def ask(self, chat_id, text, filters=None, timeout=None, *args, **kwargs):
        request = await self.send_message(chat_id, text, *args, **kwargs)
        response = await self.listen(chat_id, filters, timeout)
        response.request = await self.get_messages(chat_id, request.id, replies=0)
        return response
   
    @patchable
    def clear_listener(self, chat_id, future):
        if future == self.listening[chat_id]["future"]:
            self.listening.pop(chat_id, None)
     
    @patchable
    def cancel_listener(self, chat_id):
        listener = self.listening.get(chat_id)
        if not listener or listener['future'].done():
            return
        
        listener['future'].set_exception(ListenerCanceled())
        self.clear_listener(chat_id, listener['future'])


@patch(pyroherd.handlers.message_handler.MessageHandler)
class MessageHandler():
    @patchable
    def __init__(self, callback: callable, filters=None):
        self.user_callback = callback
        self.old__init__(self.resolve_listener, filters)
    
    @patchable
    async def resolve_listener(self, client, message, *args):
        listener = client.listening.get(message.chat.id)
        if listener and not listener['future'].done():
            listener['future'].set_result(message)
        else:
            if listener and listener['future'].done():
                client.clear_listener(message.chat.id, listener['future'])
            await self.user_callback(client, message, *args)
    
    @patchable
    async def check(self, client, update):
        listener = client.listening.get(update.chat.id)
        
        if listener and not listener['future'].done():
            return await listener['filters'](client, update) if callable(listener['filters']) else True
            
        return (
            await self.filters(client, update)
            if callable(self.filters)
            else True
        )


@patch(pyroherd.types.messages_and_media.message.Message)
class Message(pyroherd.types.Message):
    @patchable
    def listen(self, *args, **kwargs):
        return self._client.listen(self.chat.id, *args, **kwargs)

    @patchable
    def ask(self, *args, **kwargs):
        return self._client.ask(self.chat.id, *args, **kwargs)

    @patchable
    def cancel_listener(self):
        return self._client.cancel_listener(self.chat.id)