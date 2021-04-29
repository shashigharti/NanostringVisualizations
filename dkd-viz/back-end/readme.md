## Create a conda environment
conda create -n dkd-viz python=3.6

## Install dependencies
pip install -r requirements.txt

## Start flask

### Activate environment, set variables and run
conda activate dkd-viz
export FLASK_APP=back-end
flask run