FROM ubuntu:16.04

MAINTAINER Cryptic Labs <kaben.nanlohy@gmail.com>

# Install software dependencies using apt-get, the Ubuntu package manager.
RUN apt-get update --fix-missing \
 && apt-get install -y \
    wget \
    bzip2 \
    ca-certificates \
    sudo \
    locales \
    libglib2.0-0 \
    libxext6 \
    libsm6 \
    libxrender1 \
    git \
    mercurial \
    subversion

# Install Anaconda.
RUN echo 'export PATH=/opt/conda/bin:$PATH' \
  > /etc/profile.d/conda.sh \
 && wget --quiet https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh -O ~/anaconda.sh \
 && /bin/bash ~/anaconda.sh -b -p /opt/conda \
 && rm ~/anaconda.sh

# Install Tini.
RUN apt-get install -y \
    curl \
    grep \
    sed \
    dpkg \
 && TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest \
  | grep -o "/v.*\"" \
  | sed 's:^..\(.*\).$:\1:'` \
 && curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" \
  > tini.deb \
 && dpkg -i tini.deb \
 && rm tini.deb \
 && apt-get clean

# Configure Conda for community-driven "conda-forge" recipes.
# Disable automatic updates.
ENV CONDA_DIR /opt/conda
ENV PATH $CONDA_DIR/bin:$PATH
RUN cd /tmp \
 && $CONDA_DIR/bin/conda config --system --add channels conda-forge \
 && $CONDA_DIR/bin/conda config --system --set auto_update_conda false \
 && $CONDA_DIR/bin/conda clean -tipsy

# Configure container startup.
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
