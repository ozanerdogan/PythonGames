# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 04:40:41 2023

@author: ozane
"""
#TREASURE HUNT
import random
import keyboard
import os
import time

def Clear():
    os.system( 'cls' )

def Menu():
    question = ("MAIN MENU\n" \
                "1.Treasure Hunt\n" \
                "2.Settings\n" \
                "3.Arrow Game\n" \
                "4.Records\n" \
                "5.Quit\n")
    
    choice = InputValidation(1, 5, question)
    return choice

def ScoreMenu(thScores, agScores):
    current = 0
    while(True):
        time.sleep(0.1)
        print("\nUse arrow keys to navigate.\n" \
              "Press esc to go to the main menu.")   
        key = keyboard.read_hotkey(suppress=False)            
        if key == "esc":
            keyboard.unhook_all_hotkeys()
            return        
        if key == "right" or key == "left":
            if current == 0:
                current = 1
            elif current == 1:
                current = 0
        Clear()
        if current == 0:
            print("TREASURE HUNT")
            DisplayScores(thScores)
        elif current == 1:
            print("ARROW GAME")
            DisplayScores(agScores)
            
    
def DisplayScores(scores): 
    highScore = 0
    for score in scores:
        if score > highScore:
            highScore = score
    print("SCORES\tHigh Score:", highScore)
    for i in range(1, len(scores)):
        print(f"{i}. {scores[i]}")
    
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
 
#Wording can improve
def GetMapSize():
    print("Map size must be between (5x5 - 20x20)")
    question = "Enter map size: "
    size = InputValidation(5, 20, question)
    return size

def GenerateMap(row, column):
    Map = [[0 for x in range(column)] for y in range(row)]
    return Map

def GenerateTreasure(Map):    
    treasureCol = random.randint(0, len(Map[0]) - 1)
    treasureRow = random.randint(0, len(Map) - 1)
    Map[treasureRow][treasureCol] = 2
    return treasureCol, treasureRow

def DisplayGrid(Map):
    for row in Map:
        for value in row:
            if value == 2:
                symbol = "X"
            elif value == 1:
                symbol = "0"
            else:
                symbol = " "
            print(f"[{symbol}]", end="")
        print()

#DEFINE CONGRATS END SCREEN
def WinScreen():
    print()

def CalculateDistance(treasureRow, treasureCol, userRow, userCol):
    distance = abs(treasureCol - userCol) + abs(treasureRow - userRow)
    return distance

def Hint(distance, oldDistance):
    if distance > oldDistance:
        print("Colder")
    elif distance < oldDistance:
        print("Warmer")
        
def GetStartingLocation(row, column):
    print("Enter your starting location.")
    question = f"Row: 1 - {row}: "
    userRow = InputValidation(1, row, question) - 1
    question = f"Column: 1 - {column}: "
    userCol = InputValidation(1, column, question) - 1
    return userRow, userCol

def GetDirection():  #Doesnt needed after arrows
    question = "1-left 2-Up 3-Right 4-Down"
    direction = InputValidation(1, 4, question)
    return direction

def CalculateNewLocation(direction, userRow, userCol, mapSize):
    if direction == 1:
        userCol += -1
    elif direction == 2:
        userRow += -1
    elif direction == 3:
        userCol += 1
    elif direction == 4:
        userRow += 1
        
    if userRow == -1:
        userRow = mapSize - 1
    elif userRow == mapSize:
        userRow = 0
    if userCol == -1:
        userCol = mapSize - 1
    elif userCol == mapSize:
        userCol = 0
        
    return userRow, userCol

def ChangeDirection(direction, value):
    direction[0] = value
    
def ArrowKeys(direction):   
    keyboard.add_hotkey('left', lambda: ChangeDirection(direction, 1))
    keyboard.add_hotkey('up', lambda: ChangeDirection(direction, 2))
    keyboard.add_hotkey('right', lambda: ChangeDirection(direction, 3))
    keyboard.add_hotkey('down', lambda: ChangeDirection(direction, 4))

def ArrowGame(mapSize):
    Map = GenerateMap(mapSize, mapSize)
    treasureCol, treasureRow = GenerateTreasure(Map)
    Clear()
    userRow, userCol = GetStartingLocation(mapSize, mapSize)
    Clear()
    moveCount = 0
    distance = CalculateDistance(treasureRow, treasureCol, userRow, userCol)
    if distance == 0:
        print("YOU WON")
        print("Your score is", 100)
        input("Press enter to go to main menu. ")
        return 100
    Map[userRow][userCol] = 1
    DisplayGrid(Map)
    direction = [0]
    ArrowKeys(direction)    
    while(True):
        time.sleep(0.1)
        if(keyboard.is_pressed('left') \
          or keyboard.is_pressed('right')) \
          or keyboard.is_pressed('up') \
          or keyboard.is_pressed('down'):
            Map[userRow][userCol] = 0 #delete old location
            userRow, userCol = CalculateNewLocation(direction[0], userRow, userCol, mapSize)
            Clear()
            moveCount += 1
            distance = CalculateDistance(treasureRow, treasureCol, userRow, userCol)
            if distance == 0:
                print("YOU WON")
                keyboard.unhook_all_hotkeys()
                break
            Map[userRow][userCol] = 1
            DisplayGrid(Map)
    
    score = 100 - 5 * moveCount
    print("Your score is", score)
    input("Press enter to go to main menu. ")
    
    return score



def NewGame(mapSize):
    Map = GenerateMap(mapSize, mapSize) 
    treasureCol, treasureRow = GenerateTreasure(Map)
    Clear()
    userRow, userCol = GetStartingLocation(mapSize, mapSize)
    Clear()
    moveCount = 0
    distance = CalculateDistance(treasureRow, treasureCol, userRow, userCol)
    if distance == 0:
        print("YOU WON")
        print("Your score is", 100)
        input("Press enter to go to main menu. ")
        return 100
    print("Distance is", distance)
    Map[userRow][userCol] = 1
    DisplayGrid(Map)
    
    while(True):
        direction = GetDirection()
        Map[userRow][userCol] = 0 #delete old location
        userRow, userCol = CalculateNewLocation(direction, userRow, userCol, mapSize)
        Clear()
        moveCount += 1
        oldDistance = distance
        distance = CalculateDistance(treasureRow, treasureCol, userRow, userCol)
        Hint(distance, oldDistance)
        if distance == 0:
            print("YOU WON")
            break
        print("Distance is", distance)
        Map[userRow][userCol] = 1
        DisplayGrid(Map)
    
    score = 100 - 5 * moveCount
    print("Your score is", score)
    input("Press enter to go to main menu. ")
    
    return score
    
    
def main():
    mapSize = 5 #default map size
    thScores = [0]
    agScores = [0]
    while True:
        choice = Menu()
        Clear()
        if choice == 1:
            thScores.append(NewGame(mapSize))
        elif choice == 2:
            mapSize = GetMapSize()
        elif choice == 3:
            agScores.append(ArrowGame(mapSize))
        elif choice == 4:
            ScoreMenu(thScores, agScores)
        else:
            break
        Clear()
    
    input("Thanks for playing.")
    
        

main()


