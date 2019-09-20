install:
	pip3 install --user -r requirements.txt

test:
	nosetests --with-coverage --cover-erase --cover-package . --cover-html
	coverage-badge -f -o coverage.svg
