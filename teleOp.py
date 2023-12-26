from djitellopy import tello
import cv2
import pygame
import sys

class teleOp:

    def __init__(self):

        self.Drone = tello.Tello()
        self.Drone.connect()

        self.pGame = pygame.init()
        self.speed = 80
        self.liftSpeed = 80
        self.moveSpeed = 50
        self.rotationSpeed = 100

        self.operateDrone()

    def keyboardInput(self):
        #Array with drone values left/right,front/back,up/down,yaw velocity
        droneVals = [0,0,0,0]
        key = pygame.key.get_pressed() #Gets key being pressed
        #Checks if app is closed to shutoff program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        #Right/Left
        if key[pygame.K_RIGHT]: droneVals[0] = self.speed
        elif key[pygame.K_LEFT]: droneVals[0] = -self.speed
        #Forwards/Backwards
        if key[pygame.K_UP]: droneVals[1] = self.moveSpeed
        elif key[pygame.K_DOWN]: droneVals[1] = -self.moveSpeed
        #Up/Down
        if key[pygame.K_w]: droneVals[2] = self.liftSpeed
        elif key[pygame.K_s]: droneVals[2] = -self.liftSpeed
        #Rotate right/left
        if key[pygame.K_d]: droneVals[3] = self.rotationSpeed
        elif key[pygame.K_a]: droneVals[3] = -self.rotationSpeed
        #Liftoff/Land
        if key[pygame.K_SPACE]: print("liftoff")
        elif key[pygame.K_q]: print("land")

        return droneVals

    def operateDrone(self):
        windows = pygame.display.set_mode((400, 400))
        self.Drone.streamon()
        while True:

            keyVals = self.keyboardInput()
            self.Drone.send_rc_control(keyVals)

            img = cv2.resize(self.Drone.get_frame_read(), (1080,720))
            cv2.imshow('Drone Feed', img)
            cv2.waitKey(1)

if __name__ == "__main__":
    teleOp()




