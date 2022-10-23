# Raspberry Pi Pico microcontroller
# WaveShare Pico LCD 1.3 inch 240x240 screen with Joystick and Buttons
# Import the libraries needed
from machine import Pin,SPI,PWM
import framebuf
import utime
import random
import micropython
from lib import *

timerStart = utime.ticks_ms()

while True:
    while True:
        lcd.fill(0)
        # TETRIS side of the screen
        printstring("TETRIS", 5, 5, 3, 65535)
        lcd.rect(7, 38, 102, 202, 65535)
        # level select outline and text
        printstring("LEVEL", 145, 30, 2, 65535)
        lcd.rect(126, 50, 101, 41, 65535)
        lcd.hline(126, 70, 100, 65535)
        lcd.vline(146, 50, 40, 65535)
        lcd.vline(166, 50, 40, 65535)
        lcd.vline(186, 50, 40, 65535)
        lcd.vline(206, 50, 40, 65535)
        # draw highscore grid
        lcd.rect(125, 135, 102, 60, 65535)
        lcd.vline(180, 135, 60, 65535)
        lcd.hline(125, 150, 102, 65535)
        lcd.hline(125, 165, 102, 65535)
        lcd.hline(125, 180, 102, 65535)
        printstring(" NAME  SCORE" ,129, 139, 1, 65535)
        # get high scores for the grid
        f = open("highscore")
        printstring(f.readline().rstrip('\n'), 129, 154, 1, 65535)
        printstring(f.readline().rstrip('\n'), 129, 169, 1, 65535)
        printstring(f.readline().rstrip('\n'), 129, 184, 1, 65535)
        # draw help text
        printstring("X: CONTINUE", 133, 220, 1, 65535)
        printstring("Y: HELP", 150, 230, 1, 65535)
        # release the frame
        lcd.show()
        # ========== ACTION ==========
        level = 0
        play = False
        wait = 1
        while True:
            lcd.fill_rect(127, 51, 19, 19, 0) if level != 0 else lcd.fill_rect(127, 51, 19, 19, 65535)
            printchar('0', 131, 54, 2, 65535) if level != 0 else printchar('0', 131, 54, 2, 0)
            lcd.fill_rect(147, 51, 19, 19, 0) if level != 1 else lcd.fill_rect(147, 51, 19, 19, 65535)
            printchar('1', 151, 54, 2, 65535) if level != 1 else printchar('1', 151, 54, 2, 0)
            lcd.fill_rect(167, 51, 19, 19, 0) if level != 2 else lcd.fill_rect(167, 51, 19, 19, 65535)
            printchar('2', 171, 54, 2, 65535) if level != 2 else printchar('2', 171, 54, 2, 0)
            lcd.fill_rect(187, 51, 19, 19, 0) if level != 3 else lcd.fill_rect(187, 51, 19, 19, 65535)
            printchar('3', 191, 54, 2, 65535) if level != 3 else printchar('3', 191, 54, 2, 0)
            lcd.fill_rect(207, 51, 19, 19, 0) if level != 4 else lcd.fill_rect(207, 51, 19, 19, 65535)
            printchar('4', 211, 54, 2, 65535) if level != 4 else printchar('4', 211, 54, 2, 0)
            lcd.fill_rect(127, 71, 19, 19, 0) if level != 5 else lcd.fill_rect(127, 71, 19, 19, 65535)
            printchar('5', 131, 74, 2, 65535) if level != 5 else printchar('5', 131, 74, 2, 0)
            lcd.fill_rect(147, 71, 19, 19, 0) if level != 6 else lcd.fill_rect(147, 71, 19, 19, 65535)
            printchar('6', 151, 74, 2, 65535) if level != 6 else printchar('6', 151, 74, 2, 0)
            lcd.fill_rect(167, 71, 19, 19, 0) if level != 7 else lcd.fill_rect(167, 71, 19, 19, 65535)
            printchar('7', 171, 74, 2, 65535) if level != 7 else printchar('7', 171, 74, 2, 0)
            lcd.fill_rect(187, 71, 19, 19, 0) if level != 8 else lcd.fill_rect(187, 71, 19, 19, 65535)
            printchar('8', 191, 74, 2, 65535) if level != 8 else printchar('8', 191, 74, 2, 0)
            lcd.fill_rect(207, 71, 19, 19, 0) if level != 9 else lcd.fill_rect(207, 71, 19, 19, 65535)
            printchar('9', 211, 74, 2, 65535) if level != 9 else printchar('9', 211, 74, 2, 0)
            lcd.show()
            utime.sleep(0.2) if wait == True else utime.sleep(0.05)
            wait = False
            while True:
                if right.value() == 0 and level != 9:
                    level += 1
                    break
                if left.value() == 0 and level != 0:
                    level -= 1
                    break
                if keyY.value() == 0: tetris.help()
                if keyX.value() == 0:
                    play = True
                    break
                wait = True
            if play != False: break
        if play != False: break
    tetris.initStats(level)
    while True:
        tetris.piece[0] = tetris.piece[1]
        tetris.piece[1] = random.randint(0, 6)
        tetris.rotation[0] = 0
        tetris.position = [[5, 20], [5, 20]]
        tetris.showNextPiece(tetris.piece[1])
        pieceRender = tetris.renderPiece(tetris.piece[0], tetris.rotation[0], tetris.position[0])
        if tetris.collisionCheck(pieceRender) == 1:
            print('collision 95')
            break
        else: print('no collision 97')
        while True:
            wait = False
            # write board and piece to screen
            lcd.fill_rect(8, 39, 100, 200, 0)
            pieceRender = tetris.renderPiece(tetris.piece[0], tetris.rotation[0], tetris.position[0])
            tetris.render(pieceRender)
            # receive input and update the peice position until the timer runs out
            start = utime.ticks_ms()
            while utime.ticks_ms() - start < ((level-10)*(-100)):
                if utime.ticks_ms() - timerStart > 200:
                    update = False
                    if right.value() == 0:
                        if tetris.collisionCheck(tetris.renderPiece(tetris.piece[0], tetris.rotation[0], [tetris.position[0][0]-1, tetris.position[0][1]])) == 0:
                            tetris.position[0][0] -= 1
                            update = True
                    elif left.value() == 0:
                        if tetris.collisionCheck(tetris.renderPiece(tetris.piece[0], tetris.rotation[0], [tetris.position[0][0]+1, tetris.position[0][1]])) == 0:
                            tetris.position[0][0] += 1
                            update = True
                    elif keyA.value() == 0:
                        if tetris.collisionCheck(tetris.renderPiece(tetris.piece[0], ((tetris.rotation[0]+1)%4), tetris.position[0])) == 0:
                            tetris.rotation[0] = ((tetris.rotation[0]+1)%4)
                            update = True
                    elif keyB.value() == 0:
                        if tetris.collisionCheck(tetris.renderPiece(tetris.piece[0], ((tetris.rotation[0]-1)%4), tetris.position[0])) == 0:
                            tetris.rotation[0] = ((tetris.rotation[0]-1)%4)
                            update = True
                    elif down.value() == 0: break
                    if update == True:
                        pieceRender = tetris.renderPiece(tetris.piece[0], tetris.rotation[0], tetris.position[0])
                        tetris.render(pieceRender)
                        timerStart = utime.ticks_ms()
            # move the piece down 1 unit, checking for collisions
            pendingPieceRender = tetris.renderPiece(tetris.piece[0], tetris.rotation[0], [tetris.position[0][0], tetris.position[0][1]-1])
            if tetris.collisionCheck(pendingPieceRender) == 1:
                print('collision 131')
                tetris.position[0][0] -= 1
                for x in range(10):
                    for y in range(20):
                        tetris.board[x][y] += pieceRender[x][y]
                break
            else:
                print('no collision 138')
                tetris.position[0][1] -= 1
            
    lcd.fill_rect(110, 0, 130, 255, 0)
    lcd.fill_rect(0, 0, 110, 30, 0)
    printstring("GAME", 150, 70, 3, 65535)
    printstring("OVER", 150, 100, 3, 65535)
    lcd.show()
    break
