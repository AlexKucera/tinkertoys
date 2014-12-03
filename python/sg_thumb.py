
import shotgun_api3 as api

from shotgun import Shotgun 
SERVER_PATH = 'https://babylondreams.shotgunstudio.com' # change this to https if your studio uses SSL
SCRIPT_NAME = 'pythonapi'
SCRIPT_KEY = '668ccbf1484e109b4ff5577d9dba5989d1e5fef4'
sg = Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)

sg.upload_thumbnail("Version", 52, "/Volumes/ProjectsRaid/WorkingProjects/spacedigital/space-2013_002-youngdracula_series5/img/comps/FD2-VFX-20/outsrc/FD2-VFX-20_outsrc_v01/FD2-VFX-20_outsrc_v01.0092.jpg")