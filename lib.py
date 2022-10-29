# Raspberry Pi Pico microcontroller 
# WaveShare Pico LCD 1.3 inch 240x240 screen with Joystick and Buttons
# Import the libraries needed
from machine import Pin,SPI,PWM
import framebuf
import utime
import random
import micropython
# ============ Start of Drive Code ================
BL = 13  # Pins used for WS 1.3" Pico LCD display screen
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

class LCD_1inch3(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 240
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        micropython.mem_info()
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,100000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        micropython.mem_info()
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)  

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)

    def init_display(self):
        """Initialize display"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)########### 0x70

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00) 
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xef)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0x00)
        self.write_data(0xEF)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)
# ========= End of Driver ===========
# ==== Start of Improved Text system  - 3 sizes of text ===========    
#ASCII Character Set
cmap = ['00000000000000000000000000000000000', #Space
        '00100001000010000100001000000000100', #!
        '01010010100000000000000000000000000', #"
        '01010010101101100000110110101001010', ##
        '00100011111000001110000011111000100', #$
        '11001110010001000100010001001110011', #%
        '01000101001010001000101011001001101', #&
        '10000100001000000000000000000000000', #'
        '00100010001000010000100000100000100', #(
        '00100000100000100001000010001000100', #)
        '00000001001010101110101010010000000', #*
        '00000001000010011111001000010000000', #+
        '000000000000000000000000000000110000100010000', #,
        '00000000000000011111000000000000000', #-
        '00000000000000000000000001100011000', #.
        '00001000010001000100010001000010000', #/
        '01110100011000110101100011000101110', #0
        '00100011000010000100001000010001110', #1
        '01110100010000101110100001000011111', #2
        '01110100010000101110000011000101110', #3
        '00010001100101011111000100001000010', #4
        '11111100001111000001000011000101110', #5
        '01110100001000011110100011000101110', #6
        '11111000010001000100010001000010000', #7
        '01110100011000101110100011000101110', #8
        '01110100011000101111000010000101110', #9
        '00000011000110000000011000110000000', #:
        '01100011000000001100011000010001000', #;
        '00010001000100010000010000010000010', #<
        '00000000001111100000111110000000000', #=
        '01000001000001000001000100010001000', #>
        '01100100100001000100001000000000100', #?
        '01110100010000101101101011010101110', #@
        '00100010101000110001111111000110001', #A
        '11110010010100111110010010100111110', #B
        '01110100011000010000100001000101110', #C
        '11110010010100101001010010100111110', #D
        '11111100001000011100100001000011111', #E
        '11111100001000011100100001000010000', #F
        '01110100011000010111100011000101110', #G
        '10001100011000111111100011000110001', #H
        '01110001000010000100001000010001110', #I
        '00111000100001000010000101001001100', #J
        '10001100101010011000101001001010001', #K
        '10000100001000010000100001000011111', #L
        '10001110111010110101100011000110001', #M
        '10001110011010110011100011000110001', #N
        '01110100011000110001100011000101110', #O
        '11110100011000111110100001000010000', #P
        '01110100011000110001101011001001101', #Q
        '11110100011000111110101001001010001', #R
        '01110100011000001110000011000101110', #S
        '11111001000010000100001000010000100', #T
        '10001100011000110001100011000101110', #U
        '10001100011000101010010100010000100', #V
        '10001100011000110101101011101110001', #W
        '10001100010101000100010101000110001', #X
        '10001100010101000100001000010000100', #Y
        '11111000010001000100010001000011111', #Z
        '01110010000100001000010000100001110', #[
        '10000100000100000100000100000100001', #\
        '00111000010000100001000010000100111', #]
        '00100010101000100000000000000000000', #^
        '00000000000000000000000000000011111', #_
        '11000110001000001000000000000000000', #`
        '00000000000111000001011111000101110', #a
        '10000100001011011001100011100110110', #b
        '00000000000011101000010000100000111', #c
        '00001000010110110011100011001101101', #d
        '00000000000111010001111111000001110', #e
        '00110010010100011110010000100001000', #f
        '000000000001110100011000110001011110000101110', #g
        '10000100001011011001100011000110001', #h
        '00100000000110000100001000010001110', #i
        '0001000000001100001000010000101001001100', #j
        '10000100001001010100110001010010010', #k
        '01100001000010000100001000010001110', #l
        '00000000001101010101101011010110101', #m
        '00000000001011011001100011000110001', #n
        '00000000000111010001100011000101110', #o
        '000000000001110100011000110001111101000010000', #p
        '000000000001110100011000110001011110000100001', #q
        '00000000001011011001100001000010000', #r
        '00000000000111110000011100000111110', #s
        '00100001000111100100001000010000111', #t
        '00000000001000110001100011001101101', #u
        '00000000001000110001100010101000100', #v
        '00000000001000110001101011010101010', #w
        '00000000001000101010001000101010001', #x
        '000000000010001100011000110001011110000101110', #y
        '00000000001111100010001000100011111', #z
        '00010001000010001000001000010000010', #{
        '00100001000010000000001000010000100', #|
        '01000001000010000010001000010001000', #}
        '01000101010001000000000000000000000' #}~
]

def printchar(letter,xpos,ypos,size,c):
    origin = xpos
    charval = ord(letter)
    #print(charval)
    index = charval-32 #start code, 32 or space
    #print(index)
    character = cmap[index] #this is our char...
    rows = [character[i:i+5] for i in range(0,len(character),5)]
    #print(rows)
    for row in rows:
        #print(row)
        for bit in row:
            #print(bit)
            if bit == '1':
                lcd.pixel(xpos,ypos,c)
                if size==2:
                    lcd.pixel(xpos,ypos+1,c)
                    lcd.pixel(xpos+1,ypos,c)
                    lcd.pixel(xpos+1,ypos+1,c)
                if size == 3:                    
                    lcd.pixel(xpos,ypos+1,c)
                    lcd.pixel(xpos,ypos+2,c)
                    lcd.pixel(xpos+1,ypos,c)
                    lcd.pixel(xpos+1,ypos+1,c)
                    lcd.pixel(xpos+1,ypos+2,c)
                    lcd.pixel(xpos+2,ypos,c)
                    lcd.pixel(xpos+2,ypos+1,c)
                    lcd.pixel(xpos+2,ypos+2,c)                  
            xpos+=size
        xpos=origin
        ypos+=size

def printstring(string,xpos,ypos,size,c):   
    if size == 1:
        spacing = 8
    if size == 2:
        spacing = 14
    if size == 3:
        spacing = 18
    for i in string:
        printchar(i,xpos,ypos,size,c)
        xpos+=spacing

def centrestring(string,ypos,size,c):
    if size == 1:
        spacing = 8
    if size == 2:
        spacing = 14
    if size == 3:
        spacing = 18
    used = len(string)*spacing
    xpos = int((240-used)/2)
    printstring(string, xpos, ypos, size, c)
# ========= End of Improved text system ==================

# Colour Mixing Routine
colour = lambda R, G, B: (((R&0xF8)*256) + ((G&0xFC)*8) + ((B&0xF8)>>3) & 0xFF) *256  + int((((R&0xF8)*256) + ((G&0xFC)*8) + ((B&0xF8)>>3) & 0xFF00) /256) # low nibble first

#same function as zfill:
zfill = lambda string, width: '{:0>{w}}'.format(string, w=width)

# =================== Main ======================
lcd = LCD_1inch3() # Start screen 

# Set up buttons & joystick
keyA = Pin(15,Pin.IN,Pin.PULL_UP)
keyB = Pin(17,Pin.IN,Pin.PULL_UP)
keyX = Pin(19 ,Pin.IN,Pin.PULL_UP)
keyY= Pin(21 ,Pin.IN,Pin.PULL_UP)

up = Pin(2,Pin.IN,Pin.PULL_UP)
down = Pin(18,Pin.IN,Pin.PULL_UP)
left = Pin(16,Pin.IN,Pin.PULL_UP)
right = Pin(20,Pin.IN,Pin.PULL_UP)
ctrl = Pin(3,Pin.IN,Pin.PULL_UP)
# if keyA.value() == 0: print("A Pressed")

class tetris():
    def help():
        lcd.fill(0)
        centrestring("Sorry!", 50, 3, 65535)
        lcd.show()
        centrestring("This Feature is", 100, 2, 65535)
        centrestring("Still in", 120, 2, 65535)
        centrestring("Development!", 140, 2, 65535)
        utime.sleep(1)
        lcd.show()
        centrestring("Press X to Continue", 180, 1, 65535)
        utime.sleep(1)
        lcd.show()
        while True:
            if keyX.value() == 0:
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
                utime.sleep(0.3)
                break
        
    
    # board is for hitboxes and collision detection 
    # It help differentiate between the static peices and the current peice
    board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    piece = [random.randint(0, 6), random.randint(0, 6)] # piece indices for current and pending piece
    # indices are as follows:
    #   0: Skew
    #   1: Inverted Skew
    #   2: Straight
    #   3: Inverted L-Shape
    #   4: L-Shape
    #   5: Square
    #   6: T-Shape
    rotation = [0, 0] #rotation [current, pending]
    position = [[0, 0], [0, 0]] #position [[x, y], [pendingX, pendingY]]
    score = 0
    lines = 0
    
    def updateStats(level):
        lcd.fill_rect(130, 5, 125, 20, 0)
        printstring("SCORE: " + '{:0>{w}}'.format(str(int(tetris.score)), w=6), 130, 5, 1, 65535)
        printstring("LINES: " + '{:0>{w}}'.format(str(int(tetris.lines)), w=5), 135, 15, 1, 65535)
        printstring("LEVEL: " + str(level), 148, 25, 1, 65535)
        # lcd.fill_rect(160, 43, statistic, 14, 65535)
        lcd.show()
        
    def showNextPiece(piece):
        lcd.fill_rect(90, 0, 35, 30, 0)
        if piece == 0:
            lcd.fill_rect(105, 10, 16, 8, 65535)
            lcd.fill_rect(97, 18, 16, 8, 65535)
        elif piece == 1:
            lcd.fill_rect(97, 10, 16, 8, 65535)
            lcd.fill_rect(105, 18, 16, 8, 65535)
        elif piece == 2:
            lcd.fill_rect(93, 14, 32, 8, 65535)
        elif piece == 3:
            lcd.fill_rect(113, 10, 8, 8, 65535)
            lcd.fill_rect(97, 18, 24, 8, 65535)
        elif piece == 4:
            lcd.fill_rect(113, 18, 8, 8, 65535)
            lcd.fill_rect(97, 10, 24, 8, 65535)
        elif piece == 5:
            lcd.fill_rect(101, 10, 16, 16, 65535)
        elif piece == 6:
            lcd.fill_rect(97, 10, 24, 8, 65535)
            lcd.fill_rect(105, 18, 8, 8, 65535)
        lcd.show()
    
    def deleteIfNegative(value):
        if value < 0: return 50
        else: return value
    
    def renderPiece(piece, rotation, position):
        render = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        x = position[0]
        y = position[1]
        if piece == 0:
            if rotation == 0 or rotation == 2:
                try: render[tetris.deleteIfNegative(x-2)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
            else:
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-3)] = 1
                except: pass
        elif piece == 1:
            if rotation == 0 or rotation == 2:
                try: render[tetris.deleteIfNegative(x-2)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
            else:
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-3)] = 1
                except: pass
        elif piece == 2:
            if rotation == 0 or rotation == 2:
                try: render[tetris.deleteIfNegative(x+1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-2)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
            else:
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-3)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-4)] = 1
                except: pass
        elif piece == 3:
            if rotation == 0:
                try: render[tetris.deleteIfNegative(x-2)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-2)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
            elif rotation == 1:
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-3)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-3)] = 1
                except: pass
            elif rotation == 2:
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-2)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
            else:
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-3)] = 1
                except: pass
        elif piece == 4:
            #yx
            #01
            #01
            #11
            if rotation == 0:
                try: render[tetris.deleteIfNegative(x-2)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-2)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
            elif rotation == 1:
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-3)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-3)] = 1
                except: pass
            elif rotation == 2:
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-2)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
            else:
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-3)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
        elif piece == 5:
            try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
            except: pass
            try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
            except: pass
            try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-1)] = 1
            except: pass
            try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-2)] = 1
            except: pass
            return render
        elif piece == 6:
            if rotation == 0:
                try: render[tetris.deleteIfNegative(x-2)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
            elif rotation == 1:
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-3)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
            elif rotation == 2:
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-2)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
            else:
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-1)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-1)][tetris.deleteIfNegative(y-3)] = 1
                except: pass
                try: render[tetris.deleteIfNegative(x-2)][tetris.deleteIfNegative(y-2)] = 1
                except: pass
        return render
    
    def collisionCheck(pieceRender):
        pixelCount = 0
        for x in range(10):
            pixelCount += pieceRender[x].count(1)
            for y in range(20):
                if tetris.board[x][y] + pieceRender[x][y] == 2: return 1
        if pixelCount != 4: return 1
        return 0
    
    def render(pieceRender):
        lcd.fill_rect(8, 39, 100, 200, 0)
        for x in range(10):
            for y in range(20):
                if tetris.board[x][y] == 1 or pieceRender[x][y] == 1:
                    lcd.fill_rect(8+((x-9)*(-10)), 39+((y-19)*(-10)), 10, 10, 65535)
        lcd.show()
    
