live:
	@echo "Running auto reloading local wiki site..."
	sphinx-autobuild docs docs/_build

build:
	@echo "Building documentation..."
	sphinx-build docs docs/_build

snapshot: build
	@echo "Generating PDF snapshots (Desktop + mobile)..."
	python scripts/snapshot.py

snapshot-desktop: build
	@echo "Generating PDF snapshots for Desktop (light + dark)..."
	python scripts/snapshot.py --snapshots 1 2

snapshot-mobile: build
	@echo "Generating PDF snapshots for Mobile (light + dark)..."
	python scripts/snapshot.py --snapshots 3 4
