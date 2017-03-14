 #!/bin/bash
 
 # Fixed known bug with pip & python installed with homebrew as per http://stackoverflow.com/a/41143578

 name=''
 target=''

 while getopts 'n:t:' flag; do
     case "${flag}" in
         n) name="${OPTARG}" ;;
         t) target="${OPTARG}" ;;
     esac
 done

 if [ -z "$target" ];
 then
     echo "Target parameter must be provided"
     exit 1
 fi

 if [ -z "$name" ];
 then
     echo "Name parameter must be provided"
     exit 1
 fi

 # current workaround for homebrew bug
 file=$HOME'/.pydistutils.cfg'
 touch $file

 /bin/cat <<EOM >$file
 [install]
 prefix=
 EOM
 # end of current workaround for homebrew bug

 pip install -I $name --target $target

 # current workaround for homebrew bug
 rm -rf $file
 # end of current workaround for homebrew bug