

import csv


class PostalCodes():
    _zipcode = 13029
    _iterator = 0
    zipCodes = []
    _debug = False

    def __init__(self):
        pass

    # this will load the csv file into memory
    # Source of zipcodes: https://www.aggdata.com/node/86
    def loadZipCodes(self, file='../data_files/us_postal_codes.csv'):
        with open(file, 'rb') as csvfile:
            fileReader = csv.DictReader(csvfile, delimiter=',')
            for row in fileReader:
                if self._debug:
                    print "ZipCode: {zip}".format(zip=row["Postal Code"])
                self.addZipToList(row["Postal Code"])
                self._iterator += 1
                if self._iterator > 10:
                    break

    # this will return the next ZipCode in the list
    def getNextZipCode(self):
        pass

    def addZipToList(self, zipCode):
        if zipCode not in self.zipCodes:
            self.zipCodes.append(zipCode)