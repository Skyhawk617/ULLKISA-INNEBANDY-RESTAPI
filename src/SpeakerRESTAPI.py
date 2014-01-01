'''
Created on 29. des. 2013

@author: frankda
'''
import web
import json
import re

datafile = open('../resources/fixtures.txt')
fixtures = json.load(datafile)

urls = (
    '/', 'index',
    '/innebandy/all',"list_teams",
    '/innebandy/list/(.+)', "list_fixtures"

)


VALID_KEY = re.compile('[a-zA-Z0-9_-]{1,255}')
def is_valid_key(key):
    """Checks to see if the parameter follows the allow pattern of
    keys.
    """
    if VALID_KEY.match(key) is not None:
        return True
    return False

def validate_key(fn):
    """Decorator for HTTP methods that validates if resource
    name is a valid database key. Used to protect against
    directory traversal.
    """
    def new(*args):
        if not is_valid_key(args[1]):
            web.badrequest()
        return fn(*args)
    return new


render = web.template.render('../templates')
class list_teams:
    def GET(self):
        for i in fixtures:
            print i[1]
        return render.innebandy(fixtures)
            
class list_fixtures:
    def GET(self, name):
        name_set = False
        for i in fixtures:
            if i[0]==name:
                if not name_set:
                    name_set = True
                    teamfixture = i[2]
                    teamname = i[1]
                print "assigning "
            print i[0] #+ "Name:" + name
        return render.fixtures(teamname, teamfixture)
    
class index:
    def GET(self):
        data = web.data()
        print "Data:" + data

        #print render.hello('world')
        return render.index()

if __name__ == '__main__':
    
    app = web.application(urls, globals())
    app.run()
    