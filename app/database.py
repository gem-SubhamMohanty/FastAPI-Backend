from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from .config import settings

# connection
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'



# engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# session to talk to database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Models extending base class
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()  # will talk with the databases
    try:
        yield db
    finally:
        db.close()


# setting up connection(raw sequel connectivity)
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='postgres', cursor_factory=RealDictCursor)  # gives the column names
#         cur = conn.cursor()
#         print("Database connected")
#         break
#     except Exception as error:
#         print("connection failed")
#         print(error)
#         time.sleep(2)
