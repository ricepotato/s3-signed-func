deploy:
	poetry export --without-hashes --format=requirements.txt > requirements.txt
	serverless deploy