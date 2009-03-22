#import plugins.plugin

from twisted.web import client
from BeautifulSoup import BeautifulSoup, Tag
from core import dispatcher
from core.events import COMMAND
from twisted.internet import reactor

def txtize(soup):
    if not isinstance(soup,Tag):
        return soup
    return ''.join(map(txtize,soup.childGenerator()))

class MoinSearch(object):
    _site = 'http://www.python.com.ar'
    _places = {'body':
                     {'path':'/moin?action=fullsearch&context=180&value=%s&fullsearch=Texto',
                      'tag': 'dt'},
               'title':
                     {'path': '/moin?action=fullsearch&context=180&value=%s&titlesearch=T%%C3%%ADtulos',
                      'tag': 'li'}
                    }

    def __init__(self,disp):
        disp.register(COMMAND,self.process)
        #dispatcher.register(COMMAND,self.process,['wiki'])

    def get_full_query(self,where,query):
        return '%s/%s' % (self._site,self._places[where]['path'] % query)

    def process(self, command, user, channel, *args):
        query = ' '.join(map(str,args))
        d = client.getPage(self.get_full_query('title',query))
        d.addCallback(self.parse_page)
        #d.addCallback(self.otro)
        return d

    def otro(self,titleresults):
        if titleresults:
            return titleresults
        d = client.getPage(self.get_full_query('body',query))
        d.addCallback(self.parse_page)

    def parse_page(page):
        soup = BeautifulSoup(page.read())
        if page.geturl() != url:
            # If there was only one result, moin redirected me to it
            title = txtize(soup.find('head').find('title'))
            return ['%s: %s' % (title,page.geturl())]
        div = soup.find('div','searchresults')
        results = []
        for item in div.findAll(self._places[where]['tag']):
            anchor = item.find('a')
            href = self._site + anchor.get('href')
            name = txtize(anchor)
            results.append('%s: %s' % (name,href))
        return results





    def process(self):
        results = []
        for place in ['title','body']: #I want first title results!
            d = self.get_results(place)
            d.addCallback(self.parse_page)

            #results = self.get_results(place)
            if results:
                break
        results_count = len(results)
        if not results:
            return (0,[])
        if results_count > max_resutls:
            return (results_count,[self.get_full_query(place)])
        return (results_count,results)

    def get_results(self,where):
        url = self.get_full_query(where)
        return client.getPage(url)

def main():
    disp = dispatcher.Dispatcher()
    ms = MoinSearch(disp)
    disp.push(COMMAND,'wiki', 'rafen', '#pyar', 'pycamp')
    reactor.run()

if __name__ == '__main__':
    main()
else:
    print __name__




#class _MoinSearch(object):
    #_site = 'http://www.python.com.ar'
    #_places = {'body':
                     #{'path':'/moin?action=fullsearch&context=180&value=%s&fullsearch=Texto',
                      #'tag': 'dt'},
               #'title':
                     #{'path': '/moin?action=fullsearch&context=180&value=%s&titlesearch=T%%C3%%ADtulos',
                      #'tag': 'li'}
                    #}

    #def __init__(self,query,site=None,places=None):


        #self.query = query
        #if site is not None:
            #self._site = site
        #if places is not None:
            #self._places = places

    #def get_full_query(self,where):
        #return '%s/%s' % (self._site,self._places[where]['path'] % self.query)

    #def process(self, max_resutls=1):
        #results = []
        #for place in ['title','body']: #I want first title results!
            #results = self.get_results(place)
            #if results:
                #break
        #results_count = len(results)
        #if not results:
            #return (0,[])
        #if results_count > max_resutls:
            #return (results_count,[self.get_full_query(place)])
        #return (results_count,results)

    #def get_results(self,where):
        #url = self.get_full_query(where)
        #page = urllib.urlopen(url)
        #soup = BeautifulSoup(page.read())
        #if page.geturl() != url:
            ## If there was only one result, moin redirected me to it
            #title = txtize(soup.find('head').find('title'))
            #return ['%s: %s' % (title,page.geturl())]
        #div = soup.find('div','searchresults')
        #results = []
        #for item in div.findAll(self._places[where]['tag']):
            #anchor = item.find('a')
            #href = self._site + anchor.get('href')
            #name = txtize(anchor)
            #results.append('%s: %s' % (name,href))
        #return results

