from db.engine import engine
from db.models import Base

def create_database():
    Base.metadata.create_all(bind=engine)