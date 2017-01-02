# Docker experiments

This subdirectory contains an experimental Docker deployment of JupyterHub, Anaconda3, and Jupyter Notebook.

### JupyterHub Docker image
This provides a multi-user Jupyter notebook server hub which spawns, manages,
and proxies an isolated Anaconda3-based Jupyter Notebook server for each user.
It uses GitHub login for authentication.

(For more on JupyterHub:)
* https://jupyterhub.readthedocs.io/en/latest/
* https://github.com/jupyterhub/jupyterhub

### Custom Anaconda3 Docker image
This provides a base Anaconda3 installation for use in constructing Jupyter
Notebook images. It's based on the Ubuntu-16.04 Docker image, whereas the
official Anaconda3 Docker image is based on Debian. @kaben used Ubuntu instead
of Debian because we're more familiar with Ubuntu.

### Custom Jupyter Notebook Docker image
This is basic Jupyter Notebook single-user server image, which is instantiated
on a per-user basis by the JupyterHub container. It's based on the above custom
Anaconda3 image, whereas the official Jupyter Notebook stacks are minimal
Miniconda installations. @kaben used full Anaconda3 as the basis, because when
we're experimenting on our laptops, we're probably using Anaconda rather than
Miniconda.

This image provides passwordless sudo, which gives root access within each
per-user server instance. This is done to simplify experimentation and
development of our analytics platform. For now this is safe, because only
@carriere4 and @kaben are using these images.

However, we *must* disable this before giving access to users outside of
Cryptic Labs, or before deployment on a public-facing host.

