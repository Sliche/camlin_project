from passlib.context import CryptContext


class Hash:
    def __init__(self):
        self.hash_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self.hash_context.hash(password)

    def verify_hash(self, plain_text, hashed_text):
        result = self.hash_context.verify(plain_text, hashed_text)
        return result
