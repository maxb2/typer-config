PHONY=fmt-docs
fmt-docs:
	find . -path './.venv' -prune -type f -o -name '*.md' -exec poetry run blacken-docs {} +

PHONY=fmt
fmt:
	poetry run isort --ca --profile=black .
	poetry run black .

PHONY=check-dependencies
check-dependencies:
	poetry export --only main | poetry run safety check --stdin

PHONY=check-types
check-types:
	poetry run mypy typer_config

PHONY=ruff
ruff:
	poetry run ruff check .

PHONY=check
check: ruff check-types

PHONY=test
test:
	poetry run pytest --cov=typer_config --cov-report=xml

PHONY=changelog
changelog:
	poetry run git-cliff --output CHANGELOG.md

PHONY=release
release: changelog
	NEXT_VERSION=$(shell poetry run git-cliff --bumped-version) && \
	poetry version $$NEXT_VERSION && \
	git add pyproject.toml CHANGELOG.md && \
	git commit -m "chore: Prepare release $$NEXT_VERSION" && \
	poetry publish --build && \
	mike deploy --push --update-aliases $$NEXT_VERSION latest && \
	git tag $$NEXT_VERSION && \
	git push && \
	git push --tags;
