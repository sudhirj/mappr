def check_url(url):
    if url == None or not url.isalnum():
        raise ValueError('Sorry, but that''s an invalid URL. Please use only letters and numbers.')

