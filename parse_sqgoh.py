from bs4 import BeautifulSoup
import csv
import argparse

parser = argparse.ArgumentParser(description='Parase SWGOH.gg HTML')
parser.add_argument('infile', type=argparse.FileType('r'))
parser.add_argument('outfile', type=argparse.FileType('w'))

args = parser.parse_args()

# file = open("/Users/rick/code/swgoh/SpectreCөmpanySquadTemplatesSWGOH.GG.htm", "r")
soup = BeautifulSoup(args.infile, 'html.parser')

data = []
split = []

table = soup.tbody.find_all('tr')

for row in table:
    out_row = []
    for cell in row.find_all('td'):
        val = cell.text.strip()
        if val:
            if val.find("* G") == 1:
                for entity in val.split():
                    out_row.append(entity)
            else:
                out_row.append(val)
        else:
            out_row.append(",")
            out_row.append(",")
            out_row.append(",")
    data.append(out_row)

writer = csv.writer(args.outfile, lineterminator='\n')
writer.writerows(data)

