"""
This example demonstrates how to combine multiple data sources (raw
data and Web API). Here we generate a bar chart containing video game consoles
of multiple generations and their respective prices.

We use the API provided by Giantbomb.com as a data source for the available 
video game platforms. Since prices there are only stored in the amount of money
you had to put on the table back when the console was released, we also want
to put those prices into perspective with the current value of the US Dollar.
For this we use the CPI made available by the Federal Reserve Bank of St.
Louis.

http://www.giantbomb.com/api/
http://research.stlouisfed.org/fred2/

Please note that the inflation-calculation here is not really accurate but
it's also not really the point of this tutorial to show you how to calculate
currency inflation but to show you how to combine multiple data sources
including APIs ;-)

To be able to use this script, you have to register for a Giantbomb API key
and pass it to this script using the --giantbomb-api-key argument.

Written by Horst Gutmann (https://github.com/zerok)
"""


from __future__ import print_function

import requests


CPI_DATA_URL = 'http://research.stlouisfed.org/fred2/data/CPIAUCSL.txt'


class CPIData(object):
    """Abstraction of the CPI data provided by FRED.
    This stores internally only one value per year."""
    
    def __init__(self):
        self.year_cpi = {}
        self.last_year = None
        self.first_year = None
    
    
    def load_from_url(self, url, save_as_file=None):
        """Loads data from a given URL. 
        The downloaded file can also be saved into a location for later
        re-use with the 'save_as_file' parameter specifying a filename.
        After fetching the file this implementation uses load_from_file
        internally."""

        # We don't really know how much data we are going to get here, so
        # it is recommended to just keep as little data as possible in memory
        # at all times. Since python-requests supports gzip-compression by
        # default and decoding these chunks on their own isn't that easy,
        # we just disable gzip with the empty "Accept-Encoding" header.
        fp = requests.get(url, stream=True, 
                        headers = {'Accept-Encoding' : None}).raw
        
        # If we did not pass in a save_as_file parameter, we just return
        # the raw data we got from the previous line.
        if save_as_file is None:
            return self.load_from_file(fp)
        
        # Else, we write to the desired file.
        else:
            with open(save_as_file, 'wb+') as out:
                while True:
                    buffer = fp.read(81920)
                    if not buffer:
                        break
                    out.write(buffer)
            with open(save_as_file) as fp:
                return self.load_from_file(fp)
    
    
    def load_from_file(self, fp):
        """Loads CPI data from a given file-like object."""
        
        # When iterating over the data file we will need a handful of
        # temporary variables.
        current_year = None
        year_cpi = []
        for line in fp:
            # The actual content of the file starts with a header line
            # starting with the string 'DATE'. Until we reach this line
            # we can skip ahead.
            while not line.startswith('DATE'):
                pass
            
            # Each line ends with a new-line character which we strip
            # here to make the data more easily usable.
            data = line.rstrip().split()
            
            # While we are dealing with calendar data, the format is
            # simple enough that we don't need a full date-parser.
            # All we want is the year which can be extracted by simple
            # string splitting.
            year = int(data[0].split('-')[0])
            cpi = float(data[1])
            
            if self.first_year is None:
                self.first_year = year
            self.last_year = year
            
            # The moment we reach a new year, we have to reset the
            # CPI data and calculate the average CPI of the
            # current_year.
            
            if current_year != year:
                if current_year != None:
                    self.year_cpi[current_year] = sum(year_cpi)/len(year_cpi)
                year_cpi = []
                current_year = year
            year_cpi.append(cpi)
        
        # We have to do the calculation once again for the last year
        # in the dataset.
        if current_year is not None and current_year not in self.year_cpi:
            self.year_cpi[current_year] = sum(year_cpi)/len(year_cpi)
    
    
    def get_adjusted_price(self, price, year, current_year=None):
        """Returns the adapted price from a given year compared to what
        current year is specified.
        This is essentially the calculated inflation for an item."""
        
        if current_year is None:
            current_year = datetime.datetime.now().year
        
        # If our data range doesn't provide a CPI for the given year,
        # use the edge data.
        if year < self.first_year:
            year = self.first_year
        elif year > self.last_year:
            year = self.last_year
        
        year_cpi = self.year_cpi[year]
        current_cpi = self.year_cpi[current_year]
        
        return float(price) / year_cpi * current_cpi


def main():
    """This function handles the actual logic of this script."""
    
    # Grab CPI/Inflation data
    
    # Grab API/game platform data
    
    # Figure out the current price of each platform. 
    # This will require looping through each game platform we received,
    # and calculate the adjusted price based on the CPI data we also
    # received. During this point, we should also validate our data so
    # we do not skew our results.
    
    # Generate a plot/bar graph for the adjusted price data.
    
    # Generate a CSV file to save the adjusted price data.


if __name__ == '__main__':
    main()