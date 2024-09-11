#!/usr/bin/env python3
import mysql.connector as con

"""
All necessary MySQL database functionality (connection, write, etc.).
"""


class DatabaseInstance:

    def __init__(self, hostip):
        self.connection = None
        self.hostip = hostip
        self.cursor = None
        self.tables = None
        self.sensors = {}

    def __enter__(self):
        self.connection, self.cursor = self.establishConnection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.close()

    # Connects to the running MySQL instance, selects the 'dacs' DB and returns a cursor to it
    def establishConnection(self):
        dbConnection = con.connect(
            host=self.hostip,
            user="root",
            password="aris",
            database="dacs",
        )
        dbCursor = dbConnection.cursor()
        return dbConnection, dbCursor

    # Checks if a write operation was successful
    def checkInsert(self, operation):
        if self.cursor.rowcount < 1:
            print("Write failed for ", operation)

    """
    Insertion of dynamic values
    - Sensor values
    - Actuator values
    - States
    - Safety
    """

    def sensor_to_id(self, name, config_id):
        key = tuple([name, config_id])
        if key in self.sensors:
            return self.sensors[key]
        else:
            query = "SELECT id FROM sensors WHERE name = %s AND config_id = %s"
            values = (name, config_id)
            self.cursor.execute(query, values)
            results = self.cursor.fetchone()
            if not results:
                print("Sensor is not registered in DB.")
                return
            self.sensors[tuple([name, config_id])] = results[0]
            return results[0]

    def getLatestConfigNumber(self):
        query = "SELECT id FROM configurations ORDER BY id DESC limit 1"
        self.cursor.execute(query)
        configId = self.cursor.fetchone()[0]
        return configId

    # Inserts a new entry into the 'sensor_values' table
    def writeNewSensorValue(self, sensorName, configId, value, timestamp):
        # print('hello')
        # Check if sensor exists
        query = "SELECT id FROM sensors WHERE name = %s AND config_id = %s"
        values = (sensorName, configId)
        self.cursor.execute(query, values)
        results = self.cursor.fetchone()
        if not results:
            print("Sensor is not registered in DB.")
            return
        sensorId = results[0]

        # Write sensor value
        query = "INSERT INTO sensor_values (sensor_id, value, timestamp) VALUES (%s, %s, %s)"
        values = (sensorId, value, timestamp)
        self.cursor.execute(query, values)
        self.connection.commit()
        # self.checkInsert("new sensor value")

    def writeManySensorValues(self, sensors, values, times, config_id):
        # Check if sensor exists
        data = []
        for i, sensor in enumerate(sensors):
            sensorId = self.sensor_to_id(sensor, config_id)
            datapoint = (sensorId, values[i], times[i])
            data.append(datapoint)

        # Write sensor value
        query = "INSERT INTO sensor_values (sensor_id, value, timestamp) VALUES (%s, %s, %s)"
        self.cursor.executemany(query, data)
        self.connection.commit()
        # self.checkInsert("new sensor value")

    # Inserts a new entry into the 'actuator_values' table
    def writeNewActuatorValue(self, actuatorName, configId, value, timestamp):

        # Check if actuator exists
        query = "SELECT id FROM actuators WHERE name = %s AND config_id = %s"
        values = (actuatorName, configId)
        self.cursor.execute(query, values)
        results = self.cursor.fetchone()
        if not results:
            print("Actuator" + actuatorName + " is not registered in DB.")
            return
        actuatorId = results[0]

        # Write actuator value
        query = "INSERT INTO actuator_values (actuator_id, value, timestamp) VALUES (%s, %s, %s)"
        values = (actuatorId, value, timestamp)
        self.cursor.execute(query, values)
        self.connection.commit()
        # self.checkInsert("new actuator value")

    # Inserts a new entry into the 'states' table
    def writeNewState(self, configId, state, timestamp):

        # Write state
        query = "INSERT INTO states (config_id, state, timestamp) VALUES (%s, %s, %s)"
        values = (configId, state, timestamp)
        self.cursor.execute(query, values)
        self.connection.commit()
        self.checkInsert("new state")

    # Inserts a new entry into the 'safety' table
    def writeNewSafety(self, isWarning, isAbort, timestamp):

        # Write state
        query = (
            "INSERT INTO safety (is_warning, is_abort, timestamp) VALUES (%s, %s, %s)"
        )
        values = (isWarning, isAbort, timestamp)
        self.cursor.execute(query, values)
        self.connection.commit()
        self.checkInsert("new safety")

    def writeNewCircuit(
        self, name, config_id, detected, pin_channel, issafe, timestamp
    ):

        # Write state
        query = "INSERT INTO circuit_values (name, config_id, detected, pin_channel, issafe, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (name, config_id, detected, pin_channel, issafe, timestamp)
        self.cursor.execute(query, values)
        self.connection.commit()
        self.checkInsert("new circuit")
