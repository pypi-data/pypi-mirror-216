import factory
from .project import Project
from .repositoryTree import RepositoryTree
from .branches import Branches
from .commits import Commits
from .deployments import Deployments
from .events import Events
from .issues import Issues
from .repositories import Repositories
from .projectLanguages import ProjectLanguages

class ProjectFactory(factory.Factory):
    
    class Meta:
        model = Project
        
    personal_access_token = None
  
class RepositoryTreeFactory(factory.Factory):
    
    class Meta:
        model = RepositoryTree
        
    personal_access_token = None

class BranchesFactory(factory.Factory):
    
    class Meta:
        model = Branches
        
    personal_access_token = None

class CommitsFactory(factory.Factory):
    
    class Meta:
        model = Commits
        
    personal_access_token = None

class DeploymentsFactory(factory.Factory):
    
    class Meta:
        model = Deployments
        
    personal_access_token = None

class EventsFactory(factory.Factory):
    
    class Meta:
        model = Events
        
    personal_access_token = None

class IssuesFactory(factory.Factory):
    
    class Meta:
        model = Issues
        
    personal_access_token = None

class RepositoriesFactory(factory.Factory):
    
    class Meta:
        model = Repositories
        
    personal_access_token = None



class ProjectLanguagesFactory(factory.Factory):
    
    class Meta:
        model = ProjectLanguages
        
    personal_access_token = None
