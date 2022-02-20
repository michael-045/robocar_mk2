class Sensor_Controller():
    def __init__(self, sensor_list):
        self.sensors = []
        for sensor in sensor_list:
            self.sensors.append(sensor)

    def get_sensors(self):
        return self.sensors


class Generic_Sensor:
    def __init__(self, name):
        self.name = name
        self.data = ""

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    def get_name(self):
        return self.name

    def return_print_data(self):
        return self.name + ": " + str(self.data)


class Dust_Sensor(Generic_Sensor):
    def __init__(self, name):
        Generic_Sensor.__init__(self, name)
        self.data_range = [Dust_Range("pm1"), Dust_Range("pm2.5"), Dust_Range("pm10")]

    def set_data(self, value, index):
        self.data_range[index].set_data(value)

    def return_print_data(self):
        string = self.data_range[0].return_print_data() + \
                 self.data_range[1].return_print_data() + \
                 self.data_range[2].return_print_data()
        return string


class Dust_Range(Generic_Sensor):
    def __init__(self, name):
        Generic_Sensor.__init__(self, name)

class TOF_Sensor(Generic_Sensor):
    def __init__(self, name):
        Generic_Sensor.__init__(self, name)

class Air_Sensor(Generic_Sensor):
    def __init__(self, name):
        Generic_Sensor.__init__(self, name)