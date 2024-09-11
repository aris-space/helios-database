from db_utility import DatabaseInstance
import rosbag as rb
import time
import sys
import os

bagdirectory = "/home/dacs/git/data-management/database_pro/bagsvortex/Param_anal/"
print()
object = os.scandir(bagdirectory)
n = 0
for file in object:
    n = n + 1
print(n)
object = os.scandir(bagdirectory)
with DatabaseInstance("127.0.0.1") as db:
    print("opened db")
    try:
        query = (
            "SELECT id FROM configurations ORDER BY id DESC limit 1"  # WHERE id = 26
        )
        db.cursor.execute(query)
        configId = db.cursor.fetchone()[0]
        j = 1
        print(object)
        for bag in object:
            print("reading " + bag.name)
            print(
                "bag " + str(j) + " of " + str(n) + " bags: " + str(j / n * 100) + "%"
            )
            j = j + 1
            with rb.Bag(bag) as bag:
                # Iterates through bag file
                i = 0
                names = []
                values = []
                times = []
                for topic, msg, t in bag.read_messages():
                    if "sensor" in topic and not "moving" in topic:
                        convertedTime = t.to_time()
                        name = msg.sensorName
                        value = msg.value
                        names.append(name)
                        values.append(value)
                        times.append(convertedTime)
                        i = i + 1
                        if i == 5000:
                            db.writeManySensorValues(names, values, times, configId)
                            i = 0
                            names = []
                            values = []
                            times = []
                        # db.writeNewSensorValue(name, configId, value, convertedTime)

                    elif (
                        "actuator" in topic
                        and not "detection" in topic
                        and not "update" in topic
                    ):
                        convertedTime = t.to_time()
                        name = topic[10:]
                        if topic == "/actuator_at_fss_thr":
                            state = int(msg.throttle)
                        else:
                            state = int(msg.activate)
                        db.writeNewActuatorValue(name, configId, state, convertedTime)

                    # elif "/confirmation_state_topic" in topic:
                    #     convertedTime = t.to_time()
                    #     state = msg.state
                    #     db.writeNewState(configId, state, convertedTime)

                    elif "/start_firing_confirmation_topic" in topic:
                        if msg.data:
                            convertedTime = t.to_time()
                            state = "firing confirmation"
                            db.writeNewState(configId, state, convertedTime)

    #                 #elif "circuit" in topic:
    #                 #    convertedTime = t.to_time()
    #    name = msg.name
    #    pin_channel = msg.pin_channel
    #    detected = msg.detected
    #    issafe = msg.issafe
    #    db.writeNewCircuit(name, configId, detected, pin_channel, issafe, convertedTime)

    except FileNotFoundError:
        print("Cannot find file " + bagdirectory)
