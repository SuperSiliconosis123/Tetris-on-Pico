# Raspberry Pi Pico microcontroller 
# WaveShare Pico LCD 1.3 inch 240x240 screen with Joystick and Buttons
# Tony Goodhew - 9th Nov 2021
# This is an educational demonstration with many comments
# Import the libraries needed
from machine import Pin,SPI,PWM
import framebuf
import utime
import os
import math
import random
# ============ Start of Drive Code ================
#  == Copy and paste into your code ==
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
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,100000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0 # Pre-defined colours
        self.green =   0x001f # Probably easier to use colour(r,g,b) defined below
        self.blue  =   0xf800
        self.white =   0xffff
        
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
    
def delchar(xpos,ypos,size,):
    if size == 1:
        charwidth = 5
        charheight = 9
    if size == 2:
        charwidth = 10
        charheight = 18
    if size == 3:
        charwidth = 15
        charheight = 27
    c=colour(40,40,40)
    lcd.fill_rect(xpos,ypos,charwidth,charheight,0) #xywh

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
    printstring(string,xpos,ypos,size,c)
# ========= End of Improved text system ==================

# ========== Start of Graphics routines =================        
# Colour Mixing Routine
def colour(R,G,B): # Compact method!
    mix1 = ((R&0xF8)*256) + ((G&0xFC)*8) + ((B&0xF8)>>3)
    return  (mix1 & 0xFF) *256  + int((mix1 & 0xFF00) /256) # low nibble first

# ========== Start of Triangles code =============
# Modified from https://github.com/SpiderMaf/PiPicoDsply/blob/main/filled-triangles.py
# To work on WaveShare Pi Pico displays
class Point:
    def __init__(self,x,y):
        self.X=x
        self.Y=y
    def __str__(self):
        return "Point(%s,%s)"%(self.X,self.Y)
        
class Triangle:
    def __init__(self,p1,p2,p3):
        self.P1=p1
        self.P2=p2
        self.P3=p3

    def __str__(self):
        return "Triangle(%s,%s,%s)"%(self.P1,self.P2,self.P3)
    
    def draw(self):
        print("I should draw now")
        self.fillTri()
    # Filled triangle routines ported from http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html      
    def sortVerticesAscendingByY(self):    
        if self.P1.Y > self.P2.Y:
            vTmp = self.P1
            self.P1 = self.P2
            self.P2 = vTmp
        
        if self.P1.Y > self.P3.Y:
            vTmp = self.P1
            self.P1 = self.P3
            self.P3 = vTmp

        if self.P2.Y > self.P3.Y:
            vTmp = self.P2
            self.P2 = self.P3
            self.P3 = vTmp
        
    def fillTri(self):
        self.sortVerticesAscendingByY()
        if self.P2.Y == self.P3.Y:
            fillBottomFlatTriangle(self.P1, self.P2, self.P3)
        else:
            if self.P1.Y == self.P2.Y:
                fillTopFlatTriangle(self.P1, self.P2, self.P3)
            else:
                newx = int(self.P1.X + (float(self.P2.Y - self.P1.Y) / float(self.P3.Y - self.P1.Y)) * (self.P3.X - self.P1.X))
                newy = self.P2.Y                
                pTmp = Point( newx,newy )
                fillBottomFlatTriangle(self.P1, self.P2, pTmp)
                fillTopFlatTriangle(self.P2, pTmp, self.P3)

def fillBottomFlatTriangle(p1,p2,p3):
    slope1 = float(p2.X - p1.X) / float (p2.Y - p1.Y)
    slope2 = float(p3.X - p1.X) / float (p3.Y - p1.Y)

    x1 = p1.X
    x2 = p1.X + 0.5

    for scanlineY in range(p1.Y,p2.Y):
#        lcd.pixel_span(int(x1), scanlineY, int(x2)-int(x1))   # Switch pixel_span() to hline() / Pimoroni to WS
        lcd.hline(int(x1),scanlineY, int(x2)-int(x1),c)
        x1 += slope1
        x2 += slope2

