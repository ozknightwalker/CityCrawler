from __future__ import unicode_literals

import json
import csv


def write_to_json(name, content, code='w', ext='json'):
    content = json.dumps(content, indent=4, ensure_ascii=False)
    write_to_file(name, content, code, ext=ext)


def write_to_file(name, content, code='w', ext='json'):
    file_name = '{}.{}'.format(name, ext)
    with open(file_name, code, encoding='utf8') as out_file:
        out_file.write(content)


def dict_to_csv(name, obj, mode='a'):
    file_name = '{}.csv'.format(name)
    with open(file_name, mode) as outfile:
        w = csv.DictWriter(outfile, obj.keys())
        w.writerow(obj)


def read_csv(name, fieldnames=()):
    file_name = '{}.csv'.format(name)
    with open(file_name, 'r') as readFile:
        reader = csv.DictReader(readFile, fieldnames=fieldnames)
        out = [row for row in reader]
    return out
