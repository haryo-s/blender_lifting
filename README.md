blender_lifting 0.1.0
=============

DEPRECATION NOTICE
---------
API updates to Blender and Tensorflow have also rendered this project incompatible without significant tinkering to blender_project and its main dependency Lifting-from-the-Deep.

I do not have the time anymore to actively develop and support this project, but feel free to fork this project, poke around its inner workings and make your own adjustments. Pull requests are always welcome as well!

Kind regards,
Haryo

Introduction
---------
blender_lifting is a Blender addon that implements the functionality from Denis Tome' research paper _Lifting from the Deep: Convolutional 3D Pose Estimation from a Single Image_, which uses machine learning to estimate a 3D pose from a 2D image. More information can be found about this can be found in its [GitHub repository](https://github.com/DenisTome/Lifting-from-the-Deep-release) and [its associated research paper](http://openaccess.thecvf.com/content_cvpr_2017/papers/Tome_Lifting_From_the_CVPR_2017_paper.pdf).

![Example](https://github.com/Fragrag/blender_lifting/blob/master/doc/example.png)

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

![Interface](https://github.com/Fragrag/blender_lifting/blob/master/doc/menu.PNG)

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

FAQ/Known issues
------
**Armature is not normalised**
The created armature is not normalised and will not be facing in a particular default direction. As a result the base bone might be positioned oddly as well.

**Non standard armature**
The created armature does not conform to any standard rigs or skeletons that I am aware of. Consider the created armature as a starting point rather than a production ready asset. 

**My armature came out rather weird/inaccurate**
blender_lifting relies on a machine learning model to estimate a 3D pose from a 2D image. As such it might return an anatomically incorrect armature. The estimation is also not 100% accurate, and is more of an approximation.

**It failed!/It crashed!**
blender_lifting is still in its early days of development and can be very buggy. Implementing a robust error catching is part of the future roadplan. In the meantime, make sure your image contains a single person with most, if not all, limbs clearly visible. 

Also make sure that your Python 3.7.3 installation is added to your PATH variables as `python`.

**Why do I need Python installed on my system when Blender has its Python installation**
While developing, Blender's built-in Python exhibited issues when running lifting's dependencies such as OpenCV and TensorFlow. A workaround was created by having the add-on launch a system-level Python process to analyse the image rather than the built-in Python.

Credits
---------
This addon uses a lightly modified version of Denis Tome's _Lifting from the Deep: Convolutional 3D Pose Estimation from a Single Image_.

Notes
------

Release notes
----------
