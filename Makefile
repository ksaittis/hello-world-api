.PHONY: build plan apply destroy test
test:
	pip3 install -r ./python/test/requirements.txt
	python3 -m unittest discover python/test
build:
	mkdir -p ./package
	rm -rf package/*
	zip -r package/hello-world.zip python/src/* -x python/src/__pycache__/\* -x python/src/models/__pycache__/\* -x python/src/utils/__pycache__/\*
plan:
	terraform -chdir=terraform plan
tf_apply:
	terraform -chdir=terraform apply
# Builds the lambda package and runs terraform apply
apply: build tf_apply
destroy:
	terraform -chdir=terraform destroy
