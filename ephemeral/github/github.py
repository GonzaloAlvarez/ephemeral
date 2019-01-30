# Copyright: (c) 2018, Gonzalo Alvarez
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from ephemeral import net

GITHUB_API_PREFIX = 'https://api.github.com/repos'
GITHUB_TAGS = 'tags'

def download_latest(repo_owner, repo_name):
    tags_api_url = '{}/{}/{}/{}'.format(GITHUB_API_PREFIX, repo_owner, repo_name, GITHUB_TAGS)
    tags_api_response = net.get_json(tags_api_url)
    zipball_url = tags_api_response[0]['zipball_url']
    downloaded_file = net.download_file(zipball_url)
    return downloaded_file
