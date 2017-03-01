from sqlalchemy import Integer, String, MetaData, create_engine, Table, Column

# from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST


metadata = MetaData()

# Creamos la estructura de la tabla

users = Table('users', metadata,
                 Column('chat_id', Integer, primary_key=True),
                 Column('username', String),
                 Column('password', String),
                 Column('token', String),
                 )

engine = create_engine('sqlite:///:memory:', echo=True)
metadata.create_all(engine)
