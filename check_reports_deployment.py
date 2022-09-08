import json
from pathlib import Path

import click


@click.command()
@click.argument('reports_dir', type=click.Path(file_okay=False, exists=True))
@click.argument('reports_json_file', type=click.Path(file_okay=True, exists=True))
def check_reports_deployment(reports_dir, reports_json_file):
    """
    A shell script helper that checks whether reports/reports.json is up-to-date with the '*-weekly-report.html files in
    the reports/ directory.

    :param reports_dir: reports directory
    :param reports_json_file: reports/reports.json file
    :return: prints to stdout the result of checking the inputs: 'True' if IS up-to-date, 'False' if is NOT up-to-date
    """
    reports_dir = Path(reports_dir)
    with open(reports_json_file) as reports_json_fp:
        reports_dict = json.load(reports_json_fp)
        # reports_dict format: {state_1: [date1, date2, ...], ...} . e.g.,
        #   {"US": ["2022-09-06", "2022-08-30", ...],
        #    "AK": ["2022-09-06", "2022-08-30", ...],
        #    ...,
        #    "WY": ["2022-09-06", "2022-08-30", ...]
        #   }
        for report_file in reports_dir.glob('*-weekly-report.html'):
            # a Path like: '2021-07-06-KS-weekly-report.html' . NB: we ignore non-state files like
            # '2020-12-22-weekly-report.html'
            num_dashes = report_file.name.count('-')
            file_date = report_file.name[:10]  # '2021-07-06'
            if num_dashes != 5:  # skip non-state reports, which have 4 dashes
                continue

            file_state = report_file.name[11:13]  # 'MA'
            if (file_state not in reports_dict) or (file_date not in reports_dict[file_state]):
                # state or date not in reports file
                click.echo(False)
                return

    # all states and dates in reports file
    click.echo(True)


if __name__ == '__main__':
    check_reports_deployment()
