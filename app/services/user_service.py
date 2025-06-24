import os

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.db import get_db
from app.models.user_model import User as UserModel
from app.wrappers.jwt import JWTManager
from app.schemas.user_schemas import UserCreate
from app.wrappers.hashing import Hash
from app.services.base_service import BaseService
from app.services.wallet_service import WalletService as wallet_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users/token")
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

    def update(self, user_id, update_schema):
        try:
            user = super().update(user_id, update_schema)
            return user
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username or email already exists."
            )

    def create_initial_user(self):
        if not self.db.query(self.model).filter_by(username=os.getenv("DEFAULT_USER_NAME", "camlin12")).first():
            default_user = self.model()
            default_user.username = os.getenv("DEFAULT_USER_NAME", "camlin12")
            default_user.password = hash_service.hash(os.getenv("DEFAULT_USER_NAME"))
            default_user.email = os.getenv("DEFAULT_USER_EMAIL")
            default_user.first_name = os.getenv("DEFAULT_USER_FN")
            default_user.last_name = os.getenv("DEFAULT_USER_LN")
            self.db.add(default_user)
            try:
                self.db.commit()
                wallet_service(self.db).create_default_wallet(default_user.id)
            except Exception as e:
                self.db.rollback()


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

