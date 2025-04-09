clean:
	python clean_cache.py

test: clean
	pytest

report:
	allure serve reports/allure-results
