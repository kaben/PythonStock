# Based on JupyterHub's reference deployment,
# https://github.com/jupyterhub/jupyterhub-deploy-docker,
# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

include .env

.DEFAULT_GOAL=build

network:
	docker network inspect $(DOCKER_NETWORK_NAME) >/dev/null 2>&1 || docker network create $(DOCKER_NETWORK_NAME)

volumes:
	docker volume inspect $(DATA_VOLUME_HOST) >/dev/null 2>&1 || docker volume create --name $(DATA_VOLUME_HOST)

# make a self-signed cert
self-signed-cert:
	mkdir -p jupyterhub/secrets
	openssl req -x509 -nodes -days 365 -newkey rsa -config jupyterhub/cert.conf -keyout jupyterhub/secrets/crypticlabs-jupyterhub.key -out jupyterhub/secrets/crypticlabs-jupyterhub.crt

jupyterhub/secrets/crypticlabs-jupyterhub.crt:
	@echo "Need an SSL certificate in jupyterhub/secrets/crypticlabs-jupyterhub.crt"
	@exit 1

jupyterhub/secrets/crypticlabs-jupyterhub.key:
	@echo "Need an SSL key in jupyterhub/secrets/crypticlabs-jupyterhub.key"
	@exit 1

jupyterhub/userlist:
	@echo "Add usernames, one per line, to ./jupyterhub/userlist, such as:"
	@echo "    zoe admin"
	@echo "    wash"
	@exit 1

# Do not require cert/key files if SECRETS_VOLUME defined
secrets_volume = $(shell echo $(SECRETS_VOLUME))
ifeq ($(secrets_volume),)
	cert_files=jupyterhub/secrets/crypticlabs-jupyterhub.crt jupyterhub/secrets/crypticlabs-jupyterhub.key
else
	cert_files=
endif

check-files: jupyterhub/userlist $(cert_files)

pull:
	docker pull $(DOCKER_NOTEBOOK_IMAGE)

anaconda3_image:
	docker build -t crypticlabs/anaconda3:0.0.0 anaconda3

base_notebook_image: anaconda3_image
	docker build -t crypticlabs/base-notebook:0.0.0 base-notebook

minimal_notebook_image: base_notebook_image
	docker build -t crypticlabs/minimal-notebook:0.0.0 minimal-notebook

#notebook_image: pull
notebook_image: base_notebook_image

build: check-files network volumes
	docker-compose build

clean:
	docker-compose down
	docker-compose kill
	-docker rmi ${DOCKER_MACHINE_NAME}

up: build notebook_image
	docker-compose up -d

.PHONY: network volumes check-files pull notebook_image build

