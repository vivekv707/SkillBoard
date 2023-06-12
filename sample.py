from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v6_0.work_item_tracking.models import JsonPatchOperation, WorkItemRelation

# Azure DevOps organization URL
org_url = 'https://dev.azure.com/YourOrganizationName'

# Personal access token (PAT) with appropriate permissions
pat = 'YourPersonalAccessToken'

# Create a connection to Azure DevOps
credentials = BasicAuthentication('', pat)
connection = Connection(base_url=org_url, creds=credentials)

# Get a reference to the Work Item Tracking client
wit_client = connection.clients.get_work_item_tracking_client()

# Create an Epic
epic = wit_client.create_work_item(
    project='YourProjectName',
    document=[
        JsonPatchOperation(
            op='add',
            path='/fields/System.Title',
            value='My Epic'
        ),
        JsonPatchOperation(
            op='add',
            path='/fields/System.Description',
            value='This is an epic'
        ),
        JsonPatchOperation(
            op='add',
            path='/fields/System.WorkItemType',
            value='Epic'
        )
    ]
)

epic_id = epic.id

# Create a Feature
feature = wit_client.create_work_item(
    project='YourProjectName',
    document=[
        JsonPatchOperation(
            op='add',
            path='/fields/System.Title',
            value='My Feature'
        ),
        JsonPatchOperation(
            op='add',
            path='/fields/System.Description',
            value='This is a feature'
        ),
        JsonPatchOperation(
            op='add',
            path='/fields/System.WorkItemType',
            value='Feature'
        )
    ]
)

feature_id = feature.id

# Link the Feature as a child of the Epic
relation = WorkItemRelation(
    rel='System.LinkTypes.Hierarchy-Reverse',
    url=epic.url,
    attributes={
        'comment': 'Child of'
    }
)

wit_client.add_work_item_relation(
    project='YourProjectName',
    id=feature_id,
    document=[relation]
)

print('Feature linked to Epic successfully!')
