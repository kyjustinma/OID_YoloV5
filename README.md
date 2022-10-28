# Python Project Template

## About The Project

This is a template that uses both Conda and Pre-commit, to ensure that everyone in the team has the same environment running on their device.

Pre-commit is used to ensure that certain commit standards are enforced.

## Built With

[![python][python3.8.13-shield]][python3.8.13-url]
[![conda][conda-forge-shield]][conda-forge-url]

This template is primary focused on Python 3.8.13 with Anaconda (using Conda-forge)

# Getting Started

## Prerequisites

- Python 3.8.13
- Anaconda

## Installation
1. install the pip requirements for this repo```pip install -r requirements.txt```
## Key points
1. .yaml in yolov5/data store information regarding what will be trained

```
path: ../yolov5/datasets/coco2017 # dataset root dir
train: train2017_original.txt # text files containing path to all images
val: val2017_original.txt # text file for all validation images
```

.txt format 
```
./images/train2017/000000109622.jpg
```
the label should be stored in the equivalent
```
./labels/train2017/000000109622.txt
```

## Flow for CoCo Dataset
1. Run the following python script in the yolov5 directory to train the regular CoCo dataset (coco2017.yaml uses original classes and the original .txt)
``` 
python train.py --weights yolov5s.pt --data coco2017.yaml --img 640
```


## Flow for adding items to COCO dataset
1. Download any data sets from CVAT server by `export task dataset > export as YOLO 1.1` 
2. Move new exported datasets to coco-additions (expected folder structure)
   ```
   obj_train_data
   obj.data
   obj.names
   train.txt
   ```
3. The `obj_train_data` stores the .jpg and the .txt file (however the label is according to the CVAT dataset, thus needs to be changed to match the CoCo dataset)
4. CoCo has 80 classes thus the coco-additions need to be 81 and onwards
5. Please check the Jupyter Notebook "[movefile.ipynb](yolov5\movefile.ipynb)" to re-adjust the files to be used in coco.
---
6. Now the `coco2017/train2017.txt` file should have the new datasets appended. `coco2017/images` should have all the images (coco and additional dataset). `coco2017/labels` should contain all .txt labels (adjusted for first 80 coco classees)
7. After the .txt files have been adjusted for the original classes. Adjust the path to the training and validation txt files. Add the new classes in your .yaml file. 
```
path: ../yolov5/datasets/coco2017 # dataset root dir
train: train2017.txt or train2017_10000.txt (10k images) 
val: val2017.txt 
...
80: new class
```
8. Run the following python in the yolov5 directory
``` 
python train.py --weights yolov5s.pt --data coco.yaml --img 640
```
## Working as a team with Git

1. Each person should create your branch according to feature (`git checkout -b feature/AmazingNewFeature`)
2. Add your changes (`git add -A`)
3. Commit your Changes (`git commit -a 'prefix: informative commit message'`)
   ```
   prefix must follow the following
   build | ci | docs | feat | fix | perf | refactor | style | test | chore | revert | bump
   ```
4. Push to the Branch (`git push`)
5. Open a Pull Request (PR) on GitHub to develop / main

# Roadmap

## Bugs



[python3.8.13-shield]: https://img.shields.io/badge/Python-3.8.13-brightgreen
[python3.8.13-url]: https://www.python.org/downloads/release/python-3813/
[conda-forge-shield]: https://img.shields.io/conda/dn/conda-forge/python?label=Anaconda
[conda-forge-url]: https://www.anaconda.com/products/distribution
