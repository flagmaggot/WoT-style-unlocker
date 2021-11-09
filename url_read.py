url = "https://wiki.wargaming.net/en/Tank:R160_T_50_2"

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
#myURL = urlopen("https://wiki.wargaming.net/en/Tank:R160_T_50_2")
#print(myURL.read())

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




URL = "https://wiki.wargaming.net/en/Tank:R160_T_50_2"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

#tier = soup.find_all("div", {"class": "b-performance_position"})

tier2 = soup.select("a[href*=Tier]")[0]

tier = tier2.get_text().replace("Tier ","")

print(romanToInt(tier))



# try:
    # found = re.search('Category_(.+?)_Tanks', tier2.get_text()).group(1)
# except AttributeError:
    # # AAA, ZZZ not found in the original string
    # found = 'mno' # apply your error handling

# print(found)

#m = re.search('Tier_(.+?)_Tanks', tier2)
#print(m)
#print(tier)
#print(soup.prettify())
#class="b-performance_position"

