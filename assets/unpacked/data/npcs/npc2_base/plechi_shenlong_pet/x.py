import os
import shutil

def change_extension_in_subfolders(root_folder, old_extension, new_extension):
    for folder_name, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(old_extension):
                old_path = os.path.join(folder_name, filename)
                new_filename = filename.rsplit(old_extension, 1)[0] + new_extension
                new_path = os.path.join(folder_name, new_filename)
                
                shutil.move(old_path, new_path)
                print(f"Renamed: {old_path} -> {new_path}")

# Kullanım örneği
root_directory = os.getcwd()
old_extension = ".GR2"
new_extension = ".gr2"

change_extension_in_subfolders(root_directory, old_extension, new_extension)
