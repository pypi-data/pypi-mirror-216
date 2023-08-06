import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab


# Represents a software Project
class Commits(AbstractGitLab):

	def __init__(self,personal_access_token):
		super(Commits,self).__init__(personal_access_token=personal_access_token)
	
	def get_all(self, today=False): 
		
		result = []
		commit_list = []

		try:
			logging.info("Start function: get_Commits")
			result = self.gl.projects.list(owned=True, iterator=True)

			for project in result:
				commits = project.commits.list(iterator=True)
				project = project.asdict()
				for	commit in commits:
					commit = commit.asdict()
					commit['project_id'] = project['id']
					commit_list.append(commit)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Commits")
		
		return commit_list
