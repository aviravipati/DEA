#Create a file to execute terraform commands and create the infrastructure

cd ./terraform

terraform init
terraform plan
terraform apply -auto-approve