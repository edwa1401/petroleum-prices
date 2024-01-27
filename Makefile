include .env
export

style: 
	ruff .
types:
	mypy .

tests:
	pytest --cov --lf -vv .

check:
	make style types tests

