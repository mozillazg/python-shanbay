help:
	@echo " register  register to pypi"
	@echo " publish   publish to pypi"

publish:
	@echo "publish to pypi"
	python setup.py publish

register:
	@echo "register to pypi"
	python setup.py register
