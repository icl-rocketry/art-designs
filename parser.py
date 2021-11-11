import xml.etree.ElementTree as ET

tree = ET.parse("APEX.ork")
root = tree.getroot()

rocket = root[0]
sims = root[1]

for child in rocket:
    print(child.tag)

for element in rocket.iter('motorconfiguration'):
    motor = element[0].text

length = 0
for element in rocket.iter('length'):
    length = length + float(element.text)

print(motor)
print(length)