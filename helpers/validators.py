def check_url(url):
    if url == None or not url.isalnum():
        raise ValueError('Sorry, but that''s an invalid URL.')

def check_point(ord):
    if ord > 180.0 or ord < -180.0:
        raise ValueError