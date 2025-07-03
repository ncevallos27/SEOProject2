import pandas as pd
from modules.GoogleAPI import GoogleAPI

class Agent():
    def __init__(self, gAPI, database, gCal):
        self.gen = gAPI
        self.db = database
        self.cal = gCal

    def getAnswer(self, prompt, redoFlag=False):
        return self.gen.getResponse(prompt, context="")
    
    def createEvent(self, start, end, name, description):
        newEvent = {
            'summary' : name,
            'description' : description,
            'start' : {
                'dateTime':start
            }, 
            'end' : {
                'dateTime':end
            }
        }

        retry = 1
        while retry <= 3:
            response = self.gCal.createEvent(newEvent)
            if response is None:
                retry += 1
                print(f"Trying Again... {retry}/3")
            else:
                return response
            
        return "Event Could Not be Created"