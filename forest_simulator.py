"""
forest simulator using turtle lib
based on final project from Object Oriented Programming - university

todo list:
1. finish interactions with each others
    like: breed of new turtles, feeding of animals - predatotors eat turtles, turtles eat from feeders
2. add gui for user to adjust simulation inputs
    like: nr of animals, time of simulation, movement speed of animals, feeders
3. add feeder for turtles instance

"""
import turtle as td
import random as rd
import tkinter as tk
import threading

scr_size_x=800
scr_size_y=600

# adjustable variables
no_of_predators=2
no_of_peacefuls=6

# Define screen
wn = td.Screen()
wn.title("Forest simulator")
wn.bgcolor('grey')
wn.setup(1000, 800)
wn.tracer(0)

# Draw board
pen = td.Turtle()
pen.color('black')
pen.penup()
pen.hideturtle()
pen.goto(-398, 298)
pen.pendown()
pen.goto(403, 298)
pen.goto(403, -298)
pen.goto(-398, -298)
pen.goto(-398, 298)
pen.penup()
pen.goto(-150, 320)
pen.write("SYMULATOR ŻYCIA W LESIE", align='center', font=('Courier', 24, 'normal'))

# Animal parent class inheriting after td.Turtle
class Animal(td.Turtle):

    def __init__(self, shape='square'):
        super(Animal, self).__init__()
        self.penup()
        self.shape(shape)
        # random start position
        self.RNG()        
        self.goto((self.x_breed, self.y_breed))

    # start coordinates, randomly generated
    def RNG(self):
        self.x_breed = rd.randint(-scr_size_x/2+10, scr_size_x/2-10)
        self.y_breed = rd.randint(-scr_size_y/2+10, scr_size_y/2-10)
    
    # moving animals on the screen
    def move(self):
        try:
            self.setx(self.xcor() + self.speed_x)
            self.sety(self.ycor() + self.speed_y)
            # Wall bouncing
            if self.xcor() >= 390:
                self.speed_x *= -1
            if self.xcor()<= -390:
                self.speed_x *= -1

            if self.ycor() >= 290:
                self.speed_y *= -1
            if self.ycor()<= -290:
                self.speed_y *= -1

        except:
            print('Brak atrybutu speed')

# Predator child class inheriting after Animal
class Predator(Animal):
    type = 'Predator'

    def __init__(self, speed=0.3, color='red', shape='triangle'):
        Animal.__init__(self)
        self.shape(shape)
        self.color(color)
        self.speed_x=speed
        self.speed_y=speed
        
    # method to decide what to do on collision with another object
    def onCollision(self, animal):
        if self.xcor() >= animal.xcor()-20 and self.xcor() <= animal.xcor()+20 and self.ycor() >= animal.ycor()-20 and self.ycor() <= animal.ycor()+20:

            if animal.type=='Peaceful':
                print('zderzenie predatora z peaceful')
                animal.setx(-450)
                list_of_animals.remove(animal)
            elif animal.type=='Predator':
                print('zderzenie predator z predator')
                self.speed_x *= -1
                self.speed_y *= -1
            
# Peaceful child class inheriting after Animal
class Peaceful(Animal):
    type = 'Peaceful'
    
    def __init__(self, speed=0.15, color='green', shape='turtle'):
        Animal.__init__(self)
        self.shape(shape)
        self.color(color)
        self.speed_x=speed
        self.speed_y=speed
        self.ableToBreed=True
    
    # method to decide what to do on collision with another object
    def onCollision(self, animal):
        if self.xcor() >= animal.xcor()-20 and self.xcor() <= animal.xcor()+20 and self.ycor() >= animal.ycor()-20 and self.ycor() <= animal.ycor()+20:

            if animal.type=='Peaceful':
                print('zderzenie peaceful z peaceful')
                self.speed_x *= -1
                self.speed_y *= -1
                if self.ableToBreed==True:
                    if rd.randint(1,10)>=5:
                        self.breed()
                        self.ableToBreed=False               

            elif animal.type=='Predator':
                pass

    # method for breeding new peaceful animals
    def breed(self):
        list_of_animals.append(Peaceful())
        print('breed of turtle')

class Gui:
    def __init__(self, win):
        button_start = tk.Button(win, text='Start symulacji', height=1, width=16, fg='black', bg='silver',
                            command=simulation)
        button_start.place(x=50, y=120)

        self.label_no_predators = tk.Label(win, text=f'Number of predators: {no_of_predators}')
        self.label_no_predators.place(x=100, y=50)
        button_inc_no_predators = tk.Button(win, text='+', height=1, width=1, command=self.incrementPredators)
        button_inc_no_predators.place(x=50, y=50)
        button_dec_no_predators = tk.Button(win, text='-', height=1, width=1, command=self.decrementPredators)
        button_dec_no_predators.place(x=30, y=50)

        self.label_no_peacefuls = tk.Label(win, text=f'Number of peacefuls: {no_of_peacefuls}')
        self.label_no_peacefuls.place(x=100, y=85)
        button_inc_no_peacefuls = tk.Button(win, text='+', height=1, width=1, command=self.incrementPeacefuls)
        button_inc_no_peacefuls.place(x=50, y=80)
        button_dec_no_peacefuls = tk.Button(win, text='-', height=1, width=1, command=self.decrementPeacefuls)
        button_dec_no_peacefuls.place(x=30, y=80)

    def incrementPredators(self):
        global no_of_predators
        no_of_predators+=1
        self.label_no_predators['text']=f'Number of predators: {no_of_predators}'

    def decrementPredators(self):
        global no_of_predators
        if no_of_predators!=0:
            no_of_predators-=1
            self.label_no_peacefuls['text']=f'Number of predators: {no_of_predators}'

    def incrementPeacefuls(self):
        global no_of_peacefuls
        no_of_peacefuls+=1
        self.label_no_peacefuls['text']=f'Number of peacefuls: {no_of_peacefuls}'

    def decrementPeacefuls(self):
        global no_of_peacefuls
        if no_of_peacefuls!=0:
            no_of_peacefuls-=1
            self.label_no_peacefuls['text']=f'Number of peacefuls: {no_of_peacefuls}'


def simulation():
    # screenDefine()
    window.destroy()

    # Create animal instances
    global list_of_animals
    list_of_animals=[]
    for _ in range(no_of_peacefuls):
        list_of_animals.append(Peaceful())
    for _ in range(no_of_predators):
        list_of_animals.append(Predator())
    # Run simulation
    timer=0
    while True:
        wn.update()

        for animal in list_of_animals:
            animal.move()
            for animal2 in list_of_animals:
                if animal != animal2:
                    animal.onCollision(animal2)
            # test.onCollision(animal)

        timer+=1

# Define GUI
window = tk.Tk()
window.title('GUI')
window.geometry('300x150')
Gui(window)

window.mainloop()

# thread1 = threading.Thread(target=simulation)
# thread1.start()

# thread2 = threading.Thread(target=window.mainloop)
# thread2.setDaemon(True)
# thread2.start()
