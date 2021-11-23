#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 12 17:26:56 2019

@author: root
"""
import Tkinter as tk
import random
import time
import math
from PIL import Image

class world:
    #creates a world class that represents our plain
    foods = []
    foodsG = []
    bunnies = []
    bunniesG = []
    linesG = []
    hungryG = []
    newFoodCounter = 0
    nextFood = 10
    
    def __init__(self,x,y):
        self.width = x
        self.height = y
        self.foodQuant = 0
        self.bunniesQuant = 0
        
    #creates the window
    def createWindow(self):
        window = tk.Tk()
        window.title("Ecossystem V1")
        return window
    
    #adds the canvas
    def addCanvas(self, canvas):
        self.canvas = canvas
        
    #adds a food to the world
    def addFood(self, f):
        self.foods.append(f)
        #fd = self.canvas.create_oval(f.x, f.y, f.x+f.size, f.y+f.size, outline="black", fill=f.color)
        fd = self.canvas.create_image(f.x, f.y, image=foodgraphic)
        self.foodsG.append(fd)
        self.foodQuant+=1

    #instantiates a food object and adds to the world
    def createFood(self):
        f = food(randomX(), randomY())
        self.addFood(f)
        
    #adds a bunny to the world
    def addBunny(self, b):
        #adds the bunny to the list
        self.bunnies.append(b)
        #creates the bunny graphics
        #bn = self.canvas.create_rectangle(b.x, b.y, b.x+b.size, b.y+b.size, outline="black", fill=b.color)
        if(b.sex == "Male"):
            bn = self.canvas.create_image(b.x, b.y, image=mgraphic)
        else:
            bn = self.canvas.create_image(b.x, b.y, image=fgraphic)
        #adds the graphics to the list
        self.bunniesG.append(bn)
        #one more bunny!
        self.bunniesQuant+=1
        #creates the line of the bunny target
        ln = self.canvas.create_line(b.x, b.y, b.targetX, b.targetY)
        self.linesG.append(ln)
        #creates the hungry meter
        hg = self.canvas.create_text(b.x+15, b.y+15, text=str(b.hungry))
        self.hungryG.append(hg)
        
    #instantiates a bunny object and adds to the world, if no coordinates
    #are given, then the coordinate is random
    #note: fuck python for not having function overload
    def createBunny(self,x=None, y=None,name=None,sex=None, parent1=None, parent2=None):
        #parent1 = father, parent2 = mother
        #if there's no defined sex
        sex = random.choice(mf)
        #if there's no name, choose a name
        if(sex=="Male"):
            name = random.choice(mnames)
        else:
            name = random.choice(fnames)
            
        #if there is no defined x or y, defines it
        if(x==None or y==None):
            x = randomX()
            y = randomY()
        #if there is a mother, bunny is born in the same spot as the mother
        if(parent2!=None):
            x = parent2.x
            y = parent2.y 
            
        
        b = bunny(x, y, name, sex, parent1, parent2)
         
        self.addBunny(b)
        
    #updates the world 
    def update(self):
        #increases the food timer counter
        self.newFoodCounter+=1
        #if its time to generate a new food
        if(self.newFoodCounter >= self.nextFood):
            #creates it
            self.createFood()
            #sets the new timer
            self.nextFood = random.randint(0, 50) #0,100
            #resets the counter
            self.newFoodCounter=0
            
                
        #check if bunnies ate food
        for i in xrange(len(self.bunnies)):
            #increase reproduce urge
            self.bunnies[i].reproduceUrge+=self.bunnies[i].gene.reproduceWill
            #if bunny reached the target means it has eaten its food
            if(self.bunnies[i].x == self.bunnies[i].targetX and self.bunnies[i].y == self.bunnies[i].targetY):
                #removes the food from the list
                self.foods.remove(self.bunnies[i].target)
                #decreases the bunny hungry
                self.bunnies[i].hungry -= self.bunnies[i].target.satisfaction
                #calculate the bunnies targets again, since the food has changed
                for i in xrange(len(self.bunnies)):
                    self.bunnies[i].targetX = -1
                    self.bunnies[i].targetY = -1
                    self.bunnies[i].target = None
                    self.bunnies[i].findFood(self)
            
            #check if its a female
            if(self.bunnies[i].sex == "Female"):
                #check if its not already pregnant
                if(self.bunnies[i].pregnant==0):
                    #check if its able to be pregnant
                    if(self.bunnies[i].hungry <= -200):
                        self.bunnies[i].pregnant = 1
                        print(self.bunnies[i].name+" is pregnant!")
                #check if reached the time
                elif(self.bunnies[i].pregnant < self.bunnies[i].gene.pregnancyTime and self.bunnies[i].pregnant != 0):
                    #its pregnant but no ready to have babies, increase counter
                    self.bunnies[i].pregnant+=1
                else:
                    #ready to have babies
                    self.createBunny(None,None,None,None,self.bunnies[i],self.bunnies[i])
                    self.bunnies[i].pregnant=0
            #increases the hungry meter
            #self.bunnies[i].hungry+=1
            if(self.bunnies[i].gene.vel/2 > 1):
                self.bunnies[i].hungry+=self.bunnies[i].gene.vel/2
            else:
                self.bunnies[i].hungry+=1
            
        #check for bunnies movement
        i=0
        #iterate through the bunnies
        while(i < len(self.bunnies)):
            #if the hungry meter reached 100
            if(self.bunnies[i].hungry >= self.bunnies[i].gene.hungryLimit):
                #KILL
                print("\nDead: ")
                self.bunnies[i].printStats()
                self.bunnies.remove(self.bunnies[i])
                #iterates through it again
            else:
                #if its alive, just move
                self.bunnies[i].move(self)
                i+=1
        
        self.updateGraph()    
        
    #updates the graphics
    def updateGraph(self):
        #deletes the current forms
        self.canvas.delete("all")
        self.canvas.create_image(0,0,image=bg)
        self.foodsG = []
        self.bunniesG= []
        self.linesG = []
        self.hungryG = []
        
        #generate the new foods based on the list
        for i in xrange(len(self.foods)):
            #fd = self.canvas.create_oval(self.foods[i].x, self.foods[i].y, self.foods[i].x+self.foods[i].size, self.foods[i].y+self.foods[i].size, outline="black", fill=self.foods[i].color)
            fd = self.canvas.create_image(self.foods[i].x, self.foods[i].y, image=foodgraphic)
            self.foodsG.append(fd)
        
        #generate the new bunnies based on the list (they change position)
        for i in xrange(len(self.bunnies)):
            #bn = self.canvas.create_rectangle(self.bunnies[i].x, self.bunnies[i].y, self.bunnies[i].x+self.bunnies[i].size, self.bunnies[i].y+self.bunnies[i].size, outline="black", fill=self.bunnies[i].color)
            #creates the graphic based on the sex
            if(self.bunnies[i].sex == "Male"):
                #creates the graphic based on the rotation
                if(math.cos(self.bunnies[i].ang) >= 0):
                    bn = self.canvas.create_image(self.bunnies[i].x, self.bunnies[i].y, image=mgraphic)
                else:
                    bn = self.canvas.create_image(self.bunnies[i].x, self.bunnies[i].y, image=mgraphicf)
            else: #if its a female
                #creates the graphic based on the rotation
                if(math.cos(self.bunnies[i].ang) >= 0):
                    bn = self.canvas.create_image(self.bunnies[i].x, self.bunnies[i].y, image=fgraphic)
                else:
                    bn = self.canvas.create_image(self.bunnies[i].x, self.bunnies[i].y, image=fgraphicf)
                    
            ln = self.canvas.create_line(self.bunnies[i].x, self.bunnies[i].y, self.bunnies[i].targetX, self.bunnies[i].targetY)
            hg = self.canvas.create_text(self.bunnies[i].x+15, self.bunnies[i].y+15, text=str(self.bunnies[i].hungry))
            self.bunniesG.append(bn)    
            self.linesG.append(ln)
            self.hungryG.append(hg)
            
        self.canvas.update()
        
class food:
    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.size = 40
        self.color = "red"
        #how much hungry it reduces
        self.satisfaction = 80
        
class genes: 
        def __init__(self, parent1=None, parent2=None):
            #if there are parents get randomly the genes     
            if(parent1 != None and parent2 !=None):
                self.dov = random.choice([parent1.gene.dov,parent2.gene.dov])
                self.vel = random.choice([parent1.gene.vel, parent2.gene.vel])
                self.chanceToTurn = random.choice([parent1.gene.chanceToTurn, parent2.gene.chanceToTurn])
                self.hungryLimit = random.choice([parent1.gene.hungryLimit, parent2.gene.hungryLimit])
                self.pregnancyTime = random.choice([parent1.gene.pregnancyTime,parent2.gene.pregnancyTime])
                self.reproduceWill = random.choice([parent1.gene.reproduceWill, parent2.gene.reproduceWill])
                #10% chance to mutate
                if(random.random() < mutChance):
                    self.dov += random.randint(-10,10)
                if(random.random() < mutChance):
                    self.vel += random.randint(-1,1)
                if(random.random() < mutChance):
                    self.chanceToTurn += random.randint(-1,1)/10.0
                    if(self.chanceToTurn <=0):
                        self.chanceToTurn = 0.1
                if(random.random() < mutChance):
                    self.hungryLimit += random.randint(-20,20)
                if(random.random() < mutChance):
                    self.pregnancyTime += random.randint(-10,10)
                if(random.random() < mutChance):
                    self.reproduceWill += random.randint(-2,2)
            else:
                #if there are no parents generate random values
                self.dov = defaultDov + random.randint(-100, 100)
                self.vel = defaultVel + random.randint(-5, 5)
                self.chanceToTurn = defaultChanceToTurn
                self.hungryLimit = defaultHungryLimit + random.randint(-50, 50)
                self.pregnancyTime = defaultPregnancyTime
                self.reproduceWill = defaultReproduceWill
                
class bunny:
    
    def __init__(self,x,y,name,sex,parent1,parent2):
        #position
        self.x = x
        self.y = y
        #name :D
        self.name = name
        #sex
        self.sex = sex
        #size
        self.size = 50   
        #color of the bunny
        self.color = "saddle brown"
        #target coordinates
        self.targetX = -1
        self.targetY = -1
        #angular heading in radians, everyone start looking "upwards"
        self.ang = 90
        #hungry meter, if it reaches its limit, bunny's dead :(
        self.hungry = 0
        if(parent1 != None or parent2 != None):
            self.hungry = -50
        #pregnancy counter
        self.pregnant = 0
        #reproduce need counter
        self.reproduceUrge = 0
        
        self.gene = genes(parent1,parent2)
        
    def printStats(self):
        print("Name: "+self.name)
        print("Sex: "+self.sex)
        print("DOV: "+str(self.gene.dov)+"(+ "+str(self.gene.dov-defaultDov)+")")
        print("VEL: "+str(self.gene.vel)+"(+ "+str(self.gene.vel-defaultVel)+")")
        print("CTT: "+str(self.gene.chanceToTurn)+"(+ "+str(self.gene.chanceToTurn-defaultChanceToTurn)+")")
        print("HGL: "+str(self.gene.hungryLimit)+"(+ "+str(self.gene.hungryLimit-defaultHungryLimit)+")")
        print("PNT: "+str(self.gene.pregnancyTime)+"(+ "+str(self.gene.pregnancyTime-defaultPregnancyTime)+")")
        print("RPW: "+str(self.gene.reproduceWill)+"(+ "+str(self.gene.reproduceWill-defaultReproduceWill)+")\n")
    
    def move(self, w):
        self.findFood(w)
        #if there is no target then:
        #20% chance of turning, else, moves in the heading direction
        if(self.targetX == -1):
            if(random.random() <= self.gene.chanceToTurn):
                self.ang = random.randint(0, 360)
            else:
                self.x+= math.cos(self.ang) * self.gene.vel
                self.y+= math.sin(self.ang) * self.gene.vel
            
        #if there is a target..
        else:
            #change angle to match the target
            self.ang = math.atan2(self.targetY-self.y, self.targetX-self.x)
            #if can be reached
            if(abs(self.targetX-self.x)<self.gene.vel and abs(self.targetY-self.y)<self.gene.vel):
                self.x = self.targetX
                self.y = self.targetY
            else:
                #move in direction of the angle
                self.x+= math.cos(self.ang) * self.gene.vel
                self.y+= math.sin(self.ang) * self.gene.vel
            
        #if has passed the X limit
        if(self.x+self.size > w1.width+self.size):
            self.x -= self.size
        elif(self.x < 0):
            self.x += 5
        #if has passed the Y limit
        if(self.y+self.size > w1.height+self.size):
            self.y -= self.size
        elif(self.y < 0):
            self.y += 5
                
    def findFood(self, w):
        #the distance to the actual target, if there is none, the distance is 9999
        actualDist = eucDist(self.x, self.y, self.targetX, self.targetY)
        for i in xrange(len(w.foods)):
            #compensates for the plotting distance with +20 (size of food)
            d = eucDist(self.x, self.y, w.foods[i].x, w.foods[i].y)
            if(d <= self.gene.dov+20):
                #found food
                #if the distance to this food is less than the previous, change to the nearest
                if(d < actualDist):
                    self.targetX = w.foods[i].x
                    self.targetY = w.foods[i].y
                    self.target = w.foods[i]
    
#returns a random X inside the world
def randomX():
    return random.randint(0, w1.width-30)

#returns a random Y inside the world
def randomY():
    return random.randint(0, w1.height-30)

#returns the euclidian distance between 2 points
def eucDist(x1, y1, x2, y2):
    if(x2 == -1):
        return 9999
    return math.sqrt( ((x1-x2)**2)+((y1-y2)**2) )
    
#check for pressed key, used to speed up or slow down time
def pressedKey(e, time):
    if(time[0] > 0.1):
        if(e.char=="+"):
            time[0]-=0.1
            
    if(e.char=="-"):
        time[0]+=0.1
        
    if(e.char==" "):
        print("pressed space bar")
        if(time[1] == 1):
            time[1] = 0
        else:
            time[1] = 1
    print("speed: "+str(updateTime[0]))
    
def bunnyinfo(event):
    '''
    show x, y coordinates of mouse click position
    event.x, event.y relative to ulc of widget (here root) 
    '''
    # xy relative to ulc of root
    #xy = 'root x=%s  y=%s' % (event.x, event.y)
    # optional xy relative to blue rectangle
    for i in xrange(len(w1.bunnies)):
        if(abs(event.x-w1.bunnies[i].x) < 50 and abs(event.y - w1.bunnies[i].y) < 50):
            w1.bunnies[i].printStats()
        #xy = 'rectangle x=%s  y=%s' % (event.x-x1, event.y-y1)
    
mnames= ["Thumper","Oreo","Bunn Bunn","Coco","Cinnabun","Snowball","Bugz","Marshmallow","Midnight","Tambor","Pernalonga"]
fnames = ["Sally","Cocoa","Bambi","Bunny","Raphaela","Margarida","Sarinha","Mafalda","Angel","Lola"]
mf = ["Male","Female"]
#updateTime = 1 #seconds
updateTime = [0.05,0]
#chance of mutation, default = 10%
mutChance = 0.1
#params
defaultDov = 200 #100
defaultVel = 5 #5
defaultChanceToTurn = 0.1 #0.1
defaultHungryLimit = 500 #100
defaultPregnancyTime = 100 #100
defaultReproduceWill = 1 #1
#creates a 1000x1000 world
w1 = world(1000,1000)
#creates the window
window = w1.createWindow()
#creates the canvas
canvas = tk.Canvas(window, width=w1.width, height=w1.height )
canvas.pack()
bg = tk.PhotoImage(file="images/background2.png")
#configure the canvas background color to green
#canvas.configure(background="forest green")
canvas.create_image(0,0,image=bg)
w1.addCanvas(canvas)
#add a event checker to the window to update the simulation time
window.bind('<KeyPress>', lambda ef: pressedKey(ef, updateTime))
w1.canvas.bind('<Button-1>', bunnyinfo)

mgraphic = tk.PhotoImage(file="images/male50.png")
fgraphic = tk.PhotoImage(file="images/female50.png")
mgraphicf = tk.PhotoImage(file="images/male50f.png")
fgraphicf = tk.PhotoImage(file="images/female50f.png")
foodgraphic = tk.PhotoImage(file="images/bush40.png")

#creates 30 food
for i in xrange(0, 30):
    w1.createFood()
    
#creates 5 bunnies
for i in xrange(0,5):
    w1.createBunny()
    
#main simulation loop
while(True):
    time.sleep(updateTime[0])
    if(updateTime[1]==0):
        w1.update()
    window.update()
        
w1.canvas.update()
window.mainloop()

