import json

import redis
import time
from db import connect_db_insert_sensor_data

# Connect to the Redis database
redis_host = 'localhost'  # Update this with your Redis server's host
redis_port = 6379  # Update this with your Redis server's port
redis_db = 0  # Update this with the desired database index

# Create a Redis client
client = redis.StrictRedis(host=redis_host, port=redis_port, db=redis_db)

# Set a sample key-value pair
# client.set('ss', 'my_value')

# Retrieve data
# retrieved_value = client.rpop('queue_3')
# retrieved_value = client.rpop('queue_2')
# retrieved_value = client.rpop('queue_1')
# retrieved_value = client.get('queue_3')
while True:
    # print("start")
    for queue in range(3, 0, -1):
        len_qu = client.llen(f'queue_{queue}')
        for item in range(len_qu):
            dt = client.rpop(f'queue_{queue}')
            if dt:
                print("write in cloud")
                dt = json.loads(dt)
                connect_db_insert_sensor_data(dt)
    # time.sleep(1)

# if retrieved_value:
#     decoded_value = retrieved_value.decode('utf-8')
#     print(f'Retrieved value: {decoded_value}')
# else:
#     print('Key not found in Redis')

# Close the connection
client.close()
