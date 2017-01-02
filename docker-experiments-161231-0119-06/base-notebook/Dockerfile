# Based on Jupyter's "opinionated stacks of ready-to-run" applications,
# https://github.com/jupyter/docker-stacks,
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

FROM crypticlabs/anaconda3

MAINTAINER Cryptic Labs <kaben.nanlohy@gmail.com>

ENV SHELL /bin/bash
ENV NB_USER cryptic
ENV NB_UID 1000
ENV GRANT_SUDO yes
ENV HOME /home/$NB_USER

# Add user ("cryptic") with uid=1000 and in "users" group.
RUN useradd -m -s /bin/bash -N -u $NB_UID $NB_USER \
 && mkdir -p $CONDA_DIR \
 && chown $NB_USER $CONDA_DIR

# Enable passwordless sudo. Note: this is not secure; don't enable this
# notebook server when it will be used by untrusted users, or when it will be
# used on a public-facing host.
RUN echo "$NB_USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook

# Setup user's home directory.
USER $NB_USER
RUN mkdir /home/$NB_USER/work && \
    mkdir /home/$NB_USER/.jupyter && \
    echo "cacert=/etc/ssl/certs/ca-certificates.crt" > /home/$NB_USER/.curlrc

# Install software dependencies using conda, the Anaconda package manager.
USER root
RUN $CONDA_DIR/bin/conda install --yes \
    jupyterhub \
    notebook \
    pandas-datareader \
    pandoc \
    pandocfilters \
    pypandoc \
 && $CONDA_DIR/bin/conda install --yes --channel anaconda-nb-extensions \
    nbbrowserpdf \
 && $CONDA_DIR/bin/conda clean -tipsy

EXPOSE 8888
WORKDIR /home/$NB_USER/work

# Configure container startup.
ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD ["start-notebook.sh"]

# Add local files as late as possible to avoid cache busting
COPY start.sh /usr/local/bin/
COPY start-notebook.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter_notebook_config.py /home/$NB_USER/.jupyter/
RUN chown -R $NB_USER:users /home/$NB_USER/.jupyter

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_USER
