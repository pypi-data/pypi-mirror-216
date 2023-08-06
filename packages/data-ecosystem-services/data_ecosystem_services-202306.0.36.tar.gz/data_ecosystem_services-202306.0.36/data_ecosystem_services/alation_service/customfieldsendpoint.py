import requests
import json
from .endpoint import Endpoint

class CustomFieldsEndpoint(Endpoint):
    """
    A class for interacting with the bulk metadata upload from the Alation V1 API.

    This is a subclass of Endpoint, so users should instantiate the class by providing an API token
    and the base URL of the Alation server to work with.
    """
    BULK_METADATA_ENDPOINT = '/api/v1/bulk_metadata/custom_fields/default'

    # Note - this function could be improved to batch updates for a particular object type.
    # Right now, it will only update one object at a time.
    def update(self, object_type, data_source_id, key, fields):
        """
        Update business metadata on an object in Alation.

        Parameters
        ----------
        object_type: string
            The Alation object type: "schema", "table" or "attribute". Note that columns are called 
            attributes in Alation.
        data_source_id: int
            The ID of the data source that this object belongs to.
        key: string
            The object key in Alation. See https://developer.alation.com/dev/docs/object-keys for
            details. This should be the key, except for the data source ID
        fields: dict
            The fields to update
        """
        updates = []
        single_update = {'key': '{}.{}'.format(data_source_id, key), **fields}
        updates.append(single_update)
        array_of_json = map(lambda u: json.dumps(u), updates)
        request_body = "\n".join(array_of_json)
        url = "{base_url}{metadata_endpoint}/{object_type}?replace_values=true".format(base_url = self.base_url, 
            metadata_endpoint = self.BULK_METADATA_ENDPOINT, object_type = object_type)
        response = requests.post(url, headers=self.method_with_body_headers(), data=request_body, verify=True)
        response.raise_for_status()

