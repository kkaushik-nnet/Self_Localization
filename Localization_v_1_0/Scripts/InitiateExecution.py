import os
import shutil
import time
from time import sleep
from tkinter import *
from tkinter import filedialog

from Scripts.Aruco_Marker_Input import enter_array
from Scripts.BuildCPPFiles import buildCPP
from Scripts.CopyImagesFromSrc import copyUniqueImages
from Scripts.ExecuteTemplate import execute_template_method

folder_path = '/hri/localdisk/ThesisProject/Kaushik/Kaushik/Testing_Sample_Script/'
image_format = '.jpg'
train_the_data = 'train'
test_the_data = 'test'
source_path_train = ''
source_co_ord_path_train = ''
source_path_test = ''
source_co_ord_path_test = ''
train_coordinates = []
test_coordinates = []
is_train = False
is_test = False
is_train_test_data_distinct = False


def m_folder_open_train():
    global source_path_train
    source_path_train = filedialog.askdirectory(
        initialdir="/hri/localdisk/ThesisProject/Kaushik/Kaushik/Experiment_10_2/Training_Images/Path_1/",
        title="Select Training Images")
    source_path_train = source_path_train + '/'

    global source_co_ord_path_train

    source_co_ord_path_train = filedialog.askopenfilename(initialdir="/hri/localdisk/ThesisProject/Kaushik/Kaushik"
                                                                     "/Experiment_10_2/Training_Images"
                                                                     "/",
                                                          filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
                                                          title="Choose a file."
                                                          )


def m_folder_open_test():
    global source_path_test
    source_path_test = filedialog.askdirectory(
        initialdir="/hri/localdisk/ThesisProject/Kaushik/Kaushik/Experiment_10_2/Testing_Images/Path_1/",
        title="Select Testing Images")
    source_path_test = source_path_test + '/'

    global source_co_ord_path_test

    source_co_ord_path_test = filedialog.askopenfilename(initialdir="/hri/localdisk/ThesisProject/Kaushik/Kaushik"
                                                                    "/Experiment_10_2/Testing_Images/",
                                                         filetypes=(("Text File", "*.txt"), ("All Files", "*.*")),
                                                         title="Choose a file."
                                                         )


def move_coordinates_files(filepath, source_train, source_test):
    dest = filepath
    coordinates_path_array = []
    shutil.copy(source_train, dest)
    os.chdir(filepath)
    old_name_train = 'coordinates_wp0_Kodak.txt'
    new_name_train = 'coordinates_train.txt'
    shutil.move(old_name_train, new_name_train)
    coordinates_path_array.append(dest + '/' + new_name_train)
    if is_train_test_data_distinct:
        shutil.copy(source_test, dest)
        old_name_test = 'coordinates_wp0_Kodak.txt'
        new_name_test = 'coordinates_test.txt'
        shutil.move(old_name_test, new_name_test)
        coordinates_path_array.append(dest + '/' + new_name_test)
    return coordinates_path_array


def create_folder_structure(aruco_marker_array):
    time_string = time.strftime("%d%m%Y-%H%M%S")
    directory_items = []
    extracted_folder_items = []
    if not os.path.exists(folder_path + time_string):
        current_working_folder = folder_path + time_string
        os.makedirs(current_working_folder)
        os.makedirs(current_working_folder + '/Training_Data')
        # os.makedirs(current_working_folder + '/Extracted_Train_Data')
        # os.makedirs(current_working_folder + '/Extracted_Test_Data')

        # print("---" + current_working_folder)
        directory_items.append(current_working_folder)
        detection_build_utils = os.getcwd().replace('Scripts', 'MarkerDetection/build/utils/')
        directory_items.append(detection_build_utils)
        training_folder = current_working_folder + '/Training_Data/'
        directory_items.append(training_folder)
        # training_extract = current_working_folder + '/Extracted_Train_Data/'
        # directory_items.append(training_extract)
        run_train_detection = os.getcwd() + '/run_train_detection.sh'
        directory_items.append(run_train_detection)
        train_xml = current_working_folder + '/trainList.xml'
        directory_items.append(train_xml)
        train_csv = current_working_folder + '/result_train.csv'
        directory_items.append(train_csv)

        if is_train_test_data_distinct:
            os.makedirs(current_working_folder + '/Testing_Data')
            testing_folder = current_working_folder + '/Testing_Data/'
            directory_items.append(testing_folder)
            # testing_extract = current_working_folder + '/Extracted_Test_Data/'
            # directory_items.append(testing_extract)
            run_test_detection = os.getcwd() + '/run_test_detection.sh'
            directory_items.append(run_test_detection)
            test_xml = current_working_folder + '/testList.xml'
            directory_items.append(test_xml)
            test_csv = current_working_folder + '/result_test.csv'
            directory_items.append(test_csv)

        for var in range(len(aruco_marker_array)):
            training_extract_folder = current_working_folder + '/Extracted_Train_Data_'+aruco_marker_array[var]+'/'
            os.makedirs(training_extract_folder)
            extracted_folder_items.append(training_extract_folder)

        if is_train_test_data_distinct:
            for var in range(len(aruco_marker_array)):
                testing_extract_folder = current_working_folder + '/Extracted_Test_Data_'+aruco_marker_array[var]+'/'
                os.makedirs(testing_extract_folder)
                extracted_folder_items.append(testing_extract_folder)

        return directory_items,extracted_folder_items


