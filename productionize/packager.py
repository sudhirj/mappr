#!/usr/bin/env python
"asset packager for my stuff"

HOME = "../"
CSS_DIR = "static/css/"
CSS = ["reset","main"]
JS_DIR = "static/js/"
JS = ["map","firsttime","pointlist","pointmaker","main"]
PRODUCTION = "static-production/"

try:
    prodcss = open(HOME+PRODUCTION+'styles.css','w')
except IOError, e:
    print "------ couldn't open production css file"
    
for css in CSS:
    try:
        thiscss = open(HOME+CSS_DIR+css+".css",'r')
        prodcss.writelines(thiscss)
        print "css-packed ",thiscss
    except e:
        print e         
prodcss.close()

try:
    prodjs = open(HOME+PRODUCTION+'scripts.js','w')
except IOError, e:
    print "------ couldn't open production js file"
    
for js in JS:
    try:
        thisjs = open(HOME+JS_DIR+js+".js",'r')
        prodjs.writelines(thisjs)
        print "js-packed ",thisjs
    except e:
        print e         
prodjs.close()