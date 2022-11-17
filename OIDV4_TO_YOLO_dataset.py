from distutils.sysconfig import customize_compiler
import logging
import os
import sys
import argparse
import shutil
import time

from matplotlib.pyplot import text
from utils import custom_utils


# Regular imports
from copy import deepcopy

# Yaml loaders and dumpers
from ruamel.yaml.main import round_trip_load as yaml_load, round_trip_dump as yaml_dump

# Yaml commentary
from ruamel.yaml.comments import (
    CommentedMap as OrderedDict,
    CommentedSeq as OrderedList,
)

# For manual creation of tokens
from ruamel.yaml.tokens import CommentToken
from ruamel.yaml.error import CommentMark

# Globals
# Number of spaces for an indent
INDENTATION = 2
# Used to reset comment objects
tsRESET_COMMENT_LIST = [None, [], None, None]
from datetime import date, datetime


__CWD_DIR__ = os.path.abspath(os.getcwd())
__SCRIPT_DIR__ = os.path.dirname(os.path.abspath(__file__))
__YOLO_DIR__ = os.path.abspath(os.path.join(os.getcwd(), "yolov5"))
__OIDV4_DIR__ = os.path.abspath(os.path.join(os.getcwd(), "OIDv4_ToolKit"))


def parse_arguments():
    """Read arguments from a command line."""
    parser = argparse.ArgumentParser(description="Arguments get parsed via --commands")
    parser.add_argument(
        "-t",  # Tag to add to the parse
        metavar="--Help",
        required=False,
        default="Here is a default text",
        help="Returns help information",
    )
    parser.add_argument(
        "-type",  # Tag to add to the parse
        metavar="--dataset_type",
        required=False,
        default="train",
        help="Select if you want train, validation or test data to be converted",
    )
    parser.add_argument(
        "-project",  # Tag to add to the parse
        metavar="--project_name",
        required=True,
        default="default",
        help="Select a project name to store all the images in",
    )
    parser.add_argument(  ### -list <item1> <item2>
        "-objects",
        metavar="--objects_list",
        nargs="+",
        required=True,
        default=["", ""],
        help="List of objects to convert / transfer items",
    )
    parser.add_argument(
        "-validation",
        metavar="--validation_set",
        required=False,
        default=False,
        help="Indicate if the classes supplied have validation sets or not",
    )
    parser.add_argument(
        "-adjustment",
        metavar="--adjust_labels",
        required=True,
        default=False,
        help="Indicate to change class number",
    )
    args = parser.parse_args()

    if args.validation.lower() == "true":
        args.validation = True
    else:
        args.validation = False

    if args.adjustment.lower() == "true":
        args.adjustment = True
    else:
        args.adjustment = False

    return args


"""
class_number: index to change the class to
text_file: the path to the text file that needs to be adjusted
"""


def adjust_label(class_number: int, text_file: str) -> None:
    annotations = []
    with open(text_file) as f:
        for line in f:
            labels = line.split()
            labels[0] = class_number  # Change the class number
            newline = (
                str(labels[0])
                + " "
                + str(labels[1])
                + " "
                + str(labels[2])
                + " "
                + str(labels[3])
                + " "
                + str(labels[4])
            )
            line = line.replace(line, newline)
            annotations.append(line)
    f.close()

    with open(text_file, "w") as outfile:
        for line in annotations:
            outfile.write(line)
            outfile.write("\n")
    outfile.close()


"""
  This function moves all the files from OIDv4 to the YOLO folder adjusting the name as need be
"""


