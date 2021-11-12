import xml.etree.ElementTree as ET


def headlines(design = "APEX"):
    # parse ork file
    fname = design + ".ork"
    tree = ET.parse(fname)
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
    summary = str()

    summary += f"**Motor** selected for use: {motor} \n"
    summary += f"**Apogee:** {apogee} m \n"
    summary += f"**Max speed:** {maxvel} m/s \n"
    summary += f"**Max acceleration:** {maxacc} m/s^2 \n"
    summary += f"**Flight duration:** {flightdur} s \n"
    summary += f"**Ground hit velocity:** {groundhit} m/s \n"
    summary += f"**Dry mass:** {mass} kg"

    return summary

def update_readme(design = "APEX"):
    # get data to update
    summary = headlines(design)
    # print(summary)
    # initialise markers
    start = f"<!-- {design} Info Start -->"
    end = f"<!-- {design} Info End -->"

    # read existing info 
    with open("README.md", 'r') as file:
        readme = file.read()

    # get marker location
    startin = readme.find(start) + len(start)
    endin = readme.find(end)

    # get info box from full file
    box = readme[startin:endin]
    box = box.strip()
    print(box)
    
    # replace existing info with updated
    readme = readme.replace(box, summary)
    print(readme)

    # write new readme
    with open("README.md", 'w') as file:
        file.write(readme)    


apex = headlines("APEX")
# print (apex)

update_readme("APEX")