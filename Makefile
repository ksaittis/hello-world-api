.PHONY: init plan apply destroy build test tf_plan tf_apply tf_destroy
test:
	pip3 install -r ./python/test/requirements.txt
	python3 -m unittest discover python/test
build:
	mkdir -p ./package
	rm -rf package/*
	zip -r package/hello-world.zip python/src/* -x python/src/__pycache__/\* -x python/src/models/__pycache__/\* -x python/src/utils/__pycache__/\*
init:
	if [ ! -d "terraform/.terraform" ]; then terraform -chdir=terraform init; fi
tf_plan:
	terraform -chdir=terraform plan
tf_apply:
	terraform -chdir=terraform apply
tf_destroy:
	terraform -chdir=terraform destroy
plan: init build tf_plan
apply: init build tf_apply
destroy: init tf_destroy