def fillTopFlatTriangle(p1,p2,p3):
    slope1 = float(p3.X - p1.X) / float(p3.Y - p1.Y)
    slope2 = float(p3.X - p2.X) / float(p3.Y - p2.Y)

    x1 = p3.X
    x2 = p3.X + 0.5

    for scanlineY in range (p3.Y,p1.Y-1,-1):
#        lcd.pixel_span(int(x1), scanlineY, int(x2)-int(x1))  # Switch pixel_span() to hline() / Pimoroni to WS
        lcd.hline(int(x1),scanlineY, int(x2)-int(x1),c)
        x1 -= slope1
        x2 -= slope2
            
# ============== End of Triangles Code ===============

# ============== GFX Routines ============
def ring_old(cx,cy,r,cc):   # Draws a circle - with centre (x,y), radius, colour 
    for angle in range(181):  
        y3=int(r*math.sin(math.radians(angle/2))) # Uses Trigonometry
        x3=int(r*math.cos(math.radians(angle/2)))
        lcd.pixel(cx-x3,cy+y3,cc)  # 4 quadrants
        lcd.pixel(cx-x3,cy-y3,cc)
        lcd.pixel(cx+x3,cy+y3,cc)
        lcd.pixel(cx+x3,cy-y3,cc)

def ring(x,y,r,c):
    lcd.pixel(x-r,y,c)
    lcd.pixel(x+r,y,c)
    lcd.pixel(x,y-r,c)
    lcd.pixel(x,y+r,c)

    for i in range(1,r):
        a = int(math.sqrt(r*r-i*i)) # Uses Pythagoras
        lcd.pixel(x-a,y-i,c)
        lcd.pixel(x+a,y-i,c)
        lcd.pixel(x-a,y+i,c)
        lcd.pixel(x+a,y+i,c)
        lcd.pixel(x-i,y-a,c)
        lcd.pixel(x+i,y-a,c)
        lcd.pixel(x-i,y+a,c)
        lcd.pixel(x+i,y+a,c)

def triangle(x1,y1,x2,y2,x3,y3,c): # Draw outline triangle
    lcd.line(x1,y1,x2,y2,c)
    lcd.line(x2,y2,x3,y3,c)
    lcd.line(x3,y3,x1,y1,c)
    
def tri_filled(x1,y1,x2,y2,x3,y3,c): # Draw filled triangle
    t=Triangle(Point(x1,y1),Point(x2,y2),Point(x3,y3)) # Define corners
    t.fillTri() # Call main code block  

def circle(x,y,r,c):
    lcd.hline(x-r,y,r*2,c)
    for i in range(1,r):
        a = int(math.sqrt(r*r-i*i)) # Pythagoras!
        lcd.hline(x-a,y+i,a*2,c) # Lower half
        lcd.hline(x-a,y-i,a*2,c) # Upper half

# =================== Main ======================
lcd = LCD_1inch3() # Start screen 
lcd.fill(colour(0,0,0)) # BLACK 
lcd.show()
'''
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
if keyA.value() == 0: print("A Pressed")
'''
input = {
    'a': False, 
    'b': False, 
    'x': False, 
    'y': False, 
    'up': False, 
    'down': False, 
    'left': False, 
    'right': False, 
    'ctrl': False 
}

class tetris():
    def start():
        lcd.fill(colour(0, 0, 0))
        c = colour(255, 255, 255)
        lcd.rect(220, 10, 10, 30, c, True)
        lcd.rect(200, 20, 20, 10, c, True)
        lcd.rect(200, 50, 30, 10, c, True)
        lcd.rect(222, 60, 8, 10, c, True)
        lcd.rect(211, 60, 8, 10, c, True)
        lcd.rect(200, 60, 8, 10, c, True)
        lcd.rect(220, 80, 10, 30, c, True)
        lcd.rect(200, 90, 20, 10, c, True)
        lcd.rect(200, 120, 30, 10, c, True)
        lcd.rect(220, 130, 10, 10, c, True)
        tri_filled(230, 140, 220, 140, 220, 150, c)
        lcd.show()
    #def select():
    #def tetris():
    #def highscore():

tetris.start()
