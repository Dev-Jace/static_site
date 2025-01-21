from textnode import *
from markdown_blocks import markdown_to_html_node, markdown_to_blocks, markdown_to_html_nodes
from htmlnode import *
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
    
def extract_title(markdown):
    if markdown[:2] != "# ":
        raise Exception("no h1 title")
    return markdown.split("\n",1)[0].strip()[2:]

def generate_page(from_path, template_path, dest_path):
    print(f"\nGenerating page from {from_path} to {dest_path} using {template_path}\n")
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    from_file = open(from_path, "r")
    file_contents = from_file.read()
    from_file.close()

    template_file = open(template_path,"r")
    template_contents = template_file.read()
    template_file.close()

    title = extract_title(file_contents)
    
    html_nodes = markdown_to_html_nodes(file_contents)
    html_txt = ""
    for node in html_nodes:
        html_txt += node.to_html()
    
    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html_txt)
    mk_file = open(dest_path+"index.html","w")
    mk_file.write(template_contents)
    mk_file.close

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_list = os.listdir(dir_path_content)
    for item in dir_list:
        if not os.path.isdir(dir_path_content + item):
            generate_page(dir_path_content + item, template_path, dest_dir_path)
        else: 
            new_dest = dest_dir_path + item +"/"
            generate_pages_recursive(dir_path_content + item + "/", template_path, new_dest)

def main():
    tester = TextNode("This is a text node", "bold", "https://www.boot.dev")
    dest_dir = "./public/"
    retrieve_dir = "./static/"
    template_path = "./template.html"
    content_path = "./content/"
    
    #content = open(content_path, "r")
    #print(extract_title(content.read()))

    refresh_public(retrieve_dir, dest_dir)
    generate_pages_recursive(content_path, template_path, dest_dir)
    #generate_page(content_path, template_path, dest_dir)
    print("\nDone!\nstarting web server")
    

main()