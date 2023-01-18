import os
import shutil
import pprint

DESKTOP_PATH = "C:/Users/rudik/OneDrive/Desktop/"
FOLDER_TO_SORT = ""
list_of_subfolders = []

unknown_file_formats = set()
known_file_formats = set()

file_type_dict = {
    "images": {'JPEG', 'PNG', 'JPG', 'SVG', 'JFIF'},
    "documents": {'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX', 'XLSM'},
    "video": {'AVI', 'MP4', 'MOV', 'MKV'},
    "audio": {'MP3', 'OGG', 'WAV', 'AMR'},
    "archives": {'ZIP', 'GZ', 'TAR'},
}

latin_letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z')


symbols = ((
               'а', 'б', 'в', 'г', 'д', 'е', 'є', 'ж', 'з', 'и', 'і', 'ї', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с',
               'т',
               'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ь', 'ю', 'я', 'А', 'Б', 'В', 'Г', 'Д', 'Е', 'Є', 'Ж', 'З', 'И', 'І',
               'Ї',
               'Й', 'К', 'Л', 'М', 'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Х', 'Ц', 'Ч', 'Ш', 'Щ', 'Ь', 'Ю', 'Я'),
           (
               'a', 'b', 'v', 'g', 'd', 'e', 'ye', 'zh', 'z', 'y', 'i', 'yi', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r',
               's', 't',
               'u', 'f', 'kh', 'c', 'ch', 'sh', 'shch', "'", 'yu', 'ya', 'A', 'B', 'V', 'G', 'D', 'E', 'Ye', 'Zh', 'Z',
               'Y', 'I', 'Yi',
               'Y', 'K', 'L', 'M', 'N', 'O', 'P', 'R', 'S', 'T', 'U', 'F', 'Kh', 'C', 'Ch', 'Sh', 'Shch', "'", 'Yu',
               'Ya'))

tr_dict = {a: b for a, b in zip(*symbols)}


def normalize(text: str) -> str:
    normalized_list = []
    for i in text:
        if i in latin_letters:
            normalized_list.append(i)
        else:
            try:
                normalized_list.append(tr_dict[i])
            except KeyError:
                try:
                    normalized_list.append(str(int(i)))
                except ValueError:
                    normalized_list.append("_")
    normalized_lign = "".join(normalized_list)
    return normalized_lign


# def folder_scan_func(subfolder):
#     global FOLDER_TO_SORT
#     list_of_subfolders.append(subfolder)
#     path_to_new_subfolder = f"{FOLDER_TO_SORT}/{'/'.join(list_of_subfolders)}"
#     sort(path_to_new_subfolder)


def sort(path):
    global FOLDER_TO_SORT
    list_of_files_to_sort = os.listdir(path)
    if len(list_of_files_to_sort) != 0:
        for file_name in list_of_files_to_sort:
            try:
                file_name[file_name.index(".") + 1:]

            except ValueError:
                # If subfolder encountered, go one layer further and sort the subfolder
                # by recursively calling the sort function
                list_of_subfolders.append(file_name)
                path_to_new_subfolder = f"{FOLDER_TO_SORT}/{'/'.join(list_of_subfolders)}"
                sort(path_to_new_subfolder)

                # Once subfolder sorted and emptied, delete the empty subfolder
                os.rmdir(f"{path}/{file_name}")

                # Remove the last subfolder from a list of subfolders to ensure path remains consistent
                list_of_subfolders.pop()

            else:
                # Sorting algorithm for files in the main folder/subfolder
                for grouping_folder, file_types in file_type_dict.items():
                    if file_name[file_name.index(".") + 1:].upper() in file_types:
                        new_location_path = f"{FOLDER_TO_SORT}/{grouping_folder}/{normalize(file_name[:file_name.index('.')])}"
                        if grouping_folder == "archives":
                            file_to_unpack = f"{path}/{file_name}"
                            archive_format = file_name[file_name.index(".") + 1:]
                            if grouping_folder not in os.listdir(FOLDER_TO_SORT):
                                # Create directories recursively if "archive" folder does not exist yet
                                os.makedirs(new_location_path)
                            else:
                                # Create a subfolder for the archive to be unzipped to existing "archive" directory
                                os.mkdir(new_location_path)
                            shutil.unpack_archive(file_to_unpack, new_location_path, archive_format)
                            os.remove(file_to_unpack)
                        else:
                            if grouping_folder not in os.listdir(FOLDER_TO_SORT):
                                os.mkdir(f"{FOLDER_TO_SORT}/{grouping_folder}")
                            os.replace(f"{path}/{file_name}", f"{new_location_path}{file_name[file_name.index('.'):]}")

                        # Adding known file format to the set of known file formats in the sorted directory
                        known_file_formats.add(file_name[file_name.index(".") + 1:])

        # Unknown formats added to unknown set and moved to the sorted directory unchanged
        if len(os.listdir(path)) != 0:
            for file in os.listdir(path):
                try:
                    unknown_file_formats.add(file[file.index(".") + 1:])
                except ValueError:
                    continue
                else:
                    os.replace(f"{path}/{file}", f"{FOLDER_TO_SORT}/{file}")


def sort_start(folder):
    global FOLDER_TO_SORT
    sorted_subfolders = {}
    FOLDER_TO_SORT = DESKTOP_PATH + folder
    sort(FOLDER_TO_SORT)
    for item in os.listdir(FOLDER_TO_SORT):
        try:
            item[item.index(".") + 1:]
        except ValueError:
            sorted_subfolders[item] = os.listdir(f"{FOLDER_TO_SORT}/{item}")
    print("Sorting is finished successfully!\n")
    print(f"After sorting, the following folders were created with items contained in them listed below:\n")
    print(f"{pprint.pprint(sorted_subfolders)}\n")
    print(f"Sorted folder comprises the following known file formats:\n"
          f"{known_file_formats}\n")
    print(f"There are also unidentified file formats noted listed below:\n"
          f"{unknown_file_formats}")


sort_start("To sort2")
