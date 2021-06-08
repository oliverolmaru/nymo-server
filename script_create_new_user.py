from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine  
from sqlalchemy.orm import sessionmaker
import models, schemas
import hashlib, os, binascii, datetime
import uuid
from database import Base
import math
from crud import create_user

db_string = "postgres://postgres:nymoserver@localhost"

db = create_engine(db_string)  

Session = sessionmaker(db)  
session = Session()

create_user(session,"nymoadmin","nymoadmin","47tAhjb")