import os
from json import load, dump

class sessions:

    def cheack_session(session_name):
        return os.path.exists(os.path.join(os.path.dirname(__file__), '.', f'{session_name}.json'))
    
    def session_data(session_name):
        with open(os.path.join(os.path.dirname(__file__), '.', f'{session_name}.json'), encoding='UTF-8') as data:
            return load(data)
        
    def create_session(session_name, session_data):
        path = os.path.join(os.path.dirname(__file__), '.', f'{session_name}.json')
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as data:
            return dump(session_data, data, indent=4)