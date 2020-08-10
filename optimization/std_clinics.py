import requests
import urllib
import pandas as pd
import json

df = pd.read_csv('std_clinic_data.xlsx.csv')
lats = df.Y
longs = df.X

class STDClinics:

        # if len(results['Block']) == 0:
        #     output = {
        #         "FIPS" : None
        #     }
        # else:
        #     answer = results['Block']
        #     output = {
        #         "FIPS": answer.get('FIPS')
        #     }
        #
        # output['latitudes'] = latitude
        # output['longitudes'] = longitude
        #
        # # output['number_of_results'] = len(results['results'])
        # output['status'] = results.get('status')
        # if showall is True:
        #     output['response'] = results

    def get_num_per_fips(self):

        def get_fcc_results(latitude, longitude):

            url = 'https://geo.fcc.gov/api/census/block/find?format=json&latitude={}&longitude={}'.format(latitude,
                                                                                                          longitude)
            results = requests.get(url)
            results = results.json()

            return results

        county_fips = {}

        for lat, long in zip(lats, longs):
            res = get_fcc_results(lat, long)
            data = res['County']['FIPS']
            if data in county_fips:
                county_fips[data] += 1
            else:
                county_fips[data] = 1

        for key, value in county_fips.items():
            print(key, value)

        return county_fips

    # for element in res:
    #     county_FIPS = element['County']
    #     print(county_FIPS)

    #test = json.dumps(res, indent=4)
    #print(test['response'][0]['County'])

    # county_fips = res['Block'][0]['FIPS']
    # print(county_fips)

    # params = urllib.urlencode({'latitude': lat, 'longitude':long, 'format':'json'})
    # url = 'https://geo.fcc.gov/api/census/block/find?' + params
    #
    # response = requests.get(url)
    #
    # data = response.json()
    #
    # print(data['County']['FIPS'])

