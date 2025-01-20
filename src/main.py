from textnode import *
import os , shutil

def refresh_public(retrieve_dir, dest_dir):
    shutil.rmtree(dest_dir,ignore_errors=True)
    os.mkdir(dest_dir)
    dir_2_copy = os.listdir(retrieve_dir)
    for file in dir_2_copy:
        if os.path.isdir(retrieve_dir + file):
            ret_sub_dir = f"{retrieve_dir}{file}/"
            dest_sub_dir = f"{dest_dir}{file}/"
            os.mkdir(dest_sub_dir)
            refresh_public(ret_sub_dir, dest_sub_dir)
        else:
            shutil.copy(retrieve_dir + file, dest_dir + file)
    

def main():
    tester = TextNode("This is a text node", "bold", "https://www.boot.dev")
    dest_dir = "./public/"
    retrieve_dir = "./static/"
    
    refresh_public(retrieve_dir, dest_dir)

    print(os.listdir(retrieve_dir))


main()
