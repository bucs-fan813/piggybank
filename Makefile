SHELL := /bin/bash

.DEFAULT_GOAL := help

help: ## This info
	@echo '_________________'
	@echo '| Make targets: |'
	@echo '-----------------'
	@echo
	@cat Makefile | grep -E '^[a-zA-Z\/_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo

json: provider=$(if $(p),$(p),0)
table: provider=$(if $(p),$(p),0)
sheet: provider=$(if $(p),$(p),0)

json: ## send data to stdout in table format
	pipenv run python -m main --output json --provider ${seed}

table: ## send data to stdout in table format
	pipenv run python -m main --output table --provider ${provider}

sheet: ## send data to Excel spreadsheet file
	pipenv run python -m main --output spreadsheet --provider ${provider}

test: ## Run test.py
	pipenv run python -m test

install: ## Run pipenv install
	pipenv install

