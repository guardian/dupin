import re


yarn              = re.compile('^\s*\"?resolved(?:\":)? \"(?:https|git|git\+https)://.*(?:#|/)[a-f0-9]+\"')
data_url          = re.compile('data:\w+/[\w+-]+;[^,]*,[a-zA-Z0-9+/=]+')
flow_sig          = re.compile('^// flow-typed signature: [a-z0-9]+$')
sys_images        = re.compile('/sys-images/[\w/]+/\d{4}/\d{1,2}/\d{1,2}/\d+/[\w-]+\.(?:png|jpg|jpeg)')
gu_video          = re.compile('gu-video-[0-9a-f]+')
json_allowed_hash = re.compile('^\s*\"(?:shasum|commit|id|mediaId)\":\s*\"[0-9a-f]+\",?$')
capi_fixture      = re.compile('^{"response":{"')
media_url         = re.compile('://media.guim.co.uk/[0-9a-f]{40}/')
frontend_static   = re.compile('https://aws-frontend-static\.s3\.amazonaws\.com/[\w/\-]+/[0-9a-f]{32}/')
github_reference  = re.compile('https://github.com/[\w+-]+/[\w+-]+/(?:blob|commit)/[0-9a-f]{40}')
blend64           = re.compile('blend64=[a-zA-Z0-9]\"?')
static_guim       = re.compile('http://static\.guim\.co\.uk/static/[a-f0-9]{40}/')

def false_positive(line):
    """Returns true if this line looks like a false positive.
    Tweak these to match your own requirements!
    (See also /tests/test_false_positives.py)
    """
    if yarn.search(line) or data_url.search(line) or flow_sig.search(line) or \
            sys_images.search(line) or gu_video.search(line) or json_allowed_hash.search(line) or \
            capi_fixture.search(line) or media_url.search(line) or frontend_static.search(line) or \
            github_reference.search(line) or blend64.search(line) or static_guim.search(line):
        return True
    else:
        return False
