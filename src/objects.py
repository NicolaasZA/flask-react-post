from uuid import uuid4


def generate_token():
    return uuid4()


def is_not_null(val):
    return val not in ['', None, 'null']


def debug(text: str):
    print(bcolors.OKGREEN, text, bcolors.ENDC)


def error(text: str):
    print(bcolors.FAIL, text, bcolors.ENDC)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class JSONResponse:
    status: int = 200
    success: bool = False
    message: str = ''
    data: dict = {}

    def __init__(self):
        pass

    def set_data(self, key: str, value):
        self.data[key] = value

    def remove_data(self, key: str):
        if key in self.data:
            del self.data[key]


class User:
    id: int = None
    email: str = None
    name: str = None
    utype: int = None
    token: str = None

    def __init__(self, id: int, email: str, name: str, utype: int):
        self.email = email
        self.name = name
        self.utype = utype
        self.id = id

    def to_json(self) -> dict:
        jason = {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'type': self.utype
        }
        if self.token != None:
            jason['token'] = self.token
        return jason

    def __str__(self):
        return f'<User {self.id}: {self.email} of type {self.utype}>'

    def __repr__(self):
        return self.__str__()


class Token:
    id: int = None
    token: str = None
    userid: int = None

    def __init__(self, id: int, token: str, userid: int):
        self.id = id
        self.token = token
        self.userid = userid

    def __str__(self):
        return f'<Token {self.id}: {self.userid}|{self.token}>'

    def __repr__(self):
        return self.__str__()


class Project:
    id: int = None
    name: str = None
    companyid: int = None
    created: str = None

    company: User = None

    def __init__(self, id, name, companyid, created):
        self.id = id
        self.name = name
        self.companyid = companyid
        self.created = created

    def to_json(self) -> dict:
        jason = {
            'id': self.id,
            'name': self.name,
            'company': {
                'id': self.companyid
            },
            'created': self.created
        }
        if self.company != None:
            jason['company'] = self.company.to_json()
        return jason

    def __str__(self):
        return f'<Project {self.id}: {self.name}@{self.companyid}>'

    def __repr__(self):
        return self.__str__()
