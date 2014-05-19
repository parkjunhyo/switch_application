#! /bin/env bash

current_directory=`pwd`

django_home="../django_home"
django_source="https://www.djangoproject.com/m/releases/1.6/Django-1.6.2.tar.gz"
django_rest_framework_gitsource="https://github.com/tomchristie/django-rest-framework.git"
django_cors_headers_gitsource="https://github.com/ottoyiu/django-cors-headers.git"

if [[ ! `which git` ]]
then
 echo "git is not installed"
 exit
fi

## requirement packages
yum install -y screen MySQL-python python-setuptools

## re-define the version management.
## django 
tmp_name=`mktemp` 
django_targz=`echo $django_source | awk -F'[/]' 'END{print $NF}'`
echo $django_targz > $tmp_name
sed -i 's/'.tar.gz'//' $tmp_name
django_version=`cat $tmp_name`

## django rest framework
django_git=`echo $django_rest_framework_gitsource | awk -F'[/]' 'END{print $NF}'`
echo $django_git > $tmp_name
sed -i 's/'.git'//' $tmp_name
django_rest_framework=`cat $tmp_name`

## django cors headers
django_git=`echo $django_cors_headers_gitsource | awk -F'[/]' 'END{print $NF}'`
echo $django_git > $tmp_name
sed -i 's/'.git'//' $tmp_name
django_cors_headers=`cat $tmp_name`

if [[ ! -d $django_home ]]
then
 mkdir -p $django_home
 chmod 777 $django_home
fi

if [[ ! -d $django_home/django_source ]]
then
 cd $django_home
 wget $django_source
 tar xvfz $django_targz
 rm -rf ./$django_targz
 mv $django_version ./django_source
 cd $current_directory 
fi

if [[ ! `which django-admin.py` ]]
then
 cd $django_home/django_source
 python setup.py install
 cd $current_directory
else
 version=`django-admin.py --version | awk 'END{print $NR}'`
 if [[ ! `echo $django_version | grep $version` ]]
 then
  cd $django_home/django_source
  python setup.py install
  cd $current_directory
 fi
fi

if [[ ! -d $django_home/$django_rest_framework ]]
then
 cd $django_home
 git clone $django_rest_framework_gitsource
 if [[ ! -d ./$django_rest_framework ]]
 then
  echo "django rest framework download was failed" 
  exit
 fi
 cd $django_rest_framework
 python setup.py install
 cd $current_directory
fi

if [[ ! -d $django_home/$django_cors_headers ]]
then
 cd $django_home
 git clone $django_cors_headers_gitsource
 if [[ ! -d ./$django_cors_headers ]]
 then
  echo "django cors header download was failed"
  exit
 fi
 cd $django_cors_headers
 python setup.py install
 cd $current_directory
fi

############################################################################
####                 django project creationg                          #####
############################################################################
cd $current_directory
django_project="switch_application"
django_project_relative_path="../$django_project"
if [[ ! -d $django_project_relative_path ]]
then
 cd ..
 django-admin.py startproject $django_project
 cd $current_directory
fi

############################################################################
####                 djnago application creation                       #####
############################################################################
declare -a application_names=("net_builder" "ip_manager")
for application_name in ${application_names[@]}
do

 if [[ ! -d $django_project_relative_path/$application_name ]]
 then
  cd $django_project_relative_path
  python manage.py startapp $application_name
  cd $current_directory
 fi
 if [[ ! -d $django_project_relative_path/$application_name/MyProgram ]]
 then
  mkdir -p $django_project_relative_path/$application_name/MyProgram
  touch $django_project_relative_path/$application_name/MyProgram/__init__.py
 fi

done

rm -rf $tmp_name
