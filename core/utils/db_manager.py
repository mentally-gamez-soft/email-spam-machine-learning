import datetime
import os

from bson.objectid import ObjectId
from pymongo import MongoClient


class DbManager():

    def __init__(self) -> None:
        self.client = None

    def connect(self):
        login = os.getenv('MONGO_USER')
        password = os.getenv('MONGO_PASSWORD')
        # self.client = MongoClient("mongodb://{}:{}@localhost:27017/".format(login,password))
        self.client = MongoClient("mongo-db",username=login,password=password,authSource="spam_ham")

    def exist_email(self,email) -> bool:
        return self.client.spam_ham.emails.find_one({"email": email})

    def add_email(self,ip_address,email,tag,comment) -> ObjectId:
        payload = {
            "ip-address": ip_address,
            "email": email,
            "tag": tag,
            "date-sent": datetime.datetime.now(tz=datetime.timezone.utc),
            "comment":comment
        }

        l_payloads = self.client.spam_ham.emails
        payload_id = l_payloads.insert_one(payload).inserted_id
        return payload_id
    
    def add_rejected_email(self,ip_address,email,tag,comment) -> ObjectId:
        payload = {
            "ip-address": ip_address,
            "email": email,
            "tag": tag,
            "date-sent": datetime.datetime.now(tz=datetime.timezone.utc),
            "comment":comment
        }

        l_payloads = self.client.spam_ham.rejected_bins
        payload_id = l_payloads.insert_one(payload).inserted_id
        return payload_id