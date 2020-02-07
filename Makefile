
test: export PYTHONPATH=.

test:
	echo $(PYTHONPATH)
	pytest tests/