def count_of_images(file__path):
    path, dirs, files = next(os.walk(file__path))
    file_count = len(files)
    return file_count


if __name__ == "__main__":
    num_data_sets = input("Are there two separate data sets to Train & Test ?  [y/n]")
    if num_data_sets == 'y':
        is_train_test_data_distinct = True
    print("Choose Training Data and its Co-Ordinates File, Please browse")
    browseBox = Tk()
    Button(text="open Folder", width=30, command=m_folder_open_train()).pack()
    browseBox.destroy()
    browseBox.mainloop()

    if is_train_test_data_distinct:
        print("Choose Testing Data and its Co-Ordinates File, Please browse")
        browseBox = Tk()
        Button(text="open Folder", width=30, command=m_folder_open_test()).pack()
        browseBox.destroy()
        browseBox.mainloop()

    print("source_path_train : ", source_path_train)
    print("source_co_ord_path_train : ", source_co_ord_path_train)
    print("source_path_test : ", source_path_test)
    print("source_co_ord_path_test : ", source_co_ord_path_test)

    question = input("Do you wanna re-build [y / n]")
    dir_path = os.getcwd()

    if question == 'y':
        file_path = dir_path + '/SetEnvironmentForAruco.sh'
        build_path = dir_path.replace('Scripts', 'MarkerDetection/')
        # buildCPP(build_path, file_path)
        buildCPP(file_path)

    aruco_marker_id = enter_array()
    # id_1 = aruco_marker_id[0]

    print("Process starting", end='')
    for i in range(25):
        print(".", end='')
        sleep(0.1)

    items_in_dir,extraction_folders = create_folder_structure(aruco_marker_id)
    '''
    print("items in dir are : ")
    print(items_in_dir)
    print("#####################################################")
    print("Extraction Folders are : ")
    print(extraction_folders)
    '''
    coordinates_path = move_coordinates_files(items_in_dir[0], source_co_ord_path_train, source_co_ord_path_test)
    
    copyUniqueImages(coordinates_path[0], source_path_train, items_in_dir[2])
    train_img_count = count_of_images(items_in_dir[2])
    train_set_items = [items_in_dir[0],
                       items_in_dir[1],
                       items_in_dir[2],
                       items_in_dir[3],
                       items_in_dir[4],
                       items_in_dir[5],
                       source_path_train,
                       coordinates_path[0],
                       image_format,
                       train_img_count,
                       train_the_data,
                       is_train_test_data_distinct,
                       extraction_folders,
                       aruco_marker_id]
    test_set_items = []

    if is_train_test_data_distinct:
        copyUniqueImages(coordinates_path[1], source_path_test, items_in_dir[6])
        test_img_count = count_of_images(items_in_dir[6])
        test_set_items = [items_in_dir[0],
                          items_in_dir[1],
                          items_in_dir[6],
                          items_in_dir[7],
                          items_in_dir[8],
                          items_in_dir[9],
                          source_path_test,
                          coordinates_path[1],
                          image_format,
                          test_img_count,
                          test_the_data,
                          is_train_test_data_distinct,
                          extraction_folders,
                          aruco_marker_id]

    if is_train_test_data_distinct:
        execute_template_method(train_set_items, test_set_items)
    else:
        execute_template_method(train_set_items, [])
