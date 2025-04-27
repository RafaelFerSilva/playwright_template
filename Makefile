clean:
	python clean_cache.py

test: clean
	pytest

pipeline:
	pytest --pipeline true

report:
	allure serve reports/allure-results
