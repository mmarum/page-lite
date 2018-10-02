import os
import json
import re

base = 'www'

class Page:
    def __init__(self, section, filename):
        self.section = section
        self.filename = filename
        self.filepath = '/'.join([base, self.section, self.filename])
        self.template = section + '.html'


    def get_content(self):
        f = open(self.filepath + '.json', "r")
        raw = f.read().decode('utf-8', 'replace')
        content = json.loads(raw)
        content['filename'] = filename
        f.close()
        return content


    def render_template(self, data):
        self.html = ''
        f = open(self.template, "r")
        for line in f:
            for item in data:
                if item in line and data[item] != None:
                    line = line.replace('{{ data.' + item + ' }}', data[item])
            self.html += line
        return self.html
        f.close()


    def write_page(self):
        f = open(self.filepath + '.html', "w")
        f.write(self.html)
        f.close()
        return True


def get_file_list(section, extension):
    filelist = []
    for filename in os.listdir('/'.join([base, section])):
        if filename.endswith(extension): 
            filename = filename.replace('.' + extension, '')
            filelist.append(filename)
    return filelist
            

for filename in get_file_list('lyrics', 'json'):
    print filename
    p = Page('lyrics', filename)
    data = p.get_content()
    p.render_template(data)
    p.write_page()

