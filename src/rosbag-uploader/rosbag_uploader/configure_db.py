"""
Configures database
"""

from os.path import exists
import pandas as pd
import mysql.connector as con


class DatabaseInstance:

    ## Basic connection methods
    def __init__(self, hostip):
        self.connection = None
        self.hostip = hostip
        self.cursor = None
        self.tables = None

    def __enter__(self):
        self.connection, self.cursor = self.establishConnection()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.cursor.close()
        self.connection.close()

    def establishConnection(self):
        dbConnection = con.connect(
            host=self.hostip,
            user="root",
            password="Replace_me_wh3n_deploying_on_public_server",
            database="aris",
        )
        dbCursor = dbConnection.cursor(buffered=True)
        return dbConnection, dbCursor

    ## Insert methods

    # Checks if a write operation was successful
    def checkInsert(self, operation):
        if self.cursor.rowcount < 1:
            print("Write failed for ", operation)
            return False
        else:
            return True

    # Checks if a configuration already exists
    def checkConfig(self, name):
        query = "SELECT id from configurations WHERE name = %s"
        self.cursor.execute(query, (name,))
        if self.cursor.rowcount > 0:
            return True
        else:
            return False

    # Takes note of new configuration sheet
    def writeNewConfig(self, name):
        query = "INSERT INTO configurations (name) VALUES (%s)"
        values = (name,)
        self.cursor.execute(query, values)
        self.connection.commit()
        if not self.checkInsert("new config file"):
            return -1
        else:
            return self.cursor.lastrowid

    # Inserts a new test row, returns test ID if successful
    def writeNewTest(self, name, date, starttime, configId, description):
        query = "INSERT INTO tests (name, date, starttime, config_id, description) VALUES (%s, %s, %s, %s, %s)"
        values = (name, date, starttime, configId, description)
        self.cursor.execute(query, values)
        self.connection.commit()
        if not self.checkInsert("new test"):
            return -1
        else:
            return self.cursor.lastrowid

    # Insert all static sensor information
    def writeNewSensors(self, configId, sensors, phases, phases_numbers):

        sensors = sensors.dropna(subset=["Sensor ID"])
        sensors = sensors[sensors["Read Out"] == "yes"]

        # table 'sensors'
        for idx, row in sensors.iterrows():
            query = "INSERT INTO sensors (name, config_id) VALUES (%s, %s)"
            values = (row["Sensor ID"], configId)
            self.cursor.execute(query, values)
            self.connection.commit()
            self.checkInsert("new sensor")

        sensor_ids = []
        for sensor in sensors["Sensor ID"]:
            query = "SELECT id FROM sensors WHERE name = %s AND config_id = %s"
            self.cursor.execute(query, [sensor, configId])
            results = self.cursor.fetchone()
            sensor_ids.append(results[0])

        phases = phases.dropna()
        phase_ids = []
        for phase in phases:
            print(phase)
            query = "SELECT id FROM phases WHERE name = %s"
            self.cursor.execute(query, [phase])
            results = self.cursor.fetchone()
            phase_ids.append(results[0])

        # table 'sensors_meta'
        i = 0
        for idx, row in sensors.iterrows():
            query = "INSERT INTO sensors_meta (sensor_id, model, location, ain, unit, unc, unc_type) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            # query = "INSERT INTO sensors_meta (sensor_id, model, location, ain, unit) VALUES (%s, %s, %s, %s, %s)"
            model = row["Sensor Model"]
            location = row["Sensor Location"]
            ain = row["AIN"]
            unit = row["Units [UI]"]
            uncertainty = row["Uncertainty"]
            uncertainty_type = row["Uncertainty Type"]
            # values = (sensor_ids[i], model, location, ain, unit)
            values = (
                sensor_ids[i],
                model,
                location,
                ain,
                unit,
                uncertainty,
                uncertainty_type,
            )
            self.cursor.execute(query, values)
            self.connection.commit()
            self.checkInsert("new sensor meta")
            i = i + 1

        # table 'sensor_thresholds'
        i = 0
        for idx, row in sensors.iterrows():
            j = 0
            query = "INSERT INTO sensor_thresholds (sensor_id, phase_id, warning_min, warning_max, abort_min, abort_max) VALUES (%s, %s, %s, %s, %s, %s)"
            for phase in phases_numbers:
                if "%s [Warning, min]" % (phase) in row:
                    warning_min = row["%s [Warning, min]" % (phase)]
                    warning_max = row["%s [Warning, max]" % (phase)]
                    abort_min = row["%s [Abort, min]" % (phase)]
                    abort_max = row["%s [Abort, max]" % (phase)]
                    if warning_min == "-":
                        warning_min = None
                    else:
                        warning_min = float(warning_min)
                    if warning_max == "-":
                        warning_max = None
                    else:
                        warning_max = float(warning_max)
                    if abort_min == "-":
                        abort_min = None
                    else:
                        abort_min = float(abort_min)
                    if abort_max == "-":
                        abort_max = None
                    else:
                        abort_max = float(abort_max)

                    values = (
                        sensor_ids[i],
                        phase_ids[j],
                        warning_min,
                        warning_max,
                        abort_min,
                        abort_max,
                    )
                    self.cursor.execute(query, values)
                    self.connection.commit()
                    self.checkInsert("new sensor threshold")
                j = j + 1
            i = i + 1

    # Insert all static actuator information
    def writeNewActuators(self, configId, actuators):

        actuators = actuators.dropna(subset=["Actuator ID"])

        # table 'actuators'
        for idx, row in actuators.iterrows():
            query = "INSERT INTO actuators (name, config_id) VALUES (%s, %s)"
            values = (row["Actuator ID"], configId)
            self.cursor.execute(query, values)
            self.connection.commit()
            self.checkInsert("new actuator")

        actuator_ids = []
        for actuator in actuators["Actuator ID"]:
            query = "SELECT id FROM actuators WHERE name = %s"
            self.cursor.execute(query, [actuator])
            results = self.cursor.fetchone()
            actuator_ids.append(results[0])

        i = 0
        # table 'actuators_meta'
        for idx, row in actuators.iterrows():
            query = "INSERT INTO actuators_meta (actuator_id, model, location, ain, normal_state) VALUES (%s, %s, %s, %s, %s)"
            model = row["Type"]
            location = row["Location"]
            ain = row["AIN"]
            normal_state = row["Default State"]
            values = (actuator_ids[i], model, location, ain, normal_state)
            self.cursor.execute(query, values)
            self.connection.commit()
            self.checkInsert("new sensor meta")
            i = i + 1

    # Inserts/Updates phases
    def updatePhases(self, phases):
        phases = phases.dropna()
        for idx, value in phases.items():
            query = "SELECT id FROM phases WHERE name = %s"
            self.cursor.execute(query, (value,))
            if self.cursor.rowcount < 1:
                query = "INSERT INTO phases (name) VALUES (%s)"
                self.cursor.execute(query, (value,))
                self.connection.commit()

    # Inserts all static data given for a test
    def writeNewConfiguration(self, configFilePath, configId):

        # Check if configuration sheets exist
        excelFile = pd.ExcelFile(configFilePath)

        # Updating the phases
        phases = pd.read_excel(excelFile, "Phases with descriptions")
        self.updatePhases(phases["Phase Designation"])

        # Inserting sensors
        sensors = pd.read_excel(excelFile, "Sensors")

        self.writeNewSensors(
            configId,
            sensors,
            phases["Phase Designation"],
            phases["Phase Designation with Number"],
        )

        # Inserting actuators
        actuators = pd.read_excel(excelFile, "Actuators")

        self.writeNewActuators(configId, actuators)


