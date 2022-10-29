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
        lcd.rect(120, 135, 112, 60, 65535)
        lcd.vline(175, 135, 60, 65535)
        lcd.hline(120, 150, 112, 65535)
        lcd.hline(120, 165, 112, 65535)
        lcd.hline(120, 180, 112, 65535)
        printstring(" NAME  SCORE" ,129, 139, 1, 65535)
        # get high scores for the grid
        with open("highscore") as f:
            printstring(f.readline().rstrip('\n'), 124, 154, 1, 65535)
            printstring(f.readline().rstrip('\n'), 124, 169, 1, 65535)
            printstring(f.readline().rstrip('\n'), 124, 184, 1, 65535)
        # draw help text
        printstring("X: HELP", 150, 220, 1, 65535)
        printstring("Y: CONTINUE", 133, 230, 1, 65535)
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
                if keyX.value() == 0:
                    tetris.help()
                    break
                if keyY.value() == 0:
                    play = True
                    break
                wait = True
            if play != False: break
        if play != False: break
    lcd.fill_rect(120, 0, 120, 255, 0)
    lcd.fill_rect(5, 5, 110, 30, 0)
    printstring("TETRIS", 5, 10, 2, 65535)
    printstring("SCORE: " + '{:0>{w}}'.format(str(int(tetris.score)), w=6), 130, 5, 1, 65535)
    printstring("LINES: " + '{:0>{w}}'.format(str(int(tetris.lines)), w=4), 135, 15, 1, 65535)
    printstring("LEVEL: " + str(level), 148, 25, 1, 65535)
    lcd.fill_rect(120, 40, 20, 10, 65535)# skew
    lcd.fill_rect(130, 50, 20, 10, 65535)
    lcd.fill_rect(130, 70, 20, 10, 65535)# inverted skew
    lcd.fill_rect(120, 80, 20, 10, 65535)
    lcd.fill_rect(115, 103, 40, 10, 65535)# straight
    lcd.fill_rect(140, 126, 10, 20, 65535)# L
    lcd.fill_rect(120, 136, 20, 10, 65535)
    lcd.fill_rect(140, 156, 10, 20, 65535)# inverted L
    lcd.fill_rect(120, 156, 20, 10, 65535)
    lcd.fill_rect(125, 186, 20, 20, 65535)
    lcd.fill_rect(130, 226, 10, 10, 65535)
    lcd.fill_rect(120, 216, 30, 10, 65535)
    # lcd.fill_rect(160, 43, statistic, 14, 65535)
    lcd.show()
    while True:
        tetris.piece[0] = tetris.piece[1]
        tetris.piece[1] = random.randint(0, 6)
        tetris.rotation[0] = 0
        tetris.position = [[5, 20], [5, 20]]
        tetris.showNextPiece(tetris.piece[1])
        pieceRender = tetris.renderPiece(tetris.piece[0], tetris.rotation[0], tetris.position[0])
        if tetris.collisionCheck(pieceRender) == 1: break
        while True:
            wait = False
            # write board and piece to screen
            lcd.fill_rect(8, 39, 100, 200, 0)
            pieceRender = tetris.renderPiece(tetris.piece[0], tetris.rotation[0], tetris.position[0])
            tetris.render(pieceRender)
            # receive input and update the peice position until the timer runs out
            start = utime.ticks_ms()
            while utime.ticks_ms() - start < ((level-10)*(-100)):
                if utime.ticks_ms() - timerStart > 150:
                    update = False
                    if right.value() == 0:
                        if tetris.collisionCheck(tetris.renderPiece(tetris.piece[0], tetris.rotation[0], [tetris.position[0][0]-1, tetris.position[0][1]])) == 0:
                            tetris.position[0][0] -= 1
                            update = True
                    if left.value() == 0:
                        if tetris.collisionCheck(tetris.renderPiece(tetris.piece[0], tetris.rotation[0], [tetris.position[0][0]+1, tetris.position[0][1]])) == 0:
                            tetris.position[0][0] += 1
                            update = True
                    if keyB.value() == 0:
                        if tetris.collisionCheck(tetris.renderPiece(tetris.piece[0], ((tetris.rotation[0]+1)%4), tetris.position[0])) == 0:
                            tetris.rotation[0] = ((tetris.rotation[0]+1)%4)
                            update = True
                    if keyX.value() == 0:
                        if tetris.collisionCheck(tetris.renderPiece(tetris.piece[0], ((tetris.rotation[0]-1)%4), tetris.position[0])) == 0:
                            tetris.rotation[0] = ((tetris.rotation[0]-1)%4)
                            update = True
                    if keyY.value() == 0:
                        play = False
                        utime.sleep(0.5)
                        while True:
                            lcd.fill_rect(17, 100, 88, 18, 0)
                            printstring('PAUSED', 19, 102, 2, 65535)
                            lcd.show()
                            start = utime.ticks_ms()
                            while utime.ticks_ms() - start < 400:
                                if keyY.value() == 0:
                                    # rebuild everything
                                    pieceRender = tetris.renderPiece(tetris.piece[0], tetris.rotation[0], tetris.position[0])
                                    tetris.render(pieceRender)
                                    utime.sleep(1)
                                    play = True
                                    break
                            if play == True: break
                            pieceRender = tetris.renderPiece(tetris.piece[0], tetris.rotation[0], tetris.position[0])
                            tetris.render(pieceRender)
                            start = utime.ticks_ms()
                            while utime.ticks_ms() - start < 400:
                                if keyY.value() == 0:
                                    # rebuild everything
                                    pieceRender = tetris.renderPiece(tetris.piece[0], tetris.rotation[0], tetris.position[0])
                                    tetris.render(pieceRender)
                                    utime.sleep(1)
                                    play = True
                                    break
                            if play == True: break
                    elif down.value() == 0: break
                    
                    if update == True:
                        pieceRender = tetris.renderPiece(tetris.piece[0], tetris.rotation[0], tetris.position[0])
                        tetris.render(pieceRender)
                        timerStart = utime.ticks_ms()
            # move the piece down 1 unit, checking for collisions
            pendingPieceRender = tetris.renderPiece(tetris.piece[0], tetris.rotation[0], [tetris.position[0][0], tetris.position[0][1]-1])
            if tetris.collisionCheck(pendingPieceRender) == 1:
                tetris.position[0][0] -= 1
                for x in range(10):
                    for y in range(20):
                        tetris.board[x][y] += pieceRender[x][y]
                # score the board, adjusting it so there are no completed lines
                completeLines = list([])
                for y in range(20):
                    pixelCount = 0
                    for x in range(10):
                        pixelCount += tetris.board[x][y]
                    if pixelCount == 10:
                        completeLines.append(y)
                if len(completeLines) == 0: break
                elif len(completeLines) == 1: tetris.score += (40*(level+1))
                elif len(completeLines) == 2: tetris.score += (100*(level+1))
                elif len(completeLines) == 3: tetris.score += (300*(level+1))
                elif len(completeLines) == 4: tetris.score += (1200*(level+1))
                tetris.lines += len(completeLines)
                for y in completeLines:
                    lcd.fill_rect(8, 39+((y-19)*(-10)), 100, 10, 0)
                lcd.show()
                utime.sleep(0.4)
                for y in completeLines:
                    lcd.fill_rect(8, 39+((y-19)*(-10)), 100, 10, 65535)
                lcd.show()
                utime.sleep(0.4)
                for y in completeLines:
                    lcd.fill_rect(8, 39+((y-19)*(-10)), 100, 10, 0)
                lcd.show()
                utime.sleep(0.4)
                for y in completeLines:
                    lcd.fill_rect(8, 39+((y-19)*(-10)), 100, 10, 65535)
                lcd.show()
                utime.sleep(0.4)
                for y in completeLines:
                    lcd.fill_rect(8, 39+((y-19)*(-10)), 100, 10, 0)
                lcd.show()
                utime.sleep(0.4)
                while len(completeLines) > 0:
                    for y in completeLines:
                        for x in range(10):
                            tetris.board[x][y] = tetris.board[x][y+1]
                            if y < 18: tetris.board[x][y+1] = 1
                            else: tetris.board[x][y+1] = 0
                    completeLines = list([])
                    for y in range(20):
                        pixelCount = 0
                        for x in range(10):
                            pixelCount += tetris.board[x][y]
                        if pixelCount == 10:
                            completeLines.append(y)
                tetris.updateStats(level)
                break
            else: tetris.position[0][1] -= 1
            
    lcd.fill_rect(110, 35, 130, 220, 0)
    printstring("GAME", 140, 70, 3, 65535)
    printstring("OVER", 140, 100, 3, 65535)
    # draw highscore grid
    lcd.rect(120, 135, 112, 60, 65535)
    lcd.vline(175, 135, 60, 65535)
    lcd.hline(120, 150, 112, 65535)
    lcd.hline(120, 165, 112, 65535)
    lcd.hline(120, 180, 112, 65535)
    printstring(" NAME  SCORE" ,129, 139, 1, 65535)
    printstring("PRESS Y TO", 140, 210, 1, 65535)
    printstring("CONTINUE", 148, 220, 1, 65535)
    lcd.show()
    # get high scores for the grid
    with open("highscore") as f:
        line1 = f.readline().rstrip('\n')
        line2 = f.readline().rstrip('\n')
        line3 = f.readline().rstrip('\n')
    scores = {'score1': int(line1[7:12]), 'score2': int(line2[7:12]), 'score3': int(line3[7:12]), 'myscore': tetris.score}
    highscores = [key for (key, value) in sorted(scores.items(), key=lambda key_value: key_value[1])]
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', ' ', '-', '.']
    nameNumbers = [27, 27, 27, 27, 27, 27]
    inputIndex = 0
    name = ''.join([alphabet[nameNumbers[i]] for i in range(6)])
    if highscores.index('myscore') == 3:
        line3 = line2
        line2 = line1
        line1 = str(name+' '+zfill(str(tetris.score), 6))
    elif highscores.index('myscore') == 2:
        line3 = line2
        line2 = str(name+' '+zfill(str(tetris.score), 6))
    elif highscores.index('myscore') == 1:
        line3 = str(name+' '+zfill(str(tetris.score), 6))
    printstring(line1, 124, 154, 1, 65535)
    printstring(line2, 124, 169, 1, 65535)
    printstring(line3, 124, 184, 1, 65535)
    lcd.show()
    highlight = False
    c = colour(240, 240, 240)
    if highscores.index('myscore') != 0:
        while True:
            highlight = not highlight
            lcd.fill_rect(124, 153+((highscores.index('myscore')-3)*(-15)), 48, 10, 0)
            if highlight == True: lcd.fill_rect(123+(inputIndex*8), 154+((highscores.index('myscore')-3)*(-15)), 8, 8, c)
            else: lcd.fill_rect(123+(inputIndex*8), 154+((highscores.index('myscore')-3)*(-15)), 8, 8, 0)
            printstring(name, 124, 154+((highscores.index('myscore')-3)*(-15)), 1, 65535)
            lcd.show()
            if utime.ticks_ms() - start > 150:
                if up.value() == 0:
                    nameNumbers[inputIndex] = (nameNumbers[inputIndex] + 1)%29
                    name = ''.join([alphabet[nameNumbers[i]] for i in range(6)])
                    start = utime.ticks_ms()
                elif down.value() == 0:
                    nameNumbers[inputIndex] = (nameNumbers[inputIndex] - 1)%29
                    name = ''.join([alphabet[nameNumbers[i]] for i in range(6)])
                    start = utime.ticks_ms()
                elif right.value() == 0 and inputIndex != 5:
                    inputIndex += 1
                    start = utime.ticks_ms()
                elif left.value() == 0 and inputIndex != 0:
                    inputIndex -= 1
                    start = utime.ticks_ms()
                elif keyY.value() == 0: break
    if highscores.index('myscore') == 3: line1 = str(name+' '+zfill(str(tetris.score), 6))
    elif highscores.index('myscore') == 2: line2 = str(name+' '+zfill(str(tetris.score), 6))
    elif highscores.index('myscore') == 1: line3 = str(name+' '+zfill(str(tetris.score), 6))
    with open('highscore', 'w') as f:
        f.write(line1+'\n'+line2+'\n'+line3+'\n')
    while True:
        if keyY.value() == 0: break
    score = 0
    tetris.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
