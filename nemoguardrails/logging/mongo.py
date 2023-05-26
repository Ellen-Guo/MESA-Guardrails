# Mongodb logging of Guardrails events, actions, and messages

import os
import pymongo

MONGODB_HOST = os.environ.get("MONGODB_HOST", "localhost")
MONGODB_PORT = os.environ.get("MONGODB_PORT", 27017)
MONGODB_USER = os.environ.get("MONGODB_USER")
MONGODB_PASSWORD = os.environ.get("MONGODB_PASSWORD")

# TODO: items to log -- username, date and time, user input, chain history, bot output/response

class MESALog():
    def init(self, db_name: str, collect_name: str):
        self.client = pymongo.MongoClient(
            host=MONGODB_HOST,
            port=MONGODB_PORT,
            username=MONGODB_USER,
            password=MONGODB_PASSWORD,
        )
        self.db_ref = self.client[db_name]
        self.collection_ref = self.client[db_name][collect_name]

    def insert_db(self, username, timestamp, duration, user_input, chain_history, bot_output):
        blocked = False
        bot_action = chain_history.strip().split('\n')[-1]
        if bot_action == 'bot inform cannot respond':
            blocked = True
        dictionary = {
            "username": username,
            "timestamp": timestamp,
            "duration": duration,
            "input": user_input,
            "history": chain_history,
            "blocked": blocked,
            "response": bot_output
        }
        self.collection_ref.insert_one()
    