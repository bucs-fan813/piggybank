SHELL := /bin/bash

help: ## This info
	@echo '_________________'
	@echo '| Make targets: |'
	@echo '-----------------'
	@echo
	@cat Makefile | grep -E '^[a-zA-Z\/_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo

run: pipenv run python -m main  ## Run main.py

test: pipenv run python -m test  ## Run test.py

install: pipenv install  ## Run pipenv install