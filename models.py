from sqlalchemy import Column, String, Integer, Float, DateTime  
from sqlalchemy.ext.declarative import declarative_base
from database import Base

class User(Base):  
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    email = Column(String(256), unique=True, index=True)
    password_hash = Column(String(256))
    password_salt = Column(String(256))

class AccessToken(Base):
    __tablename__ = "access_tokens"

    token = Column(String(64), primary_key=True)
    username = Column(String(256))
    creation_time = Column(DateTime)


class ShipLog(Base):
    __tablename__ = 'ship_log'

    #General
    timestamp = Column(DateTime, primary_key=True)
    #Navigation
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    course = Column(Float)
    ap_mode = Column(String(64))
    wind_direction = Column(Float)
    wind_speed = Column(Float)
    ais_message = Column(String(256))
    front_left_sensor_dist = Column(Float)
    front_center_sensor_dist = Column(Integer)
    front_right_sensor_dist = Column(Integer)
    #Propulsion
    motor_left_temp = Column(Integer)
    motor_left_power = Column(Integer)
    motor_left_current = Column(Float)
    motor_left_rpm = Column(Float)
    motor_right_temp = Column(Integer)
    motor_right_power = Column(Integer)
    motor_right_current = Column(Float)
    motor_right_rpm = Column(Float)
    #Power
    battery_current = Column(Float)
    battery_voltage = Column(Float)
    battery_soc = Column(Float)

class RawLog(Base):
    __tablename__ = 'ship_log_raw'

    #General
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, index=True)
    #Navigation
    latitude = Column(Float)
    longitude = Column(Float)
    speed = Column(Float)
    course = Column(Float)
    ap_mode = Column(String(64))
    wind_direction = Column(Float)
    wind_speed = Column(Float)
    ais_message = Column(String(256))
    front_left_sensor_dist = Column(Integer)
    front_center_sensor_dist = Column(Integer)
    front_right_sensor_dist = Column(Integer)
    #Propulsion
    motor_left_temp = Column(Integer)
    motor_left_power = Column(Integer)
    motor_left_current = Column(Float)
    motor_left_rpm = Column(Float)
    motor_right_temp = Column(Integer)
    motor_right_power = Column(Integer)
    motor_right_current = Column(Float)
    motor_right_rpm = Column(Float)
    #Power
    battery_current = Column(Float)
    battery_voltage = Column(Float)
    battery_soc = Column(Float)

class ShipLogGroup(Base):  
    __tablename__ = 'ship_log_groups'

    id = Column(Integer, primary_key=True)
    first_log_timestamp = Column(DateTime)
    last_log_timestamp = Column(DateTime)
    number_of_logs = Column(Integer)
    last_updated = Column(DateTime)

class MinMax:
    def __init__(self, value):
        self.__values_added = 1
        self.minimium = value
        self.average = value
        self.maximum = value
    def add_value(self,value):
        if(self.minimium > value):
            self.minimum = value
        if(self.maximum < value):
            self.maximum = value
        self.__values_added += 1
        self.average = self.average + (value-self.average)/(self.__values_added)
        

class InternalShipLog:
    def __init__(self, sqlalchemy_ship_log: ShipLog):
        self.timestamp = sqlalchemy_ship_log.timestamp
        self.latitude = sqlalchemy_ship_log.latitude
        self.longitude = sqlalchemy_ship_log.longitude
        self.speed = MinMax(sqlalchemy_ship_log.speed)
        self.course = sqlalchemy_ship_log.course
        self.ap_mode = sqlalchemy_ship_log.ap_mode
        self.wind_direction = MinMax(sqlalchemy_ship_log.wind_direction)
        self.wind_speed = MinMax(sqlalchemy_ship_log.wind_speed)
        self.ais_message = sqlalchemy_ship_log.ais_message
        self.front_left_sensor_dist = MinMax(sqlalchemy_ship_log.front_left_sensor_dist)
        self.front_center_sensor_dist = MinMax(sqlalchemy_ship_log.front_center_sensor_dist)
        self.front_right_sensor_dist = MinMax(sqlalchemy_ship_log.front_right_sensor_dist)
        #Propulsion
        self.motor_left_temp = MinMax(sqlalchemy_ship_log.motor_left_temp)
        self.motor_left_power = MinMax(sqlalchemy_ship_log.motor_left_power)
        self.motor_left_current = MinMax(sqlalchemy_ship_log.motor_left_current)
        self.motor_left_rpm = MinMax(sqlalchemy_ship_log.motor_left_rpm)
        self.motor_right_temp = MinMax(sqlalchemy_ship_log.motor_right_temp)
        self.motor_right_power = MinMax(sqlalchemy_ship_log.motor_right_power)
        self.motor_right_current = MinMax(sqlalchemy_ship_log.motor_right_current)
        self.motor_right_rpm = MinMax(sqlalchemy_ship_log.motor_right_rpm)
        #Power
        self.battery_current = MinMax(sqlalchemy_ship_log.battery_current)
        self.battery_voltage = MinMax(sqlalchemy_ship_log.battery_voltage)
        self.battery_soc = MinMax(sqlalchemy_ship_log.battery_soc)

    def add_additional_log(self, sqlalchemy_ship_log: ShipLog):
        self.speed.add_value(sqlalchemy_ship_log.speed)
        self.wind_direction.add_value(sqlalchemy_ship_log.wind_direction)
        self.wind_speed.add_value(sqlalchemy_ship_log.wind_speed)
        self.front_left_sensor_dist.add_value(sqlalchemy_ship_log.front_left_sensor_dist)
        self.front_center_sensor_dist.add_value(sqlalchemy_ship_log.front_center_sensor_dist)
        self.front_right_sensor_dist.add_value(sqlalchemy_ship_log.front_right_sensor_dist)
        #Propulsion
        self.motor_left_temp.add_value(sqlalchemy_ship_log.motor_left_temp)
        self.motor_left_power.add_value(sqlalchemy_ship_log.motor_left_power)
        self.motor_left_current.add_value(sqlalchemy_ship_log.motor_left_current)
        self.motor_left_rpm.add_value(sqlalchemy_ship_log.motor_left_rpm)
        self.motor_right_temp.add_value(sqlalchemy_ship_log.motor_right_temp)
        self.motor_right_power.add_value(sqlalchemy_ship_log.motor_right_power)
        self.motor_right_current.add_value(sqlalchemy_ship_log.motor_right_current)
        self.motor_right_rpm.add_value(sqlalchemy_ship_log.motor_right_rpm)
        #Power
        self.battery_current.add_value(sqlalchemy_ship_log.battery_current)
        self.battery_voltage.add_value(sqlalchemy_ship_log.battery_voltage)
        self.battery_soc.add_value(sqlalchemy_ship_log.battery_soc)