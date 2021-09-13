#!/bin/sh

# If a command fails then the deploy stops
set -e
pip install pipenv
pipenv install
# pip3 install -r requirements.txt
bundle install
if [ "$1" != "skip_gen" ]; then
	printf "Generating community file"
	python3 update-community.py
else
	printf "Skipping community file generation"
fi

python3 update-reports.py
printf "\033[0;32mDeploying updates to GitHub...\033[0m\n"

# Build the project.
bundle exec jekyll build -d docs

# Go To Public folder
# cd public

if [ "$CI" = "true" ]; then
	git config user.name "GitHub Action"
	git config user.email "user@example.com"
fi
printf "covid19forecasthub.org" > ./docs/CNAME
# Push source and build repos.
if [ "$1" != "no_push" ]  && [ "$2" != "no_push" ] 
then
	printf "Pushing to GitHub"
	# Add changes to git.
	git add .

	# Commit changes.
	msg="rebuilding site $(date)"
	git diff-index --quiet HEAD || git commit -m "$msg"

	git push origin master
else
	printf "Skipping push to GitHub"
fi
