import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab

# Represents a software Project
class RepositoryTree(AbstractGitLab):

	def __init__(self,personal_access_token):
		super(RepositoryTree,self).__init__(personal_access_token=personal_access_token)
	
	def get_all(self, today=False):
		
		projects = []
		project_repository_tree = []

		try:
			logging.info("Start function: get_projects_repository_tree")
			
			projects = self.gl.projects.list(owned=True, iterator=True)

			for project in projects:
				project_repository_tree_return = project.repository_tree()
				project = project.asdict()
				for repository_tree in project_repository_tree_return:
					repository_tree["project_id"] = project["id"]
					project_repository_tree.append(repository_tree)

			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Projects Repository Tree")
		
		return project_repository_tree	