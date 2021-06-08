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

db_string = "postgres://postgres:nymoserver@localhost"

db = create_engine(db_string)  

Session = sessionmaker(db)  
session = Session()

min_seconds_between_groups = 3600


logs = session.query(models.ShipLog).all()

#Puhastame tabeli, võibolla tulevikus muutub
session.query(models.ShipLogGroup).delete()
session.commit()
logGroups = []

count = 0

for log in logs:
    count += 1
    if(count % 100 == 0): print(count)
    #Kas on olemas mõni grupp, mille algus - min_sec on väiksem kui otsitav logi timestamp ja lõpp + min_sec on suurem kui logi timestamp
    found_group = None
    for group in logGroups:
        if((group.first_log_timestamp - log.timestamp).total_seconds()-min_seconds_between_groups < 0 and  (group.last_log_timestamp-log.timestamp).total_seconds()+min_seconds_between_groups > 0):
            #Logi kuulub siia gruppi
            found_group = group
            break
    
    #Kui ühtegi sobivat gruppi ei eksisteeri, teeme uue
    if(found_group == None):
        found_group = models.ShipLogGroup()
        found_group.first_log_timestamp = log.timestamp
        found_group.last_log_timestamp = log.timestamp
        found_group.number_of_logs = 0 #Lisame hiljem
        found_group.last_updated = datetime.datetime.now()

        logGroups.append(found_group)

    if(found_group.first_log_timestamp > log.timestamp):
        found_group.first_log_timestamp = log.timestamp

    if(found_group.last_log_timestamp < log.timestamp):
        found_group.last_log_timestamp = log.timestamp

    found_group.number_of_logs += 1

    session.add(found_group)

session.commit()







