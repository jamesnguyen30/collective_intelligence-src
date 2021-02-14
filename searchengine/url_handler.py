from requests import get
from requests.exceptions import RequestException
from contextlib import closing

def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return ((resp.status_code == 200)
            and content_type is not None
            and content_type.find('html') > -1)


def load_raw_html(url):
    try:
        with closing(get(url, stream=True)) as response:
            if is_good_response(response):
                return response.content
            else:
                return None
    except RequestException as e:
        return None