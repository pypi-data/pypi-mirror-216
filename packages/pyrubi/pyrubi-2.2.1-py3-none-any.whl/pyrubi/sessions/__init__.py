from ..cryption import cryption5
import os
from json import loads, dumps

class sessions:

    def __init__(self):
        self.key = "pyrubiIsAPowerfulLibraryForBuildingTheSelfBotInRubika"
        self.crypto = cryption5(self.key)

    def cheack_session(self, session_name):
        return os.path.exists(f'{session_name}.pyrubi')
    
    def session_data(self, session_name):
        return loads(self.crypto.decrypt(open(f'{session_name}.pyrubi', encoding='UTF-8').read()))
        
    def create_session(self, session_name, session_data):
        open(f'{session_name}.pyrubi', 'w', encoding='UTF-8').write(self.crypto.encrypt(dumps(session_data)))