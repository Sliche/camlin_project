from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.db import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")

from app.models.user import User as UserModel
from app.wrappers.jwt import JWTManager
from app.schemas.user_schemas import UserCreate
from app.wrappers.hashing import Hash
from app.services.base_service import BaseService

jwt_service = JWTManager()
hash_service = Hash()


class UserService(BaseService):

    def __init__(self, db: Session):
        self.model = UserModel
        super().__init__(db)

    def create(self, user_in: UserCreate) -> UserModel:
        hashed_pw = hash_service.hash(user_in.password)
        user_in.password = hashed_pw
        try:
            user = super().create(user_in)
            return user
        # here you can handle all possible errors during creation
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists."
            )

    def update(self, entity_id, update_schema):
        try:
            user = super().update(entity_id, update_schema)
            return user
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists."
            )

    @staticmethod
    def authenticate_user(db: Session, username, password):

        user = db.query(UserModel).filter_by(username=username).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user if hash_service.verify_hash(password, user.password) else None

    @staticmethod
    def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
        user_id = jwt_service.get_subject(token)
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

