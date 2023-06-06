.PHONY: build scrapekot scrapekot-slack myrecorder-start myrecorder-end lint test pydeps

build:
	docker compose build

scrapekot:
	docker compose run --rm app kot scrape --console --browser-kind remote

scrapekot-slack:
	docker compose run --rm app kot scrape --no-console --browser-kind remote

myrecorder-start:
	docker compose run --rm app kot myrecorder start --yes --browser-kind remote

myrecorder-end:
	docker compose run --rm app kot myrecorder end --yes --browser-kind remote

myrecorder-rest-start:
	docker compose run --rm app kot myrecorder rest_start --yes --browser-kind remote

myrecorder-rest-end:
	docker compose run --rm app kot myrecorder rest_end --yes --browser-kind remote

black:
	poetry run black .

flake8:
	poetry run pflake8 .

isort:
	poetry run isort --ca .

mypy:
	poetry run mypy kot --install-types --non-interactive

lint: black isort flake8 mypy

test:
	poetry run pytest

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
