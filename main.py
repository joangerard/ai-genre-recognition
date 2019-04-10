import librosa
import librosa.feature
import librosa.display
import glob
import numpy as np
import matplotlib.pyplot as plt
from text import Text
from neural_network import NeuralNetwork

def song_converter(index):
    songs = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    return songs[index]


def display_mfcc(song):
    y, _ = librosa.load(song)
    mfcc = librosa.feature.mfcc(y)

    plt.figure(figsize=(10, 4))
    librosa.display.specshow(mfcc, x_axis='time', y_axis='mel')
    plt.colorbar()
    plt.title(song)
    plt.tight_layout()
    plt.show()


def extract_features_song(song):
    y, _ = librosa.load(song)

    mfcc = librosa.feature.mfcc(y)
    mfcc /= np.amax(np.absolute(mfcc))

    return np.ndarray.flatten(mfcc)[:25000]


def generate_features_and_labels():
    all_features = []
    all_labels = []

    genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    for genre in genres:
        sound_files = glob.glob('genres/' + genre + '/*.au')
        print('Processing %d songs in %s genre... ' % (len(sound_files), genre))
        for song in sound_files:
            features = extract_features_song(song)
            all_features.append(features)
            all_labels.append(genre)

    label_uniq_ids, label_row_ids = np.unique(all_labels, return_inverse=True)
    label_row_ids = label_row_ids.astype(np.int32, copy=False)
    onehot_labels = to_categorical(label_row_ids, len(label_uniq_ids))

    return np.stack(all_features), onehot_labels


def cross_validation_data(all_data):
    training_split = 0.8

    np.random.shuffle(all_data)
    splitidx = int(len(all_data) * training_split)
    train, test = all_data[:splitidx, :], all_data[splitidx:, :]

    train_input = train[:, :-10]
    train_labels = train[:, -10:]

    test_input = test[:, :-10]
    test_labels = test[:, -10:]

    return train_input, train_labels, test_input, test_labels


def train_nn(train_input, train_output, test_input, test_output):
    model = Sequential([
        Dense(2000, input_dim=np.shape(train_input)[1]),
        Activation('relu'),
        Dense(10),
        Activation('softmax'),
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    print(model.summary())

    model.fit(train_input, train_output, epochs=10, batch_size=32, validation_split=0.2)

    loss, acc = model.evaluate(test_input, test_output, batch_size=32)

    print('Done')
    print("Loss: %.4f, accuracy: %.4f" % (loss, acc))


if __name__ == '__main__':
    file_name = 'test.txt'
    text = Text()

    nn = NeuralNetwork()

    # features, labels = generate_features_and_labels()
    # all_data = np.column_stack((features, labels))
    # text.write(file_name, all_data)
    all_data = text.read(file_name)
    train_input, train_output, test_input, test_output = cross_validation_data(all_data)

    # print(nn.accuracy(test_input, test_output))
    nn.fit_with_different_lambdas(train_input, train_output)
    # train_nn(train_input, train_output, test_input, test_output)


