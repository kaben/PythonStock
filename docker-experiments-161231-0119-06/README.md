# Docker experiments

This subdirectory contains experimental Docker deployments.

### JupyterHub
This provides a multi-user Jupyter notebook server hub which spawns, manages, and proxies an isolated server for each user. It uses GitHub login for authentication.

(For more on JupyterHub:)
* https://jupyterhub.readthedocs.io/en/latest/
* https://github.com/jupyterhub/jupyterhub

###### How to deploy:
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

## To do:
* Right now these build instructions are kind of monolithic, in that they will build the entire system. Need to add instructions to build individual components.
