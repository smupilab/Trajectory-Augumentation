# VariationalAutoEncoder.py

##########
# Import #
##########
import tensorflow as tf; tf.compat.v1.disable_eager_execution()
from tensorflow import keras
from tensorflow.keras import layers
from keras import backend as K

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(25)
tf.executing_eagerly()

####################
# Define Functions #
####################
def ComputeLatent( x ):
	mu, sigma = x

	batch = K.shape(mu)[0]
	dim = k.int_shape(mu)[1]
	eps = K.random_normal( shape = ( batch, dim ) )

	return mu + K.exp( sigma / 2 ) * eps

def kl_reconstruction_loss( true, pred ):
	reconstruction_loss = keras.losses.binary_crossentropy( K.flatten(true), K.flatten(pred) ) * img_height * img_width

	kl_loss = 1 + sigma - K.square(mu) - K.exp(sigma)
	kl_loss =  K.sum( kl_loss, x_axis = -1 )
	kl_loss *= -0.5

	return K.mean( reconstruction_loss + kl_loss )

def DisplayImageSequence( x_start, y_start, x_end, y_end, no_of_imgs ):
	x_axis = np.linspace( x_start, x_end, no_of_imgs )
	y_axis = np.linspace( y_start, y_end, no_of_imgs )

	x_axis = x_axis[:, np.newaxis]
	y_axis = y_axis[:, np.newaxis]

	new_points = np.hstack( ( x_axis, y_axis ) )
	new_images = decoder.predict( new_points )
	new_images = new_images.reshape( new_images.shape[0], new_images.shape[1], new_images.shape[2] )

	fig, axes = plt.subplots( ncols = no_of_imgs, sharex = False, sharey = True, figsize = ( 20, 7 ) )

	counter = 0
	for i in range( no_of_imgs ):
		axes[counter].imshow( new_images[i], cmap = 'gray' )
		axes[counter].get_xaxis().set_visible( False )
		axes[counter].get_yaxis().set_visible( False )

		counter += 1
	plt.show()


( x_train, y_train ), ( x_test, y_test ) = keras.datasets.mnist.load_data()

x_train = x_train / 255.
x_test = x_test / 255.

shape = x_train.shape
x_train = x_train.reshape( shape[0], shape[1], shape[2], 1 )

shape = x_test.shape
x_test = x_test.reshape( shape[0], shape[1], shape[2], 1 )

img_height = x_train.shape[1]
img_width = x_train.shape[2]
num_channels = x_train.shape[3]

input_shape = ( img_height, img_width, num_channels )
latent_dim = 2

encoder_input = layers.Input( shape = input_shape )
encoder_conv = layers.Conv2D( 8, 3, strides = 2, padding = 'same', activation = 'relu' )( encoder_input )
encoder_conv = layers.Conv2D( 16, 3, strides = 2, padding = 'same', activation = 'relu' )( encoder_conv )

encoder = layers.Flatten()( encoder_conv )

mu = layers.Dense( latent_dim )( encoder )
sigma = layers.Dense( latent_dim )( encoder )

latent_space = layers.Lambda( ComputeLatent, output_shape = ( latent_dim, ) )( [mu, sigma] )

conv_shape = K.int_shape( encoder_conv )

decoder_input = layers.Input( shape = ( latent_dim, ) )
decoder = layers.Dense( conv_shape[1] * conv_shape[2] * conv_shape[3], activation = 'relu' )( decoder_input )
decoder = layers.Reshape( ( conv_shape[1], conv_shape[2], conv_shape[3] ) )( decoder )
decoder_conv = layers.Conv2DTranspose( 16, 3, strides = 2, padding = 'same', activation = 'relu' )( decoder )
decoder_conv = layers.Conv2DTranspose( 8, 3, strides = 2, padding = 'same', activatioin = 'relu' )( decoder_conv )
decoder_conv = layers.Conv2DTranspose( num_channels, 3, padding = 'same', activation = 'sigmoid' )( decoder_conv )

encoder = keras.models.Model( encoder_input, latent_space )
decoder = keras.models.Model( decoder_input, decoder_conv )
vae = keras.models.Model( encoder_input, decoder( encoder( encoder_input ) ) )

vae.compile( optimizer = 'adam', loss = kl_reconstruction_loss )

history = vae.fit( x = x_train, y = y_train, epochs = 20, batch_size = 32, validation_data = ( x_test, x_test ) )

plt.plot( history.history['loss'] )
plt.plot( history.history['val_loss'] )

encoded = encoder.predict( x_train )

plt.figure( figsize = ( 14, 12 ) )
plt.scatter( encoded[:, 0], encoded[:, 1], s = 2, c = y_train, cmap = 'hsv' )
plt.colorbar()
plt.grid()
plt.show()

DisplayImageSequence( 0, 2, 2, 0, 9 )
DisplayImageSequence( -2, 1, 0, 2, 9 )
DisplayImageSequence( 0, -2, 0, 2, 19 )