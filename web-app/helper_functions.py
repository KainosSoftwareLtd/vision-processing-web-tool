# Takes out recurring / independent functions from the PillCnn file to minimise the density of the code
# candidate for refactor - possible to build a design pattern for TF to prevent ^^ ?


# region save the session variables as summary objects for use in tensorboard.
def save_data_as_summary(tf, cost, accuracy, learning_rate, pred, inputLabel, biases, weights):
    tf.scalar_summary("cost_function", cost)
    tf.scalar_summary("accuracy", accuracy)
    tf.scalar_summary("learning_rate", learning_rate)
    tf.histogram_summary("prediction", pred)
    tf.histogram_summary("inputLabel", inputLabel)
    tf.histogram_summary("bias_c1", biases["bc1"])
    tf.histogram_summary("bias_c2", biases["bc2"])
    tf.histogram_summary("bias_f", biases["bd1"])
    tf.histogram_summary("bias_o", biases["out"])
    tf.histogram_summary("weights_c1", weights["wc1"])
    tf.histogram_summary("weights_c2", weights["wc2"])
    tf.histogram_summary("weights_f", weights["wd1"])
    tf.histogram_summary("weights_o", weights["out"])
# endregion


# region save CNN model
def save_model(tf, session):

    # allows saving of the model
    saver = tf.train.Saver()

    # defaults to saving all variables in session
    saver.save(session, 'model/model.ckpt')
# endregion


# region restores a stored model
def restore_model(tf, sess):

    # allows loading of the model
    saver = tf.train.Saver()

    ckpt = tf.train.get_checkpoint_state('model/')
    if ckpt and ckpt.model_checkpoint_path:
        saver.restore(sess, ckpt.model_checkpoint_path)
    else:
        print('no check point found')
# endregion


# region batch normalisation of a tensor - might be useful in future
def batch_norm(x, n_out, phase_train, tf):
    """
    Batch normalization on convolutional maps.
    Ref.: http://stackoverflow.com/questions/33949786/how-could-i-use-batch-normalization-in-tensorflow
    Args:
        x:           Tensor, 4D BHWD input maps
        n_out:       integer, depth of input maps
        phase_train: boolean tf.Varialbe, true indicates training phase
        scope:       string, variable scope
    Return:
        normed:      batch-normalized maps
    """
    with tf.variable_scope('bn'):
        beta = tf.Variable(tf.constant(0.0, shape=[n_out]),
                                     name='beta', trainable=True)
        gamma = tf.Variable(tf.constant(1.0, shape=[n_out]),
                                      name='gamma', trainable=True)
        batch_mean, batch_var = tf.nn.moments(x, [0,1,2], name='moments')
        ema = tf.train.ExponentialMovingAverage(decay=0.5)

        def mean_var_with_update():
            ema_apply_op = ema.apply([batch_mean, batch_var])
            with tf.control_dependencies([ema_apply_op]):
                return tf.identity(batch_mean), tf.identity(batch_var)

        mean, var = tf.cond(phase_train,
                            mean_var_with_update,
                            lambda: (ema.average(batch_mean), ema.average(batch_var)))
        normed = tf.nn.batch_normalization(x, mean, var, beta, gamma, 1e-3)
    return normed
# endregion


# region Read an single instance (image / label pair from a TF Record)
def read_and_decode_single_example(tf, filename, n_classes, n_input):

    # construct a filename queue based on the input file name
    filename_queue = tf.train.string_input_producer([filename],
                                                    num_epochs=None)

    # Read a single record as a serialised string
    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)

    # The serialized example is converted back to actual values - get features
    features = tf.parse_single_example(
        serialized_example,
        features={
            'image/class/label': tf.FixedLenFeature(n_classes, tf.int64),
            'image/encoded': tf.FixedLenFeature([], tf.string)
        })

    # now return the converted data - image and label
    labelf = features['image/class/label']
    imagef = tf.image.decode_jpeg(features['image/encoded'])

    # reshape the image as a vector of pixels (h x w x RGB (3))
    imagef = tf.reshape(imagef, [n_input])

    # Convert from [0, 255] -> [-0.5, 0.5] floats - normalise into a range
    imagef = tf.cast(imagef, tf.float32)
    imagef = tf.cast(imagef, tf.float32) * (1. / 255) - 0.5

    # change type of label into a value (float)
    labelf = tf.cast(labelf, tf.float32)

    return labelf, imagef
# endregion


# region perform the convolution operation - wrapper function
def conv2d(tf, x, W, b, strides=1):
    x = tf.nn.conv2d(x, W, strides=[1, strides, strides, 1], padding='SAME')
    x = tf.nn.bias_add(x, b)
    return tf.nn.relu(x)
# endregion


# region wrapper function for pooling
def maxpool2d(tf, x, k=2):
    return tf.nn.max_pool(x, ksize=[1, k, k, 1], strides=[1, k, k, 1], padding='SAME')
# endregion


# region The CNN full pipeline
def conv_net(tf, x, weights, biases, dropout, height, width, depth, phase):

    # Reshape input picture tensor in a 2d rbg format
    x = tf.reshape(x, shape=[-1, height, width, depth])

    # Convolution Layer
    conv1 = conv2d(tf, x, weights['wc1'], biases['bc1'])

    # Max Pooling (down-sampling)
    conv1 = maxpool2d(tf, conv1, k=2)

    # Convolution Layer
    conv2 = conv2d(tf, conv1, weights['wc2'], biases['bc2'])

    # Max Pooling (down-sampling)
    conv2 = maxpool2d(tf, conv2, k=2)

    # Fully connected layer - reshape to fit the fully connected layer
    fc1 = tf.reshape(conv2, [-1, weights['wd1'].get_shape().as_list()[0]])
    fc1 = tf.add(tf.matmul(fc1, weights['wd1']), biases['bd1'])

    fc1 = tf.nn.relu(fc1)

    # Apply Dropout - prevents overfitting to the training data
    fc1 = tf.nn.dropout(fc1, dropout)

    # Output, class prediction
    out = tf.add(tf.matmul(fc1, weights['out']), biases['out'])

    return out
# endregion


# region example function which shows the built in TF data augmentation options
def augment_image_batch(tf, images_batch, dimension):

    images_batch = tf.map_fn(lambda img: tf.reshape(img, [dimension, dimension, 3]), images_batch)

    # flip left / right at random
    images_batch = tf.map_fn(lambda img: tf.image.random_flip_left_right(img), images_batch)

    images_batch = tf.map_fn(lambda img: tf.random_crop(img, [56,56,3]), images_batch)

    images_batch = tf.map_fn(lambda img: tf.image.random_brightness(img, max_delta=63), images_batch)

    images_batch = tf.map_fn(lambda img: tf.image.random_contrast(img, lower=0.2, upper=1.8), images_batch)

    images_batch = tf.map_fn(lambda img: tf.image.per_image_whitening(img), images_batch)

    # restore to vector shape
    images_batch = tf.map_fn(lambda img: tf.reshape(img, [9408]), images_batch)

    return images_batch
# endregion
