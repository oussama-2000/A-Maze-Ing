PYTHON = python3
PIP = pip3

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

clean:
	find -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache


lint:
# 	python3 -m flake8 .
	python3 -m  mypy . \
		--warn-return-any \
		--warn-unused-ignores \
		--ignore-missing-imports \
		--disallow-untyped-defs \
		--check-untyped-defs

