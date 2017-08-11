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

To run col_finder.py:

Requires:
  - javac_parser
  - py4j

You can pip install both

The path to the directory where all the java corpus files are must be set.

The variables sfid and meid number for cutting and getting the id's must be adjusted to your path.

The script will output a csv called java_fixes_col.csv

Checking syntax:
	python check_javac_syntax.py SOURCE_FILE_NAME
	python check_eclipse_syntax.py SOURCE_FILE_NAME


