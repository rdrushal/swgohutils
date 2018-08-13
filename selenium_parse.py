from bs4 import BeautifulSoup
import csv
import argparse
import re

parser = argparse.ArgumentParser(description='Parase SWGOH.gg HTML using selenium')
# parser.add_argument('infile', type=argparse.FileType('r'))
parser.add_argument('outfile', type=argparse.FileType('w'))

args = parser.parse_args()

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LoginURL="https://swgoh.gg/accounts/login/"
# Update this for the specific squad you're after.
#TODO: Iterate through all HSTR squads to get them
URL="https://swgoh.gg/g/40213/spectrecompany/squad-templates/42300/"
user="<<INSERT SWGOH USER NAME HERE"
pswd="<<INSERT SWGOH PASSWORD HERE"

#This probably needs updated for Windows to firefox, chrome, or IE. Havent tried this yet.
driver = webdriver.Safari()
driver.get(LoginURL)

assert "SWGOH" in driver.title

username = driver.find_element_by_id("id_username")
username.clear()
username.send_keys(user)

passwd = driver.find_element_by_id("id_password")
passwd.clear()
passwd.send_keys(pswd)
passwd.submit()

# Go to Spegre
driver.get(URL)
html = driver.page_source

# file = open("/Users/rick/code/swgoh/SpectreCөmpanySquadTemplatesSWGOH.GG.htm", "r")
soup = BeautifulSoup(args.infile, 'html.parser')

# Extract Squad Character Names
# Added the regex to help account for safari v. chrome diffs
characters = [x["data-name"] for x in soup.thead.find_all('th', class_=re.compile(r'text-center squad-character'))]

# Construct header
header = []
header.append("Player")
header.append("Team Power")
for character in characters:
    header.append(character + " Star Level")
    header.append(character + " Gear Level")
    header.append(character + " Speed")
    header.append(character + " Zeta Count")
    header.append(character + " Zeta List")                

data = []
split = []
val = ""

data.append(header)

table = soup.tbody.find_all('tr')

for row in table:
    out_row = []
    for cell in row.find_all('td'):
        
        #GET Character Zetas
        zetas_list = [x["title"] for x in cell.find_all('img')]
        zetas = ':'.join(zetas_list)

        #Get character stats
        val = cell.text.strip()

        if val:
            if val.find("* G") == 1:
                for entity in val.split():
                    out_row.append(entity.strip('()*G'))
                
                # Append Zeta Count to character stats
                out_row.append(len(zetas_list))

                # Append Zeta name to character stats
                out_row.append(zetas)
                
            else:
                out_row.append(val)
        else:
            #Filler if player does not have toon
            out_row.append('')
            out_row.append('')
            out_row.append('')
            out_row.append('')
            out_row.append('')        
        
    data.append(out_row)

writer = csv.writer(args.outfile, lineterminator='\n')
writer.writerows(data)

