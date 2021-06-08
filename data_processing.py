import models, schemas

def generate_timestepped_logs(logs, timestep):
    outputted_logs = []
    current_cycle_start_time = None
    cycle_log_list = []
    x = 0
    while x < len(logs):
        if(current_cycle_start_time == None): current_cycle_start_time = logs[x].timestamp

        timediff = (logs[x].timestamp - current_cycle_start_time).total_seconds()
        if(timediff < timestep):
            cycle_log_list.append(logs[x])
            x += 1
            if(x != len(logs)-1): continue

        final_log = make_average_log(cycle_log_list)
        outputted_logs.append(final_log)

        cycle_log_list = []
        current_cycle_start_time = None
    return outputted_logs    

def generate_internal_logs(logs, timestep):
    outputted_logs = []
    current_cycle_start_time = None
    x = 0
    while x < len(logs):
        cycle_log_list = []
        current_cycle_start_time = logs[x].timestamp
        internal_log = models.InternalShipLog(logs[x])
        x+= 1
        #Are we at the end of logs? (1 log)
        if(x > len(logs)-1):
            outputted_logs.append(internal_log)
            break

        timediff = (logs[x].timestamp - current_cycle_start_time).total_seconds()
        while timediff < timestep:
            internal_log.add_additional_log(logs[x])
            x += 1
            #Are we at the end of logs? (many logs)
            if(x > len(logs)-1):
                break
            timediff = (logs[x].timestamp - current_cycle_start_time).total_seconds()
        outputted_logs.append(internal_log)

    return outputted_logs



def make_average_log(logs):
    ship_log = models.ShipLog()
    ship_log.timestamp = logs[0].timestamp
    ship_log.latitude = 0.0
    ship_log.longitude = 0.0
    ship_log.speed = 0.0
    ship_log.wind_speed = 0.0
    ship_log.front_left_sensor_dist = 0
    ship_log.front_center_sensor_dist = 0
    ship_log.front_right_sensor_dist = 0
    #Propulsion
    ship_log.motor_left_temp = 0.0
    ship_log.motor_left_power = 0.0
    ship_log.motor_left_current = 0.0
    ship_log.motor_left_rpm = 0.0
    ship_log.motor_right_temp = 0.0
    ship_log.motor_right_power = 0.0
    ship_log.motor_right_current = 0.0
    ship_log.motor_right_rpm = 0.0
    #Power
    ship_log.battery_current = 0.0
    ship_log.battery_voltage = 0.0
    ship_log.battery_soc = 0.0


    total = len(logs)

    for raw_log in logs:
        #Navigation
        ship_log.latitude += raw_log.latitude/total
        ship_log.longitude += raw_log.longitude/total
        ship_log.speed += raw_log.speed/total
        ship_log.course = raw_log.course
        ship_log.ap_mode = raw_log.ap_mode
        ship_log.wind_direction = raw_log.wind_direction
        ship_log.wind_speed += raw_log.wind_speed/total
        ship_log.ais_message = raw_log.ais_message
        ship_log.front_left_sensor_dist += raw_log.front_left_sensor_dist/total
        ship_log.front_center_sensor_dist += raw_log.front_center_sensor_dist/total
        ship_log.front_right_sensor_dist += raw_log.front_right_sensor_dist/total
        #Propulsion
        ship_log.motor_left_temp += raw_log.motor_left_temp/total
        ship_log.motor_left_power += raw_log.motor_left_power/total
        ship_log.motor_left_current += raw_log.motor_left_current/total
        ship_log.motor_left_rpm += raw_log.motor_left_rpm/total 
        ship_log.motor_right_temp += raw_log.motor_right_temp/total 
        ship_log.motor_right_power += raw_log.motor_right_power/total
        ship_log.motor_right_current += raw_log.motor_right_current/total
        ship_log.motor_right_rpm += raw_log.motor_right_rpm/total
        #Power
        ship_log.battery_current += raw_log.battery_current/total 
        ship_log.battery_voltage += raw_log.battery_voltage/total
        ship_log.battery_soc += raw_log.battery_soc/total
    
    return ship_log

def update_ship_log_groups():
    return