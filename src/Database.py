from sqlalchemy import create_engine, Column, Integer, String, BigInteger
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, validates
from sqlalchemy_utils import EmailType

class Database():
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
        """ Disconnect with the database """

        # Check if a connection exists before trying to close it
        if self.connection is not None:
            self.connection.close()

        # Finally, set class defaults for connection data
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
            return False
    

# Klasy nie gotowe
class User(Database.connection_base):
    """ Class represents users table """

    # Declare table name
    __tablename__ = 'users'

    # Declare table columns
    id = Column(BigInteger, primary_key=True)
    email = Column(EmailType, unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    name = Column(String(50))
    surname = Column(String(50))
    phone_number = Column(String(50))
    

    @property
    def password(self):
        """ Raise error if tried to access password property """
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        """ Password value will be hashed default by setter """
        # Nie gotowe

        self.password_hash = password #generate_password_hash(password)

    def verify_password(self, password):
        """ Compare giv """
        return self.password_hash == password #check_password_hash(self.password_hash, password)



## TEST SECTION #############
db = Database(database_name='menadzerhasel')

print(db.connect())

print(db.is_connected())
print(db.disconnect())
