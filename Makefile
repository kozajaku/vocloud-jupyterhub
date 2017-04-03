include .env

.DEFAULT_GOAL=build

network:
	@docker network inspect $(DOCKER_NETWORK_NAME) >/dev/null 2>&1 || docker network create $(DOCKER_NETWORK_NAME)

volumes:
	@docker volume inspect $(DATA_VOLUME_HOST) >/dev/null 2>&1 || docker volume create --name $(DATA_VOLUME_HOST)

notebook_rebuild:
	docker build -f Dockerfile.notebook -t $(DOCKER_NOTEBOOK_IMAGE) .

notebook_image:
	@docker inspect $(DOCKER_NOTEBOOK_IMAGE) >/dev/null 2>&1 || docker build -f Dockerfile.notebook -t $(DOCKER_NOTEBOOK_IMAGE) .

build: network volumes notebook_image
	docker-compose build

.PHONY: network volumes notebook_rebuild notebook_image build
