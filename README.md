Lifting From The Deep for Blender 0.1.0
=============

Introduction
---------
Lifting From The Deep for Blender is a Blender addon that implements the functionality from Denis Tome' research paper _Lifting from the Deep: Convolutional 3D Pose Estimation from a Single Image_, which uses machine learning to estimate a 3D pose from a 2D image. More information can be found about this can be found in its [GitHub repository](https://github.com/DenisTome/Lifting-from-the-Deep-release) and [its associated research paper](http://openaccess.thecvf.com/content_cvpr_2017/papers/Tome_Lifting_From_the_CVPR_2017_paper.pdf).

Installation
-------
To install this addon, use `git clone https://github.com/Fragrag/blender_lifting.git` to clone this repository to Blender's addon folder or download a .zip version of this repository and unpack it in Blender's addon folder. You should now have a blender_lifting folder in your addon folder.

Run the `setup_windows.sh` bash script. This will create the Python virtual environment `blender_lifting_venv` and install the required libraries, with exception of the `lifting` module.

The `lifting` module comes included in a folder in the root of this repository. After creating the virtual environment, simply copy or move this folder to the virtual environment's module library. In Windows this is will be in `blender_lifting_venv\Lib\site-packages`

Lifting From The Deep for Blender should now be installed properly.

Usage
--------
Once installed properly, you can activate the addon in Blender in `Edit->Preferences->Add-Ons` as _Animation: Blender Lifting_.

The interface is then accessed when in Object Mode, under Tools.

![Interface](https://github.com/Fragrag/blender_lifting/doc/menu.PNG)

- **Image path:** Location of the image to estimate 3D pose from
- **Scale:** Scale of armature
- **Armature name:** Name of armature
- **Create an armature from a 2D image:** Press here to create the estimated 3D pose
- **ADVANCED: Probability Model:** Location of the probability model used by _lifting_
- **ADVANCED: Saved Sessions:** Location of the sessions used by _lifting_

Requirements
-------
Software:
- Blender 2.80
- Python 3.7.3

Python libraries:
- SciPy
- TensorFlow
- OpenCV Python
- Scikit Image
- Lifting
- and the dependencies of the libraries above

Credits
---------
This addon uses a lightly modified version of Denis Tome's _Lifting from the Deep: Convolutional 3D Pose Estimation from a Single Image_.

Notes
------

Release notes
----------