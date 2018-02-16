# -*- coding: utf-8 -*-

import os

from keras import optimizers
from keras.callbacks import CSVLogger, ModelCheckpoint
from keras.preprocessing.image import ImageDataGenerator
from common import Common, MyModel

####

train_weights_file = None

batch_size = 128
epochs = 100

train_data_dir='data/train'
validation_data_dir='data/validation'

epoch_weights_file = 'epoch_weights_{epoch:02d}_{loss:.2f}_{acc:.2f}_{val_loss:.2f}_{val_acc:.2f}.h5'
epoch_history_file = 'epoch_history.log'

result_weights_file = 'train_weights.h5'
result_history_file = 'train_history.txt'

####

def remove_file(filename):
    if os.path.isfile(filename):
        os.remove(filename)

def save_history(history, result_file):
    acc = history.history['acc']
    loss = history.history['loss']
    val_acc = history.history['val_acc']
    val_loss = history.history['val_loss']
    nb_epoch = len(acc)

    with open(result_file, "w") as fp:
        fp.write("epoch\tacc\tloss\tval_acc\tval_loss\n")
        for i in range(nb_epoch):
            fp.write("%d\t%f\t%f\t%f\t%f\n" % (i, acc[i], loss[i], val_acc[i], val_loss[i]))

####

train_datagen = ImageDataGenerator(
    rotation_range=180,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=(0.9, 1.1),
    rescale=1.0/255.0
    )

train_generator = train_datagen.flow_from_directory(
    directory=train_data_dir,
    target_size=(Common.IMG_HEIGHT, Common.IMG_WIDTH),
    classes=Common.CLASSES,
    class_mode='categorical',
    batch_size=batch_size,
    shuffle=True
    )

validation_datagen = ImageDataGenerator(
    rotation_range=180,
    width_shift_range=0.1,
    height_shift_range=0.1,
    zoom_range=(0.9, 1.1),
    rescale=1.0/255.0
    )

validation_generator = validation_datagen.flow_from_directory(
    directory=validation_data_dir,
    target_size=(Common.IMG_HEIGHT, Common.IMG_WIDTH),
    classes=Common.CLASSES,
    class_mode='categorical',
    batch_size=batch_size,
    shuffle=True
    )

model = MyModel.get_model()
model.compile(
    loss='categorical_crossentropy',
    optimizer=optimizers.Adagrad(),
    metrics=['accuracy']
    )
model.summary()

if train_weights_file is not None:
    model.load_weights(train_weights_file)
    print('load_weights:', train_weights_file)

checkpoint = ModelCheckpoint(
    epoch_weights_file,
    save_weights_only=True,
    verbose=1
    )

remove_file(epoch_history_file)
logger = CSVLogger(filename=epoch_history_file, separator='\t', append=True)

history = model.fit_generator(
    generator=train_generator,
    steps_per_epoch=batch_size,
    epochs=epochs,
    validation_data=validation_generator,
    validation_steps=batch_size,
    verbose=1,
    callbacks=[checkpoint, logger]
    )

model.save_weights(result_weights_file)
save_history(history, result_history_file)
