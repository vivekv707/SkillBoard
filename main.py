from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v7_0.core.models import TeamProject
# Azure DevOps organization URL
organization_url = 'https://dev.azure.com/t-vivekv/'

# Personal access token (PAT) with appropriate project creation access
personal_access_token = 'Put ur token'

# Create a connection to Azure DevOps
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client for the project
core_client = connection.clients.get_core_client()


def CreateSkillProject(username,skill_temp_name):
    project_name = 'Project-'+username
    project_description = 'SkillBoard for '+ username
    project_capabilities = {
        "versioncontrol": {
            "sourceControlType": "Git"
        },
        "processTemplate": {
            "templateTypeId": "6b724908-ef14-45cf-84f8-768b5384da45"  # Agile template ID
        }
    }
    new_project = TeamProject(
    name=project_name, 
    description=project_description,
    visibility= 'private',
    capabilities=project_capabilities)

    try:
        created_project = core_client.queue_create_project(new_project)
    except:
        print('Already Exists')


# Azure DevOps organization URL
organization_url = 'https://dev.azure.com/t-vivekv/'

# Personal access token (PAT) with appropriate project access
personal_access_token = 'tmp6wanuzj5ygjineef3i3tgy5z7cq3e4jejx4uwzsxgn5cd42rq'

# Project name
project_name = 'Project_UStories_Trial'

# Create a connection to Azure DevOps
credentials = BasicAuthentication('', personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get a client for the project
core_client = connection.clients.get_core_client()

# Get the project
project = core_client.get_project(project_name)

# Print project details
print(f"Project Name: {project.name}")
print(f"Project ID: {project.id}")
print(f"Project Description: {project.description}")
print(f"Project URL: {project.url}")
