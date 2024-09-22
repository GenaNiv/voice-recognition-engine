import time 
import pathlib
import os
import re
import file_management.bst as bst


# The program should generate 5 files with name that have file's uniq ID and time stamps


def current_time():
    t = time.localtime()
    current_time = time.strftime("%Y_%m_%d_%H_%M_%s", t)
    return current_time

def read_files(target_directory):
    """TBD"""
    files_data = {}
    for filename in os.listdir(target_directory):
        file_path = os.path.join(target_directory, filename)
        
        if os.path.isfile(file_path) and filename.endswith(".txt"):
            with open(file_path, "r") as f:
                lines = f.readlines()
                # Extract file_id and timestamp from the lines
                file_id = int(lines[0].split(":")[1].strip())
                timestamp = lines[1].split(":")[1].strip()
                files_data[file_id] = timestamp
    return files_data
    
                
def generate_files(number_of_files, target_directory):
    """TBD"""
    file_info = {}

    for i in range(number_of_files):
        file_info[i + 1] = current_time()
        
        file_name = f"{i + 1}_{file_info[i + 1]}.txt"
        full_path = os.path.join(target_directory, file_name)
        with open(full_path, "w") as f:
            f.write("File ID: " + str(i + 1) )
            f.write("\n")
            f.write("File last modified: " + file_info[i + 1])
        time.sleep(1)  # Wait for 1 second between files

if __name__ == "__main__":

    
    #target_directory = "/home/gena/PROJECTS/ServerManagement/config_files"
    #number_of_files = 100
    #generate_files(number_of_files, target_directory)
    
    # Create binary search tree and insert data

    tree = bst.BinarySearchTree()
    config_files = read_files("/home/gena/PROJECTS/ServerManagement/config_files")
    print("Measure how long it take to insert one file to the BST")
    for file_id, file_timestamp in config_files.items():
        start_time = time.time()
        tree.insert(file_id, file_timestamp)
        end_time = time.time()
        print(f"Insertion of file ID {file_id} took {end_time - start_time:.6f} seconds")

    print("Measure how long it take to delete a node form the BST")
    start_time = time.time()
    file_id = 57
    tree.delete_node(file_id)
    end_time = time.time()
    print(f"Deletion of file ID {file_id} took {end_time - start_time:.6f} seconds")

            
    
    

        
    