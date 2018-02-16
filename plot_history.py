# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

####

def load_history(result_file):

    class History:
        def __init__(self):
            self.history = {}

    history = History()

    with open(result_file, 'r') as f:

        acc = []
        loss = []
        val_acc = []
        val_loss = []

        f.readline()    # ヘッダをスキップ

        for line in f:
            line = line.rstrip('\n')
            if len(line.strip()) == 0:
                continue

            items = line.split('\t')

            acc.append(float(items[1]))
            loss.append(float(items[2]))
            val_acc.append(float(items[3]))
            val_loss.append(float(items[4]))

        history.history['acc'] = acc
        history.history['loss'] = loss
        history.history['val_acc'] = val_acc
        history.history['val_loss'] = val_loss

    return history

def plot_acc_history(history):
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.xlabel('epoch')
    plt.ylabel('accuracy')
    plt.legend(['acc', 'val_acc'], loc='lower right')
    plt.show()

def plot_loss_history(history):
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.xlabel('epoch')
    plt.ylabel('loss')
    plt.legend(['loss', 'val_loss'], loc='center right')
    plt.show()

####

history_file = 'train_history.txt'
#history_file = 'epoch_history.log'

history = load_history(history_file)
plot_acc_history(history)
plot_loss_history(history)
