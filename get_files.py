import os

def gen_files_as_folders(basePath = 'D:/videos/data_training_v3/data_training/'):

    # C:\Users\patrick\Downloads\data_training_v3\data_training
    #basePath = 'C:/Users/patrick/Downloads/data_training_v3/data_training/'
    files = []
    for f in os.listdir(basePath):
        folder = []
        for ff in os.listdir(os.path.join(basePath, f)):
            if ff.endswith('jpg'):
                folder.append(os.path.splitext(os.path.join(basePath, f, ff))[0])
        files.append(folder)
    # print(files)
    return files

def get_files_in_folder(basePath):
    files = []
    for ff in os.listdir(basePath):
        files.append(os.path.splitext(os.path.join(basePath, ff))[0])
    # print(files)
    return files

def get_xml_files_in_folder(basePath):
    files = []
    for ff in os.listdir(basePath):
        if ff.endswith('xml'):
            files.append(os.path.join(basePath, ff))
    # print(files)
    return files

def get_jpg_files_in_folder(basePath):
    files = []
    for ff in os.listdir(basePath):
        if ff.endswith('jpg'):
            files.append(os.path.join(basePath, ff))
    # print(files)
    return files

def get_base_name_files_in_folder(basePath):
    files = []
    for ff in os.listdir(basePath):
        if ff.endswith('xml'):
            files.append(os.path.splitext(os.path.join(basePath, ff))[0])
    # print(files)
    return files