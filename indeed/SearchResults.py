

class SearchResults():
    ''' a class for indeed search results
    '''

    totalResult = 0
    iterations = 0
    dict_of_jobs_by_state = dict()
    _debug = True
    log = ''

#todo: fix the ability to log from non-IndeedSearch Classes
    def __init__(self,log=''):
        self.log = log
        pass

    def setResultTotal(self, result):
        self.totalResult = result
        if self._debug: self.log.debug("Setting Results Total:: {0}".format(result))
        self.setNumberOfIterations((result/25))

    def setNumberOfIterations(self, value):
        self.iterations = value
        if self._debug: self.log.debug('total pages to iterate = {0}'.format(value))
        # todo: fix iteration issue (need to round up)

    # def getNumberOfIterations(self):
    #     return self.iterations
    #     print('total pages to iterate = {0}').format(value)
    #     todo: fix iteration issue (need to round up)

    def countStateResults(self):
        return sum(len(self.dict_of_jobs_by_state[state]) for state in self.dict_of_jobs_by_state)
        # for state in self.dict_of_jobs_by_state:
        #     print "state: {state} && length:: {length}".format(state=state, length=len(dict_of_jobs_by_state[state]))

    def addjobToStateDict(self, state='', jobKey=''):
        (self.dict_of_jobs_by_state[state]).append(jobKey)

    def get_dict_of_jobs_by_state(self):
        return self.dict_of_jobs_by_state

    def set_dict_of_jobs_by_state(self, new_dict):
        self.dict_of_jobs_by_state = new_dict

    def recordResults(self, results, zipcode, query):
        # for each result, I want to capture the zipcode,
        pass

    def test_results_eq_dict_count(self):
        assert self.totalResult == self.countStateResults()

        # Graphical Mapping
        # http://wrobstory.github.io/2013/10/mapping-data-python.html
        # https://github.com/areski/python-nvd3
        #         http://python-nvd3.readthedocs.org/en/latest/classes-doc/discrete-bar-chart.html

        #
        # from nvd3 import pieChart
        # type = 'pieChart'
        # chart = pieChart(name=type, color_category='category20c', height=450, width=450)
        # xdata = ["Orange", "Banana", "Pear", "Kiwi", "Apple", "Strawberry", "Pineapple"]
        # ydata = [3, 4, 0, 1, 5, 7, 3]
        # extra_serie = {"tooltip": {"y_start": "", "y_end": " cal"}}
        # chart.add_serie(y=ydata, x=xdata, extra=extra_serie)
        # chart.buildcontent()
        # print chart.htmlcontent

    # todo: create a generic save method which saves the entire listing and create sub-objects like state/zip dict
    def saveJobs(self, single_result):
        _jobtitle   = single_result['jobtitle']
        _company    = single_result['company']
        _city       = single_result['city']
        _state      = single_result['state']
        _country    = single_result['country']
        _location   = single_result['formattedLocation']
        _source     = single_result['source']
        _date       = single_result['date']
        _url        = single_result['url']
        _jobkey     = single_result['jobkey']
        _sponsored  = single_result['sponsored']
        _easyApply  = single_result['indeedApply']
        _full_loc   = single_result['formattedLocationFull']
        _age        = single_result['formattedRelativeTime']

