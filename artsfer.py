import os
import tensorflow as tf
from PIL import Image
from flask import url_for
import numpy as np

MAX_DIM = 128
STYLE_WEIGHT = 1e-2
CONTENT_WEIGHT = 10e4
TOTAL_VARIATION_WEIGHT = 30


def load_img(img):
    tensor = tf.constant(img)
    tensor = tf.cast(tensor, dtype=tf.float32)
    shape = tf.cast(tf.shape(tensor)[:-1], tf.float32)
    long_dim = max(shape)
    scale = MAX_DIM / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)
    tensor = tf.image.resize(tensor, new_shape)
    tensor = tensor[tf.newaxis, :]

    return tensor / 255


def vgg_layers(layer_names):
    """ Creates a vgg model that returns a list of intermediate output values."""
    # Load our model. Load pretrained VGG, trained on imagenet data
    vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
    vgg.trainable = False

    outputs = [vgg.get_layer(name).output for name in layer_names]

    model = tf.keras.Model([vgg.input], outputs)

    return model


def gram_matrix(input_tensor):
    result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
    input_shape = tf.shape(input_tensor)
    num_locations = tf.cast(input_shape[1]*input_shape[2], tf.float32)
    return result/(num_locations)


class StyleContentModel(tf.keras.models.Model):
    def __init__(self, style_layers, content_layers):
        super(StyleContentModel, self).__init__()
        self.vgg = vgg_layers(style_layers + content_layers)
        self.style_layers = style_layers
        self.content_layers = content_layers
        self.num_style_layers = len(style_layers)
        self.vgg.trainable = False

    def call(self, inputs):
        "Expects float input in [0,1]"
        inputs = inputs*255.0
        preprocessed_input = tf.keras.applications.vgg19.preprocess_input(
            inputs)
        outputs = self.vgg(preprocessed_input)
        style_outputs, content_outputs = (outputs[:self.num_style_layers],
                                          outputs[self.num_style_layers:])

        style_outputs = [gram_matrix(style_output)
                         for style_output in style_outputs]

        content_dict = {content_name: value
                        for content_name, value
                        in zip(self.content_layers, content_outputs)}

        style_dict = {style_name: value
                      for style_name, value
                      in zip(self.style_layers, style_outputs)}

        return {'content': content_dict, 'style': style_dict}


def clip_0_1(image):
    return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)


def high_pass_x_y(image):
    x_var = image[:, :, 1:, :] - image[:, :, :-1, :]
    y_var = image[:, 1:, :, :] - image[:, :-1, :, :]

    return x_var, y_var


def total_variation_loss(image):
    x_deltas, y_deltas = high_pass_x_y(image)
    return tf.reduce_sum(tf.abs(x_deltas)) + tf.reduce_sum(tf.abs(y_deltas))


'''def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)

    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]

    return Image.fromarray(tensor, 'RGB')'''


def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)

    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]

    return Image.fromarray(tensor)


def artsfer(contentImage, styleImage, epochs, emit, output_folder):
    contentImage = load_img(contentImage)
    styleImage = load_img(styleImage)

    content_layers = ['block5_conv2']

    style_layers = ['block1_conv1',
                    'block2_conv1',
                    'block3_conv1',
                    'block4_conv1',
                    'block5_conv1']

    num_content_layers = len(content_layers)
    num_style_layers = len(style_layers)

    extractor = StyleContentModel(style_layers, content_layers)
    style_targets = extractor(styleImage)['style']
    content_targets = extractor(contentImage)['content']

    image = tf.Variable(contentImage)
    '''Image.fromarray(image.numpy().astype(np.uint8)[0]).save(
        'C://Users//hp//Desktop//variable.jpg') funziona '''
    opt = tf.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)

    def style_content_loss(outputs):
        style_outputs = outputs['style']
        content_outputs = outputs['content']

        style_loss = tf.add_n([tf.reduce_mean((style_outputs[name]-style_targets[name])**2)
                               for name in style_outputs.keys()])

        style_loss *= STYLE_WEIGHT / num_style_layers

        content_loss = tf.add_n([tf.reduce_mean((content_outputs[name]-content_targets[name])**2)
                                 for name in content_outputs.keys()])

        content_loss *= CONTENT_WEIGHT / num_content_layers

        loss = style_loss + content_loss
        return loss

    @tf.function()
    def train_step(image):
        with tf.GradientTape() as tape:
            outputs = extractor(image)
            loss = style_content_loss(outputs)
            loss += TOTAL_VARIATION_WEIGHT*tf.image.total_variation(image)

        grad = tape.gradient(loss, image)
        opt.apply_gradients([(grad, image)])
        image.assign(clip_0_1(image))

    import time

    steps_per_epoch = 100
    step = 0

    for epoch in range(epochs):
        epoch_start = time.time()
        print('Epoch: %d/%d' % (epoch+1, epochs))

        for m in range(steps_per_epoch):
            step += 1
            train_step(image)

        print("Epoch time: {:.1f}".format(time.time() - epoch_start))
        Image.fromarray((image * 255).numpy().astype(np.uint8)[0]).save(
            os.path.join(output_folder, '{}.jpg'.format(epoch+1)))

        emit(
            'epoch', {'data': url_for('static', filename='results/{}.jpg'.format(epoch + 1))})
