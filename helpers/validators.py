def check_url(url):
    if url == None:
        raise ValueError('Sorry, thats an invalid URL.')

def check_point(ord):
    if ord > 180.0 or ord < -180.0:
        raise ValueError('That is an invalid co-ordinate.')