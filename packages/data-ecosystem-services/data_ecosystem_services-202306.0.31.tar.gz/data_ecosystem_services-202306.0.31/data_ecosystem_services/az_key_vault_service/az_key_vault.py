from azure.identity import ClientSecretCredential, DeviceCodeCredential
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential, AzureDeveloperCliCredential
from azure.mgmt.resource import ResourceManagementClient
import azure.keyvault.secrets

from data_ecosystem_services.cdc_admin_service import (
    environment_tracing as pade_env_tracing,
    environment_logging as pade_env_logging
)

class AzKeyVault:
    """Wrapper class for Azure Key Vault to get secrets.

    This class authenticates with the Azure Key Vault using a service 
    principal and provides a method to retrieve secrets.
    """    
    def __init__(self, tenant_id, client_id, client_secret, key_vault_name, running_interactive):
        """Initializes the KeyVaultSecrets object.
        
        Args:
            tenant_id (str): The tenant_id of your Azure account. This is the directory ID.
            client_id (str): The client ID of the service principal.
            client_secret (str): The client secret of the service principal.
            key_vault_name (str): The name of your Azure Key Vault. You can get it from the Key Vault properties in the Azure portal.
        """        

        logger_singleton = pade_env_logging.LoggerSingleton.instance()
        logger = logger_singleton.get_logger()
        pade_env_tracing.TracerSingleton.log_to_console = False
        tracer_singleton = pade_env_tracing.TracerSingleton.instance()
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("__init__"):
            
            self.vault_url = f"https://{key_vault_name}.vault.azure.net/"
            self.running_interactive = running_interactive
            self.client_id = client_id
            self.client_secret = client_secret
            self.tenant_id = tenant_id
            logger.info(f"vault_url:{self.vault_url}")
            logger.info(f"tenant_id:{self.tenant_id}")
            logger.info(f"client_id:{self.client_id}")
            logger.info(f"running_interactive:{str(self.running_interactive)}")
             

            # self.credential_default = DefaultAzureCredential()
            # self.credential_dev =  AzureDeveloperCliCredential(  tenant_id=tenant_id,additionally_allowed_tenants=['*'])
            # self.client_default = SecretClient(vault_url,credential= self.credential_default)
            # self.client_dev = SecretClient(vault_url, credential=self.credential_dev)
            
            # Create a KeyVaultTokenCallback object
            # callback_dev = azure.keyvault.secrets.KeyVaultTokenCallback(self.credential_dev)
            # Set the KeyVaultTokenCallback object on the SecretClient object
            # self.client_dev.authentication_callback = self.callback_dev


    def cdc_authentication_callback(client, context):

        # Obtain an access token from a custom authentication mechanism
        access_token = get_access_token(context)

        # Return the access token
        return access_token
        
    def get_secret(self, secret_name):
        """Retrieves a secret from the Azure Key Vault.

        Args:
            secret_name (str): The name of the secret to retrieve.

        Returns:
            str: The value of the retrieved secret.
        """        
        
        logger_singleton = pade_env_logging.LoggerSingleton.instance()
        logger = logger_singleton.get_logger()
        tracer_singleton = pade_env_tracing.TracerSingleton.instance()
        tracer = tracer_singleton.get_tracer()

        with tracer.start_as_current_span("get_secret"):
            logger.info(f"vault_url:{self.vault_url}")
            logger.info(f"tenant_id:{self.tenant_id}")
            logger.info(f"client_id:{self.client_id}")
            logger.info(f"running_interactive:{str(self.running_interactive)}")
            
            logger.info(f"get_secret:{secret_name}")
            try:
                self.client_device  = None
                if self.running_interactive is True:
                    self.credential_device =  DeviceCodeCredential(client_id=self.client_id, tenant_id=self.tenant_id,additionally_allowed_tenants=['*'])
                    self.client_device = SecretClient(vault_url=self.vault_url, credential=self.credential_device)
                    secret_value = self.client_device.get_secret(secret_name).value
                else:
                    self.credential = ClientSecretCredential(client_id=self.client_id, tenant_id=self.tenant_id, client_secret=self.client_secret)
                    self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)
                    secret_value = self.client.get_secret(secret_name).value
            except Exception as e:
                # If there is a security error, fallback to the default credential
                print(f"Error with provided credential: {e}")
                print(f"Trying second credential method for {self.vault_url}...")
                # self.token_dev = self.credential_dev.get_token("https://vault.azure.net/.default")  
                # logger.info(f"token_dev:{self.token_dev}")
                if self.client_device is None:
                    self.credential_device =  DeviceCodeCredential(client_id=self.client_id, tenant_id=self.tenant_id,additionally_allowed_tenants=['*'])
                    self.client_device = SecretClient(vault_url=self.vault_url, credential=self.credential_device)
                    secret_value = self.client_device.get_secret(secret_name).value
                else:
                    self.credential = ClientSecretCredential(client_id=self.client_id, tenant_id=self.tenant_id, client_secret=self.client_secret)
                    self.client = SecretClient(vault_url=self.vault_url, credential=self.credential)
                    secret_value = self.client.get_secret(secret_name).value

            return secret_value
