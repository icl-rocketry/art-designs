import xml.etree.ElementTree as ET
import subprocess

def headlines(design = "APEX"):
    # parse ork file
    fname = design + ".ork"
    tree = ET.parse(fname)
    root = tree.getroot()

    # split into physical attributes and simulation results
    rocket = root[0]
    sims = root[1]

    # get motor
    try:
        for element in rocket.iter('motorconfiguration'):
            motor = element[0].text
    except:
        motor = "No motor found"

    # sum mass components
    try:
        mass = 0
        for element in rocket.iter('overridemass'):
            mass = mass + float(element.text)
        for element in rocket.iter('mass'):
            mass = mass + float(element.text)
        mass = round(mass, 3) # we can only measure to nearest gram anyway
    except:
        mass = "Mass calculation not available"

    # extract simulation data
    try:
        apogee = sims[0].find('flightdata').attrib['maxaltitude']        
    except:
        apogee = "Error parsing simulation data"

    try:
        maxvel = sims[0].find('flightdata').attrib['maxvelocity']
    except:
        maxvel = "Error parsing simulation data"

    try:
        maxacc = sims[0].find('flightdata').attrib['maxacceleration']
    except:
        maxacc = "Error parsing simulation data"

    try:
        flightdur = sims[0].find('flightdata').attrib['flighttime']
    except:
        flightdur = "Error parsing simulation data"

    try:
        groundhit = sims[0].find('flightdata').attrib['groundhitvelocity']
    except:
        groundhit = "Error parsing simulation data"

    # other extractable params - max mach, time to apogee, launch rod vel, deployment vel
    # see raw xml to get attrib keys

    # pretty print data
    summary = str()

    summary += f"**Motor selected for use:** {motor} <br/> \n"
    summary += f"**Apogee:** {apogee} m <br/> \n"
    summary += f"**Max speed:** {maxvel} m/s <br/> \n"
    summary += f"**Max acceleration:** {maxacc} m/s^2 <br/> \n"
    summary += f"**Flight duration:** {flightdur} s <br/> \n"
    summary += f"**Ground hit velocity:** {groundhit} m/s <br/> \n"
    summary += f"**Dry mass:** {mass} kg "

    return summary

def update_readme(design = "APEX"):
    # get data to update
    summary = headlines(design)
    # print(summary)
    # initialise markers
    start = f"<!-- {design} Info Start -->"
    end = f"<!-- {design} Info End -->"
    # print(start)
    # read existing info 
    with open("README.md", 'r') as file:
        readme = file.read()

    # get marker location
    startin = readme.find(start) + len(start)
    endin = readme.find(end)

    # get info box from full file
    box = readme[startin:endin]
    box = box.strip()
    # print(box)
    
    # replace existing info with updated
    readme = readme.replace(box, summary)
    # print(readme)

    # write new readme
    with open("README.md", 'w') as file:
        file.write(readme)    

def create_commit(design = "APEX"):
    # create new readme
    #update_readme(design)

    # get previous commit info
    hash = subprocess.run("git log -1 --pretty=format:\"%h\"", stdout=subprocess.PIPE).stdout.decode('utf-8')
    author = subprocess.run("git log -1 --pretty=format:\"%an\"", stdout=subprocess.PIPE).stdout.decode('utf-8')
    
    # create commit info
    info = f"README updated after commit {hash} by {author}"
    print(info)
    

#update_readme("APEX")
#update_readme("ASCENSION")

create_commit("APEX")