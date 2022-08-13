AWS Refactor of klustics powderbot (which is definitely not a bot)
https://github.com/klustic/powderbot

To deploy: 
* Set up local AWS credentials with Admin (It'll need to create IAM resources)
* Install aws SAM
* Install Docker
* from clone directory:
	sam build --use-container
	sam deploy
