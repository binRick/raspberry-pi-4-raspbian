if [[ ! -d .d ]]; then
	python3 -m venv .v
	source setup.sh
	./install.sh
fi
source .v/bin/activate