def configure_db_main(
    configFilePath,
    description,
    hostip,
):

    print("This script prepares the dacs database for a new test.")
    print(
        "Make sure that the git repo configuration_tests has been cloned and pulled into the git folder!"
    )
    print(
        "Additionally, make sure that the configuration file you want to use for the test is ready and has the correct structure."
    )
    print()

    print(configFilePath)
    if not exists(configFilePath):
        print("The config file does not exist or is not in the correct location.")
        return False

    print(f"Reading the configuration name from {configFilePath}")
    excelFile = pd.ExcelFile(configFilePath)
    specs = pd.read_excel(excelFile, "Firing Parameter Specification")
    for idx, row in specs.iterrows():
        if row["Parameter"] == "Test Designation":
            configName = row["Value"]
            break

    configNameSplit = configName.split("_")
    if not len(configNameSplit) >= 3:
        print("The format of the configuration name is wrong.")
        return False

    testName = configNameSplit[1]
    testDate = configNameSplit[0]
    testTime = configNameSplit[2] + "00"
    testTime = ":".join(testTime[i : i + 2] for i in range(0, len(testTime), 2))

    with DatabaseInstance(hostip) as db:

        print("Configuring the database...")

        print("Checking if config/test already exists...")
        # if db.checkConfig(configName):
        #   exit("You have already configured the DB for this exact test and can move on to the next step in the procedures. Change the name of the config file if you want to use a new configuration or if you want to start a new test with an existing configuration.")
        # print()

        print("Adding a new configuration...")
        # configId = 1
        configId = db.writeNewConfig(configName)
        if configId == -1:
            print("Something went wrong. Check connection to the DB and start again.")
            return False
        testId = db.writeNewTest(testName, testDate, testTime, configId, description)
        if testId == -1:
            print("Something went wrong. Check connection to the DB and start again.")
            return False
        print()

        print("Configuring sensors and actuators...")
        db.writeNewConfiguration(configFilePath, configId)
        print()

        print("Success! The database is now ready for the test.")

    return True
