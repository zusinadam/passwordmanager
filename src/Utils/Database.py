from sqlalchemy import create_engine, Column, String, BigInteger, DateTime, Text, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy_utils import EmailType
from datetime import datetime
from Utils.Rsa import Rsa
from Utils.Sha512 import Sha512
from Utils.Password import Password
from re import compile, fullmatch

class Database:
    """ Class used to handle database operations """

    # Connection based used to connect this class with class which declare database table
    connection_base = declarative_base()

    def __init__(self, 
                 database_name: str,
                 username: str = 'postgres', 
                 password: str = 'admin', 
                 host: str = 'localhost', 
                 port: int = '5432', 
                 database_engine: str = 'postgresql' 
                 ) -> None:
        """ Initialize database class variables """
        
        # Database connection string data
        self.database_engine = database_engine
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.database_name = database_name

        # Database connection string
        self.connection_string = database_engine + '://' + username + ':' + password + '@' + host + ':' + port + '/' + database_name
        
        # Database connection and connection engine | None == 'Not connected'
        self.connection_engine = None
        self.connection = None

        # Sql error code | Don't display code error for the user, test only
        self.error_code = None

    def connect(self) -> bool:
        """ Create connection with database """

        # Connect with database, if success then return True
        try:
            self.connection_engine = create_engine(self.connection_string)
            self.connection_base.metadata.create_all(self.connection_engine)        
            self.connection = self.connection_engine.connect()
            self.error_code = None
            return True

        # If an error occured then return false, get code error, and clear connection data
        except SQLAlchemyError as e:
            self.connection_engine = None
            self.connection = None
            self.error_code = e.code
            print(f"Error while Creating connection to database: {e}")
            return False
        
    def is_connected(self) -> bool:
        """ Check connection with database, True - Connected | False - Not connected """

        # If not connected then return False
        if self.connection_engine == None or self.connection == None or self.connection.closed:
            return False
        
        # If connected then return True
        self.error_code = None
        return True

    def disconnect(self) -> None:
        """ Disconnect with database """

        # Try disconnect with database
        try:
            self.connection.close()
        except SQLAlchemyError as e:
            print(f"Error while disconnect database connection: {e}")
        
        # Finally set class defaults for connection data
        finally:
            self.connection_engine = None
            self.connection = None
            self.error_code = None

    def reconnect(self) -> bool:
        """ Try reconnect connection with database """

        # Try reconnect connection with database if closed 
        try:
            if self.connection.closed:
                self.connection = self.connection.engine.connect()
                self.error_code = None
                return True
            else:
              self.error_code = None
              return True
        
         # If an error occured then return false and get code error
        except SQLAlchemyError as e:
            self.error_code = e.code
            print(f"Error while reconnect connection to database: {e}")
            return False
    
class User(Database.connection_base):
    """ Class represents users table """

    # Declare table name
    __tablename__ = 'users'

    # Declare table columns
    id = Column(BigInteger, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(EmailType, unique=True, nullable=False)
    _password_hash = Column(String(128), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow)
    session = None
    
    @property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password: str) -> bool:
        """ Password value will be hashed default by setter """
        self._password_hash = Sha512.hash_message(password)

    def verify_password(self, password: str) -> bool:
        """ Compare if given password is the same as  stored hash """
        return Sha512.compare_to_hash(password, self.password_hash)

    @staticmethod
    def validate_username(username: str) -> bool:
        """ Validate if username is correct """
        if len(username) < 4:
            return [False, 'Username is too short. Minimum length is 4.']

        if len(username) > 50:
            return [False, 'Username is too long. Maximum length is 50.']

        return [True, 'Username is correct.']
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """ Validate if email is correct """

        regex = compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if not fullmatch(regex, email):
            return [False, 'Email is not valid.']

        if len(email) > 255:
            return [False, 'Email is too long. Maximum length is 255.']

        return [True, 'Email is correct.']

    @staticmethod
    def validate_password(password: str) -> list:
        """ Check if password is correct """
        x = Password.validate(password)
        
        if not x[0]:
            return [x[0], x[1]]
        
        return [True, 'Password was changed.']

    @classmethod
    def register(self, username: str, email: str, password: str, password2: str, engine) -> list:
        """ Register user """
        
        x = User.validate_username(username)
        if not x[0]:
            return x       

        x = User.validate_email(email)
        if not x[0]:
            return x    

        if password != password2:
            return [False, 'Password was not repeated correctly.']

        x = User.validate_password(password)
        if not x[0]:
            return x
        
        user = self(username=username, email=email)
        user.password_hash = password

        self.session = sessionmaker(bind=engine)()
        try:
            self.session.add(user)
            self.session.commit()
            self.session.close()
        except SQLAlchemyError as e:
            try:
                return [False, str.capitalize(str.replace(str.replace(str.replace(str.strip(str.split(e.args[0], 'DETAIL:  Key')[1]), '(', ''), ')', ''), '=', ' '))]
            except:
                return [False, 'Error occured during registration.']   
        return [True, user]

    @classmethod
    def login(self, username: str, password: str, engine) -> list:
        """ Login user """

        self.session = sessionmaker(bind=engine)()
        user = self.session.query(self).filter_by(username=username).first()

        if user:
            if user.verify_password(password):
                return [True, user]
            else:
                return [False, 'Invalid username or password.']
        
        return [False, 'Invalid username or password.']

    @classmethod
    def logout(self) -> None:
        """ Logout user """
        try:
            self.session.close()
        except:
            self.session = None
        finally:
            self.session = None
    
    @classmethod
    def is_logged(self) -> list:
        """ Check if user is alredy logged """

        if self.session == None:
            return [False, 'User is not logged.']
        return [True, 'User is logged in.']

    @classmethod
    def change_password(self, old_password: str, new_password: str, new_password2: str) -> list:
        """ Change connection of the user """

        if old_password == None or old_password == '':
            return [False, 'Entry old password.']
        
        if new_password == None or new_password == '':
            return [False, 'Entry old password.']

        if new_password != new_password2:
            return [False, 'New password not repeated correctly']
        
        if not self.verify_password(old_password):
            return [False, 'Old password is not correct.']
        
        if not Password.validate(new_password)[0]:
            return Password.validate(new_password)

        self.password_hash = new_password

        try:
            self.session.commit()
        except SQLAlchemyError as e:
            try:
                return [False, str.capitalize(str.replace(str.replace(str.replace(str.strip(str.split(e.args[0], 'DETAIL:  Key')[1]), '(', ''), ')', ''), '=', ' '))]
            except:
                return [False, 'Error occured during password modification.']   

        return [True, 'Password was changed.']


