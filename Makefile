clean:
	python clean_cache.py

test: clean
	pytest

headless: clean
	pytest --headless true

pipeline:
	pytest --junit-xml=test-results.xml --pipeline true --headless true

report:
	allure serve reports/allure-results
