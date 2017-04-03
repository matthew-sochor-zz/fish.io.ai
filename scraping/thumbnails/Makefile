fish = all_fish.csv
query_suffix = fishing
img_path = scraped_images
url_count = 1000

scrape: scrape_fish.py scrape.py $(fish)
	python scrape_fish.py $(fish) $(query_suffix) $(url_count) $(img_path) 

$(fish): invasives.csv natives.csv
	cat invasives.csv > $@
	cat natives.csv >> $@

install:
	pip update selenium
	brew update && brew install geckodriver
	brew update && brew cask install firefox
