import time
import displayio
from adafruit_magtag.magtag import MagTag
from adafruit_display_shapes.circle import Circle

#  create MagTag and connect to network
try:
    magtag = MagTag()
    # magtag.network.connect()
except (ConnectionError, ValueError, RuntimeError) as e:
    print("*** MagTag(), Some error occured, retrying! -", e)
    # Exit program and restart in 1 seconds.
    magtag.exit_and_deep_sleep(1)

# false = Dec 1st show circle 1 through to Dec 25th show circle 25
countdown_feature_flag = False
# true = Dec 1st show circle 25 through to Dec 25th show circle 1
# Nov 30 - C25
# Dec 1  - C24
# Dec 2  - C23
# Dec 3  - C22
# Dec 4  - C21
# Dec 5  - C20
# Dec 6  - C19
# Dec 7  - C18
# Dec 8  - C17
# Dec 9  - C16
# Dec 10  - C15
# Dec 11  - C14
# Dec 12  - C13
# Dec 13  - C12
# Dec 14  - C11
# Dec 15  - C10
# Dec 16  - C9
# Dec 17  - C8
# Dec 18  - C7
# Dec 19  - C6
# Dec 20  - C5
# Dec 21  - C4
# Dec 22  - C3
# Dec 23  - C2
# Dec 24  - C1
# Dec 25  - mc.bmp


#  import tree bitmap
tree_filename = "/atree.bmp"
christmas_filename = "/mc.bmp"

month = 0
day = 0
seconds_since_midnight = 0

#  displayio groups
group = displayio.Group()
tree_group = displayio.Group()
circle_group = displayio.Group()

def get_local_time():
    #  grabs time from network
    magtag.get_local_time()
    #  parses time into month, date, etc
    now = time.localtime()
    month = now[1]
    day = now[2]

    (hour, minutes, seconds) = now[3:6]
    seconds_since_midnight = 60 * (hour*60 + minutes)+seconds
    print( f"day is {day}, ({seconds_since_midnight} seconds since midnight)")

def display_merry_christmas():
    christmas = displayio.OnDiskBitmap(open(christmas_filename, "rb"))
    tile = displayio.TileGrid(
        christmas, pixel_shader=getattr(christmas, "pixel_shader", displayio.ColorConverter())
    )
    group.append(tile)

def display_tree():
    # CircuitPython 6 & 7 compatible
    tree = displayio.OnDiskBitmap(open(tree_filename, "rb"))
    tree_grid = displayio.TileGrid(
        tree, pixel_shader=getattr(tree, 'pixel_shader', displayio.ColorConverter())
    )

    #  add bitmap to its group
    tree_group.append(tree_grid)
    #  add tree group to the main group
    group.append(tree_group)

    #  list of circle positions
    spots = (
        (246, 53), # 1
        (246, 75), # 2
        (206, 42), # 3
        (206, 64), # 4
        (206, 86), # 5
        (176, 31), # 6
        (176, 53), # 7
        (176, 75), # 8
        (176, 97), # 9
        (136, 42), # 10
        (136, 64), # 11
        (136, 86), # 12
        (106, 31), # 13
        (106, 53), # 14
        (106, 75), # 15
        (106, 97), # 16
        (66, 31),  # 17
        (66, 53),  # 18
        (66, 75),  # 19
        (66, 97),  # 20
        (36, 20),  # 21
        (36, 42),  # 22
        (36, 64),  # 23
        (36, 86),  # 24
        (36, 108)  # 25
    )

    #  circles to cover-up bitmap's number ornaments
    ball_color = [0x555555, 0xaaaaaa, 0xFFFFFF] # All colors except black (0x000000)
    ball_color_index = 0

    #  creating the circles & pulling in positions from spots
    for spot in spots:
        circle = Circle(x0=spot[0], y0=spot[1], r=11, fill=ball_color[ball_color_index]) # Each ball has a color
        ball_color_index += 1
        ball_color_index %= len(ball_color)
        #  adding circles to their display group
        circle_group.append(circle)

    #  adding circles group to main display group
    group.append(circle_group)

def go_to_sleep():
    time.sleep(5)
    #   goes into deep sleep till a 'stroke' past midnight
    print("entering deep sleep")
    seconds_to_sleep = 24*60*60 - seconds_since_midnight + 10
    print( f"sleeping for {seconds_to_sleep} seconds")
    magtag.exit_and_deep_sleep(seconds_to_sleep)

## main - start
get_local_time()

if countdown_feature_flag == True:
    if month == 12 and day == 25:
        display_merry_christmas()
    else:
        display_tree()

        if month == 11 and day == 30:
            circle_group[24].fill = None
        if month == 12 and day < 25:
            for i in range(24 - day, 25, 1):
                circle_group[i].fill = None
else:
    display_tree()

    if month < 12:
        day = 0

    for i in range(day):
        circle_group[i].fill = None
        time.sleep(0.1)

magtag.display.show(group)
magtag.display.refresh()

go_to_sleep()
## main - end
