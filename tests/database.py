from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db, Base

# connection
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'


# engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# session to talk to database
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    # create all tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()  # will talk with the databases
    try:
        yield db
    finally:
        db.close()

# we can actually configure a fixture to be dependent on another fixture


@pytest.fixture()
def client(session):
    def overide_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = overide_get_db
    # run our code b4 we return our test client.
    yield TestClient(app)
    # run our code after test finishes
