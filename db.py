import psycopg2

import psycopg2

# Database connection parameters
db_params = {
    "host": "127.0.0.1",
    "database": "node",
    "user": "postgres",
    "password": "postgres"
}


def connect_db_insert_sensor_data(data):
    # Sample data to insert
    new_name = "John Doe"
    new_email = "john@example.com"
    # query = "insert into sensors(heart,temperature_sensor,blood_pressure_sensor,person_nid,start_at,pariority) values({0},{1},{2},{3}, to_timestamp({4}/1000),{5});".format(value, temperature_sensor, blood_pressure_sensor, id, date_time,pariority)

    # SQL query for insertion
    # insert_query = "INSERT INTO users (name, email) VALUES (%s, %s)"
    insert_query = f"insert into sensors(heart,temperature_sensor,blood_pressure_sensor,person_nid,start_at,pariority,is_from_queue) values(%s,%s,%s,%s,to_timestamp(%s),%s,%s)"
    # {'blood_pressure_sensor': {'c': 136, 'pariority': 3}, 'heart_sensor': {'b': 93, 'pariority': 1}, 'pariority': 1,
    # 'person_id': '1190147416', 'temperature_sensor': {'a': 40, 'pariority': 2}, 'time': '1692954182076'}
    blood_pressure_sensor = data.get('blood_pressure_sensor').get('c')
    heart_sensor = data.get('heart_sensor').get('b')
    temperature_sensor = data.get('temperature_sensor').get('a')
    time = int(data.get('time'))/1000
    person_id = data.get('person_id')
    pariority = data.get('pariority')

    # Establish a connection to the database
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Execute the insertion query
        cursor.execute(insert_query, (heart_sensor, temperature_sensor, blood_pressure_sensor, person_id, time,pariority,True))

        # Commit the transaction
        connection.commit()
        print("Data inserted successfully!")

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL:", error)

    finally:
        # Close the cursor and connection
        if connection:
            cursor.close()
            connection.close()
