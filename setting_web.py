from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from redis import Redis
from passlib.context import CryptContext
import pymongo
import configparser
import os


""" Настройка авторизации свегера в FastApi """

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/users/token",
    scheme_name="JWT", 
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.dirname(__file__)) + '/config_back.ini')
basedir = os.path.abspath(os.path.dirname(__file__))


class HeadConfigApp:
    def __init__(self):
        self.CONNECT_DB = os.getenv("CONNECT_DB", config["FASTAPI"]["CONNECT_DB"])
        self.DB_HOST = os.getenv("DB_HOST", config["DB"]["HOST"])
        self.DB_PORT = int(os.getenv("DB_PORT", config["DB"]["PORT"]))

        self.SECRET_KEY = config["FASTAPI"]["SECRET_KEY"]
        self.ALGORITHM = config["FASTAPI"]["ALGORITHM"]
        self.ACCESS_EXPIRE_MINUTES = int(config["FASTAPI"]["ACCESS_EXPIRE_MINUTES"])
        self.REFRESH_EXPIRE_MINUTES = int(config["FASTAPI"]["REFRESH_EXPIRE_MINUTES"])
        self.REFRESH_SECRET_KEY = config["FASTAPI"]["REFRESH_SECRET_KEY"]

        self.ADMIN_LOGIN = os.getenv("ADMIN_LOGIN", config["ADMIN"]["LOGIN"])
        self.ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", config["ADMIN"]["PASSWORD"])

        self.red = Redis(host=os.getenv("HOST_REDIS", config['REDIS']['HOST_REDIS']),
                                          port=os.getenv("PORT_REDIS", config['REDIS']['PORT_REDIS']),
                                          db=os.getenv("DB_REDIS", config['REDIS']['DB_REDIS']),
                                          decode_responses=True)
        
        self.file_name = os.path.dirname(__file__)


head_conf = HeadConfigApp()

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

"""   Setting Mongo   """

# db_client = pymongo.MongoClient(host=head_conf.DB_HOST, port = head_conf.DB_PORT)
db_client = pymongo.MongoClient(head_conf.CONNECT_DB)

db = db_client.files #DB

users_collection = db.get_collection("users_collection")
document_collection = db.get_collection("document_collection")

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

users_collection.create_index([("username", pymongo.TEXT)], unique = True)
                               
