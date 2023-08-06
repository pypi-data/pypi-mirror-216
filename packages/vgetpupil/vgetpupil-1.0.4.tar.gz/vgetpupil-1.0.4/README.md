# vgetpupil
Python package libray to convert left_video or right_video mp4 files into pim_left/right_pupil_positions.csv.

## Installation requirements
### Python 3.6
This program is only working with the python version 3.6 because the pupil detectors libraries can only be installed with python 3.6.
We prefer to create the virtual environment with python version 3.6 to install our program.

```
conda create -n your-environment-name python=3.6
```
```
conda activate your-environment-name
```

Other way to install python 3.6

You can use `Macports` but this is not reliable.
```
sudo port install python36
```
```
port select --set python  python36
```

You can downgrade your whole python but this can cause problem with other programs.
```
conda install anaconda
``` 
```
conda install python=3.6
```

### Install and upgrade opencv-python
```
pip install opencv-python --upgrade
```

### Install vgetpupil
After setting python version to 3.6 and upgrading opencv-python, please run
```
pip install vgetpupil
```

## Usage guide
### To display help and arguments
```
vgetpupil -h
```

### To check the version
```
vgetpupil --version
```

### Main usage
```
vgetpupil -i inputfile.mp4 -o outputfile.csv
```

#### Example usage
To covert left_video.mp4 into pim_left_pupil_positions.csv
```
vgetpupil -i left_video.mp4 -o pim_left_pupil_positions.csv
```

#### Insert the eye id by force
Normally the name of mp4 video file contains left or right or 0 or 1.
***vgetpupil*** will automatically insert eye_id column value accordingly.
If the file name does not contains signal characters or if we would like to insert the eye id by force, use -e with 0 or 1
```
vgetpupil -i inputfile.mp4 -o outputfile.csv -e (0 or 1)
```

    
