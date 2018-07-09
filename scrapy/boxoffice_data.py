import os
import time

import requests
import bs4
from bs4 import BeautifulSoup

import pandas as pd


def get_officebox_url(year):
    year = year if isinstance(year, str) else str(year)
    return "http://www.boxofficecn.com/boxoffice{}".format(year)


def extract_cell_value_from_header(html_cell):
    assert isinstance(html_cell, bs4.element.Tag), \
        "input must be in in bs4.element.Tag"

    return html_cell.select("strong")[0].contents[0]


def extract_cell_value_from_body(html_cell):
    assert isinstance(html_cell, bs4.element.Tag), \
        "input must be in in bs4.element.Tag"

    return html_cell.contents[0]


def parse_table_row(html_row):
    assert isinstance(html_row, bs4.element.Tag), \
        "input must be in in bs4.element.Tag"

    all_cells = html_row.select("td")
    parser_func = extract_cell_value_from_body

    if len(all_cells) == 0:
        all_cells = html_row.select("th")
        parser_func = extract_cell_value_from_header

    values = [parser_func(cell)
              for cell in all_cells]

    return values


def annual_data_parser(year):
    """return pandas dataframe by parsing annual boxoffice
       html_page
    """
    the_url = get_officebox_url(year)
    resp = requests.request(method='GET', url=the_url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.content.decode(), "lxml")
    html_rows = soup.select("tr")

    header, body = None, []
    for ii, html_row in enumerate(html_rows):
        if ii == 0:
            header = parse_table_row(html_row)
        else:
            parsed = parse_table_row(html_row)
            body.append(parsed)

    return pd.DataFrame(body, columns=header)


DATA_DIR = os.path.join(os.getcwd(), "data")
if __name__ == "__main__":
    for year in range(1994, 2018, 1):

        print("parsing data for year: {}".format(year))

        try:
            df = annual_data_parser(year)
            outfile_path = os.path.join(
                DATA_DIR, str(year))
            df.to_csv(
                outfile_path, header=True, index=False, sep=",")
            print('saved data for year: {}'.format(year))

        except:
            msg = "could not find page for {}".format(year)
            print(msg)

        time.sleep(30)
