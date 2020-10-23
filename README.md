# spinach2
## What is spinach2?
Spinach2 is a speedrun timer for linux that runs right in your terminal through the power of Python and curses. It is a detailed timer with splits, deltas, split deltas, personal best tracking, and more common speedrun timer features. Splits and game data are stored in a plaintext file which is easily customizable/modifiable. Spinach2 does not currently contain splits.io or speedrun.com integration, but that's one of my future development goals. It also does not support split history tracking. This is another future goal.

## Why the 2? Was there a previous spinach application?
There never was an official spinach1. I began development on a speedrun timer similar to this one at the end of 2019, but it never went anywhere. In respect of that project I've decided to call this one spinach2 as it is the spiritual successor to the unreleased spinach speedrun timer.

## Why is it called spinach then?
I thought it sounded cool... The name was originally concieved when I tried to come up with a cool sounding name that was a combination of speedrun timer and linux. One of the potential names was speenux, which, when pronounced, sounds a lot like spinach. In the end, I just decided to go with spinach.

## How do I use spinach2?
I'll add some detailed installation/setup instructions here sometime in the future, but for now I'll just provide a list of button inputs and what they do.

- `backspace` - hard-toggles a run (starts a new run if there is no active run, stops it if there is)
- `right arrow key` - split
- `up arrow key` - soft-toggles a run (pauses/resumes the active run)
- `down arrow key` - quits the speedrun timer (only works if there is no active run; you can always use `ctrl-c` if needed)