### How to deploy:
This analytics platform can be deployed on any laptop or desktop computer for
which Docker is available, using the following steps.
* (One-time:) Install [Docker](https://docs.docker.com).
* (One-time:) Setup a GitHub OAuth application.
  * @kaben has created a GitHub OAuth application for development, and can
    provide JupyterHub config info needed to use it.
  * To setup your own:
    * GitHub docs:
      * https://developer.github.com/guides/basics-of-authentication/
      * https://developer.github.com/v3/oauth/
    * URL for creating a new GitHub OAuth application:
      https://github.com/settings/applications/new
    * Example settings:
      * Application name: pythonstock-dev-01
      * Homepage URL: https://github.com/carriere4/PythonStock
      * Application description: PythonStock development
      * Authorization callback URL: https://localhost:443/hub/oauth_callback
        * Note: this URL must exactly match the value set in environment
          variable `OAUTH_CALLBACK_URL` for JupyterHub configuration.
    * Upon successful creation, OAuth client "ID" and "secret" are provided.
      Record these; they will used to set environment variables
      `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` for JupyterHub
      configuration.

* (One-time:) Generate temporary, self-signed SSL certificate and key.

  * Note: we will eventually replace these with CrypticLabs SSL certificates
    obtained from a service such as [Let's Encrypt](https://letsencrypt.org).

  * Command for temporary self-signed certificates:

    ```
    $ make self-signed-cert
    ```

  * Explanation: this invokes commands (defined in *Makefile*):

    ```
    $ mkdir -p jupyterhub/secrets
    $ openssl req -x509 -nodes -days 365 -newkey rsa -config jupyterhub/cert.conf -keyout jupyterhub/secrets/crypticlabs-jupyterhub.key -out jupyterhub/secrets/crypticlabs-jupyterhub.crt
    ```

    These use config info defined in *jupyterhub/cert.conf* to generate
    self-signed SSL certificate file
    *jupyterhub/secrets/crypticlabs-jupyterhub.crt* and key file
    *jupyterhub/secrets/crypticlabs-jupyterhub.key*. The info in
    *jupyterhub/cert.conf* is pretty self-explanatory if you're curious.

* (One-time:) Write environment-configuration file *.env* with the following
  contents, adding `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` obtained above
  (see the last three lines below).

  ```
  # Based on JupyterHub's reference deployment,
  # https://github.com/jupyterhub/jupyterhub-deploy-docker,
  # Copyright (c) Jupyter Development Team.
  # Distributed under the terms of the Modified BSD License.

  # Use this file to set default values for environment variables specified in
  # docker-compose configuration file.  docker-compose will substitute these
  # values for environment variables in the configuration file IF the variables
  # are not set in the shell environment.

  # To override these values, set the shell environment variables.

  # Name of Docker machine
  DOCKER_MACHINE_NAME=crypticlabs-jupyterhub

  # Name of Docker network
  DOCKER_NETWORK_NAME=crypticlabs-jupyterhub-network

  # Single-user Jupyter Notebook server container image
  DOCKER_NOTEBOOK_IMAGE=jupyter/scipy-notebook:18e5563b7486

  # Notebook directory in the container.
  # This directory is stored as a docker volume for each user.

  # (Unfortunately, this is fragile because it must exactly agree with the
  # "NB_USER" setting in the Dockerfile for the crypticlabs/base-notebook
  # image. If you're seeing strange "Permission denied" errors, this is
  # probably why. It's a wart that needs removal, but it's not
  # super-high-priority.)
  DOCKER_NOTEBOOK_DIR=/home/cryptic/work

  # Docker run command to use when spawning single-user containers
  DOCKER_SPAWN_CMD=start-singleuser.sh

  # Name of JupyterHub container data volume
  DATA_VOLUME_HOST=crypticlabs-jupyterhub-data

  # Data volume container mount point
  DATA_VOLUME_CONTAINER=/data

  GITHUB_CLIENT_ID=<client ID for your GitHub OAuth application>
  GITHUB_CLIENT_SECRET=<client secret for your GitHub OAuth application>
  OAUTH_CALLBACK_URL=https://localhost:443/hub/oauth_callback
  ```

* (As-needed:) Build the Docker image used to make Jupyter Notebooks.

  * Build command:

    ```
    $ make notebook_image
    ```

    @kaben has marked this step as "as-needed" because we will need to rerun
    the command each time we update the Docker image used to provide per-user
    notebook servers. But for the moment, all this does is pull in the official
    Jupyter SciPy Notebook image *jupyter/scipy-notebook*.

* Build command:

  ```
  $ make build
  ```

* Deployment command:

  ```
  $ make up
  ```

* Command to cleanup so you can build again from scratch:

  ```
  $ make clean
  ```


### How to access:
If all goes well, you'll be able to access your local JupyterHub deployment via
the URL [https://localhost:443](https://localhost:443) on your computer. Your
browser should be highly suspicious of the self-signed SSL certificate, which
you will have to persuade your browser to trust. Your browser will then take
you to GitHub, where you'll be asked to grant various permissions to the OAuth
application. Once you grant permissions, JupyterHub will be able to
authenticate you using your GitHub login.


### Access permissions:
@kaben has set things up so that both @kaben and @carriere4 will be JupyterHub
admins, which is configured in *jupyterhub/userlist*, which currently contains
the following lines:

```
kaben admin
carriere4 admin
```

Everyone listed in this file can manually grant permissions to new users via
the JupyterHub admin interface.


### To do:
* Right now these build instructions are kind of monolithic, in that they will
  build the entire system. Need to add instructions to build individual
  components.
  * @kaben has added Make targets `anaconda3_image`, `base_notebook_image`, and
    `minimal_notebook_image` to *Makefile*, in order to simplify manual
    creation of these Docker images.
* It was a bad idea to use ":0.0.0" tags for thes custom images. Need to switch
  this to ":latest", or perhaps remove entirely.
  * @kaben's thinking was to provide version tags. But that's going to get
    hairy pretty quickly. Need to give this more thought.
* There are several points of fragility having to do with configurations that
  must agree among multiple files, e.g., if the environment variable `NB_USER`
  in *base-notebook/Dockerfile* is set to "cryptic", then environment variable
  `DOCKER_NOTEBOOK_DIR` in *.env* must be set to */home/cryptic/work*. If these
  settings don't agree, it won't be possible to create any notebooks!
  * To fix this, there should be a single setting, probably in *.env*, from
    which the variables `NB_USER` and `DOCKER_NOTEBOOK_DIR` derive.
  * Probably the best way to find these kinds of fragility is to change the
    settings in `.env` willy-nilly, to see what breaks. Then use the
    "derivation" trick to fix each point of fragility. This should be exercised
    in automated tests.
* In `base-notebook/Dockerfile`, @kaben has added a hack to enable passwordless
  sudo. The correct way to handle this is not inside the Dockerfile, but by
  launching the notebook server images as "root" while setting `GRANT_SUDO` to
  yes at the launch command.
  * For more info, see
    https://github.com/jupyter/docker-stacks/tree/master/base-notebook#docker-options.
