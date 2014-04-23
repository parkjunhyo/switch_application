#! /bin/env bash


################################################
# target absolute directory search             #
################################################
current_directory=`pwd`
cd ../../switch_application
target_absolute_directory=`pwd`
cd $current_directory

declare -a directories=`ls`

for directory_name in ${directories[@]}
do


 if [[ -d $current_directory/$directory_name ]]
 then

  cd $current_directory/$directory_name

  declare -a files=`ls`

  for file_name in ${files[@]}
  do

   if [[ -f $current_directory/$directory_name/$file_name ]]
   then

    ##### generate target standard path    
    if [[ $directory_name == 'builder_shell_command' ]]
    then
     standard_directory="/usr/bin"
     matched_line=`cat $current_directory/$directory_name/$file_name | grep -ni '^form_file=' | awk -F'[:]' 'END{print $1}'`
     sed -i '/^form_file=/d' $current_directory/$directory_name/$file_name
     sed -i $matched_line'i \form_file=\"'$target_absolute_directory/configuration_templates/$file_name'\"' $current_directory/$directory_name/$file_name
    else
     standard_directory=$target_absolute_directory/$directory_name
     if [[ ! -d $standard_directory ]]
     then
      mkdir -p $standard_directory
     fi
    fi

    ##### make a link
    linking_file_route="$standard_directory/$file_name"
    if [[ -f $linking_file_route ]]
    then
     rm -rf $linking_file_route
     echo "$linking_file_route ..... removed"
    fi
    ln $current_directory/$directory_name/$file_name $linking_file_route

  
   fi

  done
  
  cd $current_directory

 fi

done ## end of "for directory_name in ${directories[@]}"
exit
