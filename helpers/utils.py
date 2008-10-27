import os,logging, gateway
from google.appengine.api import users
def path(p=''):
    return os.path.join(os.path.dirname(__file__), '../'+p )
    
def authdetails(page = "/"):
    user = users.get_current_user()
    if user: 
        label = "Logout"
        link = users.create_logout_url(page)
        status = 1
        url = gateway.check_if_user_exists(user)
        
    else:
        label = "Login"
        link = users.create_login_url(page)
        status = 0
        url = 'NULL'
        
    logging.info(status)
    logging.info(link)
    return dict(status = status,link = link,label=label,url=url)