__author__ = 'cappetta'

import logging
import json
import os
import inspect
import urllib2
import time
import threading
from Queue import Queue

from SearchResults import SearchResults
from PostalCodes import PostalCodes
# from Logger import Logger as logger

import yaml

creds_file = open('../yaml/creds.yaml', 'r')
_creds = yaml.load(creds_file)

queries_file = open('../yaml/queries.yaml', 'r')
_queries = yaml.load(queries_file)


#########################################################
# Logging Initialization
#########################################################
timestamp = time.strftime("%m%d%Y")
logdir = '../data_files/'
logfile = logdir + "indeed_job_search_" + timestamp + ".log"
dict_of_jobs_by_state = dict()

# debug = False
debug = True
_consoleTrace = True


if not os.path.exists(logdir):
    os.makedirs(logdir)

log = logging.getLogger('indeed_anaysis')
log.setLevel(logging.DEBUG)
fileHandle = logging.FileHandler(logfile)
fileHandle.setLevel(logging.DEBUG)
fileHandle.setFormatter(logging.Formatter('%(asctime)s - %(name)s - (%(threadName)-10s) - %(levelname)s - %(message)s'))
log.addHandler(fileHandle)


class IndeedSearch:

    assert _creds["publisher_id"] is not None, "publisher id in creds.yaml is empty"

    _url='http://api.indeed.com/ads/apisearch?publisher=' + str(_creds["publisher_id"])
    _url+='&limit=25&radius=1' # -1 appears to return a quick result w/ just totals
    _url+='&co=us'
    _url+='&v=2'
    _url+='&format=json'

    queries = _queries["queries"]
    _url_update         = _url
    _currentQuery       = ''
    _iterator           = 0
    _start              = 0
    _iterations         = 3
    _moreResults        = False
    # do you want to always append to the file capturing results?
    _persisentJsonFile  = True
    # do you want to delete any file that exists upon first execution?
    _initializeJsonFile = True
    # do you want to get all the possible results (e.g. first 1000?)
    _getAllResults = True

    def __init__(self):
        pass


    def getInitialSearchQuery(self, query):
        #todo: current query is only search keyword -- what is the impact to adding the zipcode???
        self._currentQuery = query
        return self._url + '&q=' + query


    def getNext25(self, startAt=25, zipcode=''):
        self._start += startAt
        self._iterator += 1
        if _consoleTrace: log.debug("*** Incrementing start Position: [{start}] ***".format(start=self._start))
        self._url_update= self._url + '&q=' + self._currentQuery + '&start=' + str(self._start) + '&l=' + str(zipcode)
        if _consoleTrace: log.debug("url update : [{url}]".format(url=self._url_update))
        return self._url_update

    # def queryAPI(self, url=_url_update + "&q=''", dataFile='indeed_datafile_', query='qa', zipcode=''): #, max_conn=''):
    def queryAPI(self, **kwargs):

        # todo: loop through yesterday's selenium events and perform data
        url         = kwargs["url"]
        zipcode     = kwargs["zipcode"]
        query       = kwargs["query"]
        dataFile    = kwargs["dataFile"]
        max_conn    = kwargs["max_conn"]
        with max_conn:
            url = url + '&l=' + str(zipcode)
            if debug: print "Querying API for - {query}".format(query=url)
            self._currentQuery = query
            log.debug("Querying API for - {q} - thread_count: {ct} - URL: {u}".format(q=query, u=url, ct=threading.active_count()))

            # todo: add assertion to ensure res = a valid object
            res = urllib2.urlopen(url)

            self.parseJSON(res, total="totalResults", query="query", resultset="results", dataFile=dataFile)

            # if we want all the results then get the total from the SearchResults Object and parse everything
            if self._getAllResults: self._iterations = searchResults.iterations

            if self._moreResults:
                while self._iterator < self._iterations:
                    if debug: print "******** Performing Iteration **********"
                    self.executeNextQuery(query_url=self.getNext25(zipcode=zipcode), dataFile=dataFile)
                    if debug: print "******** Performing Iteration - End  **********"


    def executeNextQuery(self, query_url, dataFile):
        if debug: print "**** Executing Query - Start **** \n\t[{url}]".format(url=query_url)
        res = urllib2.urlopen(query_url)
        log.debug("Executing Query {query} ".format(query=query_url))
        # _searchResults = \
        self.parseJSON(res, "totalResults", "query", "results", dataFile)
        if debug: print "**** Executing Query - End ****"


    # todo:  need to convert code and leverage kwargs
    def parseJSON(self, data, **fields):

        if debug:
            curFrame = inspect.currentframe()
            callFrame = inspect.getouterframes(curFrame, 2)
            if _consoleTrace: log.debug("Function [{name}] called by [{callFrame}]::".format(name="parseJson", callFrame=callFrame[1][3]))

        # pass
        # d = fields.get("dataFile")  -- this is for kwargs
        jsonData = json.load(data)
        self.writeOutToFile(full_response=json.dumps(jsonData, indent=4), dataFile=fields['dataFile'])
        array = []
        states = []
        # jobs = []
        state_sumcheck = 0
        global dict_of_jobs_by_state
        global searchResults
        dict_of_jobs_by_state = searchResults.get_dict_of_jobs_by_state()
        iterations=0
        # todo: review logic which attempts to gracefully handle unknown / empty states
        for field in fields:
            if (field == 'totalResults'):
                #todo: if total results > 1000 then the query needs to be redefined as all results have not been captured.
                # I can't parse more than 1000 results due to api limitations
                array.append(jsonData[field])
                if _consoleTrace: log.debug("Metadata: {field} == {value}".format(field=field, value=jsonData[field]))
                searchResults.setResultTotal(jsonData[field])
                if jsonData['totalResults'] <= 25:
                    self._moreResults=False
                    break
                else:
                    self._moreResults=True
                    # assert jsonData[field] > 100
            elif(field == 'totalResults'):
                if _consoleTrace: log.debug("TotalResults: {results}").format(field[field])
            elif(field == 'results'):
                #todo: create methods to extract all the data upon first parse.  Threading requires strong assertions
                for result in jsonData[field]:
                    iterations += 1

                    if result['state'] not in states:
                        states.append(result['state'])
                    if result['state'] in dict_of_jobs_by_state:
                        # if state exists in the dict add the job rec
                        # if debug: print "State in dictionary: {state} -- Dictionary: {dict} ".format(
                        #     state=result['state'], dict=dict_of_jobs_by_state)
                        if result['jobkey'] not in dict_of_jobs_by_state[result['state']]:
                            if debug: print "Job Key is being added to the state dictionary \t[{state}]\t:: {jobkey} " \
                                            ":: {iterator}".format(jobkey=result['jobkey'], state=result['state'],
                                                                   iterator=iterations)
                            (dict_of_jobs_by_state[result['state']]).append(result['jobkey'])
                        else:
                            if debug: print "Job Key already exists within state dictionary \t[{state}]\t:: {jobkey} " \
                                            ":: {iterator}".format(jobkey=result['jobkey'], state=result['state'],
                                                                   iterator=iterations)
                    else:
                        if _consoleTrace: log.debug("State not in dictionary: {state} -- Dictionary: {dict} ".format(
                            state=result['state'], dict=dict_of_jobs_by_state))
                        if debug: print "State & Job Key not in dictionary \t\t\t\t[{state}]\t:: {jobkey} :: " \
                                        "{iterator}".format(jobkey=result['jobkey'], state=result['state'],
                                                            iterator=iterations)
                        dict_of_jobs_by_state[result['state']] = [result['jobkey']]
                        # pprint(result)
                        # print("Date:  {date}").format(date=result['date'])
        if _consoleTrace: log.debug("Size of Job Key Dict:: {size}".format(size=len(dict_of_jobs_by_state.items())))
        searchResults.set_dict_of_jobs_by_state(dict_of_jobs_by_state)
        dict_of_jobs_by_state = searchResults.get_dict_of_jobs_by_state()
        # print("State Counters:\n",pprint(Counter(states.__iter__())))
        if _consoleTrace: log.debug("count of states: {count}".format(count=len(states)))
        for state in states:
            if _consoleTrace: log.debug("State ({state}): {count} ".format(state=state,
                                                                           count= len(dict_of_jobs_by_state[state])))
            state_sumcheck += len(dict_of_jobs_by_state[state])
        if _consoleTrace: log.debug("state sumcheck: {sum} :: Checker: {checker}".format(sum=state_sumcheck,
                                                                                         checker=searchResults.countStateResults()))
        # put data on the queue and allow the Queue to manage writeOutToFile
        self._queue.put(data.read())
        # todo: assertion error is thrown constantly
        # assert state_sumcheck == searchResults.countStateResults()


    def writeOutToFile(self, dataFile=logdir + 'indeed_resultset_' + timestamp, full_response=''):
        while True:
            try:
                if self._initializeJsonFile: os.remove(dataFile)
                self._initializeJsonFile = False
            except OSError:
                log.debug("No Data file to delete")
            if self._persisentJsonFile:
                f = open(dataFile, 'a')
            else:
                f = open(dataFile, 'w')
            # do you want to delete any file that exists upon first execution?

            f.write(full_response.encode('ascii','ignore'))
        f.close()

# order matters - declare the classes before using them in the main thread
searchResults = SearchResults()



def main():
    search = IndeedSearch()
    queries = search.queries
    api_threads = []
    max_conn = threading.BoundedSemaphore(2)
    search._queue = Queue(maxsize=0)

    for query in queries:

        postal = PostalCodes()
        postal.loadZipCodes()
        for zipcode in postal.zipCodes:
            url = search.getInitialSearchQuery(query)
            dataFile = logdir + 'indeed_resultset_' + query + "_" + timestamp
            # todo: create thread pool and limit concurrent queries using semaphore
            thread = threading.Thread(name='QueryExection', target=search.queryAPI, kwargs=dict(url=url, dataFile=dataFile, query=query, zipcode=zipcode, max_conn=max_conn) )
            thread.start()
            api_threads.append(thread)
            # search.queryAPI(url, dataFile=dataFile, query=query, zipcode=zipcode)


if __name__ == '__main__':
    main()


#todo:  things to think about:  Do I want to keep track of historical trends across cities, result sets, and queries?
