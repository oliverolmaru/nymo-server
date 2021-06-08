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

def ship_log_exists(db: Session, timestamp: datetime) -> bool:
    try:
        session.query(models.ShipLog).filter_by(timestamp=timestamp).one()
    except NoResultFound:
        return False
    return True


db_string = "postgres://postgres:nymoserver@localhost"

db = create_engine(db_string)  

Session = sessionmaker(db)  
session = Session()


logs = session.query(models.RawLog).all()

count = 0

for raw_log in logs:
    count += 1
    
    if(count % 100 == 0): print(count)
    ship_log = models.ShipLog()
    #General
    #if(raw_log.timestamp.mic) 
    if(raw_log.timestamp.microsecond < 500000):
        ship_log.timestamp = raw_log.timestamp - datetime.timedelta(microseconds = raw_log.timestamp.microsecond)
    else:
        ship_log.timestamp = raw_log.timestamp - datetime.timedelta(microseconds = raw_log.timestamp.microsecond) + datetime.timedelta(seconds = 1)
    #Navigation
    ship_log.latitude = raw_log.latitude
    ship_log.longitude = raw_log.longitude
    ship_log.speed = raw_log.speed
    ship_log.course = raw_log.course
    ship_log.ap_mode = raw_log.ap_mode
    ship_log.wind_direction = raw_log.wind_direction
    ship_log.wind_speed = raw_log.wind_speed
    ship_log.ais_message = raw_log.ais_message
    ship_log.front_left_sensor_dist = raw_log.front_left_sensor_dist
    ship_log.front_center_sensor_dist = raw_log.front_center_sensor_dist 
    ship_log.front_right_sensor_dist = raw_log.front_right_sensor_dist
    #Propulsion
    ship_log.motor_left_temp = raw_log.motor_left_temp
    ship_log.motor_left_power = raw_log.motor_left_power
    ship_log.motor_left_current = raw_log.motor_left_current
    ship_log.motor_left_rpm = raw_log.motor_left_rpm 
    ship_log.motor_right_temp = raw_log.motor_right_temp 
    ship_log.motor_right_power = raw_log.motor_right_power
    ship_log.motor_right_current = raw_log.motor_right_current
    ship_log.motor_right_rpm = raw_log.motor_right_rpm
    #Power
    ship_log.battery_current = raw_log.battery_current 
    ship_log.battery_voltage = raw_log.battery_voltage
    ship_log.battery_soc = raw_log.battery_soc

    if(ship_log_exists(session, ship_log.timestamp)): continue

    try:
        session.add(ship_log)
    except:
        print("Error while adding log")
    
try:
    session.commit()
except:
    print("Error while commiting")

