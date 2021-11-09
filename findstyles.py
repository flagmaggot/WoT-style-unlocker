import json
import os
import copy
import xml.etree.ElementTree as ET
import zipfile
from collections import defaultdict
from io import BytesIO
from typing import List, Tuple
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

from flask import Flask, render_template, request, send_file
from whitenoise import WhiteNoise

BASE_DIR = os.path.dirname(__file__)


def romanToInt(s):
      """
      :type s: str
      :rtype: int
      """
      roman = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,'IV':4,'IX':9,'XL':40,'XC':90,'CD':400,'CM':900}
      i = 0
      num = 0
      while i < len(s):
         if i+1<len(s) and s[i:i+2] in roman:
            num+=roman[s[i:i+2]]
            i+=2
         else:
            #print(i)
            num+=roman[s[i]]
            i+=1
      return num





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

            tank_class = ""

            for type in root.iter(tag='postProgressionTree'):
                if len(tank_class) == 0:
                        tank_class = "xxxx_LT_xxx"
                tank_class = type.text.strip()
                tank_class = tank_class.split('_')[1]
                
                
                if "ATSPG" in tank_class:
                    tank_class = "SPG"

            styles_set = set()
            
            styles = []
            
            all_name_elements = root.findall('.//sets')
            if bool(all_name_elements):
                if name.endswith("_bob"):
                    continue
                if name.endswith("_siege_mode"):
                    continue
                if name.endswith("_bot"):
                    continue
                
                #ROOT NAME
                #print("RootName: ",name)
                
                
                if len(tank_class) == 0:
                    tank_class = "LT"
                
                #Tank Class
                #print("    class: " + tank_class)
                
                #get tank tier
                URL = "https://wiki.wargaming.net/en/Tank:"+name
                page = requests.get(URL)
                soup = BeautifulSoup(page.content, "html.parser")
                tier2 = soup.select("a[href*=Tier]")[0]
                tier = tier2.get_text().replace("Tier ","")
                
                
                #tier = soup.find_all("div", {"class": "b-performance_position"})
                tank_name = soup.find("h1",id="firstHeading")
                
                start = '<h1 class="firstHeading" id="firstHeading"><span dir="auto">'
                end = '</span></h1>'

                #Tank NAME
                tank_name = re.search(r'<h1 class="firstHeading" id="firstHeading"><span dir="auto">(.*?)</span></h1>', str(tank_name)).group(1)
                #print("    name: "+re.search(r'<h1 class="firstHeading" id="firstHeading"><span dir="auto">(.*?)</span></h1>', str(tank_name)).group(1))
                
                
                #tankAttribList = ["name",tank_name]
                #tankAttribList = tankAttribList
                
                
                
                dictionary ={ 
                      "name": tank_name, 
                      "class": tank_class, 
                      "tier": romanToInt(tier)
                }
                
                #json_object = json.dumps(dictionary, indent = 4) 
                #print(json_object)
                
                
                TankDict = {}
                
                
                
                #print(tank_name)
                
                #TIER
                #print("    tier: "+str(romanToInt(tier)))
                #STYLES
                #print("    Styles")
                
                
                tank_style = {}
                tank_styles = {}
                for style_name in all_name_elements[0]:
                    #tank_styles.append(style_name.tag.style_name.tag)
                    tank_style[style_name.tag] = style_name.tag
                    #print("        style name: "+style_name.tag)
                
                #tank_styles[]=tank_style
                
                TankDict[name] = [dictionary,tank_style];
                print(TankDict)
            

                with open('data.json', 'w', encoding='utf-8') as f:
                    json.dump(TankDict, f, ensure_ascii=False, indent=4)
 