![CI](https://github.com/reichlab/covid19-forecast-hub-web/workflows/CI/badge.svg)

[![Netlify Status](https://api.netlify.com/api/v1/badges/41767ddf-f342-4622-b19a-e96e8c70d16f/deploy-status)](https://app.netlify.com/sites/covid19-forecast-hub/deploys)

# Website of COVID-19 Forecast Hub

This repository stores source code used to generate the website of the COVID-19 Forecast Hub.

# Building the site locally

1. Install a full [Ruby development environment](https://jekyllrb.com/docs/installation/)

1. Install Jekyll and Bundler

        gem install jekyll
        gem install bundler -v 1.16.6

1. Install dependencies from Gemfile:

        bundle install

1. Build the site and make it available on a local server

        bundle exec jekyll serve

1. Browse to [http://localhost:4000](http://localhost:4000)

# Build the site and deploy on Netlify

1. Run the Deploy Github action from the Actions tab.

The community file generation takes time and if you want to skip this step (this is anyways updated daily by the CI), you can run the action with the `skip_gen` flag: when the dropdown menu appears after click "Run workflow", specify `skip_gen` in the `Arguments to deploy script` field, and click `Run workflow`. 

## Add weekly reports

1. Add the HTML file in the `reports` directory. 
1. Add an entry in the `/doc/reports/index.md` file to link to `/reports/[name-of-html-file]` based on the template already added in that file. 
1. Additionally, you could also deploy the site after adding the weekly report from GitHub Actions [here](https://github.com/reichlab/covid19-forecast-hub-web/actions?query=workflow%3ADeploy).  
Press the `Run workflow` button and if you want to skip the community generation step (it takes time!), specify `skip_gen` in the `Arguments to deploy script` field. Click `Run workflow`. 

## Add a talk

1. If it is a PDF (or any other static file), you can add the file in the [talks](https://github.com/reichlab/covid19-forecast-hub-web/tree/master/talks) folder and the url to link would just be `/talks/[filename_with_extension]`. Ignore this step if it you want to add an existing URL.  
1. Add an item to the list [here](https://github.com/reichlab/covid19-forecast-hub-web/blob/master/doc/talks/index.md). You can use the following line as a template if you want:
```
- Talk name [link](https://link-to-your-talk.com){:target="_blank"} (Date)
```