class UserPassword(Database.connection_base):
    """ Class represents users passwords table """

    # Declare table name
    __tablename__ = 'users_passwords'

    # Declare table columns
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'), primary_key=True)
    password_label = Column(String(25), nullable=False)
    password = Column(Text, nullable=False)
    password_key = Column(Text, nullable=False)
    created_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    session = None

    @classmethod
    def store(self, label: str, password: str, user: User, engine) -> list:
        """ Store  password """
        
        if len(label) < 4:
            return [False, 'Label is too short. Minimum length is 4']

        if len(label) > 25:
            return [False, 'Label is too long. Maximum length is 25']

        if len(password) < 2:
            return [False, 'Password is too short. Minimum length is 2']

        if len(password) > 500:
            return [False, 'Password is too long. Maximum length is 500']  

        if user == None or not user.is_logged()[0]:
            return [False, 'User is not logged.']
        
        self.session = sessionmaker(bind=engine)()
        user = self.session.query(User).filter_by(username=user.username).first()
        self.session.close()
        self.session = None

        if not user:
            return [False, 'User is not logged.']
        
        public_key, private_key = Rsa.generate_key_pair()

        encrypted_password = Rsa.encrypt(password, public_key)
        key_str = Rsa.key_to_str(private_key)

        userPassword = self(user_id=user.id, password_label=label, password=encrypted_password, password_key=key_str)

        self.session = sessionmaker(bind=engine)()
        try:
            self.session.add(userPassword)
            self.session.commit()
            self.session.close()
            return [True, user]
        except SQLAlchemyError as e:
            try:
                return [False, str.capitalize(str.replace(str.replace(str.replace(str.strip(str.split(e.args[0], 'DETAIL:  Key')[1]), '(', ''), ')', ''), '=', ' '))]
            except:
                return [False, 'Error occured during password store.']   
    
    def restore(self) -> list:
        """ Restore password from database """

        try:
            key_int = Rsa.str_to_key(self.password_key)
            password_encrypted = Rsa.str_to_int(self.password)
            password = Rsa.decrypt(password_encrypted, key_int)

            return [True, password]
        except:
            [False, 'Password don\'t exist.']

    @classmethod
    def get_for_user(self, user: User, engine) -> list: 

        try:
            session = sessionmaker(bind=engine)()
            userPassword = session.query(self).filter_by(user_id=user.id).order_by(self.created_date)
            session.close()
            session = None
            return [True, userPassword]
        except SQLAlchemyError as e:
            try:
                return [False, str.capitalize(str.replace(str.replace(str.replace(str.strip(str.split(e.args[0], 'DETAIL:  Key')[1]), '(', ''), ')', ''), '=', ' '))]
            except:
                return [False, 'Error occured during get user passwords.']   

# Class functionality test
if __name__ == '__main__':

    db = Database(database_name='menadzerhasel')

    assert db.connect() == True

    assert db.is_connected() == True

    db.disconnect()

    assert db.is_connected() == False