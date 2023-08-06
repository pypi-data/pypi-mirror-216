test :
	pytest

sdist :
	python setup.py sdist

clean :
	rm dist/*

dist : pytest sdist upload clean

upload:
	twine upload dist/*