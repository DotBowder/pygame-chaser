A simple worm-like game, where the player attempts to collide their sprite with a reward sprite. See chaser.py imports for dependencies. (Designed as a training tool for Machine Learning with TensorFlow and Keras.)


gen.py
- creates a neural network model and saves it in the current working directory

gendata.py
- creates big datasets of random scenarios in the game. (specify how many images you want to generate at the bottom of the code) I don't think this is useful in the workflow for train.py currently. You problably don't need to run this.

train.py
- trains the nerual network model in the current working directory

chaser.py
- plays the game. 
- [space] - toggle's Neural Network Mode on/off. You will need a model in the current working directory
