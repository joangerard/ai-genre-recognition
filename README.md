# Genre Recognition using Neural Networks

AI project to recognize genre of a song/group of songs.

The project uses GTZAN data set to extract MFCC information about each song and then it uses that data to train a Neural
Network composed by one input layer of 25000 neurons (1 for each data extracted from mfcc), one hidden layer
of 100 neurons and one output layer of 10 outputs that corresponds to the 10 genres it classifies: blues, jazz, pop, 
hip-hop, rock, metal, country, disco, reggae, classical. The accuracy of this NN is 48%, better that random selection.

Which is nice about this project is that we developed the neural network from scratch based on Andrew Ng Machine Learning
Course on Coursera, Python Artificial Intelligence Projects for Beginners book by Joshua Eckroth and 
[this amazing blog by Srikar.](https://medium.com/analytics-vidhya/neural-networks-for-digits-recognition-e11d9dff00d5)

It is developed under the DJango framework with Python3.7 offering to the user a graphical interface to test the final 
results of a trained NN. Upload a single song file and a bunch of song files as a .zip.

## Setup
Create virtual environment
```bash
virtualenv -p python3.7 env
```
Activate virtual environment
```bash
source env/bin/activate
```
Install dependencies
```bash
pipenv install --dev
```

## Run
Enter web_app
```bash
cd web_app
```

Run application
```bash
python manage.py runserver 8000
```