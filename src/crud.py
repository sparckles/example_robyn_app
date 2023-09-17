from typing import Dict

from sqlalchemy.orm import Session

from .models import Crime


def get_crime(db: Session, crime_id: int):
    return db.query(Crime).filter(Crime.id == crime_id).first()


def get_crimes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Crime).offset(skip).limit(limit).all()


def create_crime(db: Session, crime):
    db_crime = Crime(**crime)
    db.add(db_crime)
    db.commit()
    db.refresh(db_crime)
    return db_crime


def update_crime(db: Session, crime_id: int, crime):
    db_crime = get_crime(db, crime_id)
    if db_crime is None:
        return None
    for key, value in crime.items():
        setattr(db_crime, key, value)
    db.commit()
    db.refresh(db_crime)
    return db_crime


def delete_crime(db: Session, crime_id: int):
    db_crime = get_crime(db, crime_id)
    if db_crime is None:
        return False
    db.delete(db_crime)
    db.commit()
    return True


from passlib.context import CryptContext

from .models import User

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: Dict):
    user = User(
        username=user["username"],
        hashed_password=password_context.hash(user["password"]),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_password(plain_password: str, hashed_password: str):
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return password_context.hash(password)


from jose import JWTError, jwt

SECRET_KEY = "secret"
ALGORITHM = "HS256"


def create_access_token(data):
    to_encode = data.copy()

    final_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return final_jwt


def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
