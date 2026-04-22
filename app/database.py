from sqlalchemy import create_engine, URL
import os
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://root:password@localhost:5432/network_design"

load_dotenv()
DATABASE_URL = URL.create(
    drivername=os.getenv("DB_DRIVER"),
    username=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    port=os.getenv("PORT"),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()