import pickle


"""
Responsible to save/retrieve objects to/from a text file as a binary object.
"""
class Text:
    def read(self, file_name):
        file = open(file_name, 'rb')
        data = pickle.load(file)
        file.close()
        return data

    def write(self, file_name, data):
        file = open(file_name, 'wb')
        pickle.dump(data, file)
        file.close()

