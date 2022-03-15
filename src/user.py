from uuid import uuid4


def generate_token():
    return uuid4()


class User:
    token: str = None
    email: str = None
    password: str = None

    def User(self, token: str, email: str, password: str):
        self.token = token
        self.email = email
        self.password = password

    def get_header(self):
        return ''

    def to_json(self) -> dict:
        return {
            'token': self.token,
            'email': self.email
        }
