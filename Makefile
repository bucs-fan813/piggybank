SHELL := /bin/bash

help: ## This info
	@echo '_________________'
	@echo '| Make targets: |'
	@echo '-----------------'
	@echo
	@cat Makefile | grep -E '^[a-zA-Z\/_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo

json: ## send data to stdout in table format
	pipenv run python -m main --output json

table: ## send data to stdout in table format
	pipenv run python -m main --output table

sheet: ## send data to Excel spreadsheet file
	pipenv run python -m main --output spreadsheet

test: ## Run test.py
	pipenv run python -m test

install: ## Run pipenv install
	pipenv install

