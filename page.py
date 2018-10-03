import os
import json
#import re

base = 'www'
index = []

class Page:
    def __init__(self, section, filename):
        self.section = section
        self.filename = filename
        self.filepath = '/'.join([base, self.section, self.filename])
        self.template = section + '.html'


    def render_template(self, data):
        self.html = ''
        f = open(self.template, "r")
        for line in f:
            for item in data:
                if data['title'] == 'index':
                    links = ''
                    for link in data['links']:
                        links += '<a href="' + link + '.html">' + link.replace('-',' ').title() + '</a><br>\n'
                    line = line.replace('{{ data.lyrics }}', links)
                    line = line.replace('{{ data.about }}', data['about'])
                    line = line.replace('{{ data.credits }}', '')
                    line = line.replace('{{ data.title }}', 'Lyrics Index')
                elif item in line and data[item] != None:
                    if item == 'track':
                        data['track'] = str(data['track'])
                    line = line.replace('{{ data.' + item + ' }}', data[item])
            self.html += line
        f.close()
        return self.html


    def write_page(self):
        f = open(self.filepath + '.html', "w")
        f.write(self.html)
        f.close()
        return True


def get_data(data_source):
    f = open(data_source, "r")
    raw = f.read()
    content = json.loads(raw)
    f.close()
    return content


for item in get_data('songs.json'):
    if item['lyrics'] != 'null':
        filename = item['filename']
        p = Page('lyrics', filename)
        p.render_template(item)
        p.write_page()
        index.append(filename)

# write index
index_data = { "about": "", "credits": "", "title": "index", "links": index }
p = Page('lyrics', 'index')
p.render_template(index_data)
p.write_page()

