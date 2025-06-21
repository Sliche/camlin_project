# app/utils/jwt_manager.py
import os
import jwt
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
load_dotenv()


class JWTManager:
    def __init__(self, secret_key: str = os.getenv("JWT_SECRET_KEY"),
                 algorithm: str = os.getenv("JWT_ALGORITHM"),
                 expires_minutes: int = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
                 ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expires_minutes = int(expires_minutes)

    def create_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=self.expires_minutes))
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        print(token)
        return token

    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token Invalid",
            )

    def get_subject(self, token: str) -> str:
        payload = self.decode_token(token)
        sub = payload.get("sub")
        if not sub:
            raise ValueError("Token has no subject")
        return sub
