import xml.etree.ElementTree as ET

tree = ET.parse("APEX.ork")
root = tree.getroot()

rocket = root[0]
sims = root[1]

# for child in rocket:
#     print(child.tag)

for element in rocket.iter('motorconfiguration'):
    motor = element[0].text

length = 0




print(motor)


apogee = sims[0].find('flightdata').attrib['maxaltitude']
maxvel = apogee = sims[0].find('flightdata').attrib['maxvelocity']
maxacc = sims[0].find('flightdata').attrib['maxacceleration']
flightdur = sims[0].find('flightdata').attrib['flighttime']
groundhit = sims[0].find('flightdata').attrib['groundhitvelocity']

# other extractable params - max mach, time to apogee, launch rod vel, deployment vel
# see raw xml to get attrib keys
