#
# Authors:
#  - Abhimanyu Saharan <desk.abhimanyu@gmail.com>
#

REGISTRY_HOST=docker.io
USERNAME=kryptosteam
NAME=stratum
IMAGE=$(REGISTRY_HOST)/$(USERNAME)/$(NAME)
VERSION=latest

SHELL=/bin/bash

DOCKER_BUILD_CONTEXT=.
DOCKER_FILE_PATH=Dockerfile

.PHONY: pre-build docker-build post-build build push pre-push do-push post-push publish

help:
	@echo 'Usage: make [TARGET]'
	@echo
	@echo 'Targets:'
	@echo ' build              builds a new version of your Docker image and tags it'
	@echo ' push               push the image to your registry'
	@echo ' publish            publish the package on pypi'

build: pre-build docker-build post-build

pre-build:


post-build:


pre-push:


post-push:



docker-build:
	docker build $(DOCKER_BUILD_ARGS) -t $(IMAGE):$(VERSION) $(DOCKER_BUILD_CONTEXT) -f $(DOCKER_FILE_PATH)

push: pre-push do-push post-push

do-push:
	docker push $(IMAGE):$(VERSION)

publish:
	python -m build --sdist --wheel --outdir dist/
	twine check dist/*
	twine upload dist/*
