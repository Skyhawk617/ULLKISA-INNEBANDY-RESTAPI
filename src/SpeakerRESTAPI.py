'''
Created on 29. des. 2013

@author: frankda
'''
import web
import json
import re

datafile = open('../resources/fixtures.txt')
all_data = json.load(datafile)

urls = (
    '/', 'index',
    '/innebandy/all',"list_teams",
    '/innebandy/list/(.+)', "list_fixtures"

)


VALID_KEY = re.compile('[a-zA-Z0-9_-]{1,255}')

''' A section in the fixtures.txt file is a uniform section of content:
    Currently implemented sections are:
    - Teams: List of all teams and teamID. TeamID is used to get name from Speaker.no site.
    - Fixtures: List of fixtures per team.
    - N/A
    
'''
def find_section(id, obj):
    results = []

    def _find_values(id, obj):
        try:
            for record in obj:
                if record[0] == id:
                    results.append(record[1])
                    
        except AttributeError:
            pass

    
    if not isinstance(obj, basestring):
        _find_values(id, obj)
    
    return results

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
        #for i in fixtures:
        #    print i[1]

        return render.innebandy(web.teams[0])
            
class list_fixtures:
    def GET(self, name):
        name_set = False
        for i in web.fixtures[0]:
            if i[0]==name:
                if not name_set:
                    name_set = True
                    teamfixture = i[2]
                    teamname = i[1]
                #print "assigning "
            #print i[0] #+ "Name:" + name
        return render.fixtures(teamname, teamfixture)
    
class index:
    def GET(self):
        data = web.data()
        #print "Data:" + data

        #print render.hello('world')
        return render.index()

if __name__ == '__main__':
    teams = find_section('Teams', all_data)
    fixtures = find_section('Fixtures', all_data)
    
    web.teams = teams
    web.fixtures = fixtures
    app = web.application(urls, globals())
    app.run()
    