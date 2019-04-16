import matplotlib.pyplot as plt
import librosa
import librosa.feature
import librosa.display

"""
Responsible to handle plots.
"""
class Plotter:

    def save_mfcc(self, song, name):
        path = ''.join(e for e in name if e.isalnum()) + '.png'
        y, _ = librosa.load(song)
        mfcc = librosa.feature.mfcc(y)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(mfcc, x_axis='time', y_axis='mel')
        plt.colorbar()
        plt.title('Spectrogram')
        plt.tight_layout()
        plt.savefig('media/'+path, bbox_inches='tight')
        return path

    def prediction_bar_plot(self, values, name):
        plt.figure()
        name += 'bar.png'
        # print('values: ', values)
        plt.bar(['blues', 'class', 'cntry', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock'], values)
        plt.title('Probability of classification')
        plt.savefig('media/'+name, bbox_inches='tight')
        return name