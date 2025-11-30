from brus16 import *

def col(r, g, b):
    return ((r>>3) << 11) | ((g>>2) << 5) | (b>>3)

def mswap(a, b):
    return f'''{a} ^= {b}; {b} ^= {a}; {a} ^= {b}'''

def mbool(a):
    return a != 0

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

LASER_HEAT_MAX = 480
LASER_COST = 16
RADAR_COST = 10
LASER_CHARGE = 8

# center
HERO_C = [4, 6]

RADAR_RATE = 5

BGCOL1 = col(50, 0, 80)
BGCOL2 = col(100, 0, 130)
FGCOL = col(200, 0, 255)
DOTS_RATE = 6

EXITCOL1 = col(164, 32, 164)
EXITCOL2 = col(164, 0, 164)

EXITCOL3 = col(125, 249, 255)
EXITCOL4 = col(164, 0, 164)
EXITCOL_RATE = 3

PADCOL1 = col(245, 222, 179)
PADCOL2 = col(255, 248, 220)
PADCOL_RATE = 2

LASERCOL_RATE = 1
LASERCOL1 = col(0, 191, 255)
LASERCOL2 = col(255, 255, 255)

SPAWNCOL1 = col(200, 0, 22)
SPAWNCOL2 = col(240, 255, 255)
SPAWNCOL_RATE = 1

DOORCOL = col(41,132,159)

ALIEN = [
    1, 0, 0, 24, 18, 0,
    0, 8, 6, 8, 2, col(255,0,0),
    0, 3, 18, 4, 6, 0,
    0, 10, 18, 4, 6, 0,
    0, 18, 18, 4, 6, 0,
]

ALIENS_SIZE = 8*3
ALIENS = [0]*ALIENS_SIZE
DOORS = [0]*8

c1 = col(211, 211, 211)
c2 = col(192, 192, 192)
c3 = col(169, 169, 169)
c4 = col(24, 24, 24)

HERO = [
    1, 0, 0, 8, 10, c1,
    0, -3, 1, 3, 8, c3,
    0, 3, -4, 6, 6, col(255, 255, 255),
    0, 6, -3, 3, 4, col(0, 190, 222),
    0, 1, 10, 3, 7, c2,
    0, 5, 10, 3, 7, c2,
    0, 3, 3, 11, 3, c4,
    0, 6, 6, 3, 2, col(255, 255, 255),
]

HEROU = [
    1, 0, 0, 8, 10, c1,
    0, 1, -4, 6, 6, col(255, 255, 255),
    0, 1, 2, 7, 7, c3,
    0, 8, -5, 2, 8, c4,
    0, 1, 10, 3, 7, c2,
    0, 5, 10, 3, 7, c2,
    0, 8, 3, 3, 3, col(235, 235, 235),
    0, 1, 2, 6, 1, col(160, 160, 160),
]

