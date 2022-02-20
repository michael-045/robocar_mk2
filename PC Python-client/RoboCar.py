# The RoboCar Class definitions
from User_Interface import PyGame_Interface
import Motion_Control
from Motion_Control import DirectionStates
from MQTT_Control import MQTT_Controller
import Sensors

class RoboCar:

    def __init__(self, Name):
        self.__Name = Name
        self.__State = DirectionStates.STOP

        # Sensors
        self.sensors = Sensors.Sensor_Controller([Sensors.Air_Sensor("SGP40"),
                                                  Sensors.Dust_Sensor("SM-UART-04L"),
                                                  Sensors.TOF_Sensor("VL53L0X")])

        # MQTT Controller Object is created
        self.MyMQTT = MQTT_Controller(self.sensors)

        # User Interface Object is created and RoboCar object reference is passed down
        #if IF_Type == 'Terminal':
        self.MyFace = PyGame_Interface(self, "PyGame Interface", self.sensors)
        #elif IF_Type == 'Web':
            #self.MyFace = Web_Interface(self)

        # Motion Control Object is created
        self.MyMotion = Motion_Control.Motion_Controller(self.MyMQTT)

        # Start the Main RoboCar Loop
        self.main_loop()

    def get_name(self):
        return self.__Name

    def set_state(self, State):
        self.__State = State

    def get_state(self):
        return self.__State

    def main_loop(self):

        quit = False

        actions = {DirectionStates.STOP: self.MyMotion.Stop,
                   DirectionStates.LEFT: self.MyMotion.Left,
                   DirectionStates.RIGHT: self.MyMotion.Right,
                   DirectionStates.FORWARD: self.MyMotion.Forward,
                   DirectionStates.BACKWARD: self.MyMotion.Backward}

        while not quit:
            self.MyMQTT.client.loop(0.1)

            self.MyMQTT.transfer_data()

            self.MyFace.update_pygame_display()

            key = self.MyFace.Read_Key()
            if key == 'q':
                quit = True
            elif key == "Release":
                self.set_state(DirectionStates.STOP)
            elif key == 'Arrow_Up_P':
                self.set_state(DirectionStates.FORWARD)
            elif key == 'Arrow_Down_P':
                self.set_state(DirectionStates.BACKWARD)
            elif key == 'Arrow_Left_P':
                self.set_state(DirectionStates.LEFT)
            elif key == 'Arrow_Right_P':
                self.set_state(DirectionStates.RIGHT)
            elif key == "Air_Sensor_Toggle":
                self.MyMQTT.publish(self.MyMQTT.movement_topic, "A")
            elif key == "Reconnect":
                self.MyMQTT.reconnect()

            action = actions.get(self.__State)
            action()