#! /bin/env bash

current_directory=`pwd`

#yum install -y zip


extjs_zip_file="ext-4.2.1-gpl.zip"
extjs_url="http://cdn.sencha.com/ext/gpl/$extjs_zip_file"
extjs_name=`echo $extjs_url | awk -F'[/]' 'END{print $NF}' | awk -F'[-]' 'BEGIN{name="";}{for(i=1;i<NF;i++){if(i==NF-1){name=name$i}else{name=name$i"-"}}}END{print name}'`


target_extjs_name="extjs"

declare -a project_libraries_names=("switch_application")
for project_name in ${project_libraries_names[@]}
do

 project_library_name="$project_name"_lib
 relative_extjs_lib_directory="../$project_library_name/extjs_lib"
 
 cd $relative_extjs_lib_directory
  
 if [[ ! -d ./$target_extjs_name ]]
 then
  
  ##############################
  # get extjs library          #
  ##############################
  wget $extjs_url
  unzip $extjs_zip_file
  rm -rf $extjs_zip_file
  matched_name=`ls | grep -i $extjs_name`
  mv $matched_name "./$target_extjs_name"

 fi


 cd $current_directory

done


#wget http://cdn.sencha.com/ext/gpl/ext-4.2.1-gpl.zip


