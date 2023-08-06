import requests

class DataSource:
    """
    A base class for interacting with Alation DataSource. 
    """

    @staticmethod
    def check_datasource(data_source_name, alation_data_source_id, alation_headers, alation_url):
        try:
            #service_account_authentication for this datasource
            response = requests.get('{base_url}/integration/v1/datasource/'.format(
                base_url=alation_url,alation_data_source_id=alation_data_source_id),headers=alation_headers,verify=True
            ).json()
            for r in response:
                #print(r['title'])
                if data_source_name in r['title']:
                    print("Found correct data source {}".format(r['title']))
            response = requests.get(
                        '{base_url}/integration/v1/datasource/{alation_data_source_id}/'.format(base_url=alation_url,
                        alation_data_source_id=alation_data_source_id),headers=alation_headers, verify = True, timeout = 30).json()
            print('Info for data source {}'.format(response['title']))
            print(response)
        except Exception as e:
            print("Problem with the request for data source")    
            print("ERROR : "+str(e))


    @staticmethod
    def get_datasource_schemas(alation_headers, alation_url, alation_data_source_id):
        import requests
        import json

        # Create a connection to Alation
        print(f"alation_headers:{alation_headers}")
        print(f"alation_data_source_id: {alation_data_source_id}")
        print(f"alation_url: {alation_url}")
        # Pl. Update DS Server ID with the DS Server Id you have created
        # Pl. Update limit and Skip
        ds_id = alation_data_source_id
        limit = 100
        skip = 0
        params = {}
        params['ds_id'] = ds_id
        params['limit'] = limit
        params['skip'] = skip
        params_json = json.dumps(params)
        params_json
        api_url =  f"{alation_url}/integration/v2/schema/"
        print(f"api_url:{api_url}")
        # Get the schemas for the datasource
        response = requests.get(api_url, headers=alation_headers, params=params)
        schemas = json.loads(response.text)

        # Close the connection to Alation
        response.close()

        return schemas

  