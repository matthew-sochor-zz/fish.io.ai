fish = all_fish.csv
urls = data/scraped_urls.psv
url_count = 1000

$(urls): scrape_fish.py scrape_image_urls.js $(fish)
	mkdir -p data
	python scrape_fish.py $(fish) $(url_count) $(urls)

$(fish): invasives.csv natives.csv
	cat invasives.csv > $@
	cat natives.csv >> $@

node:
	npm install nightmare
	npm install images-scraper
