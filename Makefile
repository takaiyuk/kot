.PHONY: scrapekot myrecorder mypy test pydeps

scrapekot:
	python -m kot scrape

myrecorder:
	python -m kot myrecorder

mypy:
	# pip install mypy
	mypy kot --install-types --non-interactive
	mypy kot

test:
	# pip install pytest pytest-mock
	pytest tests

pydeps:
	# brew install graphviz && dot -c && pip install pydeps
	pydeps kot \
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
