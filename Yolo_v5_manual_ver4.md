# Yolov5 Application Documentation

### I. Development Environment Set-up

1. Install [python](https://git-scm.com/download/win)
    * Version 3.8 would be needed
      ```bash 
      https://nodejs.org/dist/v14.15.5/node-v14.15.5-x64.msi
      ```

2. Install [**git**](https://git-scm.com/download/win)
    * Use Windows 64-bit Standalone Installer
      ```bash 
      https://git-scm.com/download/win
      ```

3. Install [**pip**](https://bootstrap.pypa.io/get-pip.py)
    * to install packages that aren't part of the Python standard library
    * download the **get-pip.py** file by typing on terminal:
      ```bash
      curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
      ```


4. Install [**Visual Studio Code**](https://code.visualstudio.com/download#)
    ```bash 
      https://code.visualstudio.com/download#
    ```

1. Install [**Anaconda**](https://www.anaconda.com/products/distribution)
    * To create programming environment to install and store libraries and packages 
      ```bash
      https://www.anaconda.com/products/distribution
      ```


---
### II. Installlation
Download all the required programme-related packages

1. Install Yolov5 
    ```bash
    git clone https://github.com/ultralytics/yolov5.git
    ```


2. Create a new virtual environment for yolov5
    ```
    cd .../yolov5
    python -m venv venv
    venv\Scripts\activate
    ```


3. Open the repository package and install all the required packages needed
    ```bash 
    pip install -r requirements.txt
    ```
    * Requirement.txt already includes python >=3.8 and pytorch >=1.7



4. Import pytorch (pytorch>=1.7) to the directory
    ```bash
    import torch
    ```


---
### III. Interference
1. Containing all image that are to be tested on the data image file in yolov5
    * the image should be stored in:
    ```json
    .../yolov5/data/images
    ```

    * Note: the folder should already contain two images **"bus.jpg"** and **"zidane.jpg"**


2. Use **yolov5** to perform object detection
    ```bash 
        python detect.py --source OPTION
    ```

    * Replace OPTION with **"data/images"** to detect all the image in the  file
        * To detect recording from webcam, replace **"OPTION"** with **"0"**
        * To detect image, replace **"OPTION"** with **"filename.jpg"**
        * To detect video, replace **"OPTION"** with **"filename.mp4"**  
        * For other option, please see <https://docs.ultralytics.com/quick-start/>
        
    * Results are saved to **"./runs/detect"**


---
### IV. Dataset
Dataset would be needed to train and validate the model. 

Dataset can be obtained from:

* coco128 dataset (included) 
  * Included within Yolov5. To edit, open **"coco128.yaml"** from **"yolov5/data/"** and follow instruction below starting from **step V.8**

  ```json
  python train.py --img 640 --batch 16 --epochs 3 --data coco128.yaml --weights yolov5s.pt
  ```

  * High quality dataset sample but only 80 type of class available
  * Noted that the dataset for validation is not included
  * For more detail, please see
    ```
    https://github.com/ultralytics/yolov5/blob/master/data/coco128.yaml
    ```


* &ensp; [Roboflow](https://roboflow.com/)
  * Can manually create labels on own custom dataset or uses prelabeled public dataset available, but requires large amount of time and performance cannot be compared with that of coco128 dataset.

    ```bash
    https://roboflow.com/
    ```


* There are other dataset available for autodownload, including VOC, Argoverse, Objects365, and etc

* After selection, export the dataset in the format of Yolo v5 Pytorch and download the zipped dataset


---

### V. Validation & Training 
1. Find location of **"images"** and **"label"** from the unzipped downloaded dataset
    * Location could generally be found within (may vary):
        ```bash 
        ../train
        ../val
        ../test
        ```   
    * Organize all images and labels from the zipped folder in terms of **"images"** and **"labels"** instead of **"train"**, **"val"** and **"test"** (Optional) 
        * example:
            ```bash
            ../images/train
            ../images/val
            ../images/test
            ```

2. Create a file outside the yolov5 folder named **"datasets"** to store downloaded dataset 
    ```json
        ../datasets
    ```


3. Create a new file  **"filename"** to store the organized folder **"images"** and **"labels"** (Optional)
    * The two filename **"images"** and **"labels"** should be located in:
        ```json
        ../datasets/<filename>/images
        ../datasets/<filename>/labels
        ```


4. Copy the **"coco128.yaml"** and move the copy **".yaml"**  to within the downloaded dataset Yolo v5 file
    * The **".yaml"** document should be moved to:
        ```json
        yolov5\data
        ```


5. Open the **".yaml"** document and add the path of the dataset folder to the document 
    ```bash 
        path: .../dataset/<filename>  # dataset root dir, filename: OBJECT
        train: images/train
        val: images/val
        test: images/test
    ```      
    * Please be noticed that the **".../"** should be taken as a reference only, if error occurs, please try **"../"** or **"./"**.
    * train/val/test are sets as 
        1) dir: path/to/imgs 
        2) file: path/to/imgs.txt 
        3) list: [path/to/imgs1, path/to/imgs2, ..]


6. Within the **".yaml"** document, edit the number of classes and the name of the class
    ```bash
        names: 
         0: skateboard
         1: snowboard
         2: surfboard           # Classes names     
    ```



7. Validate tha accuracy of the Yolo v5 model by running the command:
    ```json
        python val.py --weights yolov5s.pt --data <filename>.yaml --img 640 --half
    ```
    * The validation result are stored in
    ```json
    runs/val/exp
    ```

8. Before training you **must** adjust the yolov5s.pt to match the number of classes by going into **yolov5s.pt** and adjusting `nc=80 <coco dataset number of classes>` to number of classes  

9. Train the Yolo V5 model by specifying image size, batch-size, number of epochs, dataset and the pretrained **--weights yolov5s.pt**
   ```json
    python train.py --img 640 --batch 16 --epochs 3 --data <datafilename>.yaml --weights yolov5s.pt
   ```
    * detail (): 
        * img = image size in pixels 
        * batch = batch size
        * epochs = number of epochs
        * data = path to the data-configuration file
        * weight = path to the initial weight
        * `--cfg <filename>.yaml` = path to the model-configuration file (optional)

   &nbsp;

   * There are multiple model architecture available, with **"yolov5n"** as the smallest and fastest, **"yolov5s"**, **"yolov5m"**, **"yolov5l"**, and **"yolov5x"** as the largest model avaliable

   * For the sample above, the **"yolov5s"** model was trained on the dataset `**<datafilename>"**` for **3 epochs**, with the image size defined as **640*480** and the batch-size as **16**

   * After training, the train result are stored in
        ```json
        runs/train/exp
        ```
        * A model named **"best.pt"** should be contained within the file
            ```json
            runs/train/exp/weights/best.pt
            ```


---
### VI. Update Model
1. Move the document **"best.pt"** to the main file **"yolov5"**
    ```json
    yolov5/best.pt
    ```
    
2. Run 
    ```
    python detect.py --weights <weights_name>.pt --source <image directory>
    python detect.py --weights best.pt --source data/images
    ```

**Optionally** 

3. Open the document **"detect.py"**
    ```json
     yolov5/detect.py
    ```


4. Within the document **"detect.py"**, find:
    ```bash
    @smart_inference_mode()
    def run(
        weights=ROOT / 'yolov5s.pt',  # model.pt path(s)
    ```
    Rename **'yolov5s.pt"** to **'best.pt'** mentioned above



5. Within the document **"detect.py"**, find
    ```bash
    parser.add_argument('--weights', nargs='+', type=str, default=ROOT / 'yolov5s.pt', help='model path(s)')
    ```

    Rename **'yolov5s.pt'** to **'best.pt'**



6. To test the trained model **'best.pt'**:
    ```bash 
        python detect.py --source OPTION
    ```
    * Results are saved to "./runs/detect"


---

### Footnote

Please be noticed that the **".../"** for ```cd command``` is the **pathname** that should be defined by user, the example written in this guide is only the simplified path for one's reference.

---
### Additional: Open Images Tool 

1. install OIDv4 from github
```bash 
git clone https://github.com/theAIGuysCode/OIDv4_ToolKit.git
```


2. install requirement package(may need upgrade on pip)
 ```bash 
 pip install -r requirements.txt
 ```


3. Move the path to the correct directory
 ```bash
 cd OIDv4_ToolKit
 ```


4. Edit the order of the class from the txt file included in
 ```bash 
    \OIDv4_ToolKit\classes.txt
 ```
* example:
 ```bash
 Man
 Woman
 Dog
 ```


5. Terminal
 ```bash 
 python main.py downloader --classes Man Woman Dog --type_csv train --limit 100
 ```

* CLassify desired classes. In this example, **"Man"**, **"Woman"**, **"Dog"** is classified as the desired classes
* Classify desired type of datasest (train, val, test). In this example, the type  **"train"** was taken


6. Convert the format of the label to yolov5 with:
 ```bash 
 python convert_annotations.py
 ```
* Results are saved to "./OID/Dataset/"


7. Create a yaml file including the path to the image and label dataset, the name and number of the class, and attach it to the yolov5 file

* example:
 ```yaml
 path: ../datasets/OIDv4  # dataset root dir
 train: images/train2022  # train images (relative to 'path') 128 images
 val: images/train2022

 names: 
  0: Man
  1: Woman
  2: Dog
 ```

* For the format of the yaml file, please see **step V.3-V.6** take the coco128.yaml
