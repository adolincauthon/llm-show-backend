from datetime import datetime
import os
import firebase_admin
from firebase_admin import firestore, credentials

current_dir = os.path.dirname(os.path.abspath(__file__))
# Move up one level to the parent directory
parent_dir = os.path.dirname(current_dir)
# Construct the absolute path to the JSON credential file
keys_folder_path = os.path.join(parent_dir, 'keys')

credential_file_path = os.path.join(
    keys_folder_path, "../keys/firebase_account.json")
cred = credentials.Certificate(credential_file_path)
firebase_admin.initialize_app(cred)


class Agent_Model():
    def __init__(self):
        '''
        Initializes a firebase instance
        '''
        self.db = firestore.client()
        self.agents = self.db.collection('agents')

    def get_agent(self, assistant_id: str) -> dict:
        '''
        Gets an agent based off of ID. Returns default format if agent does not exist.
        :param assistant_id: Identifier for agent
        '''
        assistant = self.agents.document(assistant_id)
        assistant_doc = assistant.get()
        if assistant_doc.exists:
            return assistant_doc.to_dict()
        else:
            return {"persona": None, "inbox": {}, "outbox": {}}

    def _update_firebase_messages(self, assistant_obj, user_obj):
        assistant_id = assistant_obj.get('id')
        user_id = user_obj.get('id')
        assistant = self.agents.document(assistant_id)
        assistant_doc = assistant.get()
        # update user
        try:
            if assistant_doc.exists:
                assistant_data = assistant_doc.to_dict()
                assistant_data.get('inbox')[user_id] = assistant_data.get('inbox').get(
                    user_id, []).extend(user_obj.get('messages'))
                assistant_data.get('outbox')[user_id] = assistant_data.get('outbox').get(
                    user_id, []).extend(assistant_obj.get('messages'))
                assistant.set(assistant_data)
            else:
                persona = assistant_obj.get('persona')
                assistant_data = {"persona": persona, "outbox": {
                    user_id: assistant_obj.get('messages')}, "inbox": {user_id: user_obj.get('messages')}}
                assistant.set(assistant_data)
                return True
        except Exception as e:
            print(f'Error occurred adding messages to assistant: {e}')
            return False

    def add_messages(self, assistant_obj: dict, user_obj: dict):
        '''
        Adds messages to agent's history, create a new document if it does not exist.
        '''
        # update assistants data
        if self._update_firebase_messages(assistant_obj, user_obj) == True:
            # update users data
            if self._update_firebase_messages(user_obj, assistant_obj) == True:
                return True
            else:
                raise KeyError("Error updating firestore values")
        return True
        user = self.agents.document(user)

    def _update_firebase_message(self, assistant_obj, user_obj, message):
        assistant_id = assistant_obj.get('id')
        user_id = user_obj.get('id')
        assistant = self.agents.document(assistant_id)
        assistant_doc = assistant.get()
        # update user
        try:
            if assistant_doc.exists:
                assistant_data = assistant_doc.to_dict()
                assistant_data.get('outbox')[user_id] = assistant_data.get('outbox').get(
                    user_id, []).append(message)
                assistant.set(assistant_data, merge=True)
            else:
                persona = assistant_obj.get('persona')
                assistant_data = {"persona": persona, "outbox": {
                    user_id: [message]}, "inbox": {user_id: []}}
                assistant.set(assistant_data)
                return True
        except Exception as e:
            print(f'Error occurred adding messages: {e}')
            return False

    def add_message(self, assistant_obj: dict, user_obj: dict, message):
        '''
        Adds messages to agent's history, create a new document if it does not exist.
        '''

        pass
