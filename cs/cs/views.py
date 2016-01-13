from contextlib import closing
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, HttpResponse
from multiprocessing import Pool
import itertools
import json
import urllib
import urllib2

from forms import *

# necessary API keys and URLs
API_KEY = ''

API_PREFIX = 'https://www.googleapis.com/customsearch/v1?q='
API_SUFFIX = '&cx=017349157168230389014:_ondpc9tdeq&num=10&fields=items(link,snippet,title)&key=%s' % API_KEY
ALCHEMY_PREFIX = 'http://gateway-a.watsonplatform.net/calls/url/URLGetRankedNamedEntities?apikey={{ api_key }}&outputMode=json&disambiguate=0&maxRetrieve=10&coreference=0&url='

def make_keyword_search(result_link):
    '''Makes API call to Alchemy and extracts the entities we want.'''
    
    # make call
    dict_list = make_api_request(ALCHEMY_PREFIX + result_link)['entities']
    
    # initialization
    pruned_entities = []
    entity_list = {'JobTitle': 0, 'Organization': 0, 'TwitterHandle': 0}
    
    # for each entity that we got back
    for entity in dict_list:
        # if the entity is a type that we want and we have less than 5 so far
        if entity['type'] in entity_list.keys() and entity_list[entity['type']] < 5:
            # increment count
            entity_list[entity['type']] += 1
            
            # append to final entities
            pruned_entities.append(entity['text'])
    return pruned_entities
                
def get_keywords(results):
    '''Extracts keywords from each result link using parallel processes'''
    keywords = []
    
    # make keyword searches for all links using multithreading
    with closing(Pool(len(results))) as p:
        keywords = list(itertools.chain.from_iterable(p.map(make_keyword_search, [result['link'] for result in results])))
        p.terminate()
        
    # delete duplicates and return
    return list(set(keywords))

def make_api_request(url):
	'''Returns the dictionary from an API request.'''
	# make an ajax get request
	request = urllib2.Request(url)
	f = urllib2.urlopen(request)
	response = f.read()
	f.close()

	# format and return desired data
	api_dict = json.loads(response)
	return api_dict

def search_with_name(full_name, addition):
    '''Searches the first two pages of Google for a full name plus an additional term.'''
    url = API_PREFIX + urllib.quote(full_name + " " + addition) + API_SUFFIX
    url2 = url + '&start=11'
    return make_api_request(url)['items'] + make_api_request(url2)['items']
    
        
def generic_search(results, links, thing1, thing2):
    try:
        # search first two pages of Google
        result_sublist = search_with_name(thing1, thing2)
    except (KeyError, TypeError), e:
        # if non results, ignore
        print e, thing1, thing2
        return []
    else:
        for result in result_sublist:
            # if we haven't seen this link before
            if result['link'] not in links:
                # add to results, record the link in dictionary (constant time, right?)
                result['score'] = 0
                results.append(result)
                links[result['link']] = True
                
    # return updated results and links
    return results, links

def populate_home_page(request):
    return render(request, 'index.html', {})
    
def populate_about_us(request):
    return render(request, 'about_us.html', {})

def populate_search(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Search(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # initializations
            results = []
            links = {}
            
            # copy form data
            fdict = request.POST
            
            # create full name in quotation marks, username
            full_name = '"' + fdict['first_name'] + " " + fdict['last_name'] + '"'
            username = fdict['username']
            
            # take out first and last names, username, and csrf thing
            del fdict['first_name']
            del fdict['last_name']
            del fdict['csrfmiddlewaretoken']
            del fdict['username']
            
            # convert dictionary to list, since all keywords are treated the same now
            flist = fdict.values()
            
            # delete empty parts of form
            while True:
                try:
                    flist.remove('')
                except ValueError:
                    break
            
            # add results of all our searches for each parameter you typed in
            for element in flist:
                results, links = generic_search(results, links, full_name, element)
            
            # search for just the name
            results, links = generic_search(results, links, full_name, '')
            
            # get keywords on the pages of results
            all_entities = get_keywords(results)
            
            # search for username without name
            if username != '':
                results, links = generic_search(results, links, username, '')
            
            # print all_entities
            return render(request, 'results.html', {'result_list': results, 'associated_words': all_entities, 'full_name': full_name, 'flist': flist})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Search()

    return render(request, 'search.html', {'form': form})
    
def return_static_file(request, fname):
    '''Returns static files (CSS, images, JS, etc.)'''
    f = open(os.path.join(os.getcwd(), fname))
    return HttpResponse(f.read())

def handler404(request, whatever):
    response = render(request, '404.html', {})
    response.status_code = 404
    return response
