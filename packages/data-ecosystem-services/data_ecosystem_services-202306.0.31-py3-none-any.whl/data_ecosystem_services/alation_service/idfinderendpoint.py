import requests
from .endpoint import Endpoint

# This isn't a true endpoint as it actually points to multiple URLS
class IdFinderEndpoint(Endpoint):
    """
    A class for interacting with the Alation V2 API to find the IDs of objects by type and name.

    This is a subclass of Endpoint, so users should instantiate the class by providing an API token
    and the base URL of the Alation server to work with.

    Note that this functionality may require a user with admin priviledges.
    """

    METADATA_ENDPOINT = '/integration/v2'

    def find(self, object_type, name):
        """
        Finds the identifier for an object in Alation given a name and object type.

        Parameters
        ----------
        object_type: string
            The Alation object type: "schema", "table" or "attribute". Note that columns are called 
            attributes in Alation.
        name: string
            The name of the object in Alation.

        Returns
        -------
        int or None
            If the call finds a single object, it will return the ID for the object. If it can't
            find anything or if it finds more than one object, it will return None.
        """
        url = "{base_url}{metadata_endpoint}/{object_type}?name={name}".format(base_url = self.base_url, 
            metadata_endpoint = self.METADATA_ENDPOINT, object_type = object_type, name = name)
        response = requests.get(url, headers=self.base_headers(), verify=True)
        response.raise_for_status()
        response_json = response.json()
        if len(response_json) == 1:
            return response_json[0]['id']
        else:
            return None