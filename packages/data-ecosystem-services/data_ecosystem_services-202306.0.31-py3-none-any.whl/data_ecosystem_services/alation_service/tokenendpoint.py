from email.mime import base
from urllib import response
import requests
import sys
import os
from datetime import datetime

class TokenEndpoint:
    """
    This is a class for managing tokens for use with the Alation API.

    For details of the API tokens, see:
    https://developer.alation.com/dev/docs/authentication-into-alation-apis
    """

    def __init__(self, base_url):
        """
        Creates a TokenEndpoint object

        Parameters
        ----------
        base_url: string
            The root URL for the Alation server to use. It should not have a slash "/" at the end of the URL.
            Example: https://edc.cdc.gov
        """
        self.base_url = base_url

    REFRESH_TOKEN_ENDPOINT = '/integration/v1/validateRefreshToken/'
    API_TOKEN_ENDPOINT = '/integration/v1/createAPIAccessToken/'

    def get_api_token(self, user_id, refresh_token):
        """
        Get an API access token using a refresh token.

        Parameters
        ----------
        user_id: int
            The ID of the user obtaining the API access token
        refresh_token: string
            A valid refresh token from the user

        Returns
        -------
        string
            An API access token        
        """
        token_data = {
            "refresh_token": refresh_token,
            "user_id": user_id
        }
        response = requests.post(
            '{base_url}{api}'.format(base_url=self.base_url, api=self.API_TOKEN_ENDPOINT
            ), data=token_data, verify = True, timeout = 30)
        response.raise_for_status()
        alation_access_token = response.json().get("api_access_token")
        return alation_access_token

    
    def validate_refresh_token(self, user_id, refresh_token):
        """
        Confirms that a refresh token is valid and return the number of days until
        the token expires.

        The function will cause the interpreter to exit if the token is invalid.

        Parameters
        ----------
        user_id: int
            The ID of the user obtaining the API access token
        refresh_token: string
            A valid refresh token from the user

        Returns
        -------
        int
            The number of days until the refresh token expires.        
        """

        days_to_expiration = None
        token_data = {
            "refresh_token": refresh_token,
            "user_id": user_id
        }
        response = requests.post(
            '{base_url}{refresh}'.format(base_url=self.base_url, refresh=self.REFRESH_TOKEN_ENDPOINT
        ), data=token_data, verify = True, timeout = 30)
        response.raise_for_status()
        json_body = response.json()
        token_status = json_body.get("token_status", "invalid").lower()
        token_expires_at = json_body.get("token_expires_at").split("T")[0]
        if token_status == "active":
            print("INFO: Alation Refresh token is valid")
            print("Token will expire on " + token_expires_at)
            # Regenerate token if expires within 7 days
            if token_expires_at:
                days_to_expiration = abs(datetime.strptime(token_expires_at, "%Y-%m-%d") - datetime.now()).days
                if days_to_expiration < 7:
                    print('Alation Refresh Token will expire in ' + str(days_to_expiration) + ' days. Please create a new refresh token and replace the Pipeline API Token Variable.')
                    sys.exit('Alation Refresh Token expiring in ' + str(days_to_expiration) + ' days.')

            elif token_status == "expired":
                print("ERROR: Alation Refresh Token has EXPIRED. Please create a new refresh token and replace the Pipeline API Token Variable.")
                sys.exit('Expired Alation Refresh Token.')
            else:
                print("ERROR: Alation Refresh Token is INVALID. Please create a new refresh token and replace the Pipeline API Token Variable.")
                sys.exit('Invalid Alation Refresh Token.')
        return days_to_expiration


    @classmethod
    def getAPIToken(cls, alation_refresh_token, alation_user_id, alation_url):
        """Obtains an API token from Alation using a refresh token, user ID, and Alation URL.

        Args:
            alation_refresh_token (str): A refresh token obtained from Alation.
            alation_user_id (str): The user ID associated with the refresh token.
            alation_url (str): The URL of the Alation instance to connect to.

        Raises:
            Exception: If there is an error obtaining the API token.

        Returns:
            str: The API token.
        """

        print(f"Getting API token with {alation_refresh_token} refresh token for user {alation_user_id}")
        token_data = {
            "refresh_token": alation_refresh_token,
            "user_id": alation_user_id
        }
        alation_access_token = ""
        token_status = ""
        token_expires_at = None
        print('Token data is {token_data}')
        try:
            token_r = requests.post(
                '{base_url}/integration/v1/validateRefreshToken/'.format(base_url=alation_url
            ), data=token_data, verify = False, timeout = 30).json()
            token_status = token_r.get("token_status", "invalid").lower()
            token_expires_at = token_r.get("token_expires_at").split("T")[0]
        except Exception as e:
            print("Error in Alation refresh token validation request.")
            print("ERROR : "+str(e))
            raise e

        if token_status == "active":
            print("INFO: Alation Refresh token is valid")
            print("Token will expire on " + token_expires_at)
            # Regenerate token if expires within 7 days
            if token_expires_at:
                days_to_expiration = abs(datetime.strptime(token_expires_at, "%Y-%m-%d") - datetime.now()).days
                if days_to_expiration < 7:
                    print('Alation Refresh Token will expire in ' + str(days_to_expiration) + ' days. Please create a new refresh token and replace the Pipeline API Token Variable.')
                    sys.exit('Alation Refresh Token expiring in ' + str(days_to_expiration) + ' days.')
            
                try:
                    access_token_r = requests.post(
                        '{base_url}/integration/v1/createAPIAccessToken/'.format(base_url=alation_url
                    ), data=token_data, verify=True, timeout=30).json()
                    alation_access_token = access_token_r.get("api_access_token")
                    print('Alation API access token created is {alation_access_token}')
                except Exception as ex_access_token_request:
                    print("Error in Alation access token request.")
                    print(f"ERROR : {str(ex_access_token_request)}")
        elif token_status == "expired":
            print("ERROR: Alation Refresh Token has EXPIRED. Please create a new refresh token and replace the Pipeline API Token Variable.")
            sys.exit('Expired Alation Refresh Token.')
        else:
            print("ERROR: Alation Refresh Token is INVALID. Please create a new refresh token and replace the Pipeline API Token Variable.")
            sys.exit('Invalid Alation Refresh Token.')

        # 0.1 Create the Authorization headers with the API_TOKEN
        alation_headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Token": alation_access_token,
            "token": alation_access_token
        }

        return alation_access_token, alation_headers

    # Won't work for CDC because we use SSO
    @staticmethod
    def create_alation_refresh_token(config):

        edc_alation_base_url = config.get("edc_alation_base_url")
        az_kv_edc_client_secret_key = config.get("az_kv_edc_client_secret_key")
        az_kv_edc_env_var =  az_kv_edc_client_secret_key.replace("-", "_")
        edc_alation_client_id = config.get("edc_alation_client_id")

        # Retrieve the value of the environment variable
        edc_alation_client_secret = os.getenv(az_kv_edc_env_var)
        api_url = "/integration/v1/createRefreshToken/"
        project_id = config.get("project_id")
        # Replace email_address_here and password_here with your email and password
        data = {
        "username": edc_alation_client_id,
        "password": edc_alation_client_secret,
        "name": project_id 
        }

        print (f"data:{data}")
        # Get refresh token
        headers = {"Content-Type": "application/json"}
        response = requests.post(edc_alation_base_url + api_url, json=data)
        print(response.json())
        refresh_token = response.json()
        return refresh_token

    @staticmethod
    def create_api_access_token_via_refresh(edc_alation_base_url, edc_alation_user_Id, edc_alation_refresh_token):

        # Retrieve the value of the environment variable
        api_url =  "/integration/v1/createAPIAccessToken/"
        auth_url = edc_alation_base_url + api_url
        data = {
            "refresh_token": edc_alation_refresh_token,
            "user_id": edc_alation_user_Id
        }
        print(f"data: {data}")
        print(f"auth_url: {auth_url}")
        response = requests.post(auth_url, json=data )

        api_access_token = "not_set"
        # Check the response status code to determine if the request was successful
        if response.status_code in (200, 201) :
            # Extract the API token from the response           
            response_data = response.json()
            print(f"response_data: {response_data}")
            api_access_token = response_data.get("api_access_token","not_set")
            print(f"Generated API response: {api_access_token}")
        else:
            print("Failed to generate API token:" + str(response))

        return api_access_token

    @staticmethod
    def create_api_access_token_via_login(config):

        edc_alation_base_url = config.get("edc_alation_base_url")
        az_kv_edc_client_secret_key = config.get("az_kv_edc_client_secret_key")
        az_kv_edc_env_var =  az_kv_edc_client_secret_key.replace("-", "_")
        edc_alation_client_id = config.get("edc_alation_client_id")

        # Retrieve the value of the environment variable
        edc_alation_client_secret = os.getenv(az_kv_edc_env_var)
        api_url = "/account/auth/"
        # Get refresh token
        auth_url = edc_alation_base_url + api_url
        print(f"edc_alation_client_id: {edc_alation_client_id}")
        print(f"edc_alation_client_secret: {edc_alation_client_secret}")
        print(f"auth_url: {auth_url}")
        response = requests.post(auth_url, auth=(edc_alation_client_id, edc_alation_client_secret) )

        api_token = "not_set"
        # Check the response status code to determine if the request was successful
        if response.status_code == 200:
            # Extract the API token from the response
            api_token = response.json()["api_token"]
            print(f"Generated API token: {api_token}")
        else:
            print("Failed to generate API token:" + str(response))

        return api_token

    @classmethod
    def get_api_access_token(cls, edc_alation_base_url, edc_alation_user_Id, edc_alation_refresh_token):
        """Gets an API access token using the provided Alation base URL, user ID, and refresh token.

        This method sends a request to the Alation API to get an access token, which is then returned.

        Args:
            edc_alation_base_url (str): The base URL for the Alation instance.
            edc_alation_user_Id (str): The user ID for the Alation API.
            edc_alation_refresh_token (str): The refresh token to use when requesting an access token from the Alation API.

        Returns:
            str: The API access token.
        """

        api_token = cls.create_api_access_token_via_refresh(edc_alation_base_url, edc_alation_user_Id, edc_alation_refresh_token)
        return api_token
