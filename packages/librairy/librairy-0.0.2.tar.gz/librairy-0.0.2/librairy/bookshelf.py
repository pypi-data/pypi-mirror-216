from librairy import collector
import requests
import os
import logging
import schedule
import time
from logging.config import dictConfig
import logging
from .config import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("librairy")


TOKEN       = os.getenv("TOKEN","None")
HOST        = os.environ.get("HOST","http://localhost:8000")

def connect(credentials=TOKEN,host=HOST):
    return Bookshelf(credentials, host)

class Bookshelf():

    def __init__(self, token, host):        
        self.headers = {'Authorization': f"Bearer {token}"}
        self.endpoint = host
    
    def add(self, doc):
        resp =  requests.post(f'{self.endpoint}/add', headers=self.headers, json = doc)
        if (resp.status_code != 200):
            logger.warn(resp.text)
        return resp
    
    def remove(self, doc_id):
        request = {
            "document_id": doc_id
        }        
        resp = requests.post(f'{self.endpoint}/remove', headers=self.headers, json = request)
        if (resp.status_code != 200):
            logger.warn(resp.text)
        return resp
    

    def ask(self, question, limit=1):
        request = {
            "text": question,
            "limit" : limit
        }        
        resp = requests.post(f'{self.endpoint}/ask', headers=self.headers, json = request)
        if (resp.status_code != 200):
            logger.warn(resp.text)
        return resp

    def explore(self, query, limit=2):
        request = {
            "text": query,
            "limit" : limit
        }
        resp = requests.post(f'{self.endpoint}/explore', headers=self.headers, json = request)
        if (resp.status_code != 200):
            logger.warn(resp.text)
        return resp

    
    def collect(self, collector, interval=3600, initial_delay=0):
        request = {
            "id": collector.get_id(),
            "interval" : interval,
            "initial_delay": initial_delay,
            "parameters": collector.get_parameters()
        }
        resp = requests.post(f'{self.endpoint}/collect', headers=self.headers, json = request)
        if (resp.status_code != 200):
            logger.warn(resp.text)
        return resp

    def cancel(self, collector):
        request = {
            "id": collector
        }
        resp = requests.post(f'{self.endpoint}/cancel', headers=self.headers, json = request)
        if (resp.status_code != 200):
            logger.warn(resp.text)
        return resp