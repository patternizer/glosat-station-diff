# glosat-station-diff

Python code to extract individual station file from GloSAT archive in Pandas and to calculate differences with respect to a given CRUTEM station file version and write to CSV in CRUTEM format. Part of ongoing work for the [GloSAT](https://www.glosat.org) project: www.glosat.org. 

## Contents

* `glosat-station-diff.py` - main python script to compare a CRUTEM station file version with its corresponding variant in the GloSAT archive and to calculate differences and write out to CSV in CRUTEM format
* `make-stationfile.py` - helper python script to extract individual station data from the GloSAT archive Pandas dataframe and write to CSV in CRUTEM format (not necessary for running glosat-station-diff.py)
* `quicklook_dat.py` - helper python script to read in a given CRUTEM station file version and plot monthly timeseries (not necessary for running glosat-station-diff.py)

## Instructions for use

The first step is to clone the latest glosat-station-diff code and step into the installed Github directory: 

    $ git clone https://github.com/patternizer/glosat-station-diff.git
    $ cd glosat-station-diff

Then create a DATA/ directory and copy to it the CRUTEM station file version you would like to compare with the existing record in the GloSAT pickled temperature archive file which also needs to be placed in the same directory.

It is necessary only to know the stationcode for the file being compared. This can be found by typing in for example the station name in the GloSAT station viewer [app](https://glosat-py.herokuapp.com/glosat).

### Using Standard Python

The code is designed to run in an environment using Miniconda3-latest-Linux-x86_64.

    $ python glosat-station-diff.py
    $ python make-stationfile.py (optional)
    $ python quicklook_dat.py (optional)
   
## License

The code is distributed under terms and conditions of the [Open Government License](http://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).

## Contact information

* [Michael Taylor](michael.a.taylor@uea.ac.uk)