def move_OIDV4_YOLO(object: str, class_number: int, dataset="train") -> bool:

    print(f"[Moving] Moving images and labels {object}")
    object_name = object
    object_folder = object_name.lower().replace(" ", "_")  # new folder name

    # Get the images in the object folder
    oidv_obj_path = os.path.join(__OIDV4_DIR__, "OID", "Dataset", dataset, object_name)
    label_files_path = os.path.join(oidv_obj_path, "Label_yolo")

    # Adjusting labels
    adjusted_labels = False
    adjust_label_folder = os.path.join(
        __YOLO_DIR__, "datasets", args.project, object_folder, dataset, "labels"
    )
    if args.adjustment == True and os.path.exists(adjust_label_folder):
        print(
            f"[Adjustment] Changing class number of labels in {adjust_label_folder} to {class_number}"
        )
        for file_names in [
            file for file in os.listdir(adjust_label_folder) if file.endswith(".txt")
        ]:
            dest = os.path.normpath(os.path.join(adjust_label_folder, file_names))
            adjust_label(class_number=class_number, text_file=dest)
        adjusted_labels = True
    # Finish adjusting

    if not os.path.exists(oidv_obj_path):
        print(f"[ERROR] {oidv_obj_path} does not exists")
        return False
    if not os.path.exists(label_files_path):
        print(
            f"[ERROR] 'Label_yolo' does not exist for {object}, please convert labels to Label_yolo type"
        )
        return False

    yolo_project_folder = os.path.join(
        __YOLO_DIR__, "datasets", args.project, object_folder, dataset
    )
    print(yolo_project_folder)
    if os.path.exists(yolo_project_folder):
        if (
            input(
                f"The object {yolo_project_folder} already exists would you like to remove it (Y/N)?"
            ).lower()
            == "y"
        ):
            if (
                input(
                    f"Are you sure you want to permanently delete all items within {yolo_project_folder}, this cannot be undone (Y/N)?"
                ).lower()
                == "y"
            ):
                print(f"Deleting all files within {yolo_project_folder}")
                shutil.rmtree(yolo_project_folder)
            else:
                raise Exception(
                    f"Folder {yolo_project_folder} already exists please remove it"
                )
        else:
            print(
                f"[WARN] {yolo_project_folder} already exists, skipping migration of {object}"
            )
            return False

    custom_utils.create_folder(yolo_project_folder)
    obj_train_img_path = custom_utils.create_folder(
        os.path.join(yolo_project_folder, "images")
    )
    obj_train_txt_path = custom_utils.create_folder(
        os.path.join(yolo_project_folder, "labels")
    )

    train_files = os.listdir(oidv_obj_path)
    for file_names in [
        file for file in train_files if file.endswith(".jpg")
    ]:  # for files that are jpg
        source = os.path.normpath(os.path.join(oidv_obj_path, file_names))
        dest = os.path.normpath(os.path.join(obj_train_img_path, file_names))
        shutil.move(source, dest)

    label_files = os.listdir(label_files_path)
    for file_names in [
        file for file in label_files if file.endswith(".txt")
    ]:  # for files that are txt
        source = os.path.normpath(os.path.join(label_files_path, file_names))
        dest = os.path.normpath(os.path.join(obj_train_txt_path, file_names))
        shutil.move(source, dest)

        if adjusted_labels == False and args.adjustment == True:
            adjust_label(class_number=class_number, text_file=dest)

    with open(os.path.join(yolo_project_folder, "obj.names"), "w") as f:
        f.write(object_name)

    return True


"""
  Creates the individual .txt files by reading all the images and appending them to <dataset>.txt
"""


