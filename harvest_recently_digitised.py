import mechanicalsoup
import re
import arrow
import time
import pandas as pd
from pathlib import Path

def initialise_browser():
    '''
    This is necessary to get an active session in RS.
    '''
    browser = mechanicalsoup.StatefulBrowser()
    browser.open('https://recordsearch.naa.gov.au/scripts/Logon.asp?N=guest')
    # browser.select_form('form[id="t"]')
    # browser.submit_selected()
    return browser

def get_date_digitised(result):
    '''
    Generate a formatted date from the date digitised string (eg 'Digitised 1 days ago')
    '''
    when_digitised = result.find('div', class_='card-footer card-footer-list').span.string.strip()
    interval, unit = re.search(r'^Digitised (\d+) (hours|days) ago', when_digitised).groups()
    if unit == 'days':
        date_digitised = arrow.now('Australia/Sydney').shift(days=-(int(interval)))
    elif unit == 'hours':
        date_digitised = arrow.now('Australia/Sydney').shift(hours=-(int(interval)))
    return date_digitised.format('YYYY-MM-DD')

def get_records_from_page(page):
    '''
    Scrapes item metadata from the list of results.
    '''
    records = []
    results = page.find_all('li', class_='soda_list')
    for result in results:
        record = {}
        record['title'] = result.img['title']
        record['item_id'] = result.find('dt', string='Item ID:').find_next_sibling('dd').a.string.strip()
        record['series'] = result.find('dt', string='Series:').find_next_sibling('dd').a.string.strip()
        record['control_symbol'] = result.find('dt', string=re.compile('Control symbol:')).find_next_sibling('dd').string.strip()
        record['date_range'] = re.sub(r'\s+', ' ', result.find('dt', string=re.compile('Date range:')).find_next_sibling('dd').string.strip())
        record['date_digitised'] = get_date_digitised(result)
        records.append(record)
    return records

def get_number_of_results(page):
    '''
    Get the start, end, and total number of results from the current page of results.
    '''
    result_summary = page.find('label', id='ContentPlaceHolderSNR_lblTopPaging').string.strip()
    start, end, total = re.search(r'(\d+) to (\d+) of (\d+)', result_summary).groups()
    return (start, end, total)

def harvest_recently_digitised():
    records = []

    # Get a browser with all RecordSearch's session stuff ready
    browser = initialise_browser()

    # Open the recently digitised page
    browser.open('https://recordsearch.naa.gov.au/SearchNRetrieve/Interface/ListingReports/NewlyScannedList.aspx')

    # CONFIGURE THE RESULTS FORM
    browser.select_form('form[id="formSNRMaster"]')
    # 200 results per page
    browser['ctl00$ContentPlaceHolderSNR$ddlResultsPerPage'] = '200'
    # Results from the past month
    browser['ctl00$ContentPlaceHolderSNR$ddlDateAdded'] = 'w'
    # Set display to list view
    browser.form.set('ctl00$ContentPlaceHolderSNR$btn_viewList.x', '11', force=True)
    browser.form.set('ctl00$ContentPlaceHolderSNR$btn_viewList.y', '9', force=True)
    browser.submit_selected()

    # PROCESS RESULTS
    # Get the total number of results
    start, end, total = get_number_of_results(browser.page)

    # Process first page of results
    records += get_records_from_page(browser.page)

    # Loop through the rest of the results set
    while end != total:
        browser.select_form('form[id="formSNRMaster"]')

        # Setting these gets the next page of results
        browser.form.set('ctl00$ContentPlaceHolderSNR$listPagerTop$ctl00$ctl02.x', '10', force=True)
        browser.form.set('ctl00$ContentPlaceHolderSNR$listPagerTop$ctl00$ctl02.y', '10', force=True)
        browser.submit_selected()

        # When there are errors here to to website problems, try substituting the code below to get as much as possible.
        # Also set the number of results per page as low as possible.
        start, end, total = get_number_of_results(browser.page)
        records += get_records_from_page(browser.page)

        """"
        try:
            start, end, total = get_number_of_results(browser.page)
        except AttributeError:
            print(f"failure at {end}")
            end = total
        else:
            print(end, total)
            records += get_records_from_page(browser.page)
        """
        time.sleep(1)
    return records

def main():
    Path('data').mkdir(exist_ok=True)
    records = harvest_recently_digitised()
    df = pd.DataFrame(records)
    df.to_csv(Path('data', f'digitised-week-ending-{arrow.now().format("YYYYMMDD")}.csv'), index=False)

if __name__ == "__main__":
    main()
