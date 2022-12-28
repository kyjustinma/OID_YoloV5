# Simplified YOLO Training

## About The Project

This project was made in spare time to speed up the process of training new YOLOv5 models. The goal was to be able to use images from Open Image Dataset which are pre-labelled. Thus a new model for any of their classes can be made in a short span of time.
## Built With

[![python][python3.8.13-shield]][python3.8.13-url]

This template is primary focused on Python 3.9.12 and virtual environment (venv).
# Getting Started

## Prerequisites

- Python 3.9.12

## Installation
1. install the pip requirements for this repo```pip install -r setup/requirements/requirements.txt```
2. Alternative, `setup/pip_setup_venv.bat`


# Datasets and Training
## Using your own dataset (from OIDv4_ToolKit)
1. Start the venv environment
```
venv/Scripts/activate
```
2. Run the follow commands to download the classes needed for both "train" and "validation" set. (should run main within OIDv4_ToolKit Repo/Folder)
```
python OIDv4_ToolKit/main.py downloader --classes <Class1> <Class2> --type_csv <train/validation> --limit <Number of images>
```
3. Once finishing the download the images should be stored in a new folder under `OID_YoloV5\OIDv4_ToolKit\OID\Dataset\<train/validation>\<Class1>` from which there should be a folder within each class that is called `Label_yolo`. The class name will have also changed to **Lower case** and with **spaces replaced by underscores**.

4. After this you can run the OIDV4_TO_YOLO_dataset.py which moves the files to the dataset folder in YoloV5, separates the images and labels. After which it generates a .txt file to identify the location. Combines these .txt file to create the dataset path. And creates a .YAML file to start the training process.

```
-project: string        = project name for folder in datasets
-adjustment: boolean    = adjust labels based on "-objects" order(needed for YOLO) 
-validation: boolean    = Also takes the validation images from classes listed 
-objects: list[string]  = List of all the objects (folder names) in OIDv4

python OIDV4_TO_YOLO_dataset.py -project ProjectName -adjustment True -validation True -objects car motorcycle truck vehicle_registration_plate
``` 

5. Change directory into YoloV5 and run the train.py file
```
cd yolov5
python train.py --img 640 --batch 16 --epochs 5 --data ProjectName.yaml --weights yolov5s.pt
```
---
## Using COCO Dataset
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
