.DEFAULT_GOAL := help

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build all the containers
	pip3 install -r requirements.txt
	python3 manage.py migrate

test: ## Run tests
	python3 manage.py test

run: ## Bring the server up
	python3 manage.py runserver