from sqlalchemy import Integer, String, MetaData, create_engine, Table, Column

from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


metadata = MetaData()

# Creamos la estructura de la tabla

users = Table('users', metadata,
              Column('chat_id', Integer, primary_key=True),
              Column('username', String),
              Column('password', String),
              Column('token', String),
              )

engine = create_engine('postgresql://' +
                       DB_USER + ':' +
                       DB_PASSWORD + '@' +
                       DB_HOST + ':' +
                       DB_PORT + '/' +
                       DB_NAME
                       )
metadata.create_all(engine)
