
# define directories
data = data
test = $(data)/raw/test
train = $(data)/raw/train
scrapedDir = $(data)/scraped_images
dirs = $(data) $(test) $(train) $(scrapedDir)

s3dir = what-is-my-fish-images
s3key = scraped/

split_percent = 0.7

fish = $(shell ls $(scrapedDir))

# Modeling

model: train_head.py
	python train_head.py

features: imgs_to_arr.py arrs_to_aug.py arrs_to_emb.py | $(dirs)
	python imgs_to_arr.py
	python arrs_to_aug.py
	python arrs_to_emb.py

split: $(fish)
	echo split!

$(fish): split.py | $(dirs)
	mkdir -p $(test)/$@
	mkdir -p $(train)/$@
	python split.py $@ $(scrapedDir) $(test) $(train) $(split_percent)

# Data
pullData: | $(dirs)
	aws s3 sync s3://$(s3dir)/$(s3key) $(scrapedDir) --region=us-east-2

clean:
	rm -rf data

$(dirs):
	mkdir -p $@

# Terraform deployment 
start:
	terraform apply

connect:
	terraform refresh
	ssh -A -L 8888:localhost:8888 ubuntu@$(shell terraform output ip)

stop:
	terraform destroy
