import numpy as np

class NeuralNetwork:

    def __init__(self):
        self.dimi_1 = 25001
        self.dimo_1 = 100

        self.dimi_2 = 101
        self.dimo_2 = 10
        self.epsilon_theta = 0.12
        self.theta1 = []
        self.theta2 = []

    def fit(self, training_inputs, training_outputs):


    def costFunction(self, training_inputs, training_outputs, theta, lamb, hidden_layer_size, input_layer_size, num_labels):
        theta1 = np.reshape(theta[:(hidden_layer_size * input_layer_size +1)], (hidden_layer_size, input_layer_size + 1))
        theta2 = np.reshape(theta[(hidden_layer_size * input_layer_size +1):], (num_labels, hidden_layer_size + 1))

        m = len(training_outputs)
        ones = np.ones((m, 1))

        a1 = np.hstack((ones, training_inputs))
        a2 = self.sigmoid_function(np.matmul(a1, theta1.T)) # 800, 100
        a2 = np.hstack((ones, a2))
        h = self.sigmoid_function((np.matmul(a2, theta2.T)))

        temp1 = np.multiply(training_outputs, np.log(h))
        temp2 = np.multiply(1-training_outputs, np.log(1-h))
        temp3 = np.sum(temp1+temp2)

        sum1 = np.sum(np.sum(np.power(theta1[:,1:], 2), axis = 1))
        sum2 = np.sum(np.sum(np.power(theta2[:,1:], 2), axis = 1))

        return np.sum(-(1/m)*temp3) + (sum1 + sum2) * lamb/(2 * m)


    def forward_propagation(self, a_1, theta1, theta2):
        # forward propagation
        a_1 = np.insert(a_1, 0, 1)
        z_1 = np.matmul(theta1, a_1) # 100 x 1
        a_2 = self.sigmoid_function(z_1)

        a_2 = np.insert(a_2, 0, 1) # 101 x 1
        z_2 = np.matmul(theta2, a_2) # 10 x 1
        h = self.sigmoid_function(z_2)


    def sigmoid_function(self, z):
        return 1/(1 + np.exp(-z))

    def random_init_theta(self, dimi, dimo, epsilon):
        return  np.random.rand(dimo, dimi)*2*epsilon - epsilon
