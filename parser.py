import xml.etree.ElementTree as ET
import subprocess

def headlines(design = "APEX"):
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
    '''try:
        mass = 0
        for element in rocket.iter('overridemass'):
            mass += float(element.text)
        for element in rocket.iter('mass'):
            mass += float(element.text)
        mass = round(mass, 3) # we can only measure to nearest gram anyway
    except:
        mass = "Mass calculation not available" '''

    mass = 0
    el1 = rocket.iter('overridemass')
    if (el1 != []): 
        mass += float(el1.text)
    el1 = rocket.iter('mass')
    if (el1 != []):
        mass += float(el1.text)
    mass = round(mass, 3) # we can only measure to nearest gram anyway

    # extract simulation data
    apogee    = simdata (sims,'flightdata','maxaltitude')
    maxvel    = simdata (sims, 'flightdata','maxvelocity')
    maxacc    = simdata (sims, 'flightdata','maxacceleration')
    flightdur = simdata (sims, 'flightdata', 'flighttime') 
    groundhit = simdata (sims, 'flightdata', 'groundhitvelocity')
    maxmach   = simdata (sims,'flightdata', 'maxmach')
    timetoapp = simdata (sims, 'flightdata', 'timetoapogee')

    # other extractable params - max mach, time to apogee, launch rod vel, deployment vel
    # see raw xml to get attrib keys

    # pretty print data
    sumlist = [f"**Motor selected for use:** {motor} <br/> \n", f"**Apogee:** {apogee} m <br/> \n", f"**Max speed:** {maxvel} m/s <br/> \n", f"**Max acceleration:** {maxacc} m/s^2 <br/> \n", f"**Flight duration:** {flightdur} s <br/> \n", f"**Ground hit velocity:** {groundhit} m/s <br/> \n", f"**Dry mass:** {mass} kg "]
    summary = sumlist.join('')
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
    hash = subprocess.run("git log -1 --pretty=format:\"%h\"", stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    author = subprocess.run("git log -1 --pretty=format:\"%an\"", stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    
    # create commit info
    info = f"README updated after commit {hash} by {author}"
    print(info)

    subprocess.run(f"git commit -am \"{info}\"", shell=True)
    subprocess.run("git push origin HEAD", shell=True)
    
create_commit("APEX")
create_commit("ASCENSION")