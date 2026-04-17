from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# В реальном проекте вынеси это в .env
DATABASE_URL = "postgresql://root:password@localhost:5432/network_design"

# echo=True заставит алхимию писать все SQL-запросы в консоль (удобно при дебаге)
engine = create_engine(DATABASE_URL, echo=True)

# Это фабрика сессий (аналог пула соединений)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# От этого класса будут наследоваться все модели
Base = declarative_base()

# Эта функция — "зависимость". Она открывает сессию для запроса и закрывает её после
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()