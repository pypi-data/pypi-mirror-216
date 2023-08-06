"""Initialize the alation_service subpackage of data_ecosystem_services package"""
# allow absolute import from the root folder
# whatever its name is.
import sys  # don't remove required for error handling
import os

# Import from sibling directory ..\developer_service
OS_NAME = os.name

sys.path.append("..")
if OS_NAME.lower() == "nt":
    print("windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "\\..\\..\\..")))
else:
    print("non windows")
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../..")))
    sys.path.append(os.path.dirname(os.path.abspath(__file__ + "/../../..")))

from ..cdc_admin_service import environment_logging
from ..cdc_admin_service import environment_tracing
from ..az_storage_service import az_storage_queue
__all__ = ["endpoint", "customfieldsendpoint", "tokenendpoint", "manifest", "tagsendpoint", "idfinderendpoint", "datasource", "schema"]