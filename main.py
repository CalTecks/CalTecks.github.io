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
    else:
        return markdown.markdown(content[end+3:])


def getTemplate(filename):
    with open("./templates/"+filename+".html", "r") as file:
        content = file.read()
        template = Template(content)
    return template


def writeHTML(template, content):
    print(colored(content, 'magenta'))
    output = template.render(content)
    print()
    print()
    print(colored(output, 'grey'))
    return output


def saveHTML(filename, content):
    save_html = open("./_site/"+filename+".html", "w")
    for line in content:
        save_html.write(line)
    save_html.close()


def processContent(filename):
    content = splitContent(filename, "yaml")
    markd_content = splitContent(filename)
    content["main_content"] = markd_content
    template = getTemplate(filename)
    print(colored(content["type"], 'red'))
    if content["type"] == "blog":
        print(colored("blog!", "red"))
        full_blog_content = getBlogPosts()
        content["main_blog_content"] = full_blog_content
        contentHTML = writeHTML(template, content)
        saveHTML(filename, contentHTML)
    else:
        contentHTML = writeHTML(template, content)
        saveHTML(filename, contentHTML)


def getBlogPosts():
    # list maken van blogpost dictionaries
    posts_list = scanFiles("./posts/")
    template = getTemplate("post")
    fullblogHTML = ""
    counter = 0
    for item in posts_list:
        yaml_content = splitContent(
            item, type="yaml", path="./posts/")
        markd_content = splitContent(
            item, type="markdown", path="./posts/")
        yaml_content["post_content"] = markd_content
        blogpostHTML = writeHTML(template, yaml_content)
        fullblogHTML += blogpostHTML
        counter += 1
    print(f"getBlogPosts(): {counter} blog posts found")
    print(colored(fullblogHTML, 'blue'))
    return fullblogHTML


def scanFiles(dir):
    filename_list = []
    files_in_dir = Path(dir).iterdir()
    for item in files_in_dir:
        if item.is_file():
            file_name = item.name
            base_name, extension = os.path.splitext(file_name)
            filename_list.append(base_name)
    print(colored(filename_list, 'cyan'))
    return filename_list


def processAll():
    filename_list = scanFiles("./pages")
    for file in filename_list:
        processContent(file)


processAll()
