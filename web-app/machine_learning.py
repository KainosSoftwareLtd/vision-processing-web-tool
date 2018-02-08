import os
from keras.models import Sequential, load_model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
import numpy as np
import items
import settings
import helpers

def augment_data(path_to_images):
    datagen = ImageDataGenerator(
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest')

    image_paths = helpers.find_multi('*.jpg', path_to_images)
    for path in image_paths:
        img = load_img(path)  # this is a PIL image
        x = img_to_array(img)  # this is a Numpy array with shape (3, 150, 150)
        # this is a Numpy array with shape (1, 3, 150, 150)
        x = x.reshape((1,) + x.shape)

        # the .flow() command below generates batches of randomly transformed
        # images
        save_dir = os.path.abspath(os.path.join(path, os.pardir))
        prefix = path_to_images.split('/')[-2]
        i = 0
        for batch in datagen.flow(x, batch_size=1, save_to_dir=save_dir,
                                  save_prefix=prefix, save_format='jpeg'):
            i += 1
            if i > 20:
                break  # otherwise the generator would loop indefinitely


def train_model(augment_data_trigger=False):

    batch_size = 16

    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        # shear_range=0.2,
        # zoom_range=0.2,
        # horizontal_flip=True
    )

    train_generator = train_datagen.flow_from_directory(
        settings.data_path + 'training',
        target_size=(settings.image_width, settings.image_height),
        batch_size=batch_size,
        class_mode='binary')  # since we use binary_crossentropy loss, we need binary labels

    label_map = (train_generator.class_indices)
    print (label_map)

    if augment_data_trigger:
        augment_data(settings.data_path)
    dir1 = settings.data_path + 'training/'
    dir2 = settings.data_path + 'validation/'

    if not os.path.exists(dir1):
        os.makedirs(os.path.dirname(dir1))
    if not os.path.exists(dir2):
        os.makedirs(os.path.dirname(dir2))

    model = Sequential()
    model.add(Conv2D(32, (3, 3), input_shape=(
        settings.image_width, settings.image_height, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(32, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Conv2D(64, (3, 3)))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # this converts our 3D feature maps to 1D feature vectors
    model.add(Flatten())
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))

    model.compile(loss='binary_crossentropy',
                  optimizer='rmsprop',
                  metrics=['accuracy'])

    # this is the augmentation configuration we will use for training
    # train_datagen = ImageDataGenerator(
    #     rescale=1. / 255,
    #     shear_range=0.2,
    #     zoom_range=0.2,
    #     horizontal_flip=True)

    # # this is a similar generator, for validation data
    # validation_generator = test_datagen.flow_from_directory(
    #     settings.data_path + 'validation',
    #     target_size=(settings.image_width, settings.image_height),
    #     batch_size=batch_size,
    #     class_mode='binary')

    # validation_data=validation_generator,
    # validation_steps=800 // batch_size)

    model.fit_generator(
        train_generator,
        steps_per_epoch= 320 / batch_size,
        epochs=5)

    model.save('model.h5')


def predict(image_paths, model_path='model.h5'):

    model = load_model(model_path)
    first = True

    for path in image_paths:
        img = load_img(path)
        x = img_to_array(img)
        x.resize(settings.image_width, settings.image_height, 3, refcheck=False)
        x = x.reshape((1,) + x.shape)
        if first:
            all_x = x
            first = False
        else:
            all_x = np.append(all_x, x, axis=0)

    predictions = model.predict_classes(all_x)
    items = {}

    for i, prediction in enumerate(predictions):
        if prediction[0] in items:
            items[prediction[0]].append(image_paths[i])
        else:
            items[prediction[0]] = [image_paths[i]]

    labels = helpers.find_directories(settings.data_path + 'training/')

    items_formatted = []

    for key, value in items.iteritems():
        items_formatted.append({
            'name': labels[key].split('/')[-2],
            'items': value
        })

    return items_formatted