def create_train_file(object: str, dataset="train") -> bool:
    print(f"[.txt] Generating {dataset}.txt for {object}")
    if not os.path.exists(
        os.path.join(__YOLO_DIR__, "datasets", args.project, object, dataset)
    ):
        return False

    yolo_object_folder = os.path.join(
        __YOLO_DIR__, "datasets", args.project, object, dataset
    )
    yolo_object_images_folder = os.path.join(yolo_object_folder, "images")
    yolo_object_labels_folder = os.path.join(yolo_object_folder, "labels")

    ###  Rename file
    train_files = os.listdir(yolo_object_images_folder)
    train_text_file_data = []
    for idx, image_name in enumerate(train_files):
        fileName = os.path.splitext(os.path.basename(image_name))[0]
        label_name = fileName + ".txt"

        full_image_path = os.path.join(yolo_object_images_folder, image_name)  # SRC
        full_label_path = os.path.join(yolo_object_labels_folder, label_name)
        new_image_name = f"{object}_{idx+1}.jpg"
        new_label_name = f"{object}_{idx+1}.txt"
        new_full_image_path = os.path.join(yolo_object_images_folder, new_image_name)
        new_full_label_path = os.path.join(yolo_object_labels_folder, new_label_name)

        try:
            os.rename(full_image_path, new_full_image_path)
            os.rename(full_label_path, new_full_label_path)
        except Exception as e:
            pass
        train_text_file_data.append(f"./{object}/{dataset}/images/{new_image_name}")
        # print(f'File {txt_name} missing')

    with open(os.path.join(yolo_object_folder, f"{dataset}.txt"), "w") as outfile:
        for line in train_text_file_data:
            outfile.write(line)
            outfile.write("\n")
    outfile.close()


"""
This function generated a combined .txt for all the objects stored within the generated project
return: string of the location of the .txt file
"""


def generate_complete_file(objects: list[str], dataset="train") -> str:
    print(f"[Combining] combining {dataset}.txt for {objects}")
    combined_text_file_data = []
    for objs in objects:
        text_file = os.path.join(
            __YOLO_DIR__, "datasets", args.project, objs, dataset, f"{dataset}.txt"
        )
        if not os.path.exists(text_file):
            print(f"[ERROR] The text file for {objs} at {text_file} does not exist")
        else:
            with open(text_file) as f:
                for line in f:
                    combined_text_file_data.append(line)
                f.close()

    txt_file_path = os.path.join(
        __YOLO_DIR__, "datasets", args.project, f"{dataset}.txt"
    )
    with open(txt_file_path, "w") as outfile:
        for line in combined_text_file_data:
            outfile.write(line)
    outfile.close()
    return txt_file_path


"""
This function generated a combined version of all the .txt files
"""


def generate_yolo_yaml(objects: list[str], validation=False) -> bool:
    print(f"[YAML] Generation")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    project_path = f"../yolov5/datasets/{args.project}"

    train_path = f"train.txt"
    validation_path = f"validation.txt"
    if not os.path.exists(
        os.path.join(__YOLO_DIR__, "datasets", args.project, train_path)
    ):
        raise Exception("Missing train.txt")
    if (
        not os.path.exists(
            os.path.join(__YOLO_DIR__, "datasets", args.project, validation_path)
        )
        and validation
    ):
        print("\t\t [Error] Missing validation.txt")

    object_names = {idx: objs for idx, objs in enumerate(objects)}
    project_yaml = OrderedDict(
        {
            "path": project_path,
            "train": train_path,
            "val": validation_path,
            # "test": "",
            "names": OrderedDict(object_names),
        }
    )
    project_yaml.yaml_set_start_comment(
        f"{args.project} yaml file generated at {dt_string}"
    )

    print("\n[YAML] Yaml shown below\n", yaml_dump(project_yaml), "\n")
    yaml_file = yaml_dump(project_yaml)
    with open(
        os.path.join(__YOLO_DIR__, "datasets", args.project, f"{args.project}.yaml"),
        "w",
    ) as outfile:
        for line in yaml_file:
            outfile.write(line)
    outfile.close()

    return True


def main():
    for class_number, object in enumerate(args.objects):
        move_OIDV4_YOLO(object=object, class_number=class_number)
        create_train_file(object=object)
        if args.validation == True:
            move_OIDV4_YOLO(
                object=object, class_number=class_number, dataset="validation"
            )
            create_train_file(object=object, dataset="validation")

    generate_complete_file(objects=args.objects)
    generate_complete_file(objects=args.objects, dataset="validation")

    generate_yolo_yaml(objects=args.objects, validation=args.validation)


if __name__ == "__main__":
    args = parse_arguments()
    main()
    print("[Finish] Custom training dataset generated")
