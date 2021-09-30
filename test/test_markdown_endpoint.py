import requests
import responses
import json
from bs4 import BeautifulSoup

ENDPOINT = 'https://api.github.com/markdown'
HEADERS = {'Accept': 'application/vnd.github.v3+json'}


@responses.activate
def test_header():
    for i in range(1, 7):
        responses.add(responses.POST, ENDPOINT, body=f'<h{i}>Header {i}<h{i}>', status=200)

        document_base = f'Header {i}'
        document = '#' * i + ' ' + document_base
        print('Document: ' + document)

        response = requests.post(ENDPOINT, headers=HEADERS, data=json.dumps({'text': document}))
        print('response.text: ' + response.text)

        soup = BeautifulSoup(response.text, 'html.parser')
        assert f'Header {i}' == soup.find(f'h{i}').text.strip()

        responses.reset()


@responses.activate
def test_list():
    for list_tag, marker in {'ol': '1', 'ul': '*'}.items():
        responses.add(responses.POST, ENDPOINT, body=f'<{list_tag}><li>One</li><li>Two</li></{list_tag}>', status=200)

        document = f"{marker} One\n{marker} Two"
        print('Document: ' + document)

        response = requests.post(ENDPOINT, headers=HEADERS, data=json.dumps({'text': document}))
        print('response.text: ' + response.text)

        soup = BeautifulSoup(response.text, 'html.parser')
        list = soup.find(list_tag)
        expected_items = ['One', 'Two']
        list_items = list.find_all('li')

        assert len(expected_items) == len(list_items)
        for expected, observed in zip(expected_items, list_items):
            assert expected == observed.text

        responses.reset()
