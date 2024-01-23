.DEFAULT_GOAL := help

.PHONY: help
help: ## Show help
	@echo "Typer Config Tools"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: install-deps
install-deps:
	poetry install --all-extras

.PHONY: install
install: install-deps ## Install dependencies and pre-commit

.PHONY: fmt-docs
fmt-docs:
	poetry run duty fmt-docs

.PHONY: fmt
fmt: ## Format code
	poetry run bash -c 'isort --ca --profile=black . && black .'

.PHONY: lint
lint: ## Lint code
	poetry run black --check typer_config
	poetry run ruff .

.PHONY: check
check: lint check-types ## Lint and type check code

.PHONY: check-types
check-types: ## Type check code
	poetry run mypy typer_config

.PHONY: check-deps
check-deps: ## Check dependencies
	poetry export --only main | poetry run safety check --stdin

.PHONY: test
test: ## Test code
	poetry run pytest --cov=typer_config --cov-report=xml

.PHONY: all
all: install-deps fmt check test ## Install, format, lint, type-check, and test code

# CI tasks (doesn't format code before checking it)
.PHONY: ci
ci: install-deps check test

.PHONY: changelog
changelog: ## Generate changelog
	poetry run duty changelog

.PHONY: docs
docs: ## Build docs
	poetry run mkdocs build

.PHONY: release
release:
	poetry run duty release