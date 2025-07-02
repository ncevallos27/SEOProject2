import pandas as pd

class App():
    def __init__(self, gAPI, database):
        self.googleAPI = gAPI
        self.db = database
        self.events = pd.DataFrame(columns=['id', 'eventName', 'eventTime', 'eventDescription'])