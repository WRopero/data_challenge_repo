from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
# import json

Base = declarative_base()

class DatabaseManager:
    def __init__(self, db_url):
        self.db_engine = create_engine(db_url)
        self.conn = sessionmaker(bind=self.db_engine)
        self.session = scoped_session(self.conn)
    
    def get_session(self):
        return self.session()

    def create_tables(self, models):
        Base.metadata.create_all(self.db_engine, tables=[model.__table__ for model in models])

    def drop_tables(self, models):
        Base.metadata.drop_all(self.db_engine, tables=[model.__table__ for model in models])

    def get_session(self):
        return self.conn()
    
    def load_data(self, model, dataframe):
        session = self.get_session()
        dataframe.to_sql(model.__tablename__, self.db_engine, if_exists='append', index=False)
        session.commit()
        session.close()
    
    def execute_query(self, query):
        session = self.get_session()
        result = session.execute(text(query))
        columns = result.keys()
        rows = result.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        return data