# Created By: Nisarga Patel
# License: MIT

# dependencies
try:
    from flask import Flask

except ImportError:

    print("was unable to import flask!")

try:
    import collections

except ImportError:

    print("was unable to import itertools and collections!")

# initialize application global variables
app = Flask(__name__)
app.secret_key = 'some_secret'

# initializing two global variables: blocks, and locations
# blocks is a dictionary that will store ip range data
blocks = {}

# locations is a dictionary that will store location data
locations = {}

# preconditions: line must be a valid list of words
# postconditions: modifies line so there are no quotes and newline chars
def parse(line):

    for i in range(len(line)):

        line[i] = line[i].translate({ord('"') : None, ord('\n') : None})

# preconditions: a valid filename and dictionary must be passed
# postconditions: the data in the file is parsed and in the dictionary
def readandparse(filename, mydict):

    with open(filename) as f:

        next(f)
        next(f)
        for line in f:

            # split the line at the comma
            line = line.split(',')

            parse(line)

            mydict.update({line[0] : line[1:-1]})

# preconditions: valid locations value list is passed 
# Ex: ['US', '-73.123123', 'New York' ...]
# postconditions: returns a json array 
# Ex: {'country' : 'US', 'longitude' : '-73.123123' ...}
def formatlocation(values):

    # all the possible columns
    columns = ['country','region','city','postalCode','latitude','longitude','metroCode','areaCode']
    result = {}

    for i in range(len(values)):

        if i < len(columns):

            result[columns[i]] = values[i]

    return result

print("Nisarga Patel's GeoLiteCity HTTP API")
print("---- starting initialization ----")
print("reading & parsing GeoLiteCity-Blocks.csv ...")

readandparse('GeoLiteCity-Blocks.csv', blocks)

print("reading & parsing GeoLiteCity-Blocks.csv completed!")

print("ordering blocks dictionary ...")

blocks = collections.OrderedDict(sorted(blocks.items()))

print("ordering blocks completed!")

print("reading & parsing GeoLiteCity-Location.csv ...")

readandparse('GeoLiteCity-Location.csv', locations)

print("reading & parsing GeoLiteCity-Location.csv completed!")

print("---- initialization complete ----")

# precondition: valid term passed in
# postcondition: returns search results
def searchterm(term):

    results = []

    for locID in locations:

        valuelist = locations[locID]
        if term in valuelist:

            results.append({locID : formatlocation(valuelist)})

    if results == []:

        return "results not found!"

    else:

        return results

# precondition: valid location id
# postcondition: returns array of json data
def getlocationdata(locID):

    return {locID : formatlocation(locations[locID])}

# precondition: valid ip address
# postcondition: returns a decimal representation of ip
def convertipdec(ip):

    dotcount = 0
    for char in ip:

        if char == '.':

            dotcount += 1

    if dotcount < 3:

        return False


    ip = ip.split('.')

    return str((int(ip[0]) * (256**3)) + (int(ip[1]) * (256**2)) + (int(ip[2]) * 256) + (int(ip[3])))

# api endpoint for searchterm method
@app.route('/searchdata/<term>')
def searchdata(term):

    return str(searchterm(term))

# reverse ip address lookup (get location from ip)
@app.route('/getipdata/<ipaddr>')
def getipdata(ipaddr):

    ipaddr = convertipdec(ipaddr)

    results = []

    if ipaddr:

        for key in blocks:

            # if between startip and endip
            if ipaddr >= key and ipaddr <= blocks[key][0]:

                # append the location id
                results.append(blocks[key][1])

        if results != []:
            return str(getlocationdata(results[-1]))

        return "location not found"

    return "invalid ip"

def main():

    app.run(port=2000, debug=True, use_reloader=False)

main()