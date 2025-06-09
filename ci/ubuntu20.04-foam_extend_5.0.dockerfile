ARG OS=ubuntu OS_TAG=22.04
FROM ${OS}:${OS_TAG}
LABEL maintainer="Wikki Brasil C E LTDA <petrofoam@wikki.com.br>"

ENV TZ=America/BazilBrasilia
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt update && apt install -y tzdata
ENV DEBIAN_FRONTEND=noninteractive


SHELL ["/bin/bash", "-c"]

# # # Update and install dependencies, parallel and utilities
RUN apt-get update && apt-get dist-upgrade -y                     && \
apt-get install -y build-essential flex bison cmake zlib1g-dev       \
libboost-system-dev libboost-thread-dev libopenmpi-dev git-core      \
openmpi-bin libreadline-dev libncurses-dev libxt-dev gnuplot  curl   \
libscotch-dev libcgal-dev openssl time vim wget ssh sudo gfortran && \
apt-get clean && apt-get autoremove --purge                       && \
rm -rf /var/lib/apt/lists/*

# # # Install dependencies, python and create a sudo passwordless wikki user
RUN apt-get update                                                    && \
apt-get install -y net-tools libgl1-mesa-glx libpng16-16                 \
git libssl-dev zlib1g-dev build-essential libjpeg-dev libbz2-dev         \
xz-utils liblzma-dev bc libatlas-base-dev libatlas-base-dev              \
libblas-dev liblapack-dev make xvfb  python-is-python3  python3-pip   && \
apt-get clean && apt-get autoremove --purge                           && \
rm -rf /var/lib/apt/lists/*                                           && \
adduser --shell /bin/bash --disabled-password --gecos '' wikki        && \
passwd -d wikki                                                       && \
addgroup wikki sudo

# # # Using user wikki and its home dir
USER      wikki
WORKDIR   /home/wikki
ENV       USER         wikki
ENV       HOME         /home/wikki

# # # Get, build OpenFOAM & Third-Party, cleaning build
RUN mkdir /home/wikki/foam && cd /home/wikki/foam             && \
git clone git://git.code.sf.net/p/foam-extend/foam-extend-5.0 && \
cd foam-extend-5.0                                            && \
source etc/bashrc                                             && \
./Allwmake  -j -q
