from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_1.graph.models import Model
from azure.devops.v7_1.member_entitlement_management import AccessLevel, GraphUser, UserEntitlement


class GraphUserAADCreationContext(Model):
    """
    :param principal_name: The principal name from AAD like 'user@mydomain.com'
    :type principal_name: str
    :param storage_key: Optional: If provided, we will use this identifier for the storage key of the created user
    :type storage_key: str
    """
    
    _attribute_map = {
        'storage_key': {'key': 'storageKey', 'type': 'str'},
        'principal_name': {'key': 'principalName', 'type': 'str'}
    }

    def __init__(self, storage_key=None, principal_name=None):
        super(GraphUserAADCreationContext, self).__init__()
        self.storage_key = storage_key
        self.principal_name = principal_name

# Azure DevOps organization URL
organization_url = 'https://dev.azure.com/t-vivekv/'

# Personal access token (PAT) with appropriate project creation access
personal_access_token = 'ur pat'

# Provide the project ID of the target project
project_name = "Project-Vivekv"

# Provide the email ID of the user you want to add
email_id = "email to add"

# Create a connection to Azure DevOps
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client for the project
core_client = connection.clients.get_core_client()
graph_client = connection.clients.get_graph_client()
addAADUserContext = GraphUserAADCreationContext(principal_name=email_id)
print(addAADUserContext)
resp = graph_client.create_user(addAADUserContext)

project = core_client.get_project(project_name)


member_client = connection.clients.get_member_entitlement_management_client()

# Create a new user entitlement
access_level = AccessLevel(account_license_type='express')
graph_user = GraphUser(subject_kind='user', principal_name=email_id)
print(graph_user)
user_entitlement = UserEntitlement(access_level=access_level, user=graph_user)

# Add the user to the organization
member_client.add_user_entitlement(user_entitlement)

