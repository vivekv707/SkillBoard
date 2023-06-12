from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.core.models import TeamProject
from azure.devops.v7_0.work_item_tracking.models import JsonPatchOperation,  WorkItemRelation

# Azure DevOps organization URL
organization_url = 'https://dev.azure.com/t-vivekv/'

# Personal access token (PAT) with appropriate project creation access
personal_access_token = 'tmp6wanuzj5ygjineef3i3tgy5z7cq3e4jejx4uwzsxgn5cd42rq'

# New project name and description
new_project_name = 'Project-Vivekv'
new_project_description = 'SkillBoard for Vivekv'
new_project_capabilities = {
    "versioncontrol": {
        "sourceControlType": "Git"
    },
    "processTemplate": {
        "templateTypeId": "6b724908-ef14-45cf-84f8-768b5384da45"  # Agile template ID
    }
}

# Create a connection to Azure DevOps
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client for the project
core_client = connection.clients.get_core_client()

# Create the new project
new_project = TeamProject(
    name=new_project_name, 
    description=new_project_description,
    visibility= 'private',
    capabilities=new_project_capabilities)

try:
    created_project = core_client.queue_create_project(new_project)
except:
    print('Already Exists')

while True:
    # Get the list of projects
    projects = core_client.get_projects()

    # Check if the project with the given name exists
    project_exists = any(project.name == new_project_name for project in projects)

    # Print the result
    if project_exists:
        break


project = core_client.get_project(new_project_name)

# Print the project details
print(f"Project Name: {project.name}")
print(f"Project ID: {project.id}")
print(f"Project Description: {project.description}")
print(f"Project URL: {project.url}")

# Adding an epic then linking it to a feature
# Get a client for work item tracking
wit_client = connection.clients.get_work_item_tracking_client()

epic = wit_client.create_work_item(
    project =project.name,
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
        path='/fields/System.AssignedTo',
        value='t-sakjoshi@microsoft.com'  # Replace with the email of the user you want to assign the Epic to
    )
    ],
    type = 'Epic'
)

epic_id = epic.id

# Create a Feature
feature = wit_client.create_work_item(
    project = project.name,
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
        path='/relations/-',
        value={
            'rel': 'System.LinkTypes.Hierarchy-Reverse',
            'url': epic.url,
            'attributes': {
                'comment': 'Child of'
            }
        }
    ),
    JsonPatchOperation(
        op='add',
        path='/fields/System.AssignedTo',
        value='t-sakjoshi@microsoft.com'  # Replace with the email of the user you want to assign the Epic to
    )
    ],
    type='Feature'
)

feature_id = feature.id



