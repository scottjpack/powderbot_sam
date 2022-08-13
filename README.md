AWS Refactor of klustics powderbot (which is definitely not a bot)
https://github.com/klustic/powderbot

To deploy, 
1- Set up local AWS credentials with Admin (It'll need to create IAM resources)
2- Install aws SAM
3- Install Docker
4- from clone directory:
	sam build --use-container
	sam deploy