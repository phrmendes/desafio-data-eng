pycache := $(shell find . -name __pycache__)

prefect_deployment_run:
	@poetry run prefect deployment run "get-data/desafio_data_eng"

run:
	@poetry run python main.py

clear:
	@rm -rf $(pycache)

export_requirements: pyproject.toml
	@poetry export -f requirements.txt --output requirements.txt --whithout dev

dbt_run: ./dbt_project
	./scripts/dbt_run.sh

.PHONY: prefect clear run
