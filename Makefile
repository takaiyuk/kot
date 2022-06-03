.PHONY: scrapekot myrecorder mypy test pydeps

scrapekot:
	python -m kot scrape

myrecorder:
	python -m kot myrecorder

mypy:
	poetry run mypy kot --install-types --non-interactive

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
