from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import crud, models, schemas

# OLD - POSTGRESQL
SQLALCHEMY_DATABASE_URL = "postgres://postgres:nymoserver@localhost"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
oldDb = SessionLocal()

# NEW - MYSQL
SQLALCHEMY_MYSQL_DATABASE_URL = "mysql+mysqlconnector://d100646_arendaja:SWdvDdgQF5wQ5A0f@d100646.mysql.zonevs.eu/d100646_asv?use_unicode=1&charset=utf8"

mysql_engine = create_engine(
    SQLALCHEMY_MYSQL_DATABASE_URL,
    pool_pre_ping=True
)
MySQLSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

newDb = MySQLSessionLocal()

#Base = declarative_base()

#models.Base.metadata.create_all(bind=mysql_engine)

# TRANSFER - USERS
# users = oldDb.query(models.User).all()
# x = 0
# while x < len(users):
#   newDb.merge(users[x])
#   x += 1

# newDb.commit()


#TRANSFER - LOG GROUPS
# groups = oldDb.query(models.ShipLogGroup).all()
# x = 0
# while x < len(groups):
#   newDb.merge(groups[x])
#   x += 1

# newDb.commit()

#TRANSFER - RAW SHIP LOGS
# rawLogs = oldDb.query(models.RawLog).all()
# x = 0
# while x < len(rawLogs):
#   newDb.merge(rawLogs[x])
#   x += 1

# newDb.commit()

#TRANSFER - SHIP LOGS
shipLogs = oldDb.query(models.ShipLog).all()
x = 0
while x < len(shipLogs):
  if(x % 1000 == 0):
    print(x)
  newDb.merge(shipLogs[x])
  x += 1

newDb.commit()



