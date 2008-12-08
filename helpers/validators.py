def check_url(url):
    if url == None or not url.isalnum(): raise ValueError('Invalid URL')

