# Spinach2 speedrun timer (0.1.0)
# by _peanutButter

import curses
import time

filename = "flowercup200cc.split"
split_data = eval(open(filename).read())

# print(f"Playing {split_data['game']} ({split_data['category']})")
# for split in split_data["splits"]:
#     print(f"\t{split_data['splits'].index(split)} - {split['name']}")
#     print(f"\t\tPB: {split['personal_best']}")
#     print(f"\t\tBest: {split['best']}")

screen = curses.initscr()
window = curses.newwin(20, 60)

curses.noecho()
curses.cbreak()
curses.curs_set(False)
window.keypad(True)
window.nodelay(True)

active_run = False
paused = False
current_split = 0
num_splits = len(split_data["splits"])
split_times = []

start_time = 0
attempts = 0

while True:
    window.clear()

    keypress = window.getch()

    if keypress == curses.KEY_BACKSPACE:
        if active_run == False:
            active_run = True
            attempts += 1
            start_time = time.time_ns()
        else:
            if paused:
                splits = []
                for split in split_data["splits"]:
                    if split["personal_best"] > split_times[split_data["splits"].index(split)]:
                        splits.append({"name": split["name"], "best": 0.0, "personal_best": split_times[split_data["splits"].index(split)]})
                    else:
                        splits.append(split)

                split_data["splits"] = splits
                split_data["attempts"] += attempts
                
                with open(filename, "w") as file:
                    file.write(str(split_data))

            active_run = False
            start_time = 0
            split_times = []
            current_split = 0
            paused = False
    elif keypress == curses.KEY_RIGHT and active_run and not paused:
        current_split += 1
        split_times.append(time.time_ns() - start_time)
        if current_split >= num_splits:
            paused = True
            current_split -= 1
    # elif keypress == curses.KEY_LEFT and active_run:
    #     current_split -= 1

    window.addstr(1, 1, f"{split_data['game']}", curses.A_BOLD)
    window.addstr(2, 1, f"{split_data['category']}", curses.A_ITALIC)
    window.addstr(3, 1, f"{split_data['attempts']} attempts")

    # window.addstr(4, 1, f"Active: {active_run}")

    draw_y = 5
    for split in split_data["splits"]:
        split_index = split_data["splits"].index(split)

        if split_index < current_split and active_run or paused:
            window.addstr(draw_y, 1, f"{split['name']}\t\t{split_times[split_index] / 1000000000} ({(split_times[split_index] - split['personal_best']) / 1000000000})")
        elif split_index == current_split and active_run or paused:
            window.addstr(draw_y, 1, f"{split['name']}\t\t{(time.time_ns() - start_time) / 1000000000} ({((time.time_ns() - start_time - split['personal_best']) / 1000000000)}", curses.A_REVERSE)
        elif split_index > current_split and active_run or paused:
            window.addstr(draw_y, 1, f"{split['name']}\t\t-")
        else:
            window.addstr(draw_y, 1, f"{split['name']}")
        
        draw_y += 1

    window.refresh()
    time.sleep(0.05)

curses.nocbreak()
curses.echo()
window.keypad(False)
window.nodelay(False)

curses.endwin()
