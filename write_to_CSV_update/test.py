import csv
import os

def create_desktop_folder(foldername):
    folder_name = foldername

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    folder_path = os.path.join(desktop_path, folder_name)

    try:
        os.mkdir(folder_path)
        print(f"Folder '{folder_name}' created on Desktop")
        return folder_path
    except FileExistsError:
        print(f"Folder '{folder_name}' already exists on Desktop.")
        return folder_path
    

fname = 'hello.txt'
csv_folder_name = 'TEC_Output'

folder_path = create_desktop_folder(csv_folder_name)

filepath = os.path.join(folder_path, fname)
                
with open(filepath, 'a', newline='') as file:
    file.write('Hello, world!')
    file.close()