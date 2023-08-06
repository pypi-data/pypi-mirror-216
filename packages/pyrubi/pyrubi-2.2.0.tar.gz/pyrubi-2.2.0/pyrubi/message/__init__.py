class message:

    def __init__(self, data):
        self.data = data

    def chat_id(self):
        try:
            return self.data['message_updates'][0]['object_guid']
        except KeyError:
            return self.data.get('object_guid', None)

    def author_id(self):
        try:
            return self.data['message_updates'][0]['message']['author_object_guid']
        except KeyError:
            return self.data['last_message']['author_object_guid']

    def message_id(self):
        try:
            return self.data['message_updates'][0]['message_id']
        except KeyError:
            return self.data['last_message']['message_id']

    def reply_to_message_id(self):
        try:
            return self.data['message_updates'][0]['message'].get('reply_to_message_id', None)
        except KeyError:
            return None

    def text(self):
        try:
            return self.data['message_updates'][0]['message'].get('text', None)
        except KeyError:
            return self.data['last_message'].get('text', None)

    def chat_type(self):
        try:
            return self.data['message_updates'][0]['type']
        except KeyError:
            return self.data['abs_object']['type']

    def author_type(self):
        try:
            return self.data['message_updates'][0]['message']['author_type']
        except KeyError:
            return self.data['last_message']['author_type']

    def message_type(self):
        try:
            return self.data['message_updates'][0]['message'].get('type', None)
        except KeyError:
            return self.data['last_message'].get('type', None)

    def is_forward(self):
        try:
            return 'forwarded_from' in self.data['message_updates'][0]['message'].keys()
        except KeyError:
            return None
        
    def forward_type(self):
        try:
            return self.data['message_updates'][0]['message']['forwarded_from'].get('type_from', None)
        except KeyError:
            return None
        
    def forward_id(self):
        try:
            return self.data['message_updates'][0]['message']['forwarded_from'].get('object_guid', None)
        except KeyError:
            return None
        
    def forward_message_id(self):
        try:
            return self.data['message_updates'][0]['message']['forwarded_from'].get('message_id', None)
        except KeyError:
            return None
        
    def is_event(self):
        try:
            return 'event_data' in self.data['message_updates'][0]['message'].keys()
        except KeyError:
            return self.message_type() == 'Other'

    def is_user_chat(self):
        return self.chat_type() == 'User'

    def is_group_chat(self):
        return self.chat_type() == 'Group'

    def is_channel_chat(self):
        return self.chat_type() == 'Channel'

    def chat_title(self):
        try:
            return self.data['show_notifications'][0].get('title', None)
        except KeyError:
            return self.data['abs_object'].get('title', None)

    def author_title(self):
        try:
            return self.data['chat_updates'][0]['chat']['last_message'].get('author_title', self.chat_title())
        except KeyError:
            return self.data['last_message'].get('author_title', self.chat_title())

    def event_type(self):
        try:
            return self.data['message_updates'][0]['message']['event_data'].get('type', None)
        except KeyError:
            return None

    def event_id(self):
        try:
            return self.data['message_updates'][0]['message']['event_data']['performer_object'].get('object_guid', None)
        except KeyError:
            return None
        
    def count_unseen(self):
        try:
            return self.data['chat_updates'][0]['chat'].get('count_unseen', '0')
        except KeyError:
            return None