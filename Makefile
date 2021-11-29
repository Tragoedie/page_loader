install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 #gendiff tests

#gendiff:
	#poetry run gendiff

#test:
#	poetry run pytest --cov=gendiff --cov-report xml tests/

#test-cov:
#	poetry run coverage xml
