#!/usr/bin/env bash
#goes into /etc/

/bin/launchctl setenv NEXUS_ASSET /Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/modo/content/assets
/bin/launchctl setenv NEXUS_CONTENT /Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/modo/content
/bin/launchctl setenv NEXUS_LICENSE /Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/modo/user_resources/alex/license
/bin/launchctl setenv NEXUS_PREFS /Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/modo/user_resources/alex/os_spec
/bin/launchctl setenv NEXUS_TEMP /Volumes/SSD/Cache/modo/temp
/bin/launchctl setenv NEXUS_USER /Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/modo/user_resources/alex
/bin/launchctl setenv PATH /usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin:/usr/X11/bin:/opt/local/bin:/usr/local/git/bin:/Applications/Deadline/Resources/bin
/bin/launchctl setenv NUKE_TEMP_DIR /Volumes/SSD/Cache/Nuke
/bin/launchctl setenv NUKE_PATH /Volumes/ProjectsRaid/x_Pipeline/x_AppPlugins/Nuke/plugins 