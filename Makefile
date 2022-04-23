SHELL := /bin/bash

.DEFAULT_GOAL := help

help: ## This info
	@echo '_________________'
	@echo '| Make targets: |'
	@echo '-----------------'
	@echo
	@cat Makefile | grep -E '^[a-zA-Z\/_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo

json table sheet: provider=$(if $(p),$(p),0)
json table sheet: is_deductible=$(if $(d),$(d),0)

json: ## send data to stdout in table format
	pipenv run python -m main --output json --provider ${provider}

table: ## send data to stdout in table format
	pipenv run python -m main --output table --provider ${provider} --is_deductible ${is_deductible}

sheet: ## send data to Excel spreadsheet file
	pipenv run python -m main --output spreadsheet --provider ${provider} --is_deductible ${is_deductible}

test: ## Run test.py
	pipenv run python -m test

install: ## Run pipenv install
	pipenv install

