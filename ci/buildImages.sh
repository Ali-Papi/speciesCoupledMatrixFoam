#!/bin/bash -e
# Copyright
#     WIKKI BRASIL C E LTDA. All rights reserved
cd "${0%/*}" || exit 1                        # Run from this directory


### Functions definitions ###

# Valid options
function valid_build_image_options()
{
echo -e "Valid options to build images:
1: Just base image with $FOAM_VERSION
2: Just porousMedia image (needs base image)
12: Both"
}

function help()
{
echo -e "usage: ./Allcreate <output tag version> <image to buid: 1, 2, 12> <optional entry: input image tag version>
where:
       output tag version   the tag to be used in the docker image version builded.
       image to build        which image to be buided. Be sure the version tag on FROM for Dockerfiles
                            for ${IMAGE_BASE_NAME}_porousmedia is correct.

   Optional entries:
       input tag version    the tag to be used in the Dockerfile FROM image for ${IMAGE_BASE_NAME}_porousmedia
                            image. If not provided use the  value from output
                            tag version.
Example usage

\$ ./buildImages.sh --os=ubuntu --os_tag=20.04 --foam_version=foam_extend_5.0 --input_tag=v01 --output_tag=v01 --images_to_build=12

This command build a base image with ubuntu 20.04, FOAM extend 5.0, and the porousMedia code."
}

function images_to_build()
{
  if [[ ! $IMAGES_TO_BUILD =~ ^\s?[1-4]{1,2}$ ]]
      then
      echo "No valid build image option, valid options are: 1, 2, or 12"
      valid_build_image_options
      exit 1
  fi
}

TEMP=$(getopt -o o::t::f::i::g::b:h --long os::,os_tag::,foam_version::,input_tag::,output_tag::,images_to_build::,help -n 'buildImages.sh' -- "$@")

if [ $# == 0 ] ; then echo "No arguments were given, displaying help message"; help >&2 ; exit 1 ; fi

# Note the quotes around '$TEMP': they are essential!
eval set -- "$TEMP"

# Default values
OS=ubuntu
OS_TAG=20.04
FOAM_VERSION=foam_extend_5.0

# Variables assignment
while true ; do
    case "$1" in
        -o|--os)
            case "$2" in
                "") echo "Invalid Option for -o,--os"; shift 2 ;;
                *)  OS=$2 ; shift 2 ;;
            esac ;;
        -t|--os_tag)
            case "$2" in
                "") echo "Invalid Option -t, --os_tag"; shift 2 ;;
                *)  OS_TAG=$2 ; shift 2 ;;
            esac ;;
        -f|--foam_version)
            case "$2" in
                "") echo "Invalid Option -f, --foam_version"; shift 2 ;;
                *)  FOAM_VERSION=$2 ; shift 2 ;;
            esac ;;
        -i|--input_tag)
            case "$2" in
                "") echo "Invalid Option -i, --input_tag"; shift 2 ;;
                *)  INPUT_TAG=$2 ; shift 2 ;;
            esac ;;
        -g|--output_tag)
            case "$2" in
                "") echo "Invalid Option -g, --output_tag"; shift 2 ;;
                *)  OUTPUT_TAG=$2 ; shift 2 ;;
            esac ;;
        -b|--images_to_build)
            case "$2" in
                "") valid_build_image_options && exit 1; shift 2 ;;
                *)  IMAGES_TO_BUILD=$2 ; shift 2 ;;
            esac ;;
        -h|--help) help; exit ;;
        --) shift ; break ;;
        *) echo "Invalid option name" ; exit 1 ;;
    esac
done

# Compound variable names
IMAGE_BASE_NAME=$OS$OS_TAG-$FOAM_VERSION

echo -e "Building Option: $IMAGES_TO_BUILD    Output tag version: $OUTPUT_TAG    Input tag version: $INPUT_TAG\n"


if [[ $IMAGES_TO_BUILD =~ [1] ]]
then
    IMAGE_NAME=wikkibrasil/$IMAGE_BASE_NAME:$OUTPUT_TAG
    DOCKERFILE=$IMAGE_BASE_NAME.dockerfile
    echo $DOCKERFILE
    echo "------------------------------------------------"
    # Test for Dockerfile
    if [ -f $DOCKERFILE ]
    then
        echo "Dockerfile for $IMAGE_BASE_NAME OK..."
    else
        echo "Dockerfile for $IMAGE_BASE_NAME does not exist..." >&2
        exit 1
    fi

    echo "Creating $OS $OS_TAG + $FOAM_VERSION image... tag version: $OUTPUT_TAG"
    docker build -t wikkibrasil/$IMAGE_BASE_NAME:$OUTPUT_TAG --build-arg OS_TAG=$OS_TAG --build-arg OS=$OS  -f $DOCKERFILE .
fi

# Create porousMedia image
if [[ $IMAGES_TO_BUILD =~ \s?[2] ]]
then
    IMAGE_NAME=wikkibrasil/${IMAGE_BASE_NAME}_porousmedia:$OUTPUT_TAG
    DOCKERFILE=${IMAGE_BASE_NAME}_porousmedia.dockerfile
    echo "------------------------------------------------"
    # Test for Dockerfile
    if [ -f $DOCKERFILE ]
    then
        echo "Dockerfile for $IMAGE_NAME OK..."
    else
        echo "Dockerfile for $IMAGE_NAME does not exist..." >&2
        exit 1
    fi

    echo "Creating porousMedia image... tag version : $OUTPUT_TAG  from input tag version: $INPUT_TAG"
    cd ..
    docker build -t $IMAGE_NAME --build-arg INPUT_TAG=$INPUT_TAG --build-arg IMAGE_BASE_NAME=$IMAGE_BASE_NAME -f ci/$DOCKERFILE .
fi
