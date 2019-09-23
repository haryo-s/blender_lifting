#!/bin/bash

mkdir -p data/saved_sessions
cd data/saved_sessions

echo 'Downloading models...'
curl -O http://visual.cs.ucl.ac.uk/pubs/liftingFromTheDeep/res/init_session.tar.gz
curl -O http://visual.cs.ucl.ac.uk/pubs/liftingFromTheDeep/res/prob_model.tar.gz

echo 'Extracting models...'
tar -xvzf init_session.tar.gz
tar -xvzf prob_model.tar.gz
rm -rf init_session.tar.gz
rm -rf prob_model.tar.gz
cd ../..

# echo 'Checking Python version'
# correct_version="Python 3.7."
# installed_version=$(Python -V)
# echo $python_version
# if [*"$correct_version"* == "$python_version"]; then
# 	echo 

echo 'Creating Python virtual environment'
python -m venv blender_lifting_venv

echo 'Activating virtual environment and installing dependencies'
source blender_lifting_venv/Scripts/activate
pip install tensorflow
pip install opencv-python
pip install scikit-image
pip install scipy

echo 'Done'
