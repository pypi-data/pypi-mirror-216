<!-- SPDX-FileCopyrightText: 2023-present Leiden University Libraries <beheer@library.leidenuniv.nl>
SPDX-License-Identifier: CC-BY-4.0
-->
# Marginados WARC Scraper

[![PyPI - Version](https://img.shields.io/pypi/v/marginados-warc-scraper.svg)](https://pypi.org/project/marginados-warc-scraper)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/marginados-warc-scraper.svg)](https://pypi.org/project/marginados-warc-scraper)

-----

`marginados-warc-scraper` is a command-line tool that extracts tabular data from a
Web archive (WARC) file that contains data on 'Marginados'.
The WARC file was created using [ArchiveWeb.page] from recorded interactions with
<https://ctmn.colmex.mx/UI/Public/BusquedaSimple.aspx>.

This tool creates a single tab-separated values (TSV) file with all search results
that are in the WARC file, in the order that they were presented and browsed.

It seemed easier to extract these data from a WARC file than directly scraping from
the website, because the website uses POST requests with dynamic data to retrieve
more search results. We did not attempt to reverse engineer such requests.

We believe extracting the data from the website is allowed by the publisher under
the CC-BY-NC-ND license that cover the data.
Our request for a copy of the dataset was unanswered.

[ArchiveWeb.page]: https://archiveweb.page/

**Table of Contents**

- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

## Installation

```console
pip install marginados-warc-scraper
```

## Usage

This tool has very specific expectations about the input WARC file.
We have used it on a WARC file that was exported from the ArchiveWeb.page desktop
app.
In the app, we recorded a search for all results on the website that lists
*Los Catálogos de textos marginados novohispanos*.
It included clicking through search results, so that all pages of rows were recorded.
At the end of the session, we exported the "recording" as a WARC file.

It is expected that you use it like this (note the shorter name):

```console
marwar-scraper my-input.warc output.tsv
```

The output TSV file does not include a header row.

See `marginados-warc-scraper --help` for the full usage.

## License

`marginados-warc-scraper` was created by Ben Companjen at Leiden University Libraries'
[Centre for Digital Scholarship][cds] in 2023.

This program is free software:
you can redistribute it and/or modify it under the terms of the [GNU General Public
License][GPLv3] as published by the Free Software Foundation,
either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see <http://www.gnu.org/licenses/>.


[cds]: https://www.library.universiteitleiden.nl/about-us/centre-for-digital-scholarship
[GPLv3]: https://spdx.org/licenses/GPL-3.0-or-later.html
