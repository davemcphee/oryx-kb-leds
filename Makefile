clean:
	python setup.py clean

install:
	python setup.py install

test:
	python setup.py test

sdist:
	python setup.py sdist

bdist_wheel:
	python setup.py bdist_wheel

all_dist:
	python setup.py sdist bdist_wheel

getversion:
	python setup.py --version
