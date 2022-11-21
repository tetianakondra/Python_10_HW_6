#for operations with folders and files

from pathlib import Path

#for unpacking archives and moving the files

import shutil

# for importing file directory from cmd

import sys

archives_list = []
docs_list = []
music_list = []
pictures_list = []
unknown_files_list = []
videos_list = []

ext_set = set()
unknown_ext_set = set()

def delete_folder(clean_folder):

    """ 
    This functions deletes folders if it's empty 

    """

    path_clean_folder = Path(clean_folder)

    for sorted_elem in path_clean_folder.iterdir():

        if sorted_elem.is_dir() and sorted_elem.name not in ["archives", "video", "audio", "documents", "images"]:

            if not len(list(sorted_elem.iterdir())):

                Path(sorted_elem).rmdir()
                
            else:

                delete_folder(sorted_elem)

def normalize(elem_name):

    """
    This function makes file/folder name's translation: all Cyrillic symbols to and all symbols those not a number or a letter changes to "_"

    Big letters leave as big, small - as small.

    The extension of file is not changed.

    """

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯЄІЇҐ"
    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g", "A", "B", "V", "G",
               "D", "E", "E", "J", "Z", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "F", "H", "Ts", "Ch",
               "Sh", "Sch", "", "Y", "", "E", "Yu", "Ya", "Je", "I", "Ji", "G")

    TRANS = {}
    translated_name = ""
    name_ext = ""
    
    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    name_parts = elem_name.split(".")

    for symb in name_parts[0]:

        if symb in CYRILLIC_SYMBOLS:

            translated_name += symb.translate(TRANS)

        elif symb not in "abcdefghijklmnopqrstuvwxyuzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890":

            translated_name += "_"

        else:

            translated_name += symb

    if len(name_parts) > 1:

        translated_name_ext = translated_name + "." + name_parts[1]

    else:

        translated_name_ext = translated_name
    

    return translated_name_ext




def trash_sort(path):

    """
    This function sorts the files in Folder that was input in cmd or with opening with IDLE.

    All names of files and folders are changed according to def normalize.

    All extensions are written to the sets (known/unknown for function).
    
    The names of files (with known extensions) are written to the list according to the Folder where they are moved.

    Files are sortes according to their extensions and moved to created folders (archives, audio etc.).

    If root folder has other folders, they are also checked and sorted as main one.

    The empty folders will be deleted with using def delete_folder.

    
    """

    global clean_folder
    
    path_archive = Path(clean_folder + "\\archives")
    path_audio = Path(clean_folder + "\\audio")
    path_documents = Path(clean_folder + "\\documents")
    path_images = Path(clean_folder + "\\images")
    path_video = Path(clean_folder + "\\video")
    path_unknown_files = Path(clean_folder + "\\unknown_files")

    
    path_archive.mkdir(exist_ok=True)
    path_audio.mkdir(exist_ok=True)
    path_documents.mkdir(exist_ok=True)
    path_images.mkdir(exist_ok=True)
    path_video.mkdir(exist_ok=True)
    path_unknown_files.mkdir(exist_ok=True)


    trash_dir = Path(path)

    for elem in trash_dir.iterdir():

        if elem.is_file():

            file_name = normalize(elem.name)

            file_ext = elem.suffix

            if file_ext.upper() in [".JPEG", ".PNG", ".JPG", ".SVG"]:

                ext_set.add(file_ext.upper())
                pictures_list.append(file_name)
                new_dir = Path(str(path_images) + f"\{file_name}")
                shutil.move(elem, new_dir)

            elif file_ext.upper() in [".AVI", ".MP4", ".MOV", ".MKV"]:

                ext_set.add(file_ext.upper())
                videos_list.append(file_name)
                new_dir = Path(str(path_video) + f"\{file_name}")
                shutil.move(elem, new_dir)

            elif file_ext.upper() in [".DOC", ".DOCX", ".TXT", ".PDF", ".XLSX", ".PPTX"]:

                ext_set.add(file_ext.upper())
                docs_list.append(file_name)
                new_dir = Path(str(path_documents) + f"\{file_name}")
                shutil.move(elem, new_dir)

            elif file_ext.upper() in [".MP3", ".OGG", ".WAV", ".AMR"]:

                ext_set.add(file_ext.upper())
                music_list.append(file_name)
                new_dir = Path(str(path_audio) + f"\{file_name}")
                shutil.move(elem, new_dir)

            elif file_ext.upper() in [".ZIP", ".GZ", ".TAR"]:

                ext_set.add(file_ext.upper())
                archives_list.append(file_name)
                shutil.unpack_archive(elem, str(path_archive) + "\\"+ file_name.removesuffix(elem.suffix))
                new_dir = Path(str(path_archive) + f"\{file_name}")
                shutil.move(elem, new_dir)

            else:

                unknown_ext_set.add(file_ext.upper())
                new_dir = Path(str(path_unknown_files) + f"\{file_name}")
                shutil.move(elem, new_dir)


        elif elem.is_dir() and elem.name not in ["archives", "video", "audio", "documents", "images"]:

            delete_folder(elem)
            folder_name = normalize(elem.name)
            
            try:
                
                new_dir = Path(f"{elem.parent}\{folder_name}")
                full_folder_name = elem.rename(new_dir)

            except FileExistsError:

                new_dir = Path(f"{elem.parent}\{folder_name}_1")
                full_folder_name = elem.rename(new_dir)
                trash_sort(full_folder_name)

            else:

                trash_sort(full_folder_name)

                
    delete_folder(clean_folder)


try:
    
    clean_folder = sys.argv[1]
    
except IndexError:

    clean_folder = input("Please, input the direction of trash folder: ")
    trash_sort(clean_folder)

else:

    trash_sort(clean_folder)





