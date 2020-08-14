![CI](https://github.com/reichlab/covid19-forecast-hub-web/workflows/CI/badge.svg)
# Running Your Site Locally

1. Install a full [Ruby development environment](https://jekyllrb.com/docs/installation/)

1. Install Jekyll and Bundler

        gem install jekyll
        gem install bundler -v 1.16.6

1. Install dependencies from Gemfile:

        bundle install

1. Build the site and make it available on a local server

        bundle exec jekyll serve

1. Browse to [http://localhost:4000](http://localhost:4000)

# Build the site and deploy on GitHub Pages

1. Run this bash script in the root dirctory of this repository

        ./deploy.sh

The community file generation takes time and if you want to skip this step (this is anyways updated daily by the CI), you can run with the `skip_gen` flag:

        ./deploy.sh skip_gen

## Add weekly reports

1. Add the HTML file in the `reports` directory. 
1. Add an entry in the `/doc/reports/index.md` file to link to `/reports/[name-of-html-file]` based on the template already added in that file. 

