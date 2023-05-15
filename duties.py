from duty import duty


@duty(aliases=["format", "black"])
def fmt(ctx):
    ctx.run("isort .", title="Sorting imports")
    ctx.run("black .", title="Code formatting")


@duty
def check(ctx):
    ctx.run("mypy typer_config", title="Type checking")
    ctx.run("pylint typer_config", title="Linting")

@duty
def docs(ctx):
    ctx.run('mkdocs serve')

@duty
def changelog(ctx):
    ctx.run("git-changelog -Tbio CHANGELOG.md -c conventional")