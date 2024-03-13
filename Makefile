include .env
export

style: 
	ruff check .
types:
	mypy .

tests:
	pytest --cov --lf -vv .

check:
	make style types tests

