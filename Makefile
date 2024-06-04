build:
	mv dist/* releases || true
	rm -rf dist/* || true
	python -m build .