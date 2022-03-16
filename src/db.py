# pip install SQLAlchemy
# pip install mysql-connector-python

from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, create_engine, text, insert

from src.objects import Project, Token, User, debug, generate_token, is_not_null

meta = MetaData()

usersTable = Table(
    'users', meta,
    Column('id', Integer, primary_key=True),
    Column('email', String),
    Column('password', String),
    Column('utype', Integer)
)

tokensTable = Table(
    'logins', meta,
    Column('id', Integer, primary_key=True),
    Column('token', String),
    Column('userid', Integer, ForeignKey('users.id'))
)

projectsTable = Table(
    'projects', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('companyid', Integer, ForeignKey('users.id')),
    Column('created', Integer)
)

engine = create_engine(
    "mysql+mysqlconnector://root:rootytooty@127.0.0.1/demoapp", echo=False, future=True)


def get_user_from_id(userid: int) -> User:
    with engine.connect() as conn:
        user_result = conn.execute(text(
            "SELECT * FROM users WHERE id=:id"), {'id': userid})
        for row in user_result:
            return User(row.id, row.email, row.name, row.utype)
    return None


def get_user(email: str, password: str) -> User:
    with engine.connect() as conn:
        user_result = conn.execute(text(
            "SELECT * FROM users WHERE email=:e AND password=:p"), {'e': email, 'p': password})
        for row in user_result:
            return User(row.id, row.email, row.name, row.utype)
    return None


def get_user_from_token(tokenValue: str) -> User:
    token = get_token(tokenValue)
    if token != None:
        return get_user_from_id(token.userid)
    else:
        return None


def register_user(email: str, password: str, utype: int) -> User:
    debug(f'register_user({email}, {password}, {utype})')
    stmt = usersTable.insert().values(email=email, password=password, utype=utype)
    with engine.connect() as conn:
        result = conn.execute(stmt)
        conn.commit()

        if result.inserted_primary_key[0] > 0:
            return get_user(email, password)
        else:
            return None


def verify_token_header(header: str) -> bool:
    """Verify a session header is valid and belongs to the given user."""
    debug(f'verify_token_header({header})')
    if is_not_null(header) and ('|' in header):
        return verify_token(header.split('|')[1], header.split('|')[0])
    return False


def verify_token(token: str, userID: int) -> bool:
    """Verify a session token is valid and belongs to the given user. Returns True if valid."""
    debug(f'verify_token({token}, {userID})')
    with engine.connect() as conn:
        _res = conn.execute(
            text(f"SELECT * FROM logins WHERE token=:t AND userid=:u"), {'t': token, 'u': userID})
        for _ in _res:
            return True
    return False


def get_token(token: str) -> Token:
    debug(f'get_token({token})')
    with engine.connect() as conn:
        _res = conn.execute(
            text(f"SELECT * FROM logins WHERE token=:t"), {'t': token})
        for _ in _res:
            return Token(_.id, _.token, _.userid)
    return None


def register_token(userID: int) -> str:
    """Generate a new session token for the given user and insert it into DB. Returns the new token, if inserted into DB."""
    token = str(generate_token())
    debug(f'get_new_token({userID}) => {token}')
    stmt = tokensTable.insert().values(token=token, userid=int(userID))
    with engine.connect() as conn:
        _new_token_result = conn.execute(stmt)
        conn.commit()

        if _new_token_result.inserted_primary_key[0] > 0:
            return token
        else:
            return None


def get_available_projects(userID: int) -> list[Project]:
    projects = []
    # TODO filter out blocked company projects
    # TODO filter out projects this user is already asigned to
    with engine.connect() as conn:
        _result = conn.execute(text('SELECT p.id as pid, p.name as pname, p.created as pcreated, u.id as cid, u.email as cemail, u.name as cname, u.utype FROM projects p INNER JOIN users u ON p.companyid = u.id'))
        for _ in _result:
            _p = Project(_.pid, _.pname, _.cid, _.pcreated)
            _p.company = User(_.cid, _.cemail, _.cname, _.utype)
            projects.append(_p.to_json())
    return projects
