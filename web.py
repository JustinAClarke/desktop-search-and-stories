import json
from base import base
from flask import Flask,render_template,jsonify,request,url_for

app = Flask(__name__)
base = base()

def getRoutes(app):
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    return links

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def returnDisp(data,template=None,title=None):
    format = request.args.get('format',default='html')
    if format == 'json':
        return jsonify(data)
    else:
        if not template == None:
            return render_template(template, title=title, data=data,links=getRoutes(app),categories=base.getCategories())
        else:
            return str(data)

@app.route('/')
def Home():
    return returnDisp("Hello World","home.html","Home")

@app.route('/categories')
def ListCat():
    return returnDisp(base.getCategories(),'categories.html','ListCat')

@app.route('/providers')
def ListProviders():
    return returnDisp(base.getProviders(),'providers.html','ListProviders')

@app.route('/stories')
def ListStories():
    return returnDisp(base.getStories(),'stories.html','Stories')

@app.route('/stories/<category>')
def ListStoriesCat(category):
    return returnDisp(base.getStoriesCategory(category),'stories.html',category)

@app.route('/providers/<provider>')
def ListStoriesProv(provider):
    return returnDisp(base.getStoriesProvider(provider),'stories.html',base.getProvider(provider)['title'])

@app.route("/story/<id>")
def ShowStory(id):
    return returnDisp(base.getStory(id),'story.html')

if __name__ == '__main__':
    app.run()

