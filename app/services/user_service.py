from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

from app.models.user import User as UserModel
from app.wrappers.jwt import JWTManager
from app.schemas.user import UserCreate
from app.wrappers.hashing import Hash

jwt_service = JWTManager()
hash_service = Hash()


class UserService:

    def __init__(self):
        pass

    def create_user(self, db: Session, user_in: UserCreate) -> UserModel:
        hashed_pw = hash_service.hash(user_in.password)
        db_user = UserModel()

        db_user.username = user_in.username
        db_user.password = hashed_pw
        db_user.email = user_in.email
        db_user.first_name = user_in.first_name
        db_user.last_name = user_in.last_name
        db_user.id="sjehfa"

        db.add(db_user)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists"
            )
        except Exception as e:
            print("got some other xception")

            print("Exception type:", type(e))
            print("Exception class name:", type(e).__name__)
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Oops, something went wrong..."
            )
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, user_id: int) -> bool:
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            return False
        db.delete(user)
        db.commit()
        return True

    @staticmethod
    def authenticate_user(db: Session, username, password):

        user = db.query(UserModel).filter_by(username=username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user if hash_service.verify_hash(password, user.password) else None

    def hash_password(self, password):
        pass

    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme),
                               db: Session = Depends(get_db)):
        user_id = jwt_service.get_subject(token)
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

