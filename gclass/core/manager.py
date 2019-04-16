import librosa
import librosa.feature
import librosa.display
import glob
import numpy as np
import matplotlib.pyplot as plt
from .text import Text
from .neural_network import NeuralNetwork
# from keras.utils.np_utils import to_categorical

"""
Class manager that is in charge of manage song features extraction
like mfcc, handle data, standarize it, etc.
"""
class Manager:

    def __init__(self):
        self.nn = NeuralNetwork()

    def song_converter(self, index):
        songs = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
        return songs[index]

    def display_mfcc(self, song):
        y, _ = librosa.load(song)
        mfcc = librosa.feature.mfcc(y)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mfcc, x_axis='time', y_axis='mel')
        plt.colorbar()
        plt.title('Spectogram')
        plt.tight_layout()
        plt.show()

    def fit(self,training_inputs, training_outputs):
        self.nn.fit(training_inputs,training_outputs)

    def extract_features_song(self, song):
        y, _ = librosa.load(song)

        mfcc = librosa.feature.mfcc(y)
        mfcc /= np.amax(np.absolute(mfcc))

        return np.ndarray.flatten(mfcc)[:25000]


    def generate_features_and_labels(self):
        all_features = []
        all_labels = []

        genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
        for genre in genres:
            sound_files = glob.glob('genres/'+genre+'/*.au')
            print('Processing %d songs in %s genre... ' % (len(sound_files), genre))
            for song in sound_files:
                features = self.extract_features_song(song)
                all_features.append(features)
                all_labels.append(genre)

        label_uniq_ids, label_row_ids = np.unique(all_labels, return_inverse=True)
        label_row_ids = label_row_ids.astype(np.int32, copy=False)
        onehot_labels = to_categorical(label_row_ids, len(label_uniq_ids))

        return np.stack(all_features), onehot_labels

    """
    Split data for cross-validation.
    """
    def cross_validation_data(self, all_data):
        training_split = 0.8

        np.random.shuffle(all_data)
        splitidx = int(len(all_data) * training_split)
        train, test = all_data[:splitidx, :], all_data[splitidx:, :]

        train_input = train[:, :-10]
        train_labels = train[:, -10:]

        test_input = test[:, :-10]
        test_labels = test[:, -10:]


        return train_input, train_labels, test_input, test_labels

    """
    Predict data. 
    """
    def predict(self, data):
        features = self.extract_features_song(data)
        prediction, values = self.nn.predict_custom(features)
        return self.song_converter(prediction), values

