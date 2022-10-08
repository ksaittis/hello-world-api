.PHONY: build plan apply destroy
build:
	zip -j lambdas/put_user_lambda.zip python/hello-world/put_user_lambda.py
	zip -j lambdas/get_user_lambda.zip python/hello-world/get_user_lambda.py
plan:
	terraform -chdir=terraform plan
apply:
	terraform -chdir=terraform apply
destroy:
	terraform -chdir=terraform destroy
