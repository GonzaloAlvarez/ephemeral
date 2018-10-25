#!/usr/bin/env python
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from pylib import net
import pprint

GITHUB_API_PREFIX = 'https://api.github.com/repos'
GITHUB_TAGS = 'tags'

def download_latest(repo_owner, repo_name):
    tags_api_url = '{}/{}/{}/{}'.format(GITHUB_API_PREFIX, repo_owner, repo_name, GITHUB_TAGS)
    tags_api_response = net.get_json(tags_api_url)
    zipball_url = tags_api_response[0]['zipball_url']
    downloaded_file = net.download_file(zipball_url)
    return downloaded_file
