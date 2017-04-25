
# define directories
data = data
rawDir = $(data)/raw
test = $(rawDir)/test
train = $(rawDir)/train
plotDir = $(data)/plots

dirs = $(data) $(rawDir) $(test) $(train) $(plotDir)

s3dir = what-is-my-fish-images
testS3key = testfilter/ 
trainS3key = trainfilter/

# Modeling

predict: predict.py
	python predict.py

model: train_head.py
	python train_head.py

features: imgs_to_arr.py arrs_to_aug.py arrs_to_emb.py | $(dirs)
	python imgs_to_arr.py
	python arrs_to_aug.py
	python arrs_to_emb.py

# Data
pullData: | $(dirs)
	aws s3 sync s3://$(s3dir)/$(testS3key) $(test) --region=us-east-2
	aws s3 sync s3://$(s3dir)/$(trainS3key) $(train) --region=us-east-2

clean:
	rm -rf $(data)

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
