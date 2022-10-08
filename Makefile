.PHONY: build plan apply destroy test
test:
	pip3 install -r ./python/test/requirements.txt
	python3 -m unittest discover python/test
build:
	mkdir -p ./lambdas
	zip -j lambdas/put_user_lambda.zip python/src/put_user_lambda.py
	zip -j lambdas/get_user_lambda.zip python/src/get_user_lambda.py
plan:
	terraform -chdir=terraform plan
apply:
	terraform -chdir=terraform apply
destroy:
	terraform -chdir=terraform destroy
