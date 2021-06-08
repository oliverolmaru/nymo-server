from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class AccessTokenBase(BaseModel):
    token: str
    username: str
    creation_time: datetime

class AccessToken(AccessTokenBase):
    class Config:
        orm_mode = True

class ShipLogBase(BaseModel):
    timestamp: datetime
    #Navigation
    latitude: float
    longitude: float
    speed: float
    course: float
    ap_mode: str
    wind_direction: float
    wind_speed: float
    ais_message: str
    front_left_sensor_dist: int
    front_center_sensor_dist: int
    front_right_sensor_dist: int
    #Propulsion
    motor_left_temp: int
    motor_left_power: int
    motor_left_current: float
    motor_left_rpm: float
    motor_right_temp: int
    motor_right_power: int
    motor_right_current: float
    motor_right_rpm: float
    #Power
    battery_current: float
    battery_voltage: float
    battery_soc: float   

class ShipLog(ShipLogBase):
    id: int
    class Config:
        orm_mode = True

class RawLogBase(BaseModel):
    timestamp: datetime
    #Navigation
    latitude: float
    longitude: float
    speed: float
    course: float
    ap_mode: str
    wind_direction: float
    wind_speed: float
    ais_message: str
    front_left_sensor_dist: int
    front_center_sensor_dist: int
    front_right_sensor_dist: int
    #Propulsion
    motor_left_temp: int
    motor_left_power: int
    motor_left_current: float
    motor_left_rpm: float
    motor_right_temp: int
    motor_right_power: int
    motor_right_current: float
    motor_right_rpm: float
    #Power
    battery_current: float
    battery_voltage: float
    battery_soc: float   

class RawLog(RawLogBase):
    id: int
    class Config:
        orm_mode = True

class ShipLogGroup(BaseModel):
    id: int
    first_log_timestamp: datetime
    last_log_timestamp: datetime
    number_of_logs: int
    last_updated: datetime
    class Config:
        orm_mode = True