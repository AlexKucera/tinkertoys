#!/usr/bin/env bash

# basic Nuke render command line

/Applications/Nuke7.0v5/NukeX7.0v5.app/NukeX7.0v5 -x -m 8 -f --gpu -F 20-299 /Volumes/ProjectsRaid/WorkingProjects/spacedigital/space-2013_001-castrol_truck_engine/work/nuke/12sec_v003_comp_v03.nk
/Applications/Nuke7.0v5/NukeX7.0v5.app/NukeX7.0v5 -x -m 8 -f --gpu /Volumes/ProjectsRaid/WorkingProjects/spacedigital/space-2013_001-castrol_truck_engine/work/nuke/Component-Life-V001-MW_comp_v04_wet.nk
/Applications/Nuke7.0v5/NukeX7.0v5.app/NukeX7.0v5 -x -m 8 -f --gpu /Volumes/ProjectsRaid/WorkingProjects/spacedigital/space-2013_001-castrol_truck_engine/work/nuke/Fuel-Consumption-V001-MW_comp_v03_dry.nk
/Applications/Nuke7.0v5/NukeX7.0v5.app/NukeX7.0v5 -x -m 8 -f --gpu /Volumes/ProjectsRaid/WorkingProjects/spacedigital/space-2013_001-castrol_truck_engine/work/nuke/Fuel-Consumption-V001-MW_comp_v03_wet.nk
