
# define directories
data = data
test = $(data)/raw/test
train = $(data)/raw/train
dirs = $(data) $(test) $(train)

scraped = ../scraping/thumbnails/scraped_images

percent = 0.7

fish = walleye carp white_perch yellow_perch

split: $(fish)
	echo split!

clean:
	rm -rf data

$(fish): split.py | $(dirs)
	mkdir -p $(test)/$@
	mkdir -p $(train)/$@
	python split.py $@ $(scraped) $(test) $(train) $(percent)

$(dirs):
	mkdir -p $@
