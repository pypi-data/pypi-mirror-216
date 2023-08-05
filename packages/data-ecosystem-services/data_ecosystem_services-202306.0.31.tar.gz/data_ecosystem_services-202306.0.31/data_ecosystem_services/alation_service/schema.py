import requests
import json
from opentelemetry import trace

from .tokenendpoint import TokenEndpoint
from .customfieldsendpoint import CustomFieldsEndpoint
from .tagsendpoint import TagsEndpoint
from .idfinderendpoint import IdFinderEndpoint


from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

from data_ecosystem_services.az_storage_service import (
    az_storage_queue as pade_az_storage_queue
)


class Schema:
    """
    A base class for interacting with Alation Schema. 
    """


    @staticmethod
    def get_schema(alation_headers, alation_url, alation_schema_id):
        """ 
        Retrieves details for a specific schema from Alation using the provided schema ID.

        Args:
            alation_headers (dict): Headers to be used in the request, typically including authentication information.
            alation_url (str): The base URL of the Alation instance.
            alation_schema_id (int): ID of the Alation schema to retrieve.

        Returns:
            dict: A dictionary containing details of the schema.
        """    

        logger_singleton = pade_env_logging.LoggerSingleton.instance()
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance()
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_schema"):

            try:
                logger_singleton = pade_env_logging.LoggerSingleton.instance()
                logger = logger_singleton.get_logger()

                # Create a connection to Alation
                logger.info(f"alation_headers:{alation_headers}")
                logger.info(f"alation_schema_id: {alation_schema_id}")
                logger.info(f"alation_url: {alation_url}")
                # Pl. Update DS Server ID with the DS Server Id you have created
                # Pl. Update limit and Skip
                schema_id = alation_schema_id
                limit = 100
                skip = 0
                params = {}
                params['id'] = schema_id
                params['limit'] = limit
                params['skip'] = skip
                params_json = json.dumps(params)
                params_json
                api_url = f"{alation_url}/integration/v2/schema/"
                logger.info(f"api_url:{api_url}")
                # Get the schemas for the datasource
                response = requests.get(
                    api_url, headers=alation_headers, params=params)
                schemas = json.loads(response.text)

                # Close the connection to Alation
                response.close()

                if schemas:
                    return schemas[0]
                else:
                    return {"reason": "no results"}

            except Exception as e:
                # Log the error.
                logger_singleton = pade_env_logging.LoggerSingleton.instance()
                logger = logger_singleton.get_logger()

                error_message = f"An error occurred: {e}",
                logger.error(error_message)
                return {"reason": error_message}

    @staticmethod
    def get_schema_tables(alation_schema_id, alation_headers, alation_url, alation_data_source_id):
        """ 
        Get list of tables for this schema from the provided Alation URL, like: "https://alation_domain/integration/v2/table/?limit=100000&skip=0".

        Args:
            alation_schema_id (int): ID of the Alation schema.
            alation_headers (dict): Headers to be used in the request, typically including authentication information.
            alation_url (str): The base URL of the Alation instance.
            alation_data_source_id (int): ID of the Alation data source.

        Returns:
            list: List of tables in the schema. Each table is represented as a dictionary.
        """    

        logger_singleton = pade_env_logging.LoggerSingleton.instance()
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance()
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_schema_tables"):
            response = requests.get(
                '{base_url}/integration/v2/table/?skip=0&schema_id={schema_id}&ds_id={ds_id}'.format(base_url=alation_url,
                                                                                                     schema_id=alation_schema_id, ds_id=alation_data_source_id), headers=alation_headers,
                timeout=30).json()
            # Go through all tables listed for this schema and add to our manifest template
            tables_dict = {}
            for thisTable in response:
                tables_dict[thisTable['name']] = thisTable
            return tables_dict

    @staticmethod
    def get_table_columns(alation_schema_id, alation_headers, alation_url, alation_data_source_id, alation_table_id):
        """ 
        Get list of tables for this schema from the provided Alation URL, like: "https://alation_domain/integration/v2/table/?limit=100000&skip=0".

        Args:
            alation_schema_id (int): ID of the Alation schema.
            alation_headers (dict): Headers to be used in the request, typically including authentication information.
            alation_url (str): The base URL of the Alation instance.
            alation_data_source_id (int): ID of the Alation data source.
            alation_table_id (int): ID of the Alation table.

        Returns:
            list: List of tables in the schema. Each table is represented as a dictionary.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance()
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance()
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_table_columns"):
            response = requests.get(
                '{base_url}/integration/v2/column/?skip=0&schema_id={schema_id}&ds_id={ds_id}&table_id={table_id}'.format(base_url=alation_url,
                                                                                                                          schema_id=alation_schema_id, ds_id=alation_data_source_id, table_id=alation_table_id), headers=alation_headers,
                timeout=30).json()
            # Go through all tables listed for this schema and add to our manifest template
            columns_dict = {}
            for thisColumn in response:
                columns_dict[thisColumn['name']] = thisColumn
            return columns_dict

    @classmethod
    def upload_schema_manifest(cls, alation_schema_id, alation_headers, edc_alation_base_url, manifest, manifest_file, alation_data_source_id, alation_refresh_token, schema_name, config):
        """ 
        Uploads a schema manifest to Alation.

        Args:
            alation_schema_id (int): ID of the Alation schema to which the manifest should be uploaded.
            alation_headers (dict): Headers to be used in the request, typically including authentication information.
            edc_alation_base_url (str): The base URL of the Alation instance.
            manifest (dict): The schema manifest to be uploaded.
            manifest_file (str): Path to the file containing the schema manifest.
            alation_data_source_id (int): ID of the Alation data source related to the schema.
            alation_refresh_token (str): Alation API refresh token.
            schema_name (str): Name of the schema.
            config (dict): Configuration data.

        Returns:
            response (requests.Response): The response from the Alation API.
        """

        logger_singleton = pade_env_logging.LoggerSingleton.instance()
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance()
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("upload_schema_manifest"):

            queue_name =  config.get("json_metadata_az_storage_queue_name")
            storage_queue = AzureStorageQueue(connection_string='your_connection_string', queue_name=queue_name)

            environment = config.get("environment")
            schema_location = config.get("edc_schema_location")
            alation_user_id = config.get("edc_alation_user_id")

            logger.info('Validating the manifest file at {0} with schema'.format(
                manifest_file))
            metadata = manifest.validateManifest(manifest_file)

            token_endpoint = TokenEndpoint(edc_alation_base_url)

            logger.info(f"alation_user_id:{alation_user_id}")
            logger.info(f"alation_refresh_token:{alation_refresh_token}")
            if token_endpoint.validate_refresh_token(alation_user_id, alation_refresh_token) is not None:
                logger.info('We have a valid refresh token begin import')
                api_token = token_endpoint.get_api_token(
                    alation_user_id, alation_refresh_token)
                logger.info('Using API token {0}'.format(api_token))
                custom_fields_endpoint = CustomFieldsEndpoint(
                    api_token, edc_alation_base_url)
                logger.info(
                    'Created custom fields endpoint for updating custom fields via API')

                tags_endpoint = TagsEndpoint(api_token, edc_alation_base_url)
                logger.info('Created tags endpoint for updating tags via API')

                id_finder_endpoint = IdFinderEndpoint(
                    api_token, edc_alation_base_url)
                logger.info(
                    'Created id finder for getting detailed information on Alation objects')
                logger.info('Updating the schema fields for data source {0} and schema {1}'.format(
                    alation_data_source_id, schema_name))
                custom_fields_endpoint.update(
                    "schema", alation_data_source_id, schema_name, manifest.getAlationData())
                schema_id = id_finder_endpoint.find('schema', schema_name)
                for tag in manifest.tags:
                    tags_endpoint.apply('schema', schema_id, tag)
                for table in manifest.getTablesData():
                    logger.info('Updating table {}'.format(table.name))
                    custom_fields_endpoint.update("table",
                                                  alation_data_source_id,
                                                  'cdh_premier.{}'.format(
                                                      table.name),
                                                  table.getAlationData())
                    if table.tags is not None:
                        table_id = id_finder_endpoint.find('table', table.name)
                        for table_tag in table.tags:
                            tags_endpoint.apply('table', table_id, table_tag)
                    if table.columns is not None:
                        for column in table.columns:
                            logger.info(f"Updating column: {column.name} on table: {table.name}")
                            custom_fields_endpoint.update("attribute",
                                                          alation_data_source_id,
                                                          'cdh_premier.{}.{}'.format(
                                                              table.name, column.name),
                                                          column.getAlationData())

            manifest_dict = {"result": "success"}
            return manifest_dict

    @classmethod
    def get_schema_structure(cls, alation_schema_id, alation_headers, alation_url, manifest, alation_data_source_id):
        """ 
        Retrieves the structure of a specific schema from Alation using the provided schema ID and manifest.

        Args:
            alation_schema_id (int): ID of the Alation schema whose structure is to be retrieved.
            alation_headers (dict): Headers to be used in the request, typically including authentication information.
            alation_url (str): The base URL of the Alation instance.
            manifest (dict): The manifest defining the structure of the schema.
            alation_data_source_id (int): ID of the Alation data source related to the schema.

        Raises:
            ValueError: If the response from Alation API is not successful.

        Returns:
            dict: A dictionary containing the structure of the schema.
        """  

        logger_singleton = pade_env_logging.LoggerSingleton.instance()
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance()
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_schema_structure"):

            response = requests.get(
                '{base_url}/integration/v2/schema/?id={alation_schema_id}'.format(base_url=alation_url,
                                                                                alation_schema_id=alation_schema_id), headers=alation_headers,  timeout=30).json()
            logger.info('Info for schema {}'.format(alation_schema_id))
            logger.info(response)
            found = False
            schema_fields, table_fields, column_fields = manifest.getManifestExpectedFields()
            manifest_dict = {}
            for s in response:
                logger.info(s['id'])
                if s['id'] == int(alation_schema_id):
                    found = True
                    logger.info('Found the schema id we want {}'.format(s['name']))
                    logger.info("Structure:\n", s)
                    for sf in schema_fields:
                        # see if this field is already populated, otherwise use a default value
                        if sf in s:
                            manifest_dict[sf] = s[sf]
                        else:
                            # is this field in the list of custom fields?
                            foundCustomField = False
                            for customField in s['custom_fields']:
                                # TODO DJJ : Hackish way to normalize the field names between target schema and custom fields
                                formated_sf_name = sf.lower().replace(" ", "")
                                formatted_customField_name = customField['field_name'].lower().replace(
                                    " ", "")
                                if formated_sf_name in formatted_customField_name:
                                    foundCustomField = True
                                    manifest_dict[sf] = customField['value']
                            # Exceptions to the rule - Fields that need to be manually mapped
                            if not foundCustomField:
                                # Enter name in the identifier field
                                if sf == "identifier" and 'name' in s:
                                    manifest_dict[sf] = s['name']
                                else:
                                    manifest_dict[sf] = schema_fields[sf]
                                if sf == "alationDatasourceID":
                                    manifest_dict[sf] = alation_data_source_id
                                if sf == "alationSchemaID":
                                    manifest_dict[sf] = alation_schema_id
                    # iterate through each table and add a manifest template entry
                    tables_dict = cls.get_schema_tables(
                        alation_schema_id, alation_headers, alation_url, alation_data_source_id)
                    if tables_dict:
                        manifest_dict["tables"] = []
                        # for each table associated with this schema...
                        for t in tables_dict:
                            this_table_dict = {}
                            for tf in table_fields:
                                # see if this field is already populated, otherwise use a default value
                                if tf in tables_dict[t]:
                                    this_table_dict[tf] = tables_dict[t][tf]
                                else:
                                    this_table_dict[tf] = table_fields[tf]
                            # iterate through each column associated with this table and add a manifest template entry
                            alation_table_id = tables_dict[t]['id']
                            columns_dict = cls.get_table_columns(
                                alation_schema_id, alation_headers, alation_url, alation_data_source_id, alation_table_id)
                            if columns_dict:
                                this_table_dict["columns"] = []
                                # for each column associated with this table...
                                for c in columns_dict:
                                    this_column_dict = {}
                                    for cf in column_fields:
                                        if cf in columns_dict[c]:
                                            this_column_dict[cf] = columns_dict[c][cf]
                                        else:
                                            this_column_dict[cf] = column_fields[cf]
                                    this_table_dict["columns"].append(
                                        this_column_dict)
                            manifest_dict["tables"].append(this_table_dict)
            if not found:
                raise Exception(
                    "Could not find the schema id in the list of schemas for this data source")
            # create a JSON structure around the schema, tables, and columns
            return manifest_dict
