from invoke import task


@task
def build(c):
    """
    Build docker compose
    """
    c.run(
        """
        echo 'docker compose build'
        docker compose build -q
    """
    )


@task(build)
def scrapekot(c):
    """
    Run scrapekot to notify on console
    """
    c.run(
        """
        docker compose run --rm app kot scrape --console --browser-kind remote
    """
    )


@task(build)
def scrapekot_slack(c):
    """
    Run scrapekot to notify on slack
    """
    c.run(
        """
        docker compose run --rm app kot scrape --no-console --browser-kind remote
    """
    )


@task(build)
def myrecorder_start(c):
    """
    Run MyRecorder to start working
    """
    c.run(
        """
        docker compose run --rm app kot myrecorder start --yes --browser-kind remote
    """
    )


@task(build)
def myrecorder_end(c):
    """
    Run MyRecorder to end working
    """
    c.run(
        """
        docker compose run --rm app kot myrecorder end --yes --browser-kind remote
    """
    )


@task(build)
def myrecorder_start_rest(c):
    """
    Run MyRecorder to start rest
    """
    c.run(
        """
        docker compose run --rm app kot myrecorder rest_start --yes --browser-kind remote
    """
    )


@task(build)
def myrecorder_end_rest(c):
    """
    Run MyRecorder to end rest
    """
    c.run(
        """
        docker compose run --rm app kot myrecorder rest_end --yes --browser-kind remote
    """
    )


@task
def lint(c):
    """
    Lint
    """
    c.run(
        """
        poetry run black .
        poetry run isort --ca .
        poetry run pflake8 .
        poetry run mypy kot --install-types --non-interactive
    """
    )


@task
def test(c):
    """
    Test
    """
    c.run(
        """
        poetry run pytest
    """
    )


@task
def pydeps(c):
    """
    Create pydeps graph
    """
    c.run(
        """
        # brew install graphviz && dot -c
        poetry run pydeps kot \
            -o statics/img/kot.svg \
            --cluster \
            --exclude-exact \
                bs4 \
                requests \
                selenium \
                typer \
                yaml \
                webdriver_manager \
                kot.common \
                kot.common.config \
                kot.common.logger \
                kot.myrecorder \
                kot.scrapekot
    """
    )
