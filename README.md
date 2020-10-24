# spinach2
## What is spinach2?
Spinach2 is a speedrun timer for linux that runs right in your terminal through the power of Python and curses. It is a detailed timer with splits, deltas, split deltas, personal best tracking, and more common speedrun timer features. Splits and game data are stored in a plaintext file which is easily customizable/modifiable. Spinach2 does not currently contain splits.io or speedrun.com integration, but that's one of my future development goals. It also does not support split history tracking. This is another future goal.

## How do I use spinach2?
I'll add some detailed installation/setup instructions here sometime in the future, but for now I'll just provide a list of button inputs and what they do.

- `backspace` - hard-toggles a run (starts a new run if there is no active run, stops it if there is)
- `right arrow key` - split
- `up arrow key` - soft-toggles a run (pauses/resumes the active run)
- `down arrow key` - quits the speedrun timer (only works if there is no active run; you can always use `ctrl-c` if needed)
- `left arrow key` - switches between displaying times in seconds and in minutes

Although it isn't enforced in the code, it's important that you do not exceed 24 splits per file, as spinach2 can currently only display that many on screen at one time. Support for scrolling splits will be included in a future update.
