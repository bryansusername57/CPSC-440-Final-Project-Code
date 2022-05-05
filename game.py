# --------------- IMPORTS ------------- #
import pygame as py
import time
import random
from gpiozero import LED, Button

# --------------- SETTINGS ------------- #
py.init()
py.font.init()

WIDTH = 1080
LENGTH = 500

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

screen = py.display.set_mode((WIDTH, LENGTH))
clock = py.time.Clock()
py.display.set_caption('Racing Game')


# ---------------- LEDS and BUTTON for I/O --------------- #
ledWhite = LED(23)
ledRed = LED(24)
ledBlue = LED(8)
ledGreen = LED(25)
button = Button(21)

# ------------------- Class for the "Car" ------------------ #
class Car:
    def __init__(self, color, x, y, acceleration, maxspeed):
        super().__init__()
        self.color = color
        self.image = py.Surface((32,32))
        self.image.fill(color)
        self.rect = py.Rect((x, y), (32, 32))
        #self.speed = speed
        self.acceleration = acceleration
        self.maxspeed = maxspeed
        self.changex = 0

    # Is used for moving the "car" across the screen
    def update(self):
        screen.blit(self.image, self.rect)
        if (self.rect.x < WIDTH - 32): # Checks to see if the "car" is over the end of the screen
           self.changex += self.acceleration 
           if abs(self.changex) >= self.maxspeed: # If the positive changex is greater than or equal to the max speed 
               self.changex = self.changex / abs(self.changex) * self.maxspeed # Then divides the itself and multiples the max speed (which will be the max speed
                                                                               # because if 10 is changex then (10/10) = 1 * max speed = max speed)
            
            # Moves the "car" to the right of the screen by the change in x
           self.rect.x += self.changex 
           
    # Returns the "cars" x position to find which car is in first place
    def cars_x(self):
        return self.rect.x

#List of possible accelerations and max speeds a "car" could have
accellist = [2,3,4,5,6]
maxspeedlist = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

# Main loop of the game
def main_loop():
    # Picks a random acceleration and max speed for each "car" 
    randaccel1 = random.choice(accellist)
    randmaxspeed1 = random.choice(maxspeedlist)
    randaccel2 = random.choice(accellist)
    randmaxspeed2 = random.choice(maxspeedlist)
    randaccel3 = random.choice(accellist)
    randmaxspeed3 = random.choice(maxspeedlist)
    randaccel4 = random.choice(accellist)
    randmaxspeed4 = random.choice(maxspeedlist)

    # Creates 4 "car" each with a color, where it is on the screen, a random acceleration, and a random max speed
    car1 = Car(WHITE, 16, 100, randaccel1, randmaxspeed1)
    car2 = Car(RED, 16, 200, randaccel2, randmaxspeed2)
    car3 = Car(BLUE, 16, 300, randaccel3, randmaxspeed3)
    car4 = Car(GREEN, 16, 400, randaccel4, randmaxspeed4)

    #Used for the main while loop
    not_finished = True

    while not_finished:
        # First gets each "cars" x positions
        car1pos = car1.cars_x()
        car2pos = car2.cars_x()
        car3pos = car3.cars_x()
        car4pos = car4.cars_x()

        # Puts each of the x positions into a dictionary
        carpos_dict = {
            'Car 1': car1pos, 
            'Car 2': car2pos, 
            'Car 3': car3pos, 
            'Car 4': car4pos
            }

        # Puts each into a tuple to be sorted and then puts it back into a dictionary to be read
        sorted_tuple = sorted(carpos_dict.items(), key=lambda item: item[1], reverse=True)
        carpos_dict_sorted = {k: v for k, v in sorted_tuple}
        #print(carpos_dict_sorted)

        # Uses first variable to show who is in first place
        # Working on dealing with ties
        first = (next(iter(carpos_dict_sorted)))
        #second = (next(next(iter(carpos_dict_sorted))))
        print(first)
        #print(second)

        # Background color
        screen.fill(BLACK)

        # Checks to see if the x was clicked
        for event in py.event.get():
            if event.type == py.QUIT:
                quit()

        # Draws all the "cars" on the screen and moves each across
        car1.update()
        car2.update()
        car3.update()
        car4.update()

        # If a "car" reaches the end, break out of the loop
        for value in carpos_dict_sorted:
            if carpos_dict_sorted[value] >= WIDTH - 35:
                not_finished = False
        
        # Checks to see which "car" is in first and lights up the respective LED
        if first == 'Car 1':
            ledWhite.on()
            ledRed.off()
            ledBlue.off()
            ledGreen.off()
        elif first == 'Car 2':
            ledRed.on()
            ledWhite.off()
            ledBlue.off()
            ledGreen.off()
        elif first == 'Car 3':
            ledBlue.on()
            ledWhite.off()
            ledRed.off()
            ledGreen.off()
        elif first == 'Car 4':
            ledGreen.on()
            ledWhite.off()
            ledRed.off()
            ledBlue.off()
        
        # Updates the screen
        py.display.update()  # Or pygame.display.flip()
        clock.tick(20)

    # After the game is over, the LED will blink for about 8 seconds and then turn off and restart the loop
    print('WINNER')
    if first == 'Car 1':
        ledWhite.blink()
        time.sleep(8)
        ledWhite.off()
    elif first == 'Car 2':
        ledRed.blink()
        time.sleep(8)
        ledRed.off()
    elif first == 'Car 3':
        ledBlue.blink()
        time.sleep(8)
        ledBlue.off()
    elif first == 'Car 4':
        ledGreen.blink()
        time.sleep(8)
        ledGreen.off()

# Font and words for the title screen of the game
font1 = py.font.SysFont('chalkduster.ttf',72)
img1 = font1.render('ARE YOU READY!', True, WHITE)
img2 = font1.render('Push the button to start', True, WHITE)

# Main menu loop
running = True
background = BLACK
while running:
    for event in py.event.get():
        if event.type == py.QUIT:
            runnning = False
            
    screen.fill(background)
    screen.blit(img1, (WIDTH / 2 - 220, 50))
    screen.blit(img2, (WIDTH / 2 - 295, 200))
    py.display.update()
    
    # Once the button gets pressed, it start the game and will loop back until the x is pressed
    button.wait_for_press()
    main_loop()
