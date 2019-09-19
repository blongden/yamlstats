install:
	pip install --user -r requirements.txt

test:
	nosetests --with-coverage --cover-erase --cover-package yamlstats --cover-html
