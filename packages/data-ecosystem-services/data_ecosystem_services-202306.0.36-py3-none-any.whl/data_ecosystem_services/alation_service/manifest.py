import json
import jsonschema
from jsonschema import validate

class Column:
    """Represents a column in a database table.

    Args:
        name (str): The name of the column.
        data_type (str): The data type of the column.
        nullable (bool, optional): Indicates if the column is nullable. Defaults to True.
        primary_key (bool, optional): Indicates if the column is a primary key. Defaults to False.
        default (Any, optional): The default value of the column. Defaults to None.

    Attributes:
        name (str): The name of the column.
        data_type (str): The data type of the column.
        nullable (bool): Indicates if the column is nullable.
        primary_key (bool): Indicates if the column is a primary key.
        default (Any): The default value of the column.

    """
    def __init__(self, column_json):
        """Initialize a Column instance.

        Args:
            name (str): The name of the column.
            data_type (str): The data type of the column.
            nullable (bool, optional): Indicates if the column is nullable. Defaults to True.
            primary_key (bool, optional): Indicates if the column is a primary key. Defaults to False.
            default (Any, optional): The default value of the column. Defaults to None.
        """     
        self.name = column_json['name']
        self.title = column_json['title']
        self.extra_description_fields = self.getColumnExtraDescriptionFields(column_json)
        self.description = self.formatDescription(column_json)
        tags = column_json.get('tags')
        if tags is not None:
            self.tags = tags
        else:
            self.tags = []

    def formatDescription(self, column_json):
        """_summary_

        Args:
            column_json (_type_): _description_

        Returns:
            _type_: _description_
        """        
        description = column_json['description']
        if self.extra_description_fields:
            description += '<br><table><tr><th>Field</th><th>Value</th></tr>'
            for key in self.extra_description_fields:
                description += '<tr><td>' + key + '</td><td>' + self.extra_description_fields[key] + '</td></tr>' 
            description += '</table>'
        return description

    def getColumnExtraDescriptionFields(self, column_json):
        """_summary_

        Args:
            column_json (_type_): _description_

        Returns:
            _type_: _description_
        """        
        extra_description_fields = {}
        if "extraDescriptionFields" in column_json:
            optional_description_fields = column_json['extraDescriptionFields']
            print("Extra description fields: ", optional_description_fields)
            for key in optional_description_fields:
                extra_description_fields[key] = optional_description_fields[key]
        return extra_description_fields
    
    def getAlationData(self):
        return {'title': self.title, 'description': self.description}

class Table:
    """_summary_
    """    
    def __init__(self, table_json):
        """_summary_

        Args:
            table_json (_type_): _description_
        """        
        self.name = table_json['name']
        self.title = table_json['title']
        self.extra_description_fields = self.getTableExtraDescriptionFields(table_json)
        self.description = self.formatDescription(table_json)
        tags = table_json.get('tags')
        if tags is not None:
            self.tags = tags
        else:
            self.tags = []
        columns_json = table_json.get('columns')

        if columns_json is not None:
            self.columns = list(map(lambda c: Column(c), columns_json))
        else:
            self.columns = None
    
    def getAlationData(self):
        """_summary_

        Returns:
            _type_: _description_
        """        
        return {'title': self.title, 'description': self.description}

    def getTableExtraDescriptionFields(self, table_json):
        """_summary_

        Args:
            table_json (_type_): _description_

        Returns:
            _type_: _description_
        """        
        extra_description_fields = {}
        if "extraDescriptionFields" in table_json:
            optional_description_fields = table_json['extraDescriptionFields']
            print("Extra description fields: ", optional_description_fields)
            for key in optional_description_fields:
                extra_description_fields[key] = optional_description_fields[key]
        return extra_description_fields

    def formatDescription(self, table_json):
        """_summary_

        Args:
            table_json (_type_): _description_

        Returns:
            _type_: _description_
        """        
        description = table_json['description']
        if self.extra_description_fields:
            description += '<br><table><tr><th>Field</th><th>Value</th></tr>'
            for key in self.extra_description_fields:
                description += '<tr><td>' + key + '</td><td>' + self.extra_description_fields[key] + '</td></tr>' 
            description += '</table>'
        return description

