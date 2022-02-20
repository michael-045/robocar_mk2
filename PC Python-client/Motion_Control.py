# The Motion Control Class definitions
from enum import Enum

"""
def on_connect(client,userdata,flags,rc):
    print("connected  with code"+str(rc))
    client.subscribe("group1/test")

def on_message(client,userdata,msg):
    print(msg.topic+"  "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

topic = "group1/test"
broker = "10.120.0.211" #172.20.10.6

client.connect(broker,1883,60)"""

class DriveStates(Enum):
    STOP = 0
    FORWARD = 1
    BACKWARD = 2

class DirectionStates(Enum):
    FORWARD = 1
    LEFT = 2
    RIGHT = 3
    BACKWARD = 4
    STOP = 5

class Motion_Controller:

    def __init__(self, client):
        self.__Left_DriveUnit = Drive_Unit('LeftDrive')
        self.__Right_DriveUnit = Drive_Unit('RightDrive')
        self.__Direction_State = DirectionStates.STOP

        self.client = client

    def Stop(self):
        left = self.__Left_DriveUnit.Set_Drive_State(DriveStates.STOP)
        right = self.__Right_DriveUnit.Set_Drive_State(DriveStates.STOP)
        if self.__Direction_State != DirectionStates.STOP:
            self.client.publish(self.client.movement_topic, left + right)
            self.__Direction_State = DirectionStates.STOP

    def Forward(self):
        left = self.__Left_DriveUnit.Set_Drive_State(DriveStates.FORWARD)
        right = self.__Right_DriveUnit.Set_Drive_State(DriveStates.FORWARD)
        if self.__Direction_State != DirectionStates.FORWARD:
            self.client.publish(self.client.movement_topic, left + right)
            self.__Direction_State = DirectionStates.FORWARD

    def Backward(self):
        left = self.__Left_DriveUnit.Set_Drive_State(DriveStates.BACKWARD)
        right = self.__Right_DriveUnit.Set_Drive_State(DriveStates.BACKWARD)
        if self.__Direction_State != DirectionStates.BACKWARD:
            self.client.publish(self.client.movement_topic, left + right)
            self.__Direction_State = DirectionStates.BACKWARD

    def Left(self):
        left = self.__Left_DriveUnit.Set_Drive_State(DriveStates.BACKWARD)
        right = self.__Right_DriveUnit.Set_Drive_State(DriveStates.FORWARD)
        if self.__Direction_State != DirectionStates.LEFT:
            self.client.publish(self.client.movement_topic, left + right)
            self.__Direction_State = DirectionStates.LEFT

    def Right(self):
        left = self.__Left_DriveUnit.Set_Drive_State(DriveStates.FORWARD)
        right = self.__Right_DriveUnit.Set_Drive_State(DriveStates.BACKWARD)
        if self.__Direction_State != DirectionStates.RIGHT:
            self.client.publish(self.client.movement_topic, left + right)
            self.__Direction_State = DirectionStates.RIGHT


class Drive_Unit:

    count_debug = 1

    def __init__(self, Name):
        self.__Drive_State = DriveStates.STOP
        self.__Last_Drive_State = DriveStates.STOP
        self.__Name = Name

    def Set_Drive_State(self, Drive_State):
        DriveActions = {DriveStates.STOP: self.__Drive_Stop,
                        DriveStates.FORWARD: self.__Motor_forward,
                        DriveStates.BACKWARD: self.__Motor_backward}

        self.__Drive_State = Drive_State

        if Drive_State != self.__Last_Drive_State:  # To avoid multiple calls to the motors
            action = DriveActions.get(Drive_State)
            self.__Last_Drive_State = Drive_State
            return action()
        return "Z"

    def __Drive_Stop(self):  # This function made with a dummy speed because the action lookup
        print(Drive_Unit.count_debug, self.__Name, 'Motor Stop')
        Drive_Unit.count_debug += 1
        return "Z"

    def __Motor_forward(self):
        print(Drive_Unit.count_debug, self.__Name, 'Motor Forward')
        Drive_Unit.count_debug += 1
        return "F"

    def __Motor_backward(self):
        print(Drive_Unit.count_debug, self.__Name, 'Motor Backward')
        Drive_Unit.count_debug += 1
        return "B"