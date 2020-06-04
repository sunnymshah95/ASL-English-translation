import tensorflow as tf 
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt 
import os
from tensorflow.keras.layers import Activation, Conv3D, MaxPooling3D, Flatten, Dense
from tensorflow.keras.layers import Dropout, Input, BatchNormalization
from sklearn.metrics import confusion_matrix, accuracy_score
from tensorflow.keras import optimizers, losses
from tensorflow.keras import models

class ConvNet:
    def __init__(self, shape, num_classes, model_num):
        self.img_shape = shape
        self.num_classes = num_classes

        if model_num == 1:
            model = self.get_model1()

        elif model_num == 2:
            model = self.get_model2()

        elif model_num == 3:
            model = self.get_model3()


        self.model = model


    def summary(self):
        self.model.summary()

    def get_model(self):
        return self.model

    def get_model1(self):
        # "regular"
        model = models.Sequential()

        model.add(Conv3D(16, kernel_size = (5, 5, 5), input_shape = self.img_shape))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling3D(pool_size = (5, 5, 5)))

        model.add(Conv3D(32, kernel_size = (5, 5, 5)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling3D(pool_size = (5, 5, 5)))

        model.add(Conv3D(32, kernel_size = (5, 5, 5)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling3D(pool_size = (5, 5, 5)))

        model.add(Flatten())
        model.add(Dense(512, activation = 'sigmoid'))
        model.add(Dense(self.num_classes, activation = 'softmax'))

        return model



    def get_model2(self):
        # deeper
        model = models.Sequential()

        model.add(Conv3D(16, kernel_size = (5, 5, 5), input_shape = self.shape))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling3D(pool_size = (5, 5, 5)))

        model.add(Conv3D(16, kernel_size = (5, 5, 5)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling3D(pool_size = (5, 5, 5)))

        model.add(Conv3D(32, kernel_size = (5, 5, 5)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling3D(pool_size = (5, 5, 5)))

        model.add(Conv3D(32, kernel_size = (5, 5, 5)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling3D(pool_size = (5, 5, 5)))

        model.add(Conv3D(48, kernel_size = (5, 5, 5)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling3D(pool_size = (5, 5, 5)))

        model.add(Conv3D(64, kernel_size = (5, 5, 5)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling3D(pool_size = (5, 5, 5)))

        model.add(Flatten())
        model.add(Dense(1024, activation = 'sigmoid'))
        model.add(Dense(512, activation = 'sigmoid'))
        model.add(Dense(self.num_classes, activation = 'softmax'))

        return model



    def get_model3(self):
        # wider
        model = models.Sequential()

        model.add(Conv3D(16, kernel_size = (5, 5, 5), input_shape = self.shape))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling3D(pool_size = (5, 5, 5)))

        model.add(Conv3D(128, kernel_size = (5, 5, 5)))
        model.add(Activation('relu'))
        model.add(BatchNormalization())
        model.add(MaxPooling3D(pool_size = (5, 5, 5)))

        model.add(Flatten())
        model.add(Dense(512, activation = 'sigmoid'))
        model.add(Dense(self.num_classes, activation = 'softmax'))

        return model



    def train(self, train_paths, test_paths, num_epochs = 20, batch = 4, lr = 0.0001):
        xtr_path, ytr_path = train_paths
        xts_path, yts_path = test_paths

        x_train = np.load(xtr_path)
        y_train = np.load(ytr_path)

        x_test = np.load(xts_path)
        y_test = np.load(yts_path)

        opt = optimizers.Adam(learning_rate = lr, beta_1 = 0.95, beta_2 = 0.98)
        # opt = optimizers.SGD(learning_rate = 0.0001)
        self.model.compile(optimizer = opt, loss = 'categorical_crossentropy', metrics = ['accuracy'])
        self.history = self.model.fit(x_train, y_train.T, epochs = num_epochs, batch_size = batch)
        
        # test_eval = self.model.evaluate(x_test, y_test.T)
        # print("Test evaluation:\nLoss = {}\nAccuracy = {}".format(test_eval[0], test_eval[1]))

        self.plot_accuracy()
        self.plot_loss()

        return train_eval



    def plot_accuracy(self, save = True):
        hist = self.history 

        # plot the accuracy over epochs
        plt.plot(hist.history['accuracy'])
        plt.title('Model accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        
        if not save:
            plt.show()

        else:
            plt.savefig('accuracy.png')

    def plot_loss(self, save = True):
        hist = self.history 

        # plot the loss over epochs
        plt.plot(hist.history['loss'])
        plt.title('Model loss')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        
        if not save:
            plt.show()

        else:
            plt.savefig('loss.png')

    def vary_AdamLR(self, xtr_path, ytr_path, xts_path, yts_path):
        x_train, y_train = np.load(xtr_path), np.load(ytr_path)
        x_test, y_test = np.load(xts_path, yts_path)

        model = self.get_model()

        rates = np.linspace(1.e-6, 1.e-2, 8)
        accuracies = []
        losses = []

        for r in rates:
            opt = optimizers.Adam(learning_rate = r)
            model.compile(optimizer = opt, loss = 'categorical_crossentropy', metrics = ['accuracy'])
            history = model.fit(x_train, y_train.T, epochs = 6, batch_size = 8)

            train_eval = model.evaluate(x_train, y_train.T)
            accuracies.append(history.hist['accuracy'])
            losses.append(history.hist['loss'])

        plot('Adam', rates, losses, accuracies)



    def vary_SGDLR(self, xtr_path, ytr_path, xts_path, yts_path):
        x_train, y_train = np.load(xtr_path), np.load(ytr_path)
        x_test, y_test = np.load(xts_path, yts_path)

        model = self.get_model()

        rates = np.linspace(1.e-6, 1.e-2, 8)
        accuracies = []

        for r in rates:
            opt = optimizers.SGD(learning_rate = r)
            model.compile(optimizer = opt, loss = 'categorical_crossentropy', metrics = ['accuracy'])
            history = model.fit(x_train, y_train.T, epochs = 6, batch_size = 8)

            train_eval = model.evaluate(x_train, y_train.T)
            accuracies.append(history.hist['accuracy'])

        plot('SGD', rates, losses, accuracies)





def plot(opt, rates, losses, accuracies):
    for i in range(len(rates)):
        plt.plot(rates[i], accuracies[i], label = f'$r$ = {rates[i]:.3f}')

    plt.xlabel('Learning rates')
    plt.ylabel('Accuracy')
    plt.legend()
    plt.title('Accuracy versus Learning Rate')
    file_name = 'accuracy_' + opt + '.png'
    plt.savefig(file_name)

    for i in range(len(rates)):
        plt.plot(rates[i], losses[i], label = f'$r$ = {rates[i]:.3f}')

    plt.xlabel('Learning rates')
    plt.ylabel('Loss')
    plt.legend()
    plt.title('Loss versus Learning Rate')
    file_name = 'loss_' + opt + '.png'
    plt.savefig(file_name)