HEROD = [
    1, 0, 0, 8, 10, c1,
    0, 1, -4, 6, 6, col(255, 255, 255),
    0, 1, -2, 6, 3, col(0, 190, 222),
    0, -2, 3, 3, 5, col(235, 235, 235),
    0, 1, 10, 3, 7, c2,
    0, 5, 10, 3, 7, c2,
    0, 0, 4, 2, 8, c4,
    0, 3, 5, 5, 3, col(173, 173, 173),
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
# ###=#####=###
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
# #####=##### #
# ####   #### #
#      E      #
# ####   #### #
# #####=##### #
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
            elif i == '=' or i == '|':
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

save_game('zona-451.bin', f'''
def start():
    main()

HERO_DEAD = 0
HERO_LDIRS = {HERO_LASER_DIR}
DIRS = {DIRS}
HERO_C = {HERO_C}
FRAMES = 0
PADS_MAP = {PADS_MAP}
SPAWN_MAP = {SPAWN_MAP}
RADAR_MAP = {RADAR_MAP}
DOORS_MAP = {DOORS_MAP}
SPAWN_FRAME = 0
PADS_NR = 0
PADS_MAX = 0
PADS_S = 0
SPAWNS_NR = 0
SPAWN_ID = 0
TELEPORT_FRAME = 0
LASER_HEAT = 0
MAP = {LEVELS}
HEROR = {HERO}
HEROL = {HEROL}
HEROU = {HEROU}
HEROD = {HEROD}
ALIEN = {ALIEN}
ALIENS = {ALIENS}
ALIENS_NR = 0
DOORS = {DOORS}
DOORS_NR = 0

SPAWNS = [0, 0, 0, 0, 0, 0, 0, 0]
LEVEL = 0
NEXT_LEVEL = 0
HERO_DIR = 0

PX = 0
PY = 0

EXIT_CX = 0
EXIT_CY = 0

LASER_X = -1
LASER_Y = 0
LASER_X2 = 0
LASER_Y2 = 0

def rgb(r, g, b):
    return ((r>>3) << 11) | ((g>>2) << 5) | (b>>3)

def abs(a):
    if a < 0:
        return -a
    return a

def max(a, b):
    if a > b:
        return a
    return b

def min(a, b):
    if a < b:
        return a
    return b

def memcpy(src, dst, size):
    end = src + size
    while src < end:
        poke(dst, src[0])
        src += 1
        dst += 1

def bzero(dst, size):
    end = dst + size
    while dst < end:
        dst[0] = 0
        dst += 1

def bit(a, v):
    return (a&v) != 0

def not_bit(a, v):
    return (a&v) == 0

def or2(a, b):
    if a != 0:
        return 1
    return b != 0

def or3(a, b, c):
    if a != 0:
        return 1
    return or2(b, c)

def and2(a, b):
    if a == 0:
        return 0
    if b == 0:
        return 0
    return 1

def and3(a, b, c):
    if a == 0:
        return 0
    return and2(b, c)

def bit_sethi(a, mask, v):
    a &= ~mask
    a |= v<<8
    return a

def bit_gethi(a, mask):
    return (a & mask)>>8

def to_bool(a):
    return a != 0

seed = 7

def rnd():
    seed ^= seed << 7
    seed ^= seed >> 9
    seed ^= seed << 8
    return seed

def mset(m, cx, cy, v):
    mask = 1<<cx
    r = (m[cy]&mask) != 0
    if v:
        m[cy] |= mask
    else:
        m[cy] &= ~mask
    return r

def mclr(m, cx, cy):
    return mset(m, cx, cy, 0)

def msetxy(m, cx, cy, v):
    return mset(m, cx>>{TWS}, cy>>{THS}, v)

def mclrxy(m, cx, cy):
    return mset(m, cx>>{TWS}, cy>>{THS}, 0)

def inside(cx, cy):
    if (cx < 0) | (cx >= {W}):
        return 0
    if (cy < 0) | (cy >= {H}):
        return 0
    return 1

def insidexy(x, y):
    return inside(x>>{TWS}, y>>{THS})

def mget(m, cx, cy):
    return (m[cy]&(1<<cx)) != 0

def mgetxy(m, x, y):
    return mget(m, x>>{TWS}, y>>{THS})

def x2c(x):
    return x >> {TWS}

def y2c(y):
    return y >> {THS}

def x2tl(x, w):
    return x - (w>>1)

def y2tl(y, h):
    return y - (h>>1)

def c2int(cx, cy):
    return (cy<<4)|cx

def int2cx(v):
    return v&0xf

def int2cy(v):
    return (v>>4)&0xf

def c2x(c):
    return c*{TW}+({TW}>>1)

def c2y(c):
    return c*{TH}+({TH}>>1)

def lookup_door(cx, cy):
    i = 0
    while i < DOORS_NR:
        if c2int(cx, cy) == (DOORS[i]&0xff):
            return DOORS + i
        i += 1
    return 0

def loadlev():
    NEXT_LEVEL = LEVEL
    SCROLL_MODE = 480
    RADAR_MODE = 0
    ALIEN_DIR = 0
    HERO_DEAD = 0

    cb = LEVEL + {H}

    t = cb[0]

    # hero
    PX = c2x(int2cx(t))
    PY = c2y(int2cy(t))

    # exit
    EXIT_CX = (t>>8)&0xf
    EXIT_CY = (t>>12)&0xf

    ALIENS_NR = 0
    bzero(ALIENS, {ALIENS_SIZE})

    DOORS_NR = 0
    bzero(DOORS, 8)

    # items
    cb += 1
    bzero(PADS_MAP, {H})
    bzero(SPAWN_MAP, {H})
    bzero(DOORS_MAP, {H})
    bzero(SPAWNS, 8)
    PADS_NR = 0
    SPAWNS_NR = 0
    SPAWN_ID = 0
    SPAWN_FRAME = FRAMES

    TELEPORT_FRAME = FRAMES

    ecb = cb + {MAX_ITEMS}
    while cb < ecb:
        if (cb[0]&{ITEM_MASK}) != 0:
            cx = int2cx(cb[0])
            cy = int2cy(cb[0])
            it = cb[0]&{ITEM_MASK}
            if it == {ITEM_PAD}:
                mset(PADS_MAP, cx, cy, 1)
                PADS_NR += 1
            elif it == {ITEM_SPAWN}:
                SPAWNS[SPAWNS_NR] = c2int(cx, cy)
                mset(SPAWN_MAP, cx, cy, 1)
                SPAWNS_NR += 1
            elif it == {ITEM_ALIEN}:
                new_alien(c2x(cx), c2y(cy))
            elif it == {ITEM_DOOR}:
                mset(DOORS_MAP, cx, cy, 1)
                DOORS[DOORS_NR] = c2int(cx, cy)
                DOORS_NR += 1
        cb += 1
    PADS_S = 0
    PADS_MAX = PADS_NR
    while (1<<PADS_S) < PADS_NR:
        PADS_S += 1

def draw_rect(ptr, x, y, w, h, col):
    ptr[0] = 1
    ptr[1] = x
    ptr[2] = y
    ptr[3] = w
    ptr[4] = h
    ptr[5] = col
    return ptr + {RECT_SIZE}

# ha-ha :)
def draw_circle(ptr, cx, cy, r, col):
    ptr[0] = 1
    ptr[1] = cx - r
    ptr[2] = cy - r
    ptr[3] = 2*r
    ptr[4] = 2*r
    ptr[5] = col
    return ptr + {RECT_SIZE}

def inside_view(x, y):
    return hit1(x2c(PX) - {VIEW_R}, y2c(PY) - {VIEW_R}, {VIEW_SIZE}, {VIEW_SIZE}, x2c(x), y2c(y))

def draw_laser(ptr):
    if LASER_X < 0:
        return ptr

    ex = LASER_X2
    ey = LASER_Y2

    if LASER_X2 != LASER_X:
        ex &= ~{TWM}
        ex += {TW//2}
        ey += 1

    if LASER_Y2 != LASER_Y:
        ey &= ~{THM}
        ey += {TH//2}
        ex += 1

    if inside_view(ex, ey) == 0:
        ptr = draw_mrect(ptr, x2c(ex), y2c(ey), 0, 0)

    x = LASER_X
    y = LASER_Y

    if (ex < x) | (ey < y):
        {mswap("x", "ex")}
        {mswap("y", "ey")}

    color = rate_color({LASERCOL_RATE}, {LASERCOL1}, {LASERCOL2})

    return draw_rect(ptr, x, y, abs(ex - x), abs(ey - y), color)

def upd_doors():
    i = 0
    while i < DOORS_NR:
        if bit(DOORS[i], {DOOR_DEAD}):
            e = bit_gethi(DOORS[i], {DOOR_MASK}) + 1
            if e > 4:
                mclr(DOORS_MAP, int2cx(DOORS[i]), int2cy(DOORS[i]))
            else:
                DOORS[i] = bit_sethi(DOORS[i], {DOOR_MASK}, e)
        i += 1

def upd_laser():
    a = ALIENS
    ae = ALIENS + {ALIENS_SIZE}
    while a < ae:
        a[2] &= {~ALIEN_HIT}
        a += 3

    i = 0
    while i < DOORS_NR:
        DOORS[i] &= ~{DOOR_HIT}
        i += 1

    if (HERO_DEAD > 0) | (abs(FRAMES-TELEPORT_FRAME) < 30):
        LASER_X = -1
        return

    if INP_STATE[{KEY_A}] == 0:
        if (INP_X == 0) & (INP_Y == 0):
            LASER_HEAT = max(0, LASER_HEAT - {LASER_CHARGE})
        else:
            LASER_HEAT = max(0, LASER_HEAT - {LASER_CHARGE//5})
        LASER_X = -1
        return 0

    LASER_HEAT = min(LASER_HEAT + {LASER_COST}, {LASER_HEAT_MAX})
    if LASER_HEAT >= {LASER_HEAT_MAX}:
        LASER_X = -1
        return 0

    x = PX + HERO_LDIRS[HERO_DIR*2]
    y = PY + HERO_LDIRS[HERO_DIR*2+1]
    dx = DIRS[HERO_DIR*2]*({TW//2})
    dy = DIRS[HERO_DIR*2+1]*({TH//2})

    ex = x
    ey = y

    a = 0

    while and3(insidexy(ex, ey), (mgetxy(LEVEL, ex, ey) == 0), (mgetxy(DOORS_MAP, ex, ey) == 0)):
        ex += dx
        ey += dy
        a = scan_alien(ex, ey, 0)
        if a != 0:
            e = bit_gethi(a[2], {ALIEN_MASK})
            a[2] |= {ALIEN_HIT}
            if (e > 0) & not_bit(a[2], {ALIEN_DEAD}):
                e -= 1
                a[2] = bit_sethi(a[2], {ALIEN_MASK}, e)
            elif not_bit(a[2], {ALIEN_DEAD}):
                a[2] = {ALIEN_DEAD | (DOOR_HEALTH<<8)}
            break

    if and2(insidexy(ex, ey), mgetxy(DOORS_MAP, ex, ey)):
        door = lookup_door(x2c(ex), y2c(ey))
        e = bit_gethi(door[0], {DOOR_MASK}) + 2
        door[0] |= {DOOR_HIT}
        if (e >= 0x1f) & not_bit(door[0], {DOOR_DEAD}):
            door[0] = bit_sethi(door[0], {DOOR_MASK}, 0)
            door[0] |= {DOOR_DEAD}
        elif not_bit(door[0], {DOOR_DEAD}):
            door[0] = bit_sethi(door[0], {DOOR_MASK}, e)

    ex = max(0, ex)
    ey = max(0, ey)
    ex = min(ex, {W*TW-1})
    ey = min(ey, {H*TH-1})

    LASER_X = x
    LASER_Y = y
    LASER_X2 = ex
    LASER_Y2 = ey

LEGS = [1, 3, 5, 7, 5, 3, 2, 1]

def light_ray(x, y, tx, ty, r):
    dx = 0
    dy = 0

    if tx - x > 0:
        dx = 1
    elif tx - x < 0:
        dx = -1

    if ty - y > 0:
        dy = 1
    elif ty - y < 0:
        dy = -1

    if (x != tx) & (y != ty) & (abs(tx-x) != abs(ty-y)):
        return 0;

    while (abs(tx - x) <= r) & (abs(ty - y) <= r):
        if inside(x, y) == 0:
            return 0
        if mget(LEVEL, x, y):
            return 0
        if mget(DOORS_MAP, x, y):
            return 0
        x += dx
        y += dy
        if (x == tx) & (y == ty):
            return 1
    return 0

def alien_light_cell(a):
    if inside_view(a[0], a[1]) == 0:
        return 0

    px = PX >> {TWS}
    py = PY >> {THS}
    tx = a[0] >> {TWS}
    ty = a[1] >> {THS}

    return light_ray(px, py, tx, ty, {VIEW_R}) | \
        light_ray(px+1, py, tx, ty, {VIEW_R}) | \
        light_ray(px-1, py, tx, ty, {VIEW_R}) | \
        light_ray(px, py-1, tx, ty, {VIEW_R}) | \
        light_ray(px, py+1, tx, ty, {VIEW_R}) | \
        light_ray(px+1, py+1, tx, ty, {VIEW_R}) | \
        light_ray(px-1, py+1, tx, ty, {VIEW_R}) | \
        light_ray(px-1, py-1, tx, ty, {VIEW_R}) | \
        light_ray(px+1, py-1, tx, ty, {VIEW_R})

def alien_visible(a):
    return bit(a[2], {ALIEN_HIT}) | alien_light_cell(a)

def draw_alien(ptr, a):
    x = a[0]
    y = a[1]

    if (alien_visible(a) == 0) | (ptr >= {RECT_MEM+RECT_SIZE*RECT_NUM}):
        return ptr

    memcpy(ALIEN, ptr, {len(ALIEN)})

    ptr[1] = x2tl(x, ALIEN[3])
    ptr[2] = y2tl(y, ALIEN[4])

    i = 0
    while i < {len(ALIEN)//RECT_SIZE}:
        col = ALIEN_COLS[i]
        f = i*{RECT_SIZE}
        if bit(a[2],{ALIEN_HIT}):
            col = 0xffff
        if bit(a[2], {ALIEN_DEAD}):
            e = (0xf - (a[2]>>8)&0xf)
            ptr[f+3] = max(0, ptr[f+3]+e)
            ptr[f+4] = max(0, ptr[f+3]+e)
            ptr[f+1] -= e
            ptr[f+2] -= e
            col = 0xff00
        i += 1
        ptr[f+5] = col

    if a[2]&{ALIEN_DEAD}:
        return ptr + {len(ALIEN)}

    n = (FRAMES>>2)&0x7
    if a[2]&{ALIEN_SIGHT}:
        ptr[1*{RECT_SIZE}+1] = 8
        ptr[1*{RECT_SIZE}+3] = 7
    else:
        ptr[1*{RECT_SIZE}+3] = LEGS[n]
        ptr[1*{RECT_SIZE}+1] = 1 + (LEGS[n]*2)
    ptr[2*{RECT_SIZE}+4] = LEGS[n]
    ptr[3*{RECT_SIZE}+4] = LEGS[(n+2)&0x7]
    ptr[4*{RECT_SIZE}+4] = LEGS[(n+5)&0x7]

    return ptr + {len(ALIEN)}

def draw_hero(ptr, cx, cy):
    if HERO_DIR == 0:
        memcpy(HEROR, ptr, {len(HERO)})
    elif HERO_DIR == 2:
        memcpy(HEROL, ptr, {len(HERO)})
    elif HERO_DIR == 1:
        memcpy(HEROU, ptr, {len(HERO)})
    else:
        memcpy(HEROD, ptr, {len(HERO)})
    if (INP_X != 0) | (INP_Y != 0):
        ptr[4*{RECT_SIZE}+4] += 1 - ((FRAMES >> 2)&0x3)
        ptr[5*{RECT_SIZE}+4] += -1 + ((FRAMES >> 2)&0x3)
    ptr[1] = cx - HERO_C[0]
    ptr[2] = cy - HERO_C[1]

    if abs(FRAMES-TELEPORT_FRAME) < 48:
        i = 0
        while i < {len(HERO)}:
            poke(ptr + i + 5, rate_color(3, 0xffff, ptr[i+5]))
            i += {RECT_SIZE}

    if HERO_DEAD > 0:
        h = 16
        d = min(HERO_DEAD, h)
        wl = h - d
        ptr[2] += d
        ptr[4] = max(wl, 2)
        if ptr[4] == 2:
            ptr[5] = {col(200, 0, 0)}
            ptr[3] = min(ptr[3]+(HERO_DEAD-h), 12)
        i = {RECT_SIZE}
        while i < {len(HERO)}:
            ptr[i+2] = min(ptr[i+2], wl)
            sy = min(ptr[i+2]+ptr[i+4], wl)
            ptr[i+4] = sy - ptr[i+2]
            i += {RECT_SIZE}
    return ptr + {len(HERO)}

def rate(r):
    return (FRAMES >> r)&1

def rate_trigger(r):
    return (((FRAMES-1) >> r)&1) != ((FRAMES >> r)&1)

def rate_color(r, c1, c2):
    if rate(r):
        return c1
    return c2

def item_rect(ptr, x, y, w, h):
    if hit2(x, y, w, h, ptr[1], ptr[2], ptr[3], ptr[4]) == 0:
        return 0

    ptr[1] = max(ptr[1], x)
    ptr[2] = max(ptr[2], y)
    ptr[3] = min(ptr[3]-x, x+w-ptr[1])
    ptr[4] = min(ptr[4]-y, y+h-ptr[2])

    return 1

def atexit(cx, cy):
    return (cx == EXIT_CX) & (cy == EXIT_CY)

def atexitxy(x, y):
    return atexit(x2c(x), y2c(y))

def draw_mrect(ptr, cx, cy, xoff, yoff):
    x = 0
    y = 0
    w = {TW}
    h = {TH}

#    if inside(cx, cy) == 0:
#        return ptr

    if or2((inside(cx, cy) == 0), mget(LEVEL, cx, cy)):
        ptr[5] = {FGCOL}
    elif atexit(cx, cy):
        if PADS_NR <= 0:
            ptr[5] = rate_color({EXITCOL_RATE}, {EXITCOL3}, {EXITCOL4})
        else:
            ptr[5] = rate_color({EXITCOL_RATE}, {EXITCOL1}, {EXITCOL2})
    elif mget(PADS_MAP, cx, cy):
        ptr[5] = rate_color({PADCOL_RATE}, {PADCOL1}, {PADCOL2})
        x = {TW//4}; y = {TH//4}; w = {TW//2}; h = {TH//2}
    elif mget(SPAWN_MAP, cx, cy):
        ptr[5] = rate_color({SPAWNCOL_RATE}, {SPAWNCOL1}, {SPAWNCOL2})
    elif mget(DOORS_MAP, cx, cy):
        door = lookup_door(cx, cy)
        if bit(door[0], {DOOR_DEAD}):
            ptr[5] = 0xff00
        elif bit(door[0], {DOOR_HIT}):
            ptr[5] = 0xffff
        else:
            ptr[5] = { DOORCOL }
        if mget(LEVEL, cx + 1, cy) | mget(LEVEL, cx - 1, cy):
            x = 1; y = {TH//2-8}; w = {TW-2}; h = 16
        else:
            x = {TW//2-8}; y = 1; w = 16; h = {TH-2}

        if bit(door[0], {DOOR_DEAD}):
            x += 7 - (rnd() & 0xf)
            y += 7 - (rnd() & 0xf)
            w += 7 - (rnd() & 0xf)
            h += 7 - (rnd() & 0xf)
        elif bit(door[0], {DOOR_HIT}):
            w ^= rnd()&1
            h ^= rnd()&1
            x ^= rnd()&1
            y ^= rnd()&1
    else:
        return ptr

    ptr[0] = 1
    xmod = xoff >> 8
    ymod = yoff >> 8
    xoff = xoff & {TWM}
    yoff = yoff & {THM}

    ptr[1] = 0
    ptr[2] = 0

    if xmod == 1:
        ptr[1] = xoff
        ptr[3] = {TW} - xoff
    elif xmod == 2:
        ptr[3] = xoff
    else:
        ptr[3] = {TW}

    if ymod == 1:
        ptr[2] = yoff
        ptr[4] = {TH} - yoff
    elif ymod == 2:
        ptr[4] = yoff
    else:
        ptr[4] = {TH}

    if item_rect(ptr, x, y, w, h) == 0:
        return ptr

    ptr[1] += cx*{TW}
    ptr[2] += cy*{TH}

    return ptr + {RECT_SIZE}

def vwall_scan(sx, sy, ey):
    r = 0
    while sy <= ey:
        if inside(sx, sy) == 0:
            break
        if mget(LEVEL, sx, sy) == 0:
            break
        sy += 1
        r += 1
    return r

def hwall_scan(sx, sy, ex):
    r = 0
    while sx <= ex:
        if inside(sx, sy) == 0:
            break
        if mget(LEVEL, sx, sy) == 0:
            break
        sx += 1
        r += 1
    return r

def draw_hwall(ptr, sx, sy, ex, xoff, yoff):
    while sx <= ex:
        l = hwall_scan(sx, sy, ex)
        optr = ptr
        ptr = draw_mrect(ptr, sx, sy, xoff, yoff)
        if l > 0:
            sx += l
            optr[3] = l*{TW}
        else:
            sx += 1
    return ptr

def draw_vwall(ptr, sx, sy, ey, xoff, yoff):
    while sy <= ey:
        l = vwall_scan(sx, sy, ey)
        optr = ptr
        ptr = draw_mrect(ptr, sx, sy, xoff, yoff)
        if l > 0:
            sy += l
            optr[4] = l*{TH}
        else:
            sy += 1
    return ptr

def draw_map(ptr, x, y):
    xoff = x & {TWM}
    yoff = y & {THM}
    x >>= {TWS}
    y >>= {THS}

    r = {VIEW_R} - 1

    ptr = draw_hwall(ptr, x - r, y - {VIEW_R}, x + r, 0, yoff|0x100)
    ptr = draw_hwall(ptr, x - r, y + {VIEW_R}, x + r, 0, yoff|0x200)

    ptr = draw_vwall(ptr, x - {VIEW_R}, y - r, y + r, xoff|0x100, 0)
    ptr = draw_vwall(ptr, x + {VIEW_R}, y - r, y + r, xoff|0x200, 0)

    ptr = draw_mrect(ptr, x-{VIEW_R}, y-{VIEW_R}, xoff|0x100, yoff|0x100)
    ptr = draw_mrect(ptr, x-{VIEW_R}, y+{VIEW_R}, xoff|0x100, yoff|0x200)
    ptr = draw_mrect(ptr, x+{VIEW_R}, y-{VIEW_R}, xoff|0x200, yoff|0x100)
    ptr = draw_mrect(ptr, x+{VIEW_R}, y+{VIEW_R}, xoff|0x200, yoff|0x200)

    sy = y - r
    while sy <= y + r:
        ptr = draw_hwall(ptr, x - r, sy, x + r, 0, 0)
        sy += 1
    return ptr

INP_STATE = {KEY_STATE}

INP_Y = 0
INP_X = 0
INP_A = 0
INP_B = 0

def kbd_clear():
    INP_A = 0
    INP_B = 0

def kbd_proc():
    i = 0
    while i < {KEY_NUM}:
        c = peek({KEY_MEM} + i)
        if c != INP_STATE[i]:
            if i == {KEY_UP}:
                INP_Y = -1*c
            elif i == {KEY_DOWN}:
                INP_Y = 1*c
            elif i == {KEY_LEFT}:
                INP_X = -1*c
            elif i == {KEY_RIGHT}:
                INP_X = 1*c
            elif i == {KEY_A}:
                INP_A = c
            elif i == {KEY_B}:
                INP_B = c
            INP_STATE[i] = c
        i += 1

    if INP_X == 0:
        if INP_STATE[{KEY_LEFT}]:
            INP_X = -1
        elif INP_STATE[{KEY_RIGHT}]:
            INP_X = 1

    if INP_Y == 0:
        if INP_STATE[{KEY_UP}]:
            INP_Y = -1
        elif INP_STATE[{KEY_DOWN}]:
            INP_Y = 1

def map_coll(x, y, rx, ry):
    if insidexy(x+rx, y-ry) == 0:
        return 1
    if insidexy(x+rx, y+ry) == 0:
        return 1
    if insidexy(x-rx, y-ry) == 0:
        return 1
    if insidexy(x-rx, y+ry) == 0:
        return 1

    if mgetxy(LEVEL, x, y) | \
        mgetxy(LEVEL, x+rx, y-ry) | \
        mgetxy(LEVEL, x+rx, y+ry) | \
        mgetxy(LEVEL, x-rx, y-ry) | \
        mgetxy(LEVEL, x-rx, y+ry):
        return 1

    return mgetxy(DOORS_MAP, x, y) | \
        mgetxy(DOORS_MAP, x+rx, y-ry) | \
        mgetxy(DOORS_MAP, x+rx, y+ry) | \
        mgetxy(DOORS_MAP, x-rx, y-ry) | \
        mgetxy(DOORS_MAP, x-rx, y+ry)

def draw_radar(ptr, pos):
    y = 0
    b = 255 - (FRAMES&(0xffff>>(16-{RADAR_RATE})))*5
    pos >>= {THS}
    cx = PX>>{TWS}
    cy = PY>>{THS}
    while y < {H}:
        x = 0
        while x < {W}:
            if (pos > y):
                far = ((abs(cx-x)>{VIEW_R})|(abs(cy-y)>{VIEW_R}))
                if mget(RADAR_MAP, x, y):
                    ptr = draw_circle(ptr, c2x(x), c2y(y), 4, rgb(b,0,0))
                elif mget(PADS_MAP, x, y) & far:
                    ptr = draw_circle(ptr, c2x(x), c2y(y), 4, rgb(b,b,0))
                elif atexit(x, y) & far:
                    ptr = draw_circle(ptr, c2x(x), c2y(y), 4, rgb(0,b,b))
            x += 1
        y += 1
    return ptr

def draw_aliens(ptr):
    a = ALIENS
    ae = ALIENS + {ALIENS_SIZE}
    while a < ae:
        if a[2] != 0:
            ptr = draw_alien(ptr, a)
        a += 3
    return ptr

ALIEN_DIR = 0
def get_alien_dir():
    ALIEN_DIR = (ALIEN_DIR+1)&0x3
    return ALIEN_DIR

def spawn_alien():
    if SPAWNS_NR == 0:
        return
    if ltu(abs(FRAMES-SPAWN_FRAME), {SPAWN_DELAY}):
        return
    spawn = SPAWNS[SPAWN_ID]
    sx = c2x(int2cx(spawn))
    sy = c2y(int2cy(spawn))
    if scan_alien(sx, sy, 0) != 0:
        return
    SPAWN_ID += 1
    if SPAWN_ID >= SPAWNS_NR:
        SPAWN_ID = 0
    new_alien(sx, sy)

def new_alien(sx, sy):
    a = ALIENS
    ae = ALIENS + {ALIENS_SIZE}
    while a < ae:
        if a[2] == 0:
            a[0] = sx
            a[1] = sy
            a[2] = {ALIEN_HEALTH<<8} | get_alien_dir()
            ALIENS_NR += 1
            SPAWN_FRAME = FRAMES
            return
        a += 3

def hit1(x, y, w, h, tx, ty):
    return (tx >= x) & (tx < x + w) & \
        (ty >= y) & (ty < y + h)

def hit2(x1, y1, w1, h1, x2, y2, w2, h2):
    return (x1 < (x2+w2)) & ((x1 + w1)>x2) & \
        (y1 < (y2+h2)) & ((y1+h1)>y2)

def alien_coll(a):
    x1 = PX - HERO_C[0]
    y1 = PY - HERO_C[1]
    w1 = HERO_C[0]*2
    h1 = HERO_C[1]*2

    w2 = ALIEN[3]
    h2 = ALIEN[4]
    x2 = x2tl(a[0], w2)
    y2 = y2tl(a[1], h2)

    return hit2(x1, y1, w1, h1, x2, y2, w2, h2)

def scan_alien(x, y, aa):
    if insidexy(x, y) == 0:
        return 0
    a = ALIENS
    ae = ALIENS + {ALIENS_SIZE}
    w = ALIEN[3]
    h = ALIEN[4]
    while a < ae:
        if (a[2]!=0) & (aa != a) & hit1(x2tl(a[0], w), y2tl(a[1], h), w, h, x, y):
            return a
        a += 3
    return 0

def alien_can_move(a, dir):
    x = (a[0]>>{TWS}) + DIRS[dir*2]
    y = (a[1]>>{THS}) + DIRS[dir*2+1]

    if inside(x, y) == 0:
        return 1
    if mget(LEVEL, x, y) | mget(DOORS_MAP, x, y):
        return 1

    aa = scan_alien(c2x(x), c2y(y), a)
    if aa:
        return 1
    return 0

def alien_sight(x, y, tx, ty):
    return light_ray(x2c(x), y2c(y), x2c(tx), y2c(ty), {W})

def upd_alien(a):
    if bit(a[2], {ALIEN_DEAD}):
        e = bit_gethi(a[2], {ALIEN_MASK}) - 4
        a[2] = bit_sethi(a[2], {ALIEN_MASK}, e)
        if e <= 0:
            a[2] = 0
            ALIENS_NR -= 1
            SPAWN_FRAME = FRAMES
        return

    dir = a[2]&0x3
    x = a[0]
    y = a[1]

    aligned_x = ((x - {TW//2}) & {TWM}) == 0
    aligned_y = ((y - {TH//2}) & {THM}) == 0
    aligned = aligned_x & aligned_y

    ttl = (a[2]&0xf8)>>3

    if (ttl > 0) & aligned:
        ttl = ttl - 1

    if (HERO_DEAD == 0) & alien_sight(x, y, PX, PY):
        a[2] |= {ALIEN_SIGHT}
    else:
        a[2] &= ~{ALIEN_SIGHT}

    if aligned & bit(a[2], {ALIEN_SIGHT}):
        if (x>>{TWS}) == (PX>>{TWS}):
            if PY > y:
                dir = 3
            else:
                dir = 1
        else:
            if PX > x:
                dir = 0
            else:
                dir = 2
        ttl = 8

    t = 4
    while (aligned) & (t > 0) & (alien_can_move(a, dir)):
        dir += 1
        dir &= 0x3
        t -= 1

    dl = (dir + 1)&0x3
    dr = (dir + 3)&0x3
    if (get_alien_dir() & 1):
        {mswap("dl", "dr")}

    if (ttl == 0) & aligned & (t > 0):
        if (alien_can_move(a, dl) == 0):
            dir = dl
            ttl = 4
        elif (alien_can_move(a, dr) == 0):
            dir = dr
            ttl = 4

    if (t > 0):
        aa = scan_alien(x, y, a)
        if (aa == 0) | (aa > a):
            x += DIRS[dir*2]
            y += DIRS[dir*2+1]

    a[2] &= ~0x0ff
    a[2] |= dir | (ttl << 3)
    a[0] = x
    a[1] = y

    if (HERO_DEAD == 0) & (alien_coll(a)==1):
        HERO_DEAD = 1
        kbd_clear()

    if and3(insidexy(x, y), (RADAR_MODE == 480), (alien_visible(a) == 0)):
        msetxy(RADAR_MAP, x, y, 1)
    return

def upd_aliens():
    if RADAR_MODE == 480:
        bzero(RADAR_MAP, {H})

    if ALIENS_NR < SPAWNS_NR:
        spawn_alien()

    a = ALIENS
    ae = ALIENS + {ALIENS_SIZE}

    if ALIENS_NR > 0:
        a = ALIENS
        while a < ae:
            if a[2] != 0:
                upd_alien(a)
            a += 3
        return

def upd_hero():
    if HERO_DEAD > 0:
        HERO_DEAD += 1
        if INP_A & (HERO_DEAD>100):
            INP_A = 0
            SCROLL_MODE = - 480
        return

    if RADAR_MODE > 0:
        LASER_HEAT = min(LASER_HEAT + {RADAR_COST}, {LASER_HEAT_MAX})
        if LASER_HEAT >= {LASER_HEAT_MAX}:
            RADAR_MODE = 0
        else:
            RADAR_MODE -= 8

    if INP_B & (RADAR_MODE == 0):
        INP_B = 0
        RADAR_MODE = 480

    ox = PX
    oy = PY
    if map_coll(PX+INP_X, PY, 4, 10) == 0:
        PX = PX + INP_X
    if map_coll(PX, PY+INP_Y, 4, 10) == 0:
        PY = PY + INP_Y
    if (INP_X > 0) & ((HERO_DIR == 2) | (INP_Y == 0)):
        HERO_DIR = 0
    elif (INP_X < 0) & ((HERO_DIR == 0) | (INP_Y == 0)):
        HERO_DIR = 2
    elif (INP_Y > 0) & ((HERO_DIR == 1) | (INP_X == 0)):
        HERO_DIR = 3
    elif (INP_Y < 0) & ((HERO_DIR == 3) | (INP_X == 0)):
        HERO_DIR = 1

    if insidexy(PX, PY) == 0:
        return

    if mclrxy(PADS_MAP, PX, PY):
        PADS_NR -= 1
        LASER_HEAT = 0
    if (PADS_NR == 0) & atexitxy(PX, PY):
        NEXT_LEVEL = LEVEL + {LEVEL_SIZE}
        SCROLL_MODE = -480
        return
    if mgetxy(SPAWN_MAP, PX, PY) & (mgetxy(SPAWN_MAP, ox, oy) != 1) & (SPAWNS_NR > 1):
        i = 0
        cx = x2c(PX)
        cy = y2c(PY)
        while i < SPAWNS_NR:
            spawn = SPAWNS[i]
            i += 1
            if c2int(cx, cy) == (spawn&0xff):
                if i == SPAWNS_NR:
                    i = 0
                spawn = SPAWNS[i]
                PX = c2x(int2cx(spawn))
                PY = c2y(int2cy(spawn))
                TELEPORT_FRAME = FRAMES
                return

def update():
    if SCROLL_MODE > 0:
        SCROLL_MODE -= 16
        return
    elif SCROLL_MODE < 0:
        SCROLL_MODE += 16
        if SCROLL_MODE >= 0:
            SCROLL_MODE = 480
            LEVEL = NEXT_LEVEL
            loadlev()
        return
    kbd_proc()
    upd_laser()
    upd_doors()
    upd_aliens()
    upd_hero()

ALIEN_COLS = [0,0,0,0,0]
SCROLL_MODE = 0

def setup():
    LEVEL = MAP# + 4*{LEVEL_SIZE}
    i = 0
    while i < {len(ALIEN)}:
        ALIEN_COLS[i] = ALIEN[i*{RECT_SIZE}+5]
        i += 1

def screen_off(ox, oy):
    ptr = {RECT_MEM} + {RECT_SIZE} # skip bg
    eptr = {RECT_MEM} + {RECT_NUM}*{RECT_SIZE}
    while ptr < eptr:
        if ptr[0]:
            ptr[1] += ox
            ptr[2] += oy
        ptr += {RECT_SIZE}

def draw_status(ptr):
    l = {LASER_HEAT_MAX} - LASER_HEAT

    ptr = draw_rect(ptr, 640-6, 0,
        6, l, rgb(min(128+(l>>2), 255), 32, 0))
    if PADS_NR == 0:
        l = 480
    else:
        l = ((PADS_MAX - PADS_NR)*480) >> PADS_S
    if l >= 480:
        col = rate_color(2, {col(0, 32, 255)}, {col(0, 212, 255)})
    else:
        col = rgb(0, 32, min(128+(l>>2), 255))
    ptr = draw_rect(ptr, 0, 0,
        6, l, col)
    return ptr

RADAR_MODE = 0

def draw():
    ptr = {RECT_MEM}
    bzero(ptr, {RECT_SIZE}*{RECT_NUM})

    ptr = draw_rect(ptr, 0, 0, 640, 480, {BGCOL1})
    ptr = draw_rect(ptr, PX-{TW}*{VIEW_R}, PY-{TH}*{VIEW_R}, {VIEW_SIZE-1}*32, {VIEW_SIZE-1}*32, {BGCOL2})

    ptr = draw_map(ptr, PX, PY)
    ptr = draw_hero(ptr, PX, PY)
    ptr = draw_laser(ptr)
    ptr = draw_aliens(ptr)

    if (RADAR_MODE > 0):
        ptr = draw_rect(ptr, 0, 480 - RADAR_MODE, 15*32, 1, rate_color(3, rgb(255,0,0), rgb(128, 128, 128)))
        ptr = draw_radar(ptr, 480 - RADAR_MODE)
#    screen_off(-PX+320, -PY+240)
    if SCROLL_MODE < 0:
        screen_off((640-{W}*{TW})>>1, -SCROLL_MODE-480)
    else:
        screen_off((640-{W}*{TW})>>1, SCROLL_MODE)
    ptr = draw_status(ptr)

def main():
    setup()
    loadlev()
    while 1:
        update()
        draw()
        wait()
        FRAMES += 1
''')
