everything:
	python src/amapola_download.py
	python src/amapola_obs.py
	python src/obsplan.py

clean:
	rm plots/*/*.png