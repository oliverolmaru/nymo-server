import re
import datetime

log_file = open('log.txt')
lines = log_file.readlines()

log_output = []
count = 0

for line in lines:
    original_list = line.split(", ")

    processed_list = [re.sub("^[^:\r\n]+:", '', i) for i in original_list]
    separator = ", "
    log_output.append(separator.join(processed_list))

    #if(count % 100 == 0): print(log.timestamp)

separator = "\n"

output = separator.join(log_output)
output_file = open('processed_log.txt',"w")

output_file.write(output)

output_file.close()

print("DONE")