import logging
logging.basicConfig(level=logging.INFO)
from gitlabx.abstract import AbstractGitLab

# Represents a software Project
class Issues(AbstractGitLab):

	def __init__(self,personal_access_token):
		super(Issues,self).__init__(personal_access_token=personal_access_token)
	
	def get_all(self, today=False): 
		
		result = []
		issue_list = []

		try:
			logging.info("Start function: get_Issues")
			result = self.gl.projects.list(owned=True, iterator=True)
			for project in result:
				issues = project.issues.list(iterator=True)
				project = project.asdict()
				for	issue in issues:
					issue = issue.asdict()
					issue['project_id'] = project['id']
					issue_list.append(issue)
			
		except Exception as e: 
			logging.error("OS error: {0}".format(e))
			logging.error(e.__dict__) 

		logging.info("Retrieve All Project Issues")
		
		return issue_list
