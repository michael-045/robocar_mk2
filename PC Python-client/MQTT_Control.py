import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("connected  with code"+str(rc))
    for topic in MQTT_Controller.sensor_topics:
        client.subscribe((MQTT_Controller.robocar_topic + topic), 0)
    # client.subscribe([("test/robocar1",0),("test/air",0),("test/dust",0)])

def on_message(client, userdata, msg):
    payload = msg.payload.decode("utf-8")
    topic = msg.topic
    #print(msg.topic+"  "+ payload)
    #MQTT_Controller.get_outputs()[msg.topic] = payload
    MQTT_Controller.message_topic = topic
    MQTT_Controller.message_payload = payload


class MQTT_Controller:

    robocar_topic = "robocar"
    movement_topic = "move_input"

    sensor_topics = ("/air_output",
                     "/dust_output/pm1",
                     "/dust_output/pm2.5",
                     "/dust_output/pm10",
                     "/tof_output",
                     "/debug_rb")

    message_topic = ""
    message_payload = ""

    def __init__(self, sensors):
        self.broker = "10.120.0.211"  # 172.20.10.6

        self.client = mqtt.Client()
        self.client.on_connect = on_connect
        self.client.on_message = on_message

        self.client.connect(self.broker, 1883, 60)  # broker, port, hz??

        self.sensors = sensors

        self.outputs = {MQTT_Controller.robocar_topic + "/air_output": self.sensors.get_sensors()[0],
                   MQTT_Controller.robocar_topic + "/dust_output/pm1": self.sensors.get_sensors()[1].data_range[0],
                   MQTT_Controller.robocar_topic + "/dust_output/pm2.5": self.sensors.get_sensors()[1].data_range[1],
                   MQTT_Controller.robocar_topic + "/dust_output/pm10": self.sensors.get_sensors()[1].data_range[2],
                   MQTT_Controller.robocar_topic + "/tof_output": self.sensors.get_sensors()[2],
                   MQTT_Controller.robocar_topic + "/debug_rb": "debug123"}

    def transfer_data(self):
        print("1", MQTT_Controller.message_topic + MQTT_Controller.message_payload)
        if MQTT_Controller.message_payload != "":
            self.outputs[MQTT_Controller.message_topic].set_data(MQTT_Controller.message_payload)
            print("2", self.outputs[MQTT_Controller.message_topic])

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def reconnect(self):
        self.client.connect(self.broker, 1883, 60)