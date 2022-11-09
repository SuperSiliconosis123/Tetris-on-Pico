# Tetris-on-Pico
A Tetris-Clone for the Raspberry Pi Pico in combination with a WaveShare 1.3" LCD
## Installation
The first step is to install the micropython firmware on your Raspberry Pi Pico.
Once you've done that, you can use any REPL software to upload `main.py`, `lib.mpy`, and the defualt `highscore` file, but I prefer to use `rshell`.
```
/home/Pi/Tetris-on-Pico-master> cp main.py /pyboard/main.py
/home/Pi/Tetris-on-Pico-master> cp lib.mpy /pyboard/lib.mpy
/home/Pi/Tetris-on-Pico-master> cp highscore /pyboard/highscore
```
You can build lib.py from source using `mpy-cross`.
```bash
pi@raspberrypi:/Tetris-on-Pico-master~ $ mpy-cross lib.py
```
###### GPIO used: 2, 3, 9, 8, 10, 11, 12, 13, 15, 16, 17, 18, 19, 20, 21, 27, 28
