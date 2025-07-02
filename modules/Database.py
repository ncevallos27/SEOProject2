import sqlalchemy as db
import pandas as pd

class Database():
    def __init__(self, path=None, load=None):
        self.path = path
        self.engine = db.create_engine(self.path)

        with self.engine.connect() as connection:
            if load is None:
                connection.execute(db.text("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, " \
                                                                              "eventName TEXT, " \
                                                                              "eventTime TEXT, " \
                                                                              "eventDescription TEXT);"))
            else:
                load.to_sql('events', con=self.engine, if_exists='replace', index=False)

    def returnDatabase(self, options=None):
        df = pd.read_sql("SELECT * FROM events", con=self.engine)
        return df
    
    