# Spinach2 speedrun timer (0.2.8)
# by _peanutButter

import curses
import time
import sys

filename = sys.argv[1]

#try:
split_data = eval(open(filename).read())
# except:
#     sys.exit()

# print(f"Playing {split_data['game']} ({split_data['category']})")
# for split in split_data["splits"]:
#     print(f"\t{split_data['splits'].index(split)} - {split['name']}")
#     print(f"\t\tPB: {split['personal_best']}")
#     print(f"\t\tBest: {split['best']}")

screen = curses.initscr()
window = curses.newwin(70, 100)

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

time_division_factor = 1000000000

start_time = 0
pause_time = 0
attempts = 0

while True:
    window.clear()

    keypress = window.getch()

    current_time = time.time_ns() - pause_time

    if keypress == curses.KEY_DOWN and not active_run:
        break
    elif keypress == curses.KEY_BACKSPACE:
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
                attempts = 0
                
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

            sum_of_best = sum([x['best'] for x in split_data['splits']])
            elapsed_time = (current_time - start_time)
            best_possible = (sum_of_previous_splits + (sum([x["best"] for x in split_data["splits"][current_split:]]))) / time_division_factor
            pb_delta = (elapsed_time - split_data['personal_best']) / time_division_factor
            best_delta = (elapsed_time - sum_of_best) / time_division_factor
    elif keypress == curses.KEY_LEFT and active_run:
        if time_division_factor == 1000000000:
            time_division_factor = 60000000000
        else:
            time_division_factor = 1000000000
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
        sum_of_previous_splits = split_times[-1] if not len(split_times) == 0 else 0

        if split_index < current_split and active_run or finished:
            window.addstr(draw_y, 1, f"{split['name']}\t\t{round(split_times[split_index] / time_division_factor, 4)} ({round((split_times_shortened[split_index] - split['personal_best']) / time_division_factor, 4)}/{round((split_times[split_index] - sum([x['personal_best'] for x in split_data['splits'][0:split_index + 1]])) / time_division_factor, 4)}/{round((split_times_shortened[split_index] - split['best']) / time_division_factor, 4)})")
        elif (split_index == current_split and active_run or finished) and not paused:
            window.addstr(draw_y, 1, f"{split['name']}\t\t{round((current_time - start_time - sum_of_previous_splits) / time_division_factor, 4)} ({round(((current_time - start_time - split['personal_best'] - sum_of_previous_splits) / time_division_factor), 4)})", curses.A_REVERSE)
        elif (split_index > current_split and active_run or finished) or (split_index == current_split and paused):
            window.addstr(draw_y, 1, f"{split['name']}\t\t-")
        else:
            window.addstr(draw_y, 1, f"{split['name']}")
        
        draw_y += 1

    if active_run or finished or paused:
        if not finished and not paused:
            sum_of_best = sum([x['best'] for x in split_data['splits']])
            elapsed_time = (current_time - start_time)
            best_possible = (sum_of_previous_splits + (sum([x["best"] for x in split_data["splits"][current_split:]]))) / time_division_factor
            possible_time_save = ((split_data["personal_best"] / time_division_factor) - best_possible)
            pb_delta = (elapsed_time - split_data['personal_best']) / time_division_factor
            best_delta = (elapsed_time - sum_of_best) / time_division_factor

        draw_y += 1
        window.addstr(draw_y, 1, f"Elapsed time: {round(elapsed_time / time_division_factor, 4)}")

        draw_y += 1
        window.addstr(draw_y, 1, f"Personal best: {round(split_data['personal_best'] / time_division_factor, 4)}")

        draw_y += 1
        window.addstr(draw_y, 1, f"PB delta: {round(pb_delta, 4)}")

        draw_y += 1
        window.addstr(draw_y, 1, f"Best delta: {round(best_delta, 4)}")

        draw_y += 1
        window.addstr(draw_y, 1, f"Best possible: {round(best_possible, 4)}")

        draw_y += 1
        window.addstr(draw_y, 1, f"Possible time save: {round(possible_time_save, 4)}")

        draw_y += 1
        window.addstr(draw_y, 1, f"Sum of best: {round(sum_of_best / time_division_factor, 4)}")

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
