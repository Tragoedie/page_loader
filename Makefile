install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python3 -m pip install --force-reinstall dist/*.whl

lint:
	poetry run flake8 page_loader

page-loader:
	poetry run page-loader

test:
	poetry run pytest --cov=page_loader --cov-report xml tests/ -vv

test-cov:
	poetry run coverage xml
