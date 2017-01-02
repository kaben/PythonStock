# Based on Jupyter's "opinionated stacks of ready-to-run" applications,
# https://github.com/jupyter/docker-stacks,
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM crypticlabs/base-notebook:0.0.0

MAINTAINER Cryptic Labs <kaben.nanlohy@gmail.com>

USER root

# Install all OS dependencies for fully functional notebook server
RUN apt-get update \
 && apt-get install -yq --no-install-recommends \
    git \
    vim \
    jed \
    emacs \
    build-essential \
    python-dev \
    unzip \
    libsm6 \
    pandoc \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-fonts-recommended \
    texlive-generic-recommended \
    libxrender1 \
    inkscape \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_USER
