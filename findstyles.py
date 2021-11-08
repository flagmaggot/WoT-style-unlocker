import json
import os
import copy
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
from io import BytesIO
from typing import List, Tuple

from flask import Flask, render_template, request, send_file
from whitenoise import WhiteNoise

BASE_DIR = os.path.dirname(__file__)

with open('source/display_names.json') as f:
    display_names = json.load(f)

    for root_dir, _, files in os.walk(os.path.join(BASE_DIR, 'source', 'res', 'scripts', 'item_defs', 'vehicles'), topdown=False):
        split_path = root_dir.split(os.sep)
        for file_name in files:
            with open(os.path.join(root_dir, file_name)) as f:
                lines = f.readlines()
                xml = ''.join(lines[:1] + lines[2:])
            

            root = ET.fromstring(xml)
            
            name, _ = os.path.splitext(root.tag)

            styles_set = set()
            for model_tag in root.iter(tag='models'):
                model_styles = model_tag.find('sets')
                
                if not model_styles:
                    continue

                for style in list(model_styles):
                    if style.tag != 'ProgressionStyle':
                        #if style.tag not in display_names:
                        #    print(style.tag)
                         
                        for dict in display_names:
                                print(dict)

                         
                            #print(display_names[name])
                            #print(style.tag)
                         # if style.tag not in display_names[name]["styles"][style.tag]:
                             # print(style.tag)
                             #print(file_name)
                        # for k in my_list:
                            # if k in my_dict:
                                # print k, my_dict[k]
                        #styles_set.add((style.tag, display_names[name]["styles"][style.tag]))