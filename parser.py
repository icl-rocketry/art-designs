import xml.etree.ElementTree as ET
import subprocess
import sys

design = sys.argv[1]      # getting cmd line argument 
def headlines(design):
    # parse ork file
    fname = design + ".ork"
    tree = ET.parse(fname)
    root = tree.getroot()

    # split into physical attributes and simulation results
    rocket = root[0]
    sims   = root[1]

    def simdata(rootObj,dataset,att):
        try:
            res = rootObj[0].find(dataset).attrib[att]
        except: 
            res = "Error parsing simulation/rocket data"
        return res 
    
    # get motor
    motor   = "motor not found"
    element = rocket.iter('motorconfiguration')
    if (element != []):
        motor = element[0].text

    # sum mass components

    mass = 0
    for elementkey in [rocket.iter('overridemass'),rocket.iter('mass')]:
        for element in elementkey:
            mass += float(element.text)
    mass = round(mass, 3) # we can only measure to nearest gram anyway
    if mass == 0 :
        mass = "mass not found"
    

    # extract simulation data
    apogee    = simdata (sims,'flightdata','maxaltitude')
    maxvel    = simdata (sims, 'flightdata','maxvelocity')
    maxacc    = simdata (sims, 'flightdata','maxacceleration')
    flightdur = simdata (sims, 'flightdata', 'flighttime') 
    groundhit = simdata (sims, 'flightdata', 'groundhitvelocity')
    maxmach   = simdata (sims,'flightdata', 'maxmach')
    timetoapp = simdata (sims, 'flightdata', 'timetoapogee')

    launchAngle = sims[0].find('launchrodangle')[0]

    # other extractable params - max mach, time to apogee, launch rod vel, deployment vel
    # see raw xml to get attrib keys

    # pretty print data
    sumlist = "**Motor selected for use:** {0} <br/> \n **Apogee:** {1} m <br/> \n **Max speed:** {2} m/s <br/> \n **Max acceleration:** {3} m/s^2 <br/> \n **Flight duration:** {4} <br/> \n **Ground hit velocity:** {5} m/s <br/> \n **Dry mass:** {6} kg "
    summary = sumlist.format(motor, apogee, maxvel, maxacc, flightdur, groundhit, mass)
    return summary

def update_readme(design):
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

def create_commit(design):
    # create new readme
    #update_readme(design)

    # get previous commit info
    hash = subprocess.run("git log -1 --pretty=format:\"%h\"", stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    author = subprocess.run("git log -1 --pretty=format:\"%an\"", stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    
    # create commit info
    info = f"README updated after commit {hash} by {author}"
    print(info)

    subprocess.run(f"git commit -am \"{info}\"", shell=True)
    subprocess.run("git push origin HEAD", shell=True)
    
create_commit("APEX")
