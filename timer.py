# Spinach2 speedrun timer (0.2.2)
# by _peanutButter

import curses
import time
import sys

filename = sys.argv[1]

try:
    split_data = eval(open(filename).read())
except:
    sys.exit()

# print(f"Playing {split_data['game']} ({split_data['category']})")
# for split in split_data["splits"]:
#     print(f"\t{split_data['splits'].index(split)} - {split['name']}")
#     print(f"\t\tPB: {split['personal_best']}")
#     print(f"\t\tBest: {split['best']}")

screen = curses.initscr()
window = curses.newwin(40, 100)

curses.noecho()
curses.cbreak()
curses.curs_set(False)
window.keypad(True)
window.nodelay(True)

active_run = False
finished = False
paused = False
current_split = 0
num_splits = len(split_data["splits"])
split_times = []
split_times_shortened = []

start_time = 0
pause_time = 0
attempts = 0

while True:
    window.clear()

    keypress = window.getch()

    current_time = time.time_ns() - pause_time

    if keypress == curses.KEY_BACKSPACE:
        if active_run == False:
            active_run = True
            attempts += 1
            start_time = current_time
        else:
            if finished:
                splits = []
                if split_data["personal_best"] > split_times[-1]:
                    split_data["personal_best"] = split_times[-1]
                    for split in split_data["splits"]:
                        split["personal_best"] = split_times_shortened[split_data["splits"].index(split)]
                
                for split in split_data["splits"]:
                    if split["best"] > split_times_shortened[split_data["splits"].index(split)]:
                        splits.append({"name": split["name"], "best": split_times_shortened[split_data["splits"].index(split)], "personal_best": split["personal_best"]})
                    else:
                        splits.append(split)

                split_data["splits"] = splits
                split_data["attempts"] += attempts
                
                with open(filename, "w") as file:
                    file.write(str(split_data))

            active_run = False
            start_time = 0
            split_times = []
            split_times_shortened = []
            current_split = 0
            finished = False
    elif keypress == curses.KEY_RIGHT and active_run and not finished:
        current_split += 1
        split_times.append(current_time - start_time)
        split_times_shortened.append(current_time - start_time - sum_of_previous_splits)
        if current_split >= num_splits:
            finished = True
            current_split -= 1
    # elif keypress == curses.KEY_LEFT and active_run:
    #     current_split -= 1
    elif keypress == curses.KEY_UP and active_run and not finished:
        if not paused:
            paused = True
            pause_start_time = current_time
        else:
            paused = False
            pause_time += current_time - pause_start_time

    window.addstr(1, 1, f"{split_data['game']}", curses.A_BOLD)
    window.addstr(2, 1, f"{split_data['category']}", curses.A_ITALIC)
    window.addstr(3, 1, f"{split_data['attempts']} attempts")

    # window.addstr(4, 1, f"Active: {active_run}")

    draw_y = 5
    for split in split_data["splits"]:
        split_index = split_data["splits"].index(split)
        sum_of_previous_splits = 0
        for x in split_times_shortened:
            sum_of_previous_splits += x

        if split_index < current_split and active_run or finished:
            window.addstr(draw_y, 1, f"{split['name']}\t\t{split_times[split_index] / 1000000000} ({(split_times_shortened[split_index] - split['personal_best']) / 1000000000}/{(split_times[split_index] - sum([x['personal_best'] for x in split_data['splits'][0:split_index + 1]])) / 1000000000})")
        elif (split_index == current_split and active_run or finished) and not paused:
            window.addstr(draw_y, 1, f"{split['name']}\t\t{(current_time - start_time - sum_of_previous_splits) / 1000000000} ({((current_time - start_time - split['personal_best'] - sum_of_previous_splits) / 1000000000)})", curses.A_REVERSE)
        elif (split_index > current_split and active_run or finished) or (split_index == current_split and paused):
            window.addstr(draw_y, 1, f"{split['name']}\t\t-")
        else:
            window.addstr(draw_y, 1, f"{split['name']}")
        
        draw_y += 1

    if active_run or finished or paused:
        if not finished and not paused:
            delta = ((current_time - start_time) - split_data['personal_best']) / 1000000000
            elapsed_time = (current_time - start_time) / 1000000000
            best_possible = (sum_of_previous_splits + sum([x['best'] for x in split_data['splits'][current_split:]])) / 1000000000

        draw_y += 1
        window.addstr(draw_y, 1, f"Elapsed time: {elapsed_time}")

        draw_y += 1
        window.addstr(draw_y, 1, f"Delta: {delta}")

        draw_y += 1
        window.addstr(draw_y, 1, f"Best possible: {best_possible}")

    draw_y += 1
    window.addstr(draw_y, 1, f"Sum of best: {sum([x['best'] for x in split_data['splits']]) / 1000000000}")

    if paused:
        draw_y += 2
        window.addstr(draw_y, 1, f"PAUSED")

    window.refresh()
    time.sleep(0.05)

curses.nocbreak()
curses.echo()
window.keypad(False)
window.nodelay(False)

curses.endwin()
