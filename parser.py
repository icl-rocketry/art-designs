import xml.etree.ElementTree as ET

# parse ork file
tree = ET.parse("APEX.ork")
root = tree.getroot()

# split into physical attributes and simulation results
rocket = root[0]
sims = root[1]


# get motor
for element in rocket.iter('motorconfiguration'):
    motor = element[0].text

# sum mass components
mass = 0

for element in rocket.iter('overridemass'):
    mass = mass + float(element.text)

for element in rocket.iter('mass'):
    mass = mass + float(element.text)

mass = round(mass, 3) # we can only measure to nearest gram anyway

# extract simulation data
apogee = sims[0].find('flightdata').attrib['maxaltitude']
maxvel = sims[0].find('flightdata').attrib['maxvelocity']
maxacc = sims[0].find('flightdata').attrib['maxacceleration']
flightdur = sims[0].find('flightdata').attrib['flighttime']
groundhit = sims[0].find('flightdata').attrib['groundhitvelocity']

# other extractable params - max mach, time to apogee, launch rod vel, deployment vel
# see raw xml to get attrib keys


# pretty print data

print(f"Motor selected for use: {motor}")
print(f"Apogee: {apogee}m")
print(f"Max speed: {maxvel}m/s")
print(f"Max acceleration: {maxacc}m/s^2")
print(f"Flight duration: {flightdur}s")
print(f"Ground hit velocity: {groundhit} m/s")
print(f"Wet mass: {mass}kg")
