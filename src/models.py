#pylint: disable-all

from sqlalchemy import create_engine, Column, Integer, String, Float , Engine, Date
from sqlalchemy.orm import sessionmaker, declarative_base


DATABASE_URL = "sqlite:///./gotham_database.db"

engine: Engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class Crime(Base):
    __tablename__ = "crimes"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    description = Column(String)
    location = Column(String)
    date = Column(Date)
    latitude = Column(Float)
    longitude = Column(Float)

    def __repr__(self):
        return f"<Crime(id={self.id}, type={self.type}, description={self.description}, location={self.location}, date={self.date}, latitude={self.latitude}, longitude={self.longitude})>"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, hashed_password={self.hashed_password})>"

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
