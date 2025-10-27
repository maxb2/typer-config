PHONY=fmt-docs
fmt-docs:
	find . -path './.venv' -prune -type f -o -name '*.md' -exec uvx --from git+https://github.com/maxb2/blacken-docs@87fadc3 blacken-docs {} +

PHONY=fmt
fmt:
	uvx isort --ca --profile=black .
	uvx black .

PHONY=check-types
check-types:
	uv run mypy src/typer_config

PHONY=ruff
ruff:
	uvx ruff check .

PHONY=check
check: ruff check-types

PHONY=test
test:
	uv run --all-extras pytest --cov=typer_config --cov-report=xml

PHONY=check-workflows
check-workflows:
	uvx zizmor .

PHONY=changelog
changelog:
	uvx git-cliff --output CHANGELOG.md

PHONY=release
release: 
	NEXT_VERSION=$(shell uvx git-cliff --bumped-version) && \
	uvx --from=toml-cli toml set --toml-path=pyproject.toml project.version $$NEXT_VERSION && \
	uvx git-cliff --output CHANGELOG.md --tag $$NEXT_VERSION && \
	git add pyproject.toml CHANGELOG.md && \
	git commit -m "chore: Prepare release $$NEXT_VERSION" && \
	rm -rf ./dist && \
	uv build && \
	uv publish && \
	uv run mike deploy --push --update-aliases $$NEXT_VERSION latest && \
	git tag $$NEXT_VERSION && \
	git push && \
	git push --tags;
