# Recently digitised files in the National Archives of Australia

This repository scrapes a list of recently digitised files from the NAA's [RecordSearch](https://recordsearch.naa.gov.au/) database. It's currently scheduled to run each Sunday, saving a list of files that have been digitised in the previous week. The weekly datasets are saved as CSV files in the `data` directory. The date of the harvest is recorded in the file name, so `digitised-week-ending-20210328.csv` was harvested on 28 March 2021.

The CSV files contain the following fields:

* `title`
* `item_id`
* `series`
* `control_symbol`
* `date_range`
* `date_digitised`

More information can be found in the [RecordSearch section](https://glam-workbench.github.io/recordsearch/) of the GLAM Workbench.

---

Created by [Tim Sherratt](https://timsherratt.org), March 2021
