import yaml
import markdown
from jinja2 import Template
from termcolor import colored
from pathlib import Path
import os


def splitContent(filename, type="markdown", path="./pages/"):
    with open(path+filename+".yaml", 'r') as file:
        content = file.read()
    start = content.find('---')
    end = content.find('---', start+1)
    if start == -1 or end == -1:
        return False
    if type == "yaml":
        return yaml.safe_load(content[start+3:end])
    return markdown.markdown(content[end+3:])


def getTemplate(filename):
    with open("./templates/"+filename+".html", "r") as file:
        content = file.read()
        template = Template(content)
    return template


def writeHTML(filename, template, content):
    print(colored(content, 'magenta'))
    output = template.render(content)
    print()
    print()
    print(colored(output, 'grey'))
    save_html = open("./_site/"+filename+".html", "w")
    for line in output:
        save_html.write(line)
    save_html.close()


def processContent(filename):
    content = splitContent(filename, "yaml")
    markd_content = splitContent(filename)
    content["main_content"] = markd_content
    template = getTemplate(filename)
    print(content["type"])
    if content["type"] == "blog":
        print(colored("blog!", "red"))
        blog_content = getBlogPosts()
        content_list = []
        content_list.append(content)
        content_list.extend(blog_content)
        writeHTML(filename, template, content_list)
    else:
        writeHTML(filename, template, content)


def getBlogPosts():
    # list maken van blogpost dictionaries
    bloglist = []
    files_in_posts = Path("./posts/").iterdir()
    counter = 0
    for item in files_in_posts:
        if item.is_file():
            file_name = item.name
            base_name, extension = os.path.splitext(file_name)
            yaml_content = splitContent(
                base_name, type="yaml", path="./posts/")
            markd_content = splitContent(
                base_name, type="markdown", path="./posts/")
            yaml_content["main_content"] = markd_content
            bloglist.append(yaml_content)
            counter += 1
    print(f"getBlogPosts(): {counter} blog posts found")
    print(colored(bloglist, 'blue'))
    return bloglist


def scanFiles():
    filename_list = []
    files_in_dir = Path("./pages/").iterdir()
    for item in files_in_dir:
        if item.is_file():
            file_name = item.name
            base_name, extension = os.path.splitext(file_name)
            filename_list.append(base_name)
    print(colored(filename_list, 'cyan'))
    return filename_list


filename_list = scanFiles()
for file in filename_list:
    processContent(file)
