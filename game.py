import pygame as py
import time
import random
from gpiozero import LED, Button

#py.init()
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
FPS = 60

ledWhite = LED(23)
ledRed = LED(24)
ledBlue = LED(8)
ledGreen = LED(25)
button = Button(21)

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

    def update(self):
        screen.blit(self.image, self.rect)
        if (self.rect.x < WIDTH - 32):
           self.changex += self.acceleration
           if abs(self.changex) >= self.maxspeed:
               self.changex = self.changex / abs(self.changex) * self.maxspeed
            
           self.rect.x += self.changex
           

    def cars_x(self):
        return self.rect.x

accellist = [2,3,4,5,6]
maxspeedlist = [6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]

def main_loop():
    randaccel1 = random.choice(accellist)
    randmaxspeed1 = random.choice(maxspeedlist)
    randaccel2 = random.choice(accellist)
    randmaxspeed2 = random.choice(maxspeedlist)
    randaccel3 = random.choice(accellist)
    randmaxspeed3 = random.choice(maxspeedlist)
    randaccel4 = random.choice(accellist)
    randmaxspeed4 = random.choice(maxspeedlist)

    car1 = Car(WHITE, 16, 100, randaccel1, randmaxspeed1)
    car2 = Car(RED, 16, 200, randaccel2, randmaxspeed2)
    car3 = Car(BLUE, 16, 300, randaccel3, randmaxspeed3)
    car4 = Car(GREEN, 16, 400, randaccel4, randmaxspeed4)

    not_finished = True

    while not_finished:
        font = py.font.SysFont("comicsansms", 55)
        testing_word = font.render("Hello World", 1, WHITE)

        screen.blit(testing_word, ((WIDTH / 2 - testing_word.get_width() / 2) - 15, 40))

        car1pos = car1.cars_x()
        car2pos = car2.cars_x()
        car3pos = car3.cars_x()
        car4pos = car4.cars_x()

        carpos_dict = {
            'Car 1': car1pos, 
            'Car 2': car2pos, 
            'Car 3': car3pos, 
            'Car 4': car4pos
            }

        sorted_tuple = sorted(carpos_dict.items(), key=lambda item: item[1], reverse=True)
        carpos_dict_sorted = {k: v for k, v in sorted_tuple}
        #print(carpos_dict_sorted)

        first = (next(iter(carpos_dict_sorted)))
        #print(first)

        screen.fill(BLACK)

        for event in py.event.get():
            if event.type == py.QUIT:
                quit()

        car1.update()
        car2.update()
        car3.update()
        car4.update()

        for value in carpos_dict_sorted:
            if carpos_dict_sorted[value] >= WIDTH - 35:
                not_finished = False
        
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
        
        py.display.update()  # Or pygame.display.flip()
        clock.tick(20)

    print('WINNER')
    if first == 'Car 1':
        ledWhite.blink()
        time.sleep(10)
        ledWhite.off()
    elif first == 'Car 2':
        ledRed.blink()
        time.sleep(10)
        ledRed.off()
    elif first == 'Car 3':
        ledBlue.blink()
        time.sleep(10)
        ledBlue.off()
    elif first == 'Car 4':
        ledGreen.blink()
        time.sleep(10)
        ledGreen.off()

font1 = py.font.SysFont('chalkduster.ttf',72)
img1 = font1.render('ARE YOU READY!', True, WHITE)
img2 = font1.render('Push the button to start', True, WHITE)

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
    
    button.wait_for_press()
    main_loop()
