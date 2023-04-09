import yaml
import markdown
from jinja2 import Template


def splitContent(filename, type="markdown"):
    with open("./pages/"+filename+".yaml", 'r') as file:
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


def writeHTML(template, yaml, markdown):
    yaml["main_content"] = markdown
    print(yaml)
    output = template.render(yaml)
    print()
    print()
    print(output)


def processContent(filename):
    yaml_content = splitContent(filename, "yaml")
    markd_content = splitContent(filename)
    template = getTemplate(filename)
    writeHTML(template, yaml_content, markd_content)


processContent("contact")
