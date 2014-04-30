#! /bin/env bash


################################################
# must have directory information              #
################################################
if [[ ! -d "/var/www/html" ]]
then
 echo "there is not /var/www/html, needs httpd"
 exit
fi

if [[ ! -d "./extjs" ]]
then
 echo "there is not ./extjs, get the extjs"
 exit
fi


################################################
# target absolute directory search             #
################################################
current_directory=`pwd`
project_name="switch_application"
project_path="/var/www/html/$project_name"

if [[ ! -d $project_path ]]
then
 mkdir -p $project_path
 chmod 755 $project_path
fi


declare -a directories=`ls`
for directory_name in ${directories[@]}
do
 if [[ -d $current_directory/$directory_name ]]
 then

  ###########################################
  # jump the directory not to make link     #
  ###########################################
  if [[ $directory_name == 'extjs' ]]
  then
   continue
  fi

  ###########################################
  # extjs symbolic link                     #
  ###########################################
  if [[ -d current_directory/$directory_name/extjs ]]
  then
   rm -rf $current_directory/$directory_name/extjs
   echo "$current_directory/$directory_name/extjs .... removed"
   ln -s ./extjs $current_directory/$directory_name/extjs
  fi

  ###########################################
  # symbolic link deleted!                  #     
  ###########################################
  if [[ -d $project_path/$directory_name ]]
  then
   echo "$project_path/$directory_name .... removed"
   rm -rf $project_path/$directory_name
  fi

  ###########################################
  # soft link connecting                    #
  ###########################################
  ln -s $current_directory/$directory_name $project_path/$directory_name


 fi
done


 
