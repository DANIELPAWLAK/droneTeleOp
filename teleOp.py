from djitellopy import tello
import cv2, pygame, sys, time

""" 
Class that allows users to control Tello Drone using keyboard input captured by pyGame with a live feed
display using the opencv library with the option to take screenshots. Device executing the code should
be first connected to the drones local network first when it is powered on
"""
class teleOp:
    def __init__(self):
        pygame.init()  # Initialising pygame to start input detection
        # Connecting to drone and creating an object instance
        self.Drone = tello.Tello()
        self.Drone.connect()
        # Speed variables used for different motions such up chaning altitude and moving forwards
        self.speed = 80
        self.liftSpeed = 80
        self.moveSpeed = 50
        self.rotationSpeed = 100
        # Variable used to be in charge of feed throughout class
        self.img = None
        # Call to main loop for operating drone
        self.operateDrone()

    # Reads keyboard input and perform actions based on those, returns the values the drone uses for traversal
    def keyboardInput(self):
        # Array with drone values left/right,front/back,up/down,yaw velocity
        droneVals = [0, 0, 0, 0]
        key = pygame.key.get_pressed()  # Gets key being pressed
        # Checks if app is closed to shutoff program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Right/Left
        if key[pygame.K_RIGHT]: droneVals[0] = self.speed
        elif key[pygame.K_LEFT]: droneVals[0] = -self.speed
        # Forwards/Backwards
        if key[pygame.K_UP]: droneVals[1] = self.moveSpeed
        elif key[pygame.K_DOWN]: droneVals[1] = -self.moveSpeed
        # Up/Down
        if key[pygame.K_w]: droneVals[2] = self.liftSpeed
        elif key[pygame.K_s]: droneVals[2] = -self.liftSpeed
        # Rotate right/left
        if key[pygame.K_d]: droneVals[3] = self.rotationSpeed
        elif key[pygame.K_a]: droneVals[3] = -self.rotationSpeed
        # Liftoff/Land
        if key[pygame.K_SPACE]: self.Drone.takeoff()
        elif key[pygame.K_q]: self.Drone.land()
        # Call to take screenshot
        if key[pygame.K_e]: self.takeScreenshot()

        return droneVals

    # Takes current frame and saves it on device
    def takeScreenshot(self):
        cv2.imwrite(f"tellopy/Resources/screenshots/{time.time()}.jpg", self.img)
        time.sleep(0.2)

    # Main function that has an indefinite loop to control drone flight and show live feed
    def operateDrone(self):
        # Prints battery level on startup
        print(self.Drone.get_battery())
        time.sleep(1)
        self.Drone.streamon()  # Turns stream on
        while True:
            # Gets user input and sends it to drone for control
            keyVals = self.keyboardInput()
            self.Drone.send_rc_control(keyVals[0], keyVals[1], keyVals[2], keyVals[3])
            # Gets frame from drone to show on window popup from cv2, window can be used for input
            self.img = self.Drone.get_frame_read().frame
            cv2.imshow('Drone Feed', self.img)
            cv2.waitKey(1)  # 1 ms delay


if __name__ == "__main__":
    teleOp()
