from typing import Dict
from .models import Crime
from sqlalchemy.orm import Session

def get_crime(db: Session, crime_id: int):
    return db.query(Crime).filter(Crime.id == crime_id).first()

def get_crimes(db: Session):
    return db.query(Crime).all()

def create_crime(db: Session, crime: Crime):
    db.add(crime)
    db.commit()
    db.refresh(crime)
    return crime

def delete_crime(db: Session, crime_id: int):
    crime = db.query(Crime).filter(Crime.id == crime_id).first()
    db.delete(crime)
    db.commit()
    return crime

def update_crime(db: Session, crime_id: int, crime: dict):
    db_crime = db.query(Crime).filter(Crime.id == crime_id).first()

    if db_crime is None:
        return

    for key, value in crime.items():
        setattr(db_crime, key, value)

    db.commit()
    db.refresh(db_crime)
    return db_crime

from .models import User
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user: Dict):
    user = User(username=user["username"], hashed_password=password_context.hash(user["password"]))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return password_context.hash(password)




