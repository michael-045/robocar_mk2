# The User Interface Class definitions

import pygame
from pygame.locals import *
import sys

class User_Interface:

    def __init__(self, RC, IF_Type):
        self.__RC = RC  # RoboCar Object Reference
        self.__IF_Type = IF_Type

    def Clear_Screen(self):
        print('Clear User_Interface Screen')

    def Print_Menu(self):
        print('User_Interface Menu')

    def Read_Key(self):
        print('Read a key')


class PyGame_Interface(User_Interface):
    def __init__(self, RC, IF_Type, sensors):
        User_Interface.__init__(self, RC, IF_Type)
        pygame.init()
        self.display = pygame.display.set_mode((600, 600))

        self.__IF_type = IF_Type
        self.__RC = RC  # RoboCar Object Reference
        self.sensors = sensors

    def update_pygame_display(self):
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)
        black = (0,0,0)

        pygame.display.set_caption('Sensor Information')
        font = pygame.font.SysFont('Comic Sans MS', 26)

        index = 1

        self.display.fill(black)

        for sensor in self.sensors.get_sensors():
            if sensor.get_name() == "SM-UART-04L":
                for i in range(0,3):
                    font_render = font.render(sensor.data_range[i].return_print_data(), True, green, blue)
                    loc = font_render.get_rect()
                    loc.center = (600 // 6) + 100, (400 // 6) * index
                    self.display.blit(font_render, loc)
                    index += 1
            else:
                font_render = font.render(sensor.return_print_data(), True, green, blue)
                loc = font_render.get_rect()
                loc.center = (600 // 6) + 100, (400 // 6) * index
                self.display.blit(font_render, loc)
                index += 1

        pygame.display.update()

        """        
        for sub, payload in self.client.outputs.items():
            font_render = font.render(str(sub) + ": " + str(payload), True, green, blue)
            loc = font_render.get_rect()
            loc.center = (600 // 6) + 100, (400 // 6) * index
            self.display.blit(font_render, loc)
            index += 1
        """

    def Print_Menu(self):
        print('---------------------', self.__RC.get_name(), '---------------------')
        print('                                                                   ')
        print('      Use the arrow keys to navigate the RoboCar              ')
        print('                           ^                                  ')
        print('                           |                                  ')
        print('                       <------->                              ')
        print('                           |                                  ')
        print('                           v                                  ')
        print('                    Press q to quit                           ')
        print('                                                              ')
        print('----------------------', self.__IF_type, '------------------------')

    def Read_Key(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    print("Key Q has been pressed exit")
                    quit()
                    sys.exit()
                if event.key == pygame.K_c:
                    print("try to reconnect")
                    return "Reconnect"
                if event.key == pygame.K_a:
                    print("Key A has been pressed")
                    return "Air_Sensor_Toggle"
                if event.key == pygame.K_UP:
                    print("Key UP has been pressed")
                    return "Arrow_Up_P"
                if event.key == pygame.K_DOWN:
                    print("Key DOWN has been pressed")
                    return "Arrow_Down_P"
                if event.key == pygame.K_LEFT:
                    print("Key LEFT has been pressed")
                    return "Arrow_Left_P"
                if event.key == pygame.K_RIGHT:
                    print("Key RIGHT has been pressed")
                    return "Arrow_Right_P"
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    print("Key A has been released")
                if event.key == pygame.K_UP:
                    print("Key UP has been released")
                    return "Release"
                if event.key == pygame.K_DOWN:
                    print("Key DOWN has been released")
                    return "Release"
                if event.key == pygame.K_LEFT:
                    print("Key LEFT has been released")
                    return "Release"
                if event.key == pygame.K_RIGHT:
                    print("Key RIGHT has been released")
                    return "Release"


class Web_Interface(User_Interface):
    def __init__(self, RC):
        User_Interface.__init__(self, RC, 'Web')
        self.__RC = RC  # RoboCar Object
        self.Print_Menu()

    def Clear_Screen(self):
        print('Clear Screen on Web Interface')

    def Print_Menu(self):
        self.Clear_Screen()
        print(self.__RC.Get_Name())
        print('Print Web Interface Menu')
        print(self.__RC.Get_Interface_Type())

    def Read_Key(self):
        key = 'A'
        return key