class Manifest:
    def __init__(self, schema):
        self.schema = schema
        self.title = ''
        self.alationDatasourceID = ''
        self.alationSchemaID = ''
        self.submitting_user = ''
        self.description = ''
        #self.releasedate = ''
        self.homepageUrl =''
        self.identifier = ''
        self.dataformat = ''
        self.language = ''
        self.size = ''
        self.updateFrequency = ''
        self.temporalResolution = ''
        self.license = ''
        self.tags = []
        self.geographicCoverage = ''
        self.referencedBy = ''
        self.references = ''
        self.citation = ''
        self.reference = ''
        self.temporalApplicability = {}
        self.tables = {} 
        self.pii = {}
        self.manifest_template_properties = {}
        self.extra_description_fields = {}
        print(schema)


    def setAlationData(self,manifest):
        print(manifest)
        print("\n\nStart Field by field:")
        schemafile = open(self.schema)
        schemaContents = json.load(schemafile)
        self.manifest_template_properties = schemaContents['properties'].keys()
        self.manifest_template_table_properties = schemaContents['$defs']['table']['properties'].keys()
        self.manifest_template_column_properties = schemaContents['$defs']['column']['properties'].keys()
        # extraDescriptionFields is an optional field
        self.extra_description_fields = {}
        if "extraDescriptionFields" in manifest:
            optional_description_fields = manifest['extraDescriptionFields']
            print("Extra description fields: ", optional_description_fields)
            for key in optional_description_fields:
                self.extra_description_fields[key] = optional_description_fields[key]
        self.title       = manifest['title']
        self.alationDatasourceID       = manifest['alationDatasourceID']
        self.alationSchemaID       = manifest['alationSchemaID']
        self.submitting_user       = manifest['submitting_user']
        self.description = manifest['description']
        self.releasedate = manifest['releaseDate']
        self.homepageUrl   = manifest['homepageUrl']
        self.identifier  = manifest['identifier']
        #self.dataformat  = manifest['format']
        #self.language    = manifest['language']
        #self.size        = manifest['size']
        #self.temporalResolution = manifest['temporalResolution']
        #self.updateFrequency    = manifest['updateFrequency']
        #self.conformToStandard  = manifest['conformToStandard']
        self.license     = manifest['license']
        self.tags        = manifest['tags']
        self.referencedBy = manifest['referencedBy']
        self.citation    = manifest['citation']
        self.reference   = manifest['reference']
        self.geographicCoverage = manifest['geographicCoverage']
        self.tables = list(map(lambda t: Table(t), manifest['tables']))
        self.pii         = manifest['pii']
        self.temporalApplicability = manifest['temporalApplicability']


    def getTablesData(self):
        return self.tables

    def getColumnsData(self):
        columndata = {}
        for t in self.tables:
            columndata[t] = t.columns
        return columndata

    def formatDescription(self):
        description = self.description
        if self.extra_description_fields:
            description += '<br><table><tr><th>Field</th><th>Value</th></tr>'
            for key in self.extra_description_fields:
                description += '<tr><td>' + key + '</td><td>' + self.extra_description_fields[key] + '</td></tr>'   
            description += '</table>'
        return description
        
    def getAlationData(self):
        data = {}
        data['title']           = self.title
        data['description']     = self.formatDescription()
        #data['description']     = self.description
        #data['Release Date']    = self.releasedate
        data['Homepage URL']    = self.homepageUrl
        data['Identifier']      = self.identifier
        #data['Format']          = self.dataformat
        data['License']         = self.license

        #arrays
        #data['tags']            = self.tags
        #data['Language']        = self.language
        data['Is Referenced By']  = self.referencedBy
        data['Geographic Coverage'] = self.geographicCoverage
        data['Temporal Applicability'] = self.temporalApplicability
        data['References'] = self.references
        # self.alationdata = json.dumps(data)
        return data

    def validateJson(self,jsonData,schema):
        try:
            validate(instance=jsonData, schema=schema)
        except jsonschema.exceptions.ValidationError as err:
            print('Problem validating the input manifest data against the required schema.')
            raise err
        return True

    def printManifest(manifest):
        for k,v, in manifest.items():
            print ("{0}: {1}".format(k,v))


    def get_submitting_user_from_manifest_file(self,manifestfile):
    # Read manifest JSON file into dictionary
        schemafile = open(self.schema)
        schema = json.load(schemafile)
        f = open(manifestfile)
        manifest = json.load(f)
        return manifest['submitting_user']


    def validateManifest(self,manifestfile):
    # Read manifest JSON file into dictionary
        schemafile = open(self.schema)
        schema = json.load(schemafile)
        f = open(manifestfile)
        manifest = json.load(f)
        
        if self.validateJson(manifest,schema):
            print("Manifest schema is valid")
            #printManifest(manifest)
        else:
            print ("Manifest schema is invalid")
            return None
        self.setAlationData(manifest)
        return manifest

    def getManifestExpectedFields(self):
    # Read manifest JSON file into dictionary
        schemafile = open(self.schema)
        schema = json.load(schemafile)
        schema_fields = {}
        table_fields = {}
        column_fields = {}
        for p in schema['properties']:
            # do not add properties blank_field_examples for tables, columns, this info will be extracted from alation obj strucutre
            if p not in ["tables", "columns"]:
                schema_fields[p] = schema['properties'][p].get('blank_field_examples')
        for p in schema['$defs']['table']['properties']:
            # do not add properties blank_field_examples for tables, columns, this info will be extracted from alation obj strucutre
            if p not in ["columns"]:
                table_fields[p] = schema['$defs']['table']['properties'][p]['blank_field_examples']
        for p in schema['$defs']['column']['properties']:
            column_fields[p] = schema['$defs']['column']['properties'][p]['blank_field_examples']
        return schema_fields, table_fields, column_fields