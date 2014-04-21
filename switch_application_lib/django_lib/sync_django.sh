#! /bin/env bash

current_directory=`pwd`

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

    re_file_name=`echo $file_name | awk -F'[!@$%+]' 'BEGIN{dirname="";}{for(i=1;i<=NF;i++){dirname=dirname"/"$i;}}END{print dirname}'`
    target_origin_filepath="../../../switch_application/$directory_name$re_file_name"
    represent_linking_filepath="$current_directory/$directory_name/$file_name"

    if [[ -f $target_origin_filepath ]]
    then
     rm -rf $target_origin_filepath
     echo "$target_origin_filepath ..... removed"
    fi
    ln $represent_linking_filepath $target_origin_filepath
  
   fi

  done
  
  cd $current_directory

 fi

done ## end of "for directory_name in ${directories[@]}"
exit
