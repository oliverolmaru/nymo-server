from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
import models, schemas
import hashlib, os, binascii, datetime
import uuid
from data_processing import generate_internal_logs


def ship_log_exists(db: Session, timestamp: datetime) -> bool:
    try:
        db.query(models.ShipLog).filter_by(timestamp=timestamp).one()
    except NoResultFound:
        return False
    return True

def _checkLogGroupsWithLog(db: Session, log: models.ShipLog):
    min_seconds_between_groups = 3600
    logGroups = db.query(models.ShipLogGroup).all()

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
    try:
        db.add(found_group)
        db.commit()

    except (Exception) as error:
        return False
    
    return True

def save_ship_log(db: Session, log: schemas.ShipLogBase):
    db_log = models.ShipLog()
    #Let's format timestamp
    if(log.timestamp.microsecond < 500000):
        db_log.timestamp = log.timestamp - datetime.timedelta(microseconds = log.timestamp.microsecond)
    else:
        db_log.timestamp = log.timestamp - datetime.timedelta(microseconds = log.timestamp.microsecond) + datetime.timedelta(seconds = 1)
    
    if(ship_log_exists(db, db_log.timestamp)):
        return "EXISTS_ALREADY"

    db_log.latitude = log.latitude
    db_log.longitude = log.longitude
    db_log.speed = log.speed
    db_log.course = log.course
    db_log.ap_mode = log.ap_mode
    db_log.wind_direction = log.wind_direction
    db_log.wind_speed = log.wind_speed
    db_log.ais_message = log.ais_message
    db_log.front_left_sensor_dist = log.front_left_sensor_dist
    db_log.front_center_sensor_dist = log.front_center_sensor_dist 
    db_log.front_right_sensor_dist = log.front_right_sensor_dist
    #Propulsion
    db_log.motor_left_temp = log.motor_left_temp
    db_log.motor_left_power = log.motor_left_power
    db_log.motor_left_current = log.motor_left_current
    db_log.motor_left_rpm = log.motor_left_rpm 
    db_log.motor_right_temp = log.motor_right_temp 
    db_log.motor_right_power = log.motor_right_power
    db_log.motor_right_current = log.motor_right_current
    db_log.motor_right_rpm = log.motor_right_rpm
    #Power
    db_log.battery_current = log.battery_current 
    db_log.battery_voltage = log.battery_voltage
    db_log.battery_soc = log.battery_soc

    try:
        db.add(db_log)
        db.commit()

    except (Exception) as error:
        return "DB_FAILURE"

    if(not _checkLogGroupsWithLog(db, db_log)):
        return "DB_FAILURE"
    return "SUCCESS"


def get_ship_log(db: Session, id: int):
    return db.query(models.ShipLog).filter(models.ShipLog.id == id).first()

def get_ship_log_groups(db: Session):
    return db.query(models.ShipLogGroup).all()

def get_realtime_ship_logs(db: Session, rows: int = 1):
    logs = db.query(models.ShipLog).order_by(models.ShipLog.timestamp.desc()).limit(rows).all()
    return generate_internal_logs(logs, 1)   

def get_ship_logs(db: Session, skip: int = 0, limit: int = 100, timestep: int = 1, group_id : int = -1):
    if(group_id == -1):
        logs = db.query(models.ShipLog).offset(skip).limit(limit).all()
        if(timestep <= 1): return generate_internal_logs(logs, 1)
        return generate_internal_logs(logs, timestep)
    else:
        log_group = db.query(models.ShipLogGroup).filter_by(id = group_id).one()

        logs = db.query(models.ShipLog).order_by(models.ShipLog.timestamp).filter(models.ShipLog.timestamp >= log_group.first_log_timestamp,models.ShipLog.timestamp <= log_group.last_log_timestamp).all()

        
        if(timestep <= 1): return generate_internal_logs(logs)
        return generate_internal_logs(logs, timestep)        


def _hash(password:str, salt:str):
    pwdhash = hashlib.pbkdf2_hmac(hash_name='sha512', 
        password=password.encode('utf-8'), 
        salt=salt.encode('ascii'), 
        iterations=100000)
    
    return binascii.hexlify(pwdhash).decode("ascii")

def create_user(db: Session, email, name, password) -> bool:
    password_salt = hashlib.sha256(os.urandom(60)).hexdigest()
    password_hash = _hash(password, password_salt)
    id = None
    user = models.User()
    user.name = name
    user.email = email
    user.password_hash = password_hash
    user.password_salt = password_salt

    try:
        db.add(user)
        db.commit()
        return True

    except (Exception) as error:
        print(error)

    return False

def verify_password(db: Session, username: str, password: str) -> bool:
    try:
        if type(username) is not str or type(password) is not str:
            return False

        match = None
        try:
            match = db.query(models.User).filter_by(email=username).one()
        except (NoResultFound):
            print("User not found!")
            return False

        if match.password_hash == None or match.password_salt == None: return False
        if type(match.password_hash) is not str or type(match.password_salt) is not str: return False

        # Compare hashes
        password_hash = _hash(password, match.password_salt)
        return password_hash == match.password_hash
    except:
        print("Exception in verifyPassword")
        return False

def create_access_token(db: Session, username) -> str:
    access_token = models.AccessToken()
    access_token.token = uuid.uuid4().hex
    access_token.username = username
    access_token.creation_time = datetime.datetime.now()
    try:
        db.add(access_token)
        db.commit()
    except:
        return None
    return access_token.token

def verify_access_token(db: Session, token: str) -> bool:
        try:
            match = db.query(models.AccessToken).filter_by(token=token).one()
            return True
        except (NoResultFound):
            print("User not found!")
            return False

