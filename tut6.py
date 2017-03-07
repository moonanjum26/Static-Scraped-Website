import cherrypy
import os, os.path

from bs4 import BeautifulSoup as soup
from urllib2 import urlopen as uReq

import redis
r_server = redis.Redis(host='localhost',port=6379)
url='https://www.newegg.com/Video-Cards-Video-Devices/Category/ID-38?Tpk=graphics%20card'
uClient = uReq(url)
page_html = uClient.read()
uClient.close()
page_soup = soup(page_html,"html.parser")

class st(object):	 
    @cherrypy.expose
    
	    
    def index(self):
        res= """<html>
          <head>
            <link href="/static/css/style.css" rel="stylesheet">
          </head>
		  <body> 
		   <div class="card" >
			   <h2>Product_title, Brand_title and Shipping_title</h2>
			   <ul type="disc">"""

        containers =  page_soup.findAll('div',{'class':'item-container'})
        for container in containers:
            product_title = container.a.img["title"]
            brand_title = container.div.div.a.img["title"]
            shipping = container.findAll('li',{'class','price-ship'})
            shipping_title = shipping[0].text.strip()
            r_server.set('set1', product_title)
            r_server.set('set2', brand_title)
            r_server.set('set3', shipping_title)
			
            res += "<li>%s <br/><br/></li>" %r_server.get('set1')+ "<li>%s <br/><br/></li>" %r_server.get('set2')+"<li>%s <br/><br/></li>" %r_server.get('set3') 
         
        return res +  "</ul></div></body></html>" 
	
    
if __name__ == '__main__':
    conf = {
        '/':{
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
		},
		'/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './static'
			}
		}
	   
    cherrypy.quickstart(st(),'/',conf)
	 