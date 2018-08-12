from bs4 import BeautifulSoup
import csv
import argparse

parser = argparse.ArgumentParser(description='Parase SWGOH.gg HTML')
parser.add_argument('infile', type=argparse.FileType('r'))
parser.add_argument('outfile', type=argparse.FileType('w'))

args = parser.parse_args()

# file = open("/Users/rick/code/swgoh/SpectreCөmpanySquadTemplatesSWGOH.GG.htm", "r")
soup = BeautifulSoup(args.infile, 'html.parser')

# Extract Squad Character Names
characters = [x["data-name"] for x in soup.thead.find_all('th', class_='text-center squad-character')]

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


len(header)



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

