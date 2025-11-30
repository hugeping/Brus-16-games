#!/usr/bin/env python3

from brus16 import *

def mswap(a, b):
    return f'''{a} ^= {b}; {b} ^= {a}; {a} ^= {b}'''

def mbool(a):
    return a != 0

ZOOM_BITS = 4

VIEW_SIZE = 7
VIEW_R = (VIEW_SIZE//2)
#MRECT = [0]*(VIEW_SIZE*VIEW_SIZE)

MAX_ITEMS = 24
LEVEL_SIZE = 16 + MAX_ITEMS

KEY_STATE = [-1]*KEY_NUM
SPAWN_DELAY = 100
# r, u, l, d
DIRS = [1, 0, 0, -1, -1, 0, 0, 1]

# fire points: r, u, l, d
HERO_LASER_DIR = [10, -3, 4, -10, -10, -4, -4, 6]

POWER_DRAW_MAX = 480
LASER_COST = 16
RADAR_COST = 10
LASER_CHARGE = 8

# center
HERO_C = [4, 6]

RADAR_RATE = 5

BGCOL1 = rgb(50, 0, 80)
BGCOL2 = rgb(100, 0, 130)
FGCOL = rgb(200, 0, 255)
DOTS_RATE = 6

EXITCOL1 = rgb(164, 32, 164)
EXITCOL2 = rgb(164, 0, 164)

EXITCOL3 = rgb(125, 249, 255)
EXITCOL4 = rgb(164, 0, 164)
EXITCOL_RATE = 3

PADCOL1 = rgb(245, 222, 179)
PADCOL2 = rgb(255, 248, 220)
PADCOL_RATE = 2

LASERCOL_RATE = 1
LASERCOL1 = rgb(0, 191, 255)
LASERCOL2 = rgb(255, 255, 255)

SPAWNCOL1 = rgb(200, 0, 22)
SPAWNCOL2 = rgb(240, 255, 255)
SPAWNCOL_RATE = 1

DOORCOL = rgb(41,132,159)

TITLE = [1, 214, 64, 212, 96, 0, 1, 214, 64, 8, 96, 51071, 0, 8, 0, 24, 12, 51071, 1, 250, 64, 32, 96, 51071, 0, 8, 12, 24, 30, 0, 0, 8, 54, 24, 30, 0, 1, 286, 64, 8, 96, 51071, 0, 8, 0, 24, 54, 51071, 0, 8, 12, 16, 30, 0, 1, 322, 64, 8, 96, 51071, 0, 8, 54, 8, 24, 51071, 0, 16, 42, 8, 24, 51071, 0, 24, 0, 8, 96, 51071, 1, 358, 64, 32, 96, 51071, 0, 8, 12, 16, 72, 0, 1, 394, 64, 8, 96, 51071, 0, 8, 42, 16, 12, 51071, 0, 24, 0, 8, 96, 51071]
ASTEROID = [
    1,0,0,41,94,51807,
    0,-6,21,55,68,51935,
    0,-10,6,58,70,51999,
    0,-18,15,71,65,51999,
    0,-9,12,51,56,51999,
    0,-13,21,67,65,51999,
    0,-22,29,81,46,51999,
    0,-13,17,17,25,51679,
    0,21,33,10,13,51839,
    0,-6,51,21,25,51775,
    0,-2,6,10,19,51999,
]

ALIEN = [
    1, 0, 0, 24, 18, 0,
    0, 8, 6, 8, 2, rgb(255,0,0),
    0, 3, 18, 4, 6, 0,
    0, 10, 18, 4, 6, 0,
    0, 18, 18, 4, 6, 0,
]

ALIENS_SIZE = 8*3
ALIENS = [0]*ALIENS_SIZE
DOORS = [0]*8

c1 = rgb(211, 211, 211)
c2 = rgb(192, 192, 192)
c3 = rgb(169, 169, 169)
c4 = rgb(24, 24, 24)

HERO = [
    1, 0, 0, 8, 10, c1,
    0, -3, 1, 3, 8, c3,
    0, 3, -4, 6, 6, rgb(255, 255, 255),
    0, 6, -3, 3, 4, rgb(0, 190, 222),
    0, 1, 10, 3, 7, c2,
    0, 5, 10, 3, 7, c2,
    0, 3, 3, 11, 3, c4,
    0, 6, 6, 3, 2, rgb(255, 255, 255),
]

HEROU = [
    1, 0, 0, 8, 10, c1,
    0, 1, -4, 6, 6, rgb(255, 255, 255),
    0, 1, 2, 7, 7, c3,
    0, 8, -5, 2, 8, c4,
    0, 1, 10, 3, 7, c2,
    0, 5, 10, 3, 7, c2,
    0, 8, 3, 3, 3, rgb(235, 235, 235),
    0, 1, 2, 6, 1, rgb(160, 160, 160),
]

HEROD = [
    1, 0, 0, 8, 10, c1,
    0, 1, -4, 6, 6, rgb(255, 255, 255),
    0, 1, -2, 6, 3, rgb(0, 190, 222),
    0, -2, 3, 3, 5, rgb(235, 235, 235),
    0, 1, 10, 3, 7, c2,
    0, 5, 10, 3, 7, c2,
    0, 0, 4, 2, 8, c4,
    0, 3, 5, 5, 3, rgb(173, 173, 173),
]

def invertx(t, l):
    i = 0
    r = [1, 0, 0]
    dx = 0
    while i < l:
        if i == 0:
            r.append(t[i+3])
            r.append(t[i+4])
            r.append(t[i+5])
            dx = t[i+3]
        else:
            r.append(0)
            x, w = t[i+1], t[i+3]
            if x >= 0:
                r.append(-x+dx-w)
                r.append(t[i+2])
                r.append(w)
                r.append(t[i+4])
            else:
                r.append(dx-x-w)#-x+w)
                r.append(t[i+2])
                r.append(w)
                r.append(t[i+4])
            r.append(t[i+5])
        i += RECT_SIZE
    return r

HEROL = invertx(HERO, len(HERO))

TW = 32
TH = 32

TWS = 5
THS = 5

TWM = 0x1f
THM = 0x1f

W = 15
H = 15

PADS_MAP = [0]*H
SPAWN_MAP = [0]*H
RADAR_MAP = [0]*H
DOORS_MAP = [0]*H

ITEM_PAD   = 0x0100
ITEM_ALIEN = 0x0200
ITEM_DOOR  = 0x0300
ITEM_SPAWN = 0xff00
ITEM_MASK  = 0xff00

ALIEN_DEAD =  0x2000
ALIEN_HIT =   0x4000
ALIEN_SIGHT = 0x8000
ALIEN_MASK =  0x1F00
ALIEN_HEALTH = 0x13

DOOR_HIT    = 0x8000
DOOR_DEAD   = 0x4000
DOOR_MASK   = 0x1F00
DOOR_HEALTH = 0x16

MAP = (
'''
###############
#@   |   |   *#
####### #######
####### #######
####### #######
####### #######
######   ######
#$  |  E  |  *#
######   ######
####### #######
####### #######
####### #######
####### #######
#*   |   |   *#
###############''',

'''
###############
#@           $#
# ###-#####-###
# ##$* ### *$##
# #############
# #############
# ####   ######
#      E      #
# ####   #### #
# ########### #
# ########### #
# ########### #
#     $#$     #
#*###########*#
###############''',

'''
###############
#      @      #
# ########### #
# ###*   *### #
# ##### ##### #
# #####-##### #
# ####   #### #
#      E      #
# ####   #### #
# #####-##### #
# ##### ##### #
# ##### ##### #
# ##### ##### #
#*###*   *###*#
#######&#######''',

'''
#@#############
# ###&   &###*#
# ##### ##### #
# ##### ##### #
# ##### ##### #
# ##### ##### #
# ####   #### #
#      E      #
# ####   #### #
# ##### ##### #
# ##### ##### #
# ##### ##### #
# ##### ##### #
#*###*   *###*#
###############''',

'''
#######&#######
#             #
# ##### ##### #
# ####* *#### #
# ##### ##### #
# ##### ##### #
# #*##   ##*# #
&      @      &
# #*##   ##*# #
# ##### ##### #
# ##### ##### #
# ####* *#### #
# ##### ##### #
#             #
#######&#######
''',
)

def map2bit(t):
    r = []
    items = []
    x, y = 0, 0
    px, py = 0, 0
    ex, ey = -1, -1
    for l in t.splitlines():
#        l = l.strip()
        if l == "":
            continue
        c = 0
        x = 0
        for i in l:
            c >>= 1
            c |= 0x8000 if i == '#' else 0
            if i == '@':
                px, py = x, y
            elif i == 'E':
                ex, ey = x, y
            elif i == '*':
                items.append((x, y, ITEM_PAD))
            elif i == '&':
                items.append((x, y, ITEM_SPAWN))
            elif i == '$':
                items.append((x, y, ITEM_ALIEN))
            elif i == '-' or i == '|':
                items.append((x, y, ITEM_DOOR))
            x += 1
        r.append(c>>1)
        y += 1
    if ex < 0:
        ex, ey = px, py
    r.append((py<<4)|px|(ey<<12)|(ex<<8))
    n = 0
    for i in items:
        r.append((i[1]<<4)|i[0]|i[2])
        n += 1
    for i in range(MAX_ITEMS - n):
        r.append(0)
    return r

LEVELS = []

for m in MAP:
    LEVELS += map2bit(m)

save_game('gerion.bin', load_code('gerion.py'))
