.PHONY: scrapekot myrecorder lint test pydeps

scrapekot:
	poetry run python -m kot scrape

myrecorder:
	poetry run python -m kot myrecorder

black:
	poetry run black .

flake8:
	poetry run flake8 .

isort:
	poetry run isort --ca .

mypy:
	poetry run mypy kot --install-types --non-interactive

lint: black flake8 isort mypy

test:
	poetry run pytest tests

pydeps:
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
