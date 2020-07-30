import pandas as pd
from sys import exit
import numpy as np
import random
import pygame
import math
import os

#initialising pygame
pygame.init()

#setup display
screen = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Guess The Word!!")
icon = pygame.image.load('abcd.png')
pygame.display.set_icon(icon)

NAME_FONT = pygame.font.SysFont('comicsans',24)
game_text='ENTER YOUR NAME TO PLAY:'
user_text= ' '

#alphabet console
global won
RADIUS = 20
waittick = 0
msg = False
GAP = 15
letters = []
startx = round((800 - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
    x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
    y = starty + ((i//13) * (GAP + RADIUS * 2))
    letters.append([x, y, chr(A + i), True])

LETTER_FONT = pygame.font.SysFont('comicsans', 40)
WORD_FONT = pygame.font.SysFont('comicsans', 50)
MESSAGE_FONT = pygame.font.SysFont('comicsans', 30)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

#secret word
words = ["PYTHON", "HELLO", "DEVELOPER", "LANGUAGE", "WORLD", "STRINGS", "PYGAME", "PANDAS", "PROGRAM","WRITE", "TUTORIAL",
         "CONNECT", "EXPERT", "TEACHER", "MICROSOFT", "LEARNING", "EDUONLINE"]
word = random.choice(words)
guessed = []

#chances left
chances = 8
chancesleft = 8

FPS = 60
clock = pygame.time.Clock()
running = True


def draw():
    screen.fill((178,255,102))

    icon1 = pygame.image.load('icon1.png')
    screen.blit(icon1, (120,70))

    text = TITLE_FONT.render("Guess The Word!!", 1, (0,0,0))
    screen.blit(text, (200, 70))
    if msg :
        screen.blit(game_msg,(210, 200))

    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + "  "
        else:
            display_word += "_  "
    text = WORD_FONT.render(display_word, 1, (0,0,0))
    screen.blit(text, (250, 300))

    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(screen, (0,0,0), (x, y), RADIUS, 3)
            text = LETTER_FONT.render(ltr, 1, (0,0,0))
            screen.blit(text, (x - text.get_width()/2, y - text.get_height()/2))


    text = MESSAGE_FONT.render("You have total 8 chances to guess",True,(255,0,0))
    screen.blit(text,(250, 150))
    pygame.display.update()

def display_message(message):
    screen.fill((178,255,102))
    text = WORD_FONT.render(message,True,(0,0,0))
    screen.blit(text,(800/2 - text.get_width()/2, 500/2 - text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

running = False

while not running :
    screen.fill((120,178,255))
    icon1 = pygame.image.load('icon1.png')
    screen.blit(icon1, (120,70))

    text = TITLE_FONT.render("Guess The Word!!", 1, (0,0,0))
    screen.blit(text, (200, 70))
    text_surface_game = NAME_FONT.render(game_text,True,(0,0,0))
    text_surface_user = NAME_FONT.render(user_text,True,(0,0,0))
    screen.blit(text_surface_game,(200,200))
    screen.blit(text_surface_user,(300,250))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            #exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key != pygame.K_RETURN:
                user_text += event.unicode
            if event.key == pygame.K_RETURN:
                running = True
    pygame.display.update()

#while running:

while running :
    clock.tick(FPS)
    waittick += 1
    if waittick == FPS*1 :  #for 1 seconds
        msg = False

    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_x, m_y = pygame.mouse.get_pos()
            for letter in letters:
                x, y, ltr, visible = letter
                dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                if visible and dis < RADIUS:
                    letter[3] = False
                    guessed.append(ltr)
                    if ltr not in word:
                        chancesleft -= 1
                        game_msg = MESSAGE_FONT.render("Oops! letter is not in the word, Chances left: " +str(chancesleft),True,(255,0,0))
                    else:
                        game_msg = MESSAGE_FONT.render("Letter is in the word, Chances left: " +str(chancesleft),True,(255,0,0))
                    waittick = 0
                    msg = True
                    break
    won = True
    for letter in word :
        if letter not in guessed :
            won = False
            break
    if won:
        display_message("You WON!")
        running = False

    if chancesleft == 0:
        display_message("You Lost!,The Word is : "+word)
        running = False

isFile=os.path.isfile('data.xlsx')
if isFile is False:
    data = pd.DataFrame({"player_name":[],"Chances":[],"W/L Status":[]})
    data.to_excel('data.xlsx')
else:
    data=pd.read_excel('data.xlsx',index_col=0)

if won:
    win_loss_status="WIN"
else:
    win_loss_status="LOSS"

data_new = pd.DataFrame({'player_name':[user_text],'Chances':[chancesleft],'W/L Status':[win_loss_status]})
df = data.append(data_new,ignore_index = True)
df.to_excel('data.xlsx')
pygame.quit()
