#!/bin/sh

# If a command fails then the deploy stops
set -e
pip3 install -r requirements.txt
bundle install
printf "Generating community file"
python3 update-community.py
printf "\033[0;32mDeploying updates to GitHub...\033[0m\n"

# Build the project.
bundle exec jekyll build -d docs

# Go To Public folder
# cd public

if [ "$ENV" = "CI" ]; then
	git config user.name "GitHub Action"
	git config user.email "user@example.com"
fi
# Add changes to git.
git add .

# Commit changes.
msg="rebuilding site $(date)"
if [ -n "$*" ]; then
	msg="$*"
fi
git commit -m "$msg"

# Push source and build repos.
git push origin master 