# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 02:02:09 2023

@author: ozane
"""
import os
import time
import random
import keyboard

#For clearing the input buffer happening while getting input in MenuSettings
def flush_input():
    try:
        import msvcrt
        while msvcrt.kbhit():
            msvcrt.getch()
    except ImportError:
        import sys, termios
        termios.tcflush(sys.stdin, termios.TCIOFLUSH)

#For clearing the consoles current display
def Clear():
    os.system( 'cls' )

class Item:
    def __init__(self):
        self.category = 0           #Categories are 
        self.locX = 0               #0:empty, 1:snekBody, 2:food, 3:boulder
        self.locY = 0               #11:leftMovingSnekHead, 12:up, 13: r, 14:d
    
    def ChangeLoc(self, x, y):
        self.locX = x
        self.locY = y

class Config:
    def __init__(self):             
        self.mapSize = 12           #Default settings of the game
        self.snekSpeed = 0.5
        self.gameTime = 60
        self.boulderCount = 5
    
    def ChangeMapSize(self, size):
        if size < 5:
            self.mapSize = 5
        elif size > 20:
            self.mapSize = 20
        else:
            self.mapSize = size
    
    def ChangeSpeed(self, speed):
        #Snek speed is essentially consoles refresh rate
        if speed == 1:
            self.snekSpeed = 0.25
        elif speed == 2:
            self.snekSpeed = 0.35
        elif speed == 4:
            self.snekSpeed = 0.75
        elif speed == 5:
            self.snekSpeed = 1
        else:
            self.snekSpeed = 0.5
    
    def ChangeTime(self, time):
        #Already limited at inputValidation but I'm trying things
        if time < 20:
            self.gameTime = 20
        elif time > 300:
            self.gameTime = 300
        else:
            self.gameTime = time
    
    def ChangeBoulders(self, count):
        if count < 0:
            self.boulderCount = 0
        #Boulder count cant be more than maps tiles, it breaks
        elif count > self.mapSize + 15:
            self.boulderCount = self.mapSize + 15
        else:
            self.boulderCount = count


#Investigates incase integer input in interval input inadvertently incorrect
def InputValidation(lower, upper, question):
    while True:
        choice = input(question)
        if choice.isnumeric() == True:
            if int(choice) <= upper and int(choice) >= lower:
                return int(choice)
            else:
                print("Choice must be between " + str(lower) + "-" + str(upper))
        else:
            print("Make sure the input is all numeric.")

def MenuScores(scores): 
    highScore = 0
    for score in scores:
        if score > highScore:
            highScore = score
    print("SCORES\tHigh Score:", highScore)
    for i in range(0, len(scores)):
        print(f"{i + 1}. {scores[i]}")
    
    print("\nPress esc to close Scores.")
    while True:
        key = keyboard.read_hotkey(suppress=False)  
        if key == 'esc':
            return

def MenuSettings(config):
    key = 'unbind'
    question = ""
   
    #Variable 'key' is set to a default value 'unbind' every loop to ensure the
    #menu shows up each display
    while True:     
        if key == 'unbind':
            print("Settings\n" \
                  "1.Map Size\n" \
                  "2.Snek Speed\n" \
                  "3.Game Time\n" \
                  "4.Boulders\n")
            print("\nPress esc to exit.")
                
        key = keyboard.read_hotkey(suppress=False)    
        
        if key == 'esc':
            key = 'unbind'
            return
        elif key == '1':
            key = 'unbind'
            Clear()
            print(f"Current map size is {config.mapSize}x{config.mapSize}")
            question = "Change size to (5 - 20): "
            flush_input()
            config.ChangeMapSize(InputValidation(5, 20, question))
            #Have to recalculate boulders according to mapsize
            config.ChangeBoulders(config.boulderCount)
            Clear()
        elif key == '2':
            key = 'unbind'
            Clear()
            print(f"Current snek speed is {config.snekSpeed}")
            print("1 is fastest, 5 is slowest")
            question = "Change speed to (1 - 5): "
            flush_input()
            config.ChangeSpeed(InputValidation(1, 5, question))
            Clear()
        elif key == '3':
            key = 'unbind'
            Clear()
            print(f"Current game time is {config.gameTime} seconds")
            question = "Change time to (20 - 300): "
            flush_input()
            config.ChangeTime(InputValidation(20, 300, question))
            Clear()
        elif key == '4':
            key = 'unbind'
            Clear()
            print(f"Current number of boulders is {config.boulderCount}")
            question = "Change boulders to (0 - 35): "
            flush_input()
            config.ChangeBoulders(InputValidation(0, 35, question))
            Clear()
        else:
            continue
        
#Program runs mostly on MenuMain(). Function calls happens here and functions
#return here
def MenuMain():
    config = Config()
    scores = []
    key = 'unbind'
   
    while True:     
        if key == 'unbind':
            print("MAIN MENU\n" \
                  "1.Snake Game\n" \
                  "2.Scores\n" \
                  "3.Settings\n")
            print("\nPress esc to exit.")
                
        key = keyboard.read_hotkey(suppress=False)    
        
        if key == 'esc':
            key = 'unbind'
            return
        elif key == '1':
            key = 'unbind'
            Clear()
            scores.append(NewGame(config))
            Clear()
        elif key == '2':
            key = 'unbind'
            Clear()
            MenuScores(scores)
            Clear()
        elif key == '3':
            key = 'unbind'
            Clear()
            MenuSettings(config)
            Clear()
        else:
            continue

#Generates map as a [R]x[C] matrix with all empty Items with their locations
def GenerateMapEmpty(row, column):
    matrix = [[0 for x in range(column)] for y in range(row)]
    for y in range(row):
        for x in range(column):
            emptyTile = Item()
            emptyTile.ChangeLoc(x, y)
            matrix[y][x] = emptyTile    #Tile now has an Item(0, x, y)
    return matrix

#Displays the current state of the game map
def DisplayMap(gameMap):
    print(" ", end="")
    for x in gameMap[0]:
        print(" - ", end="")
    print()
    
    for row in gameMap:
        print("|", end="")
        for item in row:
            if item.category == 0:
                print("   ", end="")
            elif item.category == 1:
                print("[♦]", end="")
            elif item.category == 2:
                print("[ó]", end="")
            elif item.category == 3:
                print("[■]", end="")
            elif item.category == 11:
                print("[◄]", end="")
            elif item.category == 12:
                print("[▲]", end="")
            elif item.category == 13:
                print("[►]", end="")
            elif item.category == 14:
                print("[▼]", end="")
        print("|")
        
    print(" ", end="")
    for x in gameMap[0]:
        print(" - ", end="")
    print()

def DisplayTimer(passedTime, gameTime):
    print(f"Time: {gameTime-passedTime}".rjust(10, ' '))
    
def DisplayScore(food):
    print(f"Score: {food*5}".rjust(11, ' '), end="")

#This could also return the occupier type to reduce need of calls each step    
#Check if tile already has an item in matching category
def IsTileOccupiedBy(gameMap, itemCategory, x, y):
    if gameMap[y][x].category == itemCategory:
        return True
    return False  

#Can be used to create boulders, food and snek
#Creates desired Items and puts them randomly on the map
def GenerateItem(gameMap, numberOfItems, itemCategory):
    i = 0
    while i < numberOfItems:
        x = random.randint(0, len(gameMap[0]) - 1)
        y = random.randint(0, len(gameMap) - 1)
        #Only put an item if its an empty tile
        if IsTileOccupiedBy(gameMap, 0, x, y):
            gameMap[y][x].category = itemCategory
            i += 1
    #This is necessary to get sneks starting location
    if itemCategory == 1:
        return x, y
    return

#Calculating the next tile of the snek
def CalculateNewLocation(gameMap, direction, snekX, snekY):
    if direction == 1:
        snekX += -1
    elif direction == 2:
        snekY += -1
    elif direction == 3:
        snekX += 1
    elif direction == 4:
        snekY += 1
        
    if snekY == -1:
        snekY = len(gameMap) - 1
    elif snekY == len(gameMap):
        snekY = 0
    if snekX== -1:
        snekX = len(gameMap[0]) - 1
    elif snekX == len(gameMap[0]):
        snekX = 0
    
    return snekX, snekY

def MoveSnek(gameMap, direction, snekTail, snekX, snekY):
    #Don't initiate movement before game started
    if direction == 0:
        return 0, snekX, snekY
    
    oldX, oldY = snekX, snekY
    snekX, snekY = CalculateNewLocation(gameMap, direction, snekX, snekY)    
    
    if IsTileOccupiedBy(gameMap, 1, snekX, snekY):
        return 1, snekX, snekY
    
    if IsTileOccupiedBy(gameMap, 3, snekX, snekY):
        return 3, snekX, snekY
    
    direction = direction + 10          #For heads direction (11, 12, 13, 14)   
    snekTail.append([snekY, snekX])     #Adds the recently moved tile
    gameMap[oldY][oldX].category = 1    #Change tail from arrow to diamond  
    
    if IsTileOccupiedBy(gameMap, 2, snekX, snekY):
        gameMap[snekY][snekX].category = direction
        return 2, snekX, snekY
    
    gameMap[snekTail[0][0]][snekTail[0][1]].category = 0
    snekTail.pop(0)                     #Pops the least recently moved tile
    gameMap[snekY][snekX].category = direction
    return 0, snekX, snekY

def SnekEndGameScreen(food, passedTime):
    time.sleep(1)
    Clear()
    totalScore = (food * 5) + (passedTime // 1)
    print("Score:\n")
    time.sleep(0.5)
    print(f"Food: {food*5}")
    time.sleep(0.5)
    print(f"Time: {passedTime//1}")
    time.sleep(0.5)
    print(f"Total: {totalScore}")
    print("\nYOU DIED")
    time.sleep(2)
    return totalScore

def BindArrowKeys(direction):   
    keyboard.add_hotkey('left', lambda: ChangeDirection(direction, 1))
    keyboard.add_hotkey('up', lambda: ChangeDirection(direction, 2))
    keyboard.add_hotkey('right', lambda: ChangeDirection(direction, 3))
    keyboard.add_hotkey('down', lambda: ChangeDirection(direction, 4))

def BindEsc(endGame):
    keyboard.add_hotkey('esc', lambda: EndGame(endGame))

#Next two methods are used because keyboard.add_hotkey cannot change a variable
#by itself, it needs to use a method. And this worked..
def ChangeDirection(direction, value):
    direction[0] = value
        
def EndGame(endGame):
    endGame[0] = 1


#Initiates a new game and returns the score
def NewGame(config):
    #Initiate and fill the map
    gameMap = GenerateMapEmpty(config.mapSize, config.mapSize)
    snekX, snekY = GenerateItem(gameMap, 1, 1)
    GenerateItem(gameMap, 1, 2)
    GenerateItem(gameMap, config.boulderCount, 3)
    
    direction = [0]
    endGame = [0]
    BindArrowKeys(direction)
    BindEsc(endGame)
    food = 0
    passedTime = 0
    snekTail = [[snekY, snekX]]
    moveTimer = time.time()
    countdownTimer = time.time()
    
    #moveTimer and countdownTimer are distinct because moveTimer is bound to
    #snekSpeed and it refreshes the display. Countdown shouldn't be affected
    while endGame[0] == 0:          
        if direction[0] != 0:       #Timer waits until a direction has chosen    
            if time.time() > countdownTimer + 1:
                passedTime += 1
                countdownTimer = time.time()
        if time.time() > moveTimer + config.snekSpeed:
            nextTile, snekX, snekY = \
                    MoveSnek(gameMap, direction[0], snekTail, snekX, snekY)
            #Hitting a boulder or snekTail ends the game
            if nextTile == 1 or nextTile == 3:
                EndGame(endGame)
            #Generate new food if ones eaten
            if nextTile == 2:
                GenerateItem(gameMap, 1, 2)
                food += 1
            moveTimer = time.time()
            Clear()
            DisplayScore(food)
            DisplayTimer(passedTime, config.gameTime)
            DisplayMap(gameMap)
        if passedTime >= config.gameTime:   #Ends the game when times up
            EndGame(endGame)
        #time.sleep(0.05)        #does this increase performance?                
    keyboard.unhook_all_hotkeys()   #!Makes keys unusable otherwise!
    
    totalScore = SnekEndGameScreen(food, passedTime)
    return totalScore

def main():
    print("Welcome to the game.")
    time.sleep(1)
    Clear()
    
    MenuMain()
    
    print("Thanks you for playing.")
    time.sleep(1)
 
main()