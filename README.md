![CI](https://github.com/reichlab/covid19-forecast-hub-web/workflows/CI/badge.svg)

[![Netlify Status](https://api.netlify.com/api/v1/badges/41767ddf-f342-4622-b19a-e96e8c70d16f/deploy-status)](https://app.netlify.com/sites/covid19-forecast-hub/deploys)

# Website of COVID-19 Forecast Hub

This repository stores source code used to generate the website of the COVID-19 Forecast Hub.  
***
<strong>Note:</strong> As of Wednesday, May 1, 2024, the US COVID-19 Forecast Hub is no longer accepting submissions. Information provided on forecast submissions are kept for historical record.  

# Contributing / editing

Most pages can be edited directly and are located in the `doc` folder and corresponding subdirectories. Subdirectories have the name of the corresponding tab or submenu in the webpage and the main landing page is usually the file named `index.md` within that folder. To have changes reflected on the website, those markdown files need to be edited and then the site must be deployed, as detailed below.

For example, to edit the “Reports” landing page, accessible via the “Reports” tab on the [COVID-19 Forecast Hub main page](https://covid19forecasthub.org/), edit the file in `doc/reports/index.md`

## Weekly reports

Weekly reports were generated and deployed automatically by the virtual machine on Tuesdays at 8:30 am using the `run-weekly-reports.sh` script.

## Evaluation reports

Evaluation reports were produced on a monthly basis. First, [this script](https://github.com/reichlab/covid19-forecast-evals/blob/main/reports/Query-scores-weekly-report_52.R) was run locally. It took approximately one day to run and required manual saves and restarts. Afterwards, [this script](https://github.com/reichlab/covid19-forecast-evals/blob/main/reports/Weekly-Model-Evaluation_v9.Rmd) was run to generate the evaluation report. This did not take long to run. Finally, the report was reviewed manually by team members. If the report looked good, it was uploaded to [this repository](https://github.com/reichlab/covid19-forecast-hub-web/tree/master/eval-reports). The monthly evaluation report should not be uploaded on a Tuesday, as it may cause conflict with other actions scheduled for Tuesdays.

Reports and edits were deployed to the site using the `deploy-covidhub-site.sh` script, as explained below.

## Talks

1. If it is a PDF (or any other static file), you can add the file in the [talks](https://github.com/reichlab/covid19-forecast-hub-web/tree/master/talks) folder and the url to link would just be `/talks/[filename_with_extension]`. Ignore this step if it you want to add an existing URL.  
1. Add an item to the list [here](https://github.com/reichlab/covid19-forecast-hub-web/blob/master/doc/talks/index.md). You can use the following line as a template if you want:
```
- Talk name [link](https://link-to-your-talk.com){:target="_blank"} (Date)
```

# Deploying the site

The website updates are done automatically on Tuesdays using a virtual machine. Manual updates can be triggered only with access to the virtual machine.

Specifically, on Tuesday at 8:30 am, a [first script](https://github.com/reichlab/covidModels/blob/master/aws-vm-scripts/run-weekly-reports.sh) pulls the latest **covid19-forecast-hub** and **covid19-forecast-hub-web** commits, runs `render_reports.R`, and copies and commits the resulting reports html files.

At 11 am and 2 pm, a [second script](https://github.com/reichlab/covidModels/blob/master/aws-vm-scripts/deploy-covidhub-site.sh) updates community and reports data (`community.yml` and `reports.json`, respectively), builds the site into the `docs/` dir using jekyll, and then copies `docs/` to the netlify branch.

Once this is all pushed, Netlify's GitHub "Continuous deployment" integration happens, which is configured in the deploy settings in Netlify.

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

