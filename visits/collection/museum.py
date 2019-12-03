from logging import getLogger
from typing import Dict, List

from html.parser import HTMLParser

from attr import dataclass
from requests import get


@dataclass
class Museum(object):
    name: str
    city: str
    visitors_per_year: int
    year_reported: int

    @classmethod
    def from_wiki_list(cls, d: List[str]):
        logger = getLogger(f'{__name__}.{__class__.__qualname__}')
        m = None
        if len(d) > 4:
            offset = 2
            first_col = 0
            found = False
            while not found and first_col + offset + 2 < len(d):
                try:
                    m = cls(name=d[first_col],
                            city=d[first_col + offset],
                            visitors_per_year=int(d[first_col + offset + 1].replace(',', '')),
                            year_reported=int(d[first_col + offset + 2]))
                    found = True
                except ValueError as f_err:
                    logger.warning(f_err)
                    offset += 1
        if m is not None:
            return m
        else:
            raise ValueError(f'Impossible to parse {d} into a museum class')


class WikiHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        self.logger = getLogger(f'{__name__}.{__class__.__qualname__}')
        super().__init__(*args, **kwargs)
        self.table: List[Museum] = []
        self.in_table = False
        self.in_row = False
        self.in_column = False
        self._data: List[str] = []
        self._museums: List[Museum] = []

    def handle_starttag(self, tag, attrs):
        self.logger.debug(f'Encountered start tag {tag} with attrs {attrs}')
        if tag == 'table':
            self.logger.debug(f'Starting to parse table')
            self.in_table = True
        elif tag == 'tr':
            self.in_row = True
            self.logger.debug('Starting row')
        elif tag == 'td':
            self.in_column = True
            self.logger.debug(f'Need to parse following item')

    def handle_endtag(self, tag):
        self.logger.debug(f'Encountered end tag {tag}')
        if tag == 'table':
            self.logger.debug(f'Finished parsing table')
            self.in_table = False
        elif tag == 'tr':
            self.in_row = False
            self.logger.debug('Finished row')
            try:
                m = Museum.from_wiki_list(self._data)
                self.logger.info(f'Adding museum {m} to the list')
                self._museums.append(m)
            except ValueError as a_err:
                self.logger.warning(f'Failed to parse item at the end of row - {a_err}')
            finally:
                self._data = []
        elif tag == 'td':
            self.in_column = False
            self.logger.debug(f'Finished parsing column')

    def handle_data(self, data):
        if self.in_table and self.in_row and self.in_column:
            self.logger.debug(f'Encountered data to parse {data}')
            self._data.append(data)

    def error(self, message):
        self.logger.error(f'Failed to parse HTML - {message}')

    @property
    def museums(self) -> List[Museum]:
        return self._museums


def collect_from_wiki(page: str) -> Dict[str, str]:
    logger = getLogger(f'visits.{collect_from_wiki.__name__}')
    wiki_api = f'https://en.wikipedia.org/w/api.php'

    response = get(url=wiki_api, params={
        "action": "parse",
        "format": "json",
        "page": page
    })

    page_content = response.json()
    museums_parser = WikiHTMLParser()
    museums_parser.feed(page_content['parse']['text']['*'])

    logger.info(f'Found {len(museums_parser.museums)} most visited museums')

    return page_content
