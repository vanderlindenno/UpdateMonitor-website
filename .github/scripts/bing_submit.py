"""Tell Bing (and other IndexNow search engines) about new or changed pages after a push.

Two submissions, both best effort (problems are logged and never fail the workflow):
  1. the Bing Webmaster URL submission API, with the key in the BING_API_KEY secret
  2. IndexNow (Bing, Yandex, Naver, Seznam), with the public key file <key>.txt in the repo root
"""
import glob
import json
import os
import re
import subprocess
import sys
import urllib.error
import urllib.request

MAX_URLS = 50
ENDPOINT = 'https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlBatch?apikey='
INDEXNOW_ENDPOINT = 'https://api.indexnow.org/indexnow'

key = os.environ.get('BING_API_KEY', '').strip()
site = 'https://' + open('CNAME', encoding='utf-8').read().strip()


def skip(path):
    name = os.path.basename(path)
    return name == '404.html' or name.startswith('google')


def url_for(path):
    if path.endswith('index.html'):
        return site + '/' + path[:-len('index.html')]
    return site + '/' + path


def sitemap_urls():
    xml = open('sitemap.xml', encoding='utf-8').read()
    return re.findall(r'<loc>([^<]+)</loc>', xml)


def indexnow_key():
    """The IndexNow key is public by design: it lives in a file named <key>.txt on the site."""
    for path in glob.glob('*.txt'):
        name = os.path.basename(path)[:-4]
        if re.fullmatch(r'[0-9a-f]{32}', name):
            if open(path, encoding='utf-8').read().strip() == name:
                return name
    return ''


before = os.environ.get('BEFORE', '')
sha = os.environ.get('SHA', 'HEAD')
submit_all = os.environ.get('SUBMIT_ALL', '').lower() == 'true'

if submit_all or not before or set(before) == {'0'}:
    urls = sitemap_urls()
else:
    out = subprocess.run(
        ['git', 'diff', '--name-only', '--diff-filter=AM', before, sha, '--', '*.html'],
        capture_output=True, text=True)
    paths = [p for p in out.stdout.split() if p.endswith('.html') and not skip(p)]
    urls = [url_for(p) for p in paths]
    # only pages listed in the sitemap are meant to be indexed (skips legacy/duplicate pages)
    listed = set(sitemap_urls())
    for u in urls:
        if u not in listed:
            print('Skipped (not in sitemap.xml): ' + u)
    urls = [u for u in urls if u in listed]

urls = list(dict.fromkeys(urls))[:MAX_URLS]
if not urls:
    print('No changed pages to submit.')
    sys.exit(0)

print('Submitting %d URL(s) for %s:' % (len(urls), site))
for u in urls:
    print('  ' + u)


def post(url, payload, label):
    body = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=body,
                                 headers={'Content-Type': 'application/json; charset=utf-8'})
    try:
        resp = urllib.request.urlopen(req, timeout=60)
        print('%s responded:' % label, resp.status, resp.read().decode('utf-8')[:300])
    except urllib.error.HTTPError as e:
        print('%s returned an error (workflow continues):' % label, e.code, e.read().decode('utf-8')[:300])
    except Exception as e:  # network problems must not fail the workflow
        print('Could not reach %s (workflow continues):' % label, type(e).__name__)


# 1. Bing Webmaster URL submission API
if key:
    post(ENDPOINT + key, {'siteUrl': site, 'urlList': urls}, 'Bing')
else:
    print('BING_API_KEY is not set as a repository secret; skipping the Bing API.')

# 2. IndexNow
inkey = indexnow_key()
if inkey:
    host = site.split('://', 1)[1]
    post(INDEXNOW_ENDPOINT,
         {'host': host, 'key': inkey, 'keyLocation': '%s/%s.txt' % (site, inkey), 'urlList': urls},
         'IndexNow')
else:
    print('No IndexNow key file (<32 hex characters>.txt) in the repository root; skipping IndexNow.')
