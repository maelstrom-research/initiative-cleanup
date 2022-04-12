import json
import requests
import re

class MlstrInitiativeCleanup:

  def __init__(self, args):
    self.args = args

  def __logAction(self, text, indent):
    if indent is None:
      indent = 1
  
    print("%s%s" % (' ' * indent, text))

  def __sendPutMicaRequest(self, url, payload):
    basicAuthCredentials = (self.args.user, self.args.password)
    headers = {}
    headers["Content-Type"] = "application/json"
    response = requests.put(
      '%s/ws/%s' % (self.args.mica, url),
      auth=basicAuthCredentials,
      headers=headers,
      json=payload
    )
    
    return response.status_code == 200 or response.status_code == 204
    
  def __sendGetMicaRequest(self, url):
    basicAuthCredentials = (self.args.user, self.args.password)
    headers = {}
    headers["Accept"] = "application/json"
    response = requests.get(
      '%s/ws/%s' % (self.args.mica, url),
      auth=basicAuthCredentials,
      headers=headers)
    if response.status_code == 200:
      return json.loads(response.content)
    
  def __getPublishableInitiative(self, limit):
    publishables = {}
    states = self.__sendGetMicaRequest('draft/study-states?type=harmonization-study&from=0&limit=%d' % limit)
    for state in states:
      publishables[state['id']] = state['published'] and state['obiba.mica.EntityStateDto.studySummaryState']['revisionsAhead'] < 1
      
    return publishables
    

  def __cleanupStudies(self):
    self.__logAction("Removing populations from initiatives...", 0)
    initiatives = self.__sendGetMicaRequest('draft/harmonization-studies')
    if len(initiatives) > 0:
      publishables = self.__getPublishableInitiative(len(initiatives))
      
      for initiative in initiatives:
        initiativeId = initiative['id']
        self.__logAction("Removing population from %s..." % initiativeId, 2)
      
        if 'populations' in initiative:
          initiative.pop('populations')
          
        if 'content' in initiative:
          model = json.loads(initiative['content'])
          if 'populations' in model:
            model.pop('populations')
            self.__logAction("Removed populations from model...", 4)
            
          if 'populationModel' in model:
            model.pop('populationModel')
            self.__logAction("Removed populationModel from model...", 4)
            
          initiative['content'] = json.dumps(model)
          
        if self.__sendPutMicaRequest('draft/harmonization-study/%s' % initiativeId, initiative):
          self.__logAction("Saved initiative...", 4)
          if publishables[initiativeId]:
            if self.__sendPutMicaRequest('draft/harmonization-study/%s/_publish' % initiativeId, None):
              self.__logAction("Published initiative...", 4)
            
  def process(self):
    config = self.__sendGetMicaRequest("config")
    version = re.search(r"(\d+)\.(\d+)\.(\d+)", config['version'])
    [major, minor, patch] = list(map(int, version.groups()))
    if major >= 4 and minor >= 7:
      self.__cleanupStudies()

