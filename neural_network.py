import numpy as np
import scipy.optimize as opt
from text import Text


class NeuralNetwork:

    def __init__(self):
        self.dimi_1 = 25000
        self.dimo_1 = 100

        self.dimi_2 = 100
        self.dimo_2 = 10
        self.epsilon_theta = 0.12
        self.theta1 = []
        self.theta2 = []
        self.lamb = 1.2
        self.text = Text()

    def predict_custom(self, data):
        theta_opt = self.text.read('theta_opt_l12.txt')
        theta1, theta2 = self.extract_thetas(theta_opt, self.dimi_1, self.dimo_1, self.dimo_2)

        ones = np.ones(1)
        a1 = np.hstack((ones, data))
        z2 = np.matmul(a1, theta1.T)
        a2 = self.sigmoid_function(z2)
        a2 = np.hstack((ones, a2))
        z3 = np.matmul(a2, theta2.T)
        a3 = self.sigmoid_function(z3)

        return np.argmax(a3)

    def accuracy(self, test_input, test_output):
        theta_opt = self.text.read('theta_opt_l12.txt')
        theta1, theta2 = self.extract_thetas(theta_opt, self.dimi_1, self.dimo_1, self.dimo_2)
        accuracies = 0

        m = len(test_input)

        for i in range(0, m):
            ones = np.ones(1)

            a1 = np.hstack((ones, test_input[i]))
            z2 = np.matmul(a1, theta1.T)
            a2 = self.sigmoid_function(z2)  # 800, 100
            a2 = np.hstack((ones, a2))
            z3 = np.matmul(a2, theta2.T)
            a3 = self.sigmoid_function(z3)

            if test_output[i][np.argmax(a3)] == 1:
                accuracies += 1

        return accuracies / m

    def fit(self, training_inputs, training_outputs):
        self.theta1 = self.random_init_theta(self.dimi_1 + 1, self.dimo_1, self.epsilon_theta)  # 100 x 25001
        self.theta2 = self.random_init_theta(self.dimi_2 + 1, self.dimo_2, self.epsilon_theta)  # 10 x 101

        theta = np.concatenate((self.theta1, self.theta2), axis=None)

        theta_opt = opt.fmin_cg(f=self.cost_function, x0=theta, fprime=self.gradient_function,
                                args=(
                                    training_inputs, training_outputs, self.lamb, self.dimo_1, self.dimi_1,
                                    self.dimo_2),
                                maxiter=50)

        self.text.write('theta_opt_l12.txt', theta_opt)

        # self.gradientCheck(theta, backprop_params, self.dimi_1, self.dimo_1, self.dimo_2, self.lamb, training_inputs, training_outputs)
        # print("Cost Function", cf)

    # def  predict(self, theta_opt):

    def gradient_check(self, theta, backprop_params, input_layer_size, hidden_layer_size, num_labels, lamb,
                       training_inputs, training_outputs):
        epsilon = 0.0001
        n_elems = len(theta)

        for i in range(10):
            x = int(np.random.rand() * n_elems)
            epsilon_vec = np.zeros((n_elems, 1))
            epsilon_vec[x] = epsilon

            cost_high = self.cost_function(theta + epsilon_vec.flatten(), training_inputs, training_outputs, lamb,
                                           hidden_layer_size, input_layer_size, num_labels)
            cost_low = self.cost_function(theta - epsilon_vec.flatten(), training_inputs, training_outputs, lamb,
                                          hidden_layer_size, input_layer_size, num_labels)

            aprox_grad = (cost_high - cost_low) / float(2 * epsilon)
            print("Element: {0}. Numerical Gradient = {1:.9f}. BackProp Gradient = {2:.9f}.".format(x, aprox_grad,
                                                                                                    backprop_params[x]))

    def extract_thetas(self, theta, input_layer_size, hidden_layer_size, num_labels):
        theta1 = np.reshape(theta[:(hidden_layer_size * (input_layer_size + 1))],
                            (hidden_layer_size, input_layer_size + 1))
        theta2 = np.reshape(theta[(hidden_layer_size * (input_layer_size + 1)):], (num_labels, hidden_layer_size + 1))

        return theta1, theta2

    def gradient_function(self, theta, training_inputs, training_outputs, lamb, hidden_layer_size, input_layer_size,
                          num_labels):
        theta1, theta2 = self.extract_thetas(theta, input_layer_size, hidden_layer_size, num_labels)

        delta1 = np.zeros(theta1.shape)
        delta2 = np.zeros(theta2.shape)

        m = len(training_outputs)

        for i in range(training_inputs.shape[0]):
            ones = np.ones(1)

            a1 = np.hstack((ones, training_inputs[i]))
            z2 = np.matmul(a1, theta1.T)
            a2 = self.sigmoid_function(z2)  # 800, 100
            a2 = np.hstack((ones, a2))
            z3 = np.matmul(a2, theta2.T)
            a3 = self.sigmoid_function(z3)

            d3 = a3 - training_outputs[i]
            z2 = np.hstack((ones, z2))
            d2 = np.multiply(np.matmul(theta2.T, d3), self.sigmoid_derivate_function(z2).T)

            delta1 = delta1 + d2[1:, np.newaxis] @ a1[np.newaxis, :]
            delta2 = delta2 + d3[:, np.newaxis] @ a2[np.newaxis, :]

        delta1[:, 1:] = 1 / m * delta1[:, 1:] + lamb * theta1[:, 1:] / m  # j != 0
        delta1[:, 0] = 1 / m * delta1[:, 0] / m  # j == 0

        delta2[:, 1:] = 1 / m * delta2[:, 1:] + lamb * theta2[:, 1:] / m
        delta2[:, 0] = 1 / m * delta2[:, 0] / m
        print('Gradient function finishing... ')
        return np.hstack((delta1.ravel(), delta2.ravel()))

    def cost_function(self, theta, training_inputs, training_outputs, lamb, hidden_layer_size, input_layer_size,
                      num_labels):
        theta1 = np.reshape(theta[:(hidden_layer_size * (input_layer_size + 1))],
                            (hidden_layer_size, input_layer_size + 1))
        theta2 = np.reshape(theta[(hidden_layer_size * (input_layer_size + 1)):], (num_labels, hidden_layer_size + 1))

        m = len(training_outputs)
        ones = np.ones((m, 1))

        a1 = np.hstack((ones, training_inputs))
        a2 = self.sigmoid_function(np.matmul(a1, theta1.T))  # 800, 100
        a2 = np.hstack((ones, a2))
        h = self.sigmoid_function((np.matmul(a2, theta2.T)))

        temp1 = np.multiply(training_outputs, np.log(h))
        temp2 = np.multiply(1 - training_outputs, np.log(1 - h))
        temp3 = np.sum(temp1 + temp2)

        sum1 = np.sum(np.sum(np.power(theta1[:, 1:], 2), axis=1))
        sum2 = np.sum(np.sum(np.power(theta2[:, 1:], 2), axis=1))
        val = np.sum(-(1 / m) * temp3) + (sum1 + sum2) * lamb / (2 * m)
        print('Cost function: ', val)
        return val

    def forward_propagation(self, a_1, theta1, theta2):
        # forward propagation
        a_1 = np.insert(a_1, 0, 1)
        z_1 = np.matmul(theta1, a_1)  # 100 x 1
        a_2 = self.sigmoid_function(z_1)

        a_2 = np.insert(a_2, 0, 1)  # 101 x 1
        z_2 = np.matmul(theta2, a_2)  # 10 x 1
        h = self.sigmoid_function(z_2)

    def sigmoid_function(self, z):
        return 1 / (1 + np.exp(-z))

    def sigmoid_derivate_function(self, z):
        return np.multiply(self.sigmoid_function(z), 1 - self.sigmoid_function(z))

    def random_init_theta(self, dimi, dimo, epsilon):
        return np.random.rand(dimo, dimi) * 2 * epsilon - epsilon
