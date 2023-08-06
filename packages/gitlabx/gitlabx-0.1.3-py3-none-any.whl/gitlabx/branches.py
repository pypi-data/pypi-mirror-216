import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab

# Represents a software Project
class Branches(AbstractGitLab):

	def __init__(self,personal_access_token):
		super(Branches,self).__init__(personal_access_token=personal_access_token)
	
	def get_all(self, today=False): 
		
		result = []
		branch_list = []

		try:
			logging.info("Start function: get_Branches")
			result = self.gl.projects.list(owned=True, iterator=True)
			for project in result:
				branches = project.branches.list()
				project = project.asdict()
				for	branch in branches:
					branch = branch.asdict()
					branch['project_id'] = project['id']
					branch_list.append(branch)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Branches")
		
		return branch_list
