clean:
	python clean_cache.py

test: clean
	pytest
