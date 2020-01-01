REPOSITORY := lambda-server
CURRENT_DATE := $(shell echo `date +'%Y-%m-%d'`)
VERSION ?= $(CURRENT_DATE)
DOCKER_URL := docker.io/akino1976
TEST_VERSION := commit_$(shell git rev-parse --short HEAD)

PACKAGE_NAME := pkg.zip
PACKAGE_FOLDER := /packages

export CURRENT_DATE
export VERSION
export TEST_VERSION
export PACKAGE_NAME
export PACKAGE_FOLDER

build-lambdaserver:
	docker build \
		-t $(REPOSITORY):latest \
		-t $(REPOSITORY):$(VERSION) \
		-t $(DOCKER_URL)/$(REPOSITORY):latest \
		-t $(DOCKER_URL)/$(REPOSITORY):$(VERSION) \
		.

package-example-lambda:
	docker-compose $(COMPOSE_DEFAULT_FLAGS) run --rm package-example-lambda

tests: systemtests

build-systemtests:
	docker-compose build systemtests-base

systemtests: build-systemtests build-lambdaserver package-example-lambda
	docker-compose run --rm systemtests

systemtests-watch: build-systemtests build-lambdaserver package-example-lambda
	docker-compose run --rm systemtests-watch

watch: build-lambdaserver package-example-lambda
	docker-compose run --service-ports --rm lambdaserver-watch

date:
	@echo $(CURRENT_DATE)

version:
	@echo ${VERSION}

clear-pycache:
	sudo find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf

stop-containers:
	docker-compose kill

clear-containers: stop-containers
	docker-compose rm --force

stop-all-containers:
	docker ps -q | xargs -I@ docker stop @

clear-all-containers: stop-all-containers
	docker ps -aq | xargs -I@ docker rm @

clear-volumes: clear-all-containers
	docker volume ls -q | xargs -I@ docker volume rm @

clear-images: clear-volumes
	docker images -q | uniq | xargs -I@ docker rmi -f @
