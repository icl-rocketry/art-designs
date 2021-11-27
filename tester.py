import csv
import xml.etree.ElementTree as ET

def headlines(design):
    # parse ork file
    fname       = design + ".ork"
    tree        = ET.parse(fname)
    root        = tree.getroot()
    sims        = root[1]
    launchAngle = sims[0].find('conditions').find('launchrodangle').text
    apogee      = sims[0].find('flightdata').attrib['maxaltitude']
    return ([apogee, launchAngle])

with open('data.csv', mode = 'a+') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(headlines("APEX"))
