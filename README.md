A simple worm-like game, where the player attempts to collide their sprite with a reward sprite. See chaser.py imports for dependencies. (Designed as a training tool for Machine Learning with TensorFlow and Keras.)

uhoh, this may need python2, I've switched to python3, so I'll update this to 3 soon.

gen.py
- creates a neural network model and saves it in the current working directory

gendata.py
- creates big datasets of random scenarios in the game. (specify how many images you want to generate at the bottom of the code) I don't think this is useful in the workflow for train.py currently. You problably don't need to run this.

train.py
- can generate a random dataset of n value, and then trains the nerual network model on that dataset.
(dataset is a numpy array of a greyscale image from 0 to 255 as the pixel values. The numpy array also has a simple array [x,x,x,x]. x will be between 0 and 1. If the first x is bigger than the rest, then the correct direction the player needs to go, given the random dataset image we're on, is UP. If the second x is bigger than the rest, then the player should go RIGHT. If the third x is bigger than the rest, then the player should go DOWN. if the fourth x is bigger than the rest, the player should go LEFT.)


chaser.py
- plays the game. 
- [space] - toggle's Neural Network Mode on/off. You will need a model in the current working directory
- [arrowkeys] - when in player control mode, moves player
