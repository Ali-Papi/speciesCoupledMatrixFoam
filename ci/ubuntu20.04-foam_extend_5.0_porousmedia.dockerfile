ARG IMAGE_BASE_NAME=ubuntu20.04-foam_extend_5.0 INPUT_TAG=v01
FROM wikkibrasil/${IMAGE_BASE_NAME}:${INPUT_TAG}
LABEL maintainer="Wikki Brasil C E LTDA"

SHELL ["/bin/bash", "-c"]

# # # Using user wikki and its home dir
USER      wikki
WORKDIR   /home/wikki
ENV       USER         wikki
ENV       HOME         /home/wikki

# # # Compile porousMedia
COPY --chown=wikki:wikki . $HOME/porousMedia

RUN cd $HOME/porousMedia/                                                                                          && \
python -m pip install -r tests/requirements.txt                                                                    && \
source $HOME/foam/foam-extend-5.0/etc/bashrc                                                                       && \
./Allwclean                                                                                                        && \
./Allwmake -j                                                                                                      && \
echo 'export USER=wikki'                                                                 >> $HOME/.bashrc          && \
echo 'source $HOME/foam/foam-extend-5.0/etc/bashrc'                                      >> $HOME/.bashrc          && \
echo 'echo "Using OpenFOAM-"$WM_PROJECT_VERSION'                                         >> $HOME/.bashrc          && \
echo 'echo "OpenFOAM MPI version:" $FOAM_MPI'                                            >> $HOME/.bashrc          && \
echo 'echo "Python version:" $(python3 --version)'                                       >> $HOME/.bashrc          && \
cp $HOME/.bashrc $HOME/.bashrc_pm                                                                                  && \
sed -i -e 1,117d $HOME/.bashrc_pm
