# SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
#
# SPDX-License-Identifier: GPL-3.0-or-later
from warcio.archiveiterator import ArchiveIterator
import click
import pathlib
from bs4 import BeautifulSoup
import re

@click.command()
@click.argument('in-file', type=click.Path(exists=True, file_okay=True, path_type=pathlib.Path))
@click.argument('out-file', type=click.Path(file_okay=True, path_type=pathlib.Path), default='./results.tsv')
def main(in_file, out_file):
    """Extract the data tables from a WARC file and save as a TSV file.
    
    This script was created for a very specific website, which retrieves pages of
    data using AJAX requests.
    The WARC file needs not be sorted by time of the request and response; the
    output is sorted by date and time of the record.
    Output TSV may not be valid, since we do not escape special characters."""
    tables = {}
    with open(in_file, 'rb') as stream:
        for record in ArchiveIterator(stream):
            if record.rec_type == 'response':
                content_type = record.http_headers.get_header('Content-Type')
                if 'text/plain' in content_type:
                    uri = record.rec_headers.get_header('WARC-Target-URI')
                    date = record.rec_headers.get_header('WARC-Date')
                    print(uri)
                    content = str(record.content_stream().read(), encoding='utf-8')
                    print(content[:15], "...", content[-15:])
                    tables[uri + "_" + date] = content
    with out_file.open('w', encoding='utf-8') as results:
        for table_id in sorted(tables):
            table_raw = tables[table_id]
            # print(table_raw[:15])
            # print(clean_table(table_raw))
            html_raw = clean_table(table_raw)
            soup = BeautifulSoup(html_raw, 'html.parser')
            the_table = soup.select_one('table#ctl00_MainContent_grdBusqueda_ctl00 > tbody')
            for row in the_table.find_all('tr'):
                print('\t'.join([s.strip() for s in row.strings]), file=results)

def clean_table(content: str) -> str:
    """Extract only the table from a raw AJAX result."""
    # lines = content.split('\r\n')
    match = re.fullmatch(r'^.+_UP\|(.+)\s\|0\|hid.+$', content, re.M|re.S)
    if match:
        return match.group(1)
    else:
        return None

if __name__ == "__main__":
    main()
