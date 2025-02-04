# Recently digitised files in the National Archives of Australia

New! View the [National Archives of Australia Digitisation Dashboard](https://wragge.github.io/naa-recently-digitised/) for a summary of recently digitised files.

This repository scrapes a list of recently digitised files from the NAA's [RecordSearch](https://recordsearch.naa.gov.au/) database. It's currently scheduled to run each Sunday, saving a list of files that have been digitised in the previous week. The weekly datasets are saved as CSV files in the `data` directory. The date of the harvest is recorded in the file name, so `digitised-week-ending-20210328.csv` was harvested on 28 March 2021.

The CSV files contain the following fields:

* `title`
* `item_id`
* `series`
* `control_symbol`
* `date_range`
* `date_digitised`

A dataset containing annual compilations of the weekly harvests is [available from Zenodo](https://doi.org/10.5281/zenodo.14744049).

More information can be found in the [RecordSearch section](https://glam-workbench.github.io/recordsearch/) of the GLAM Workbench.

---

Created by [Tim Sherratt](https://timsherratt.org), March 2021
