from psychopy.gui import DlgFromDict
from psychopy.visual import Window
from psychopy.core import Clock, quit, wait
from psychopy.event import Mouse
from psychopy.hardware.keyboard import Keyboard
from psychopy.visual import TextStim, Rect
from psychopy import core, event, data
import numpy as np
import pandas as pd
### DIALOG BOX ROUTINE ###
exp_info = {'participant_nr': 1, 'age': 21}
dlg = DlgFromDict(exp_info)

# If pressed Cancel, abort!
if not dlg.OK:
    quit()
else:
    # Quit when either the participant nr or age is not filled in
    if not exp_info['participant_nr'] or not exp_info['age']:
        quit()
        
    # Also quit in case of invalid participant nr or age
    if exp_info['participant_nr'] > 99 or int(exp_info['age']) < 18:
        quit()
    else:  # let's star the experiment!
        print(f"Started experiment for participant {exp_info['participant_nr']} "
                 f"with age {exp_info['age']}.")

colors = ('red', 'green', 'yellow', 'blue')
texts = ('red', 'green', 'yellow', 'blue')

# Initialize a fullscreen window with my monitor (HD format) size
# and my monitor specification called "samsung" from the monitor center
win = Window(size=(1920, 1080), fullscr=False, monitor='samsung', units='norm', color=[-1, -1, -1])



# Also initialize a mouse, for later
# We'll set it to invisible for now
mouse = Mouse(visible=False)

# Initialize a (global) clock
clock = Clock()

# Initialize Keyboard
kb = Keyboard()
### START BODY OF EXPERIMENT ###
rectangle = Rect(win, fillColor='white', pos=(1,1), size = (1e-1 / 16 * 9, 1e-1))
rectangle.autoDraw = True
# We assume `win` already exists
welcome_txt_stim = TextStim(win, text="Welcome to this experiment! \n Press space bar for instructions", font='Calibri', color=(1, 1, 1))
welcome_txt_stim.draw()
win.flip()
keys = event.waitKeys(keyList=["space"])
message = """In this task, you will see color names (red, green, blue, yellow) in different "print" colors. You need to respond to the print color. The buttons are used in this study are "g", "b", "y" and "r" for green, blue, yellow and red.

(Press ‘enter’ to start the experiment!)"""

instruct_txt_stim = TextStim(win, text=message, 
                            font='Calibri',
                            color=(1, 1, 1),
                            alignText = 'left', height=0.085)
instruct_txt_stim.draw()
win.flip()


keys = event.waitKeys(keyList=["return"])


cross = TextStim(win, text='+', 
                        font='Calibri',
                        color='white',
                        alignText = 'center', height=0.2) 
num_trials = 5
stimList = [{'word' : text, 'color' : color} for color in colors for text in texts] 
trials = data.TrialHandler(stimList, 10)
                           
correct_dict = { 0 : 'incorrect', 1 : 'correct'}
for i, thisTrial in enumerate(trials):
    
    
    cross.draw()
    win.flip()
    core.wait(1)


    color = thisTrial['color']
    text = thisTrial['word']
    stimul = TextStim(win, text=text, 
                            font='Calibri',
                            color=color,
                            alignText = 'center', height=0.085)
    stimul.draw()
    
    win.flip()
    stimul_timestamp = clock.getTime()
    keys = event.waitKeys(keyList=["r", "g", "b", "y"], timeStamped = clock)
    if color  == text:
        is_congruent = 1
    else:
        is_congruent = 0
    
    if keys[0][0]  == color[0]:   
        is_correct = 1
    else:
        is_correct = 0
    # answer = TextStim(win, text=correct_dict[is_correct], 
                                # font='Calibri',
                                # color='white',
                                # alignText = 'center', height=0.085)
    # answer.draw()
    # win.flip()
    # core.wait(0.5)
    
    trials.data.add('is congruent', is_congruent)
    trials.data.add('Stim timestamp', stimul_timestamp)
    trials.data.add('key pressed', keys[0][0])    
    trials.data.add('key timestamp', keys[0][1])
    trials.data.add('delta T', keys[0][1] - stimul_timestamp)
    trials.data.add('is correct', is_correct)
### END BODY OF EXPERIMENT ###
trials.saveAsWideText('stroop_data.csv', delim = ';', appendFile=False, fileCollisionMethod='overwrite')

df = pd.read_csv('stroop_data.csv', sep = ';')
# df.drop(columns=['ran', 'order'], inplace=True)
df.to_csv('stroop_data.csv', sep = ';', index=False)

# Finish experiment by closing window and quitting
win.close()
quit()