# GeoLite City API
## By: Nisarga Patel
## License: MIT

## Dependencies
- [Flask](http://flask.pocoo.org/docs/0.10/)
- Python 3

## Usage

### Necessary files
The CSV files needed to run the API can be found [here](http://geolite.maxmind.com/download/geoip/database/GeoLiteCity_CSV/GeoLiteCity-latest.zip)

### Searching through GeoLite City data
Example: Get data about Baltimore using curl

curl localhost:2000/searchdata/Baltimore

### Reverse IP lookup
Example: Using IP address for Facebook 173.252.120.6

curl localhost:2000/getipdata/173.252.120.6

