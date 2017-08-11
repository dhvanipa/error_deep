# error_deep
An MLP to find syntax errors and suggest fixes.

Do this exactly:

	virutalenv venv

	cd venv/bin/
	
	source activate

	cd ..
	cd ..
	
	pip install keras
	pip instlal h5py
	pip install scikit-image

Setbackend As Theano:

Navigate to the config file for Keras:

Should be here: $HOME/.keras/keras.json
If it's not there, create it.

It should look like this:

{
    "image_data_format": "channels_last",
    "epsilon": 1e-07,
    "floatx": "float32",
    "backend": "theano"
}

The backend parameter should be set to theano.

Requires:

PyPy


