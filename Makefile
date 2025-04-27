clean:
	python clean_cache.py

test: clean
	pytest

headless: clean
	pytest --headless true

pipeline:
	pytest --pipeline true --headless true

report:
	allure serve reports/allure-results

generate-allure:
    allure generate reports/allure-results -o reports/allure-report --clean
