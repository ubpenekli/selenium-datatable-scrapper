# Selenium Datatable Scrapper

This is a datatable scrapper to get data from ajax-datatable plugin which is running with server-side processing. When it runs server-side, you can not scrap data from page source. So you need to surf on table pages to get data for each page. In this script, selenium clicks all page buttons from start to end, collecting all data and parsing with BeautifulSoup4.

There is a demo to scrap data from YÖK Atlas.

## Prerequisities

* Python3
* Pip3
* Selenium
* Chrome Webdriver
* BeautifulSoup4

## Installation

You can directly clone repository to your local and run.

```bash
git clone https://github.com/ubpenekli/selenium-datatable-scrapper.git
```
or with SSH
```bash
git clone git@github.com:ubpenekli/selenium-datatable-scrapper.git
```

## Usage for Demo

Stay with a strong internet connection.

Run `python3 main.py` others will be work automatically.

## Credits

- [Ugur Batuhan Penekli](https://github.com/ubpenekli)
- [All Contributors](../../contributors)

## License

The MIT License (MIT). Please see [License File](LICENSE.md) for more information.