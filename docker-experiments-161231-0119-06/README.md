# Docker experiments

This subdirectory contains experimental Docker deployments.

### JupyterHub
This provides a multi-user Jupyter notebook server hub which spawns, manages, and proxies an isolated server for each user. It uses GitHub login for authentication.

(For more on JupyterHub:)
* https://jupyterhub.readthedocs.io/en/latest/
* https://github.com/jupyterhub/jupyterhub

### How to deploy:
* (One-time:) Install [Docker](https://docs.docker.com).
* (One-time:) Setup a GitHub OAuth application.
  * @kaben has created a GitHub OAuth application for development, and can provide JupyterHub config info needed to use it.
  * To setup your own:
    * GitHub docs:
      * https://developer.github.com/guides/basics-of-authentication/
      * https://developer.github.com/v3/oauth/
    * URL for creating a new GitHub OAuth application: https://github.com/settings/applications/new
    * Example settings:
      * Application name: pythonstock-dev-01
      * Homepage URL: https://github.com/carriere4/PythonStock
      * Application description: PythonStock development
      * Authorization callback URL: https://localhost:443/hub/oauth_callback
        * Note: this URL must exactly match the value set in environment variable `OAUTH_CALLBACK_URL` for JupyterHub configuration.
    * Upon successful creation, OAuth client "ID" and "secret" are provided. Record these; they will used to set environment variables `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` for JupyterHub configuration.
* (One-time:) Generate temporary, self-signed SSL certificate and key.
  * Note: we will eventually replace these with CrypticLabs SSL certificates obtained from a service such as [Let's Encrypt](https://letsencrypt.org).
  * Command for temporary self-signed certificates:

    ```
    $ make self-signed-cert
    ```

  * Explanation: this invokes commands (defined in *Makefile*):

    ```
    $ mkdir -p jupyterhub/secrets
    $ openssl req -x509 -nodes -days 365 -newkey rsa -config jupyterhub/cert.conf -keyout jupyterhub/secrets/crypticlabs-jupyterhub.key -out jupyterhub/secrets/crypticlabs-jupyterhub.crt
    ```

    These use config info defined in *jupyterhub/cert.conf* to generate self-signed SSL certificate file *jupyterhub/secrets/crypticlabs-jupyterhub.crt* and key file *jupyterhub/secrets/crypticlabs-jupyterhub.key*. The info in *jupyterhub/cert.conf* is pretty self-explanatory if you're curious.
* (One-time:) Write environment-configuration file *.env* with the following contents, adding `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` obtained above (see the last three lines below).

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
  # This will be /home/jovyan/work if the default
  # This directory is stored as a docker volume for each user
  DOCKER_NOTEBOOK_DIR=/home/crypticlabs/work

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

    @kaben has marked this step as "as-needed" because we will need to rerun the command each time we update the Docker image used to provide per-user notebook servers. But for the moment, all this does is pull in the official Jupyter SciPy Notebook image *jupyter/scipy-notebook*.

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
If all goes well, you'll be able to access your local JupyterHub deployment via the URL https://localhost:443 on your computer. Your browser should be highly suspicious of the self-signed SSL certificate, which you will have to persuade your browser to trust. Your browser will then take you to GitHub, where you'll be asked to grant various permissions to the OAuth application. Once you grant permissions, JupyterHub will be able to authenticate you using your GitHub login.

### Access permissions:
@kaben has set things up so that both @kaben and @carriere4 will be JupyterHub admins, which is configured in *jupyterhub/userlist*, which currently contains the following lines:

```
kaben admin
carriere4 admin
```

Everyone listed in this file can manually grant permissions to new users via the JupyterHub admin interface.

### To do:
* Right now these build instructions are kind of monolithic, in that they will build the entire system. Need to add instructions to build individual components.
