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

  def __cleanupInitiativeConfig(self):
    self.__logAction("Cleaning up initiative configuration...", 0)
    config = self.__sendGetMicaRequest('config/harmonization-study/form-custom')
    schema = json.loads(config['schema'])
    schemaProperties = schema['properties']
    dirty = False

    if 'populations' in schemaProperties:
      schemaProperties.pop('populations')
      self.__logAction("Removed 'populations' from form 'schema'.", 2)
      dirty = True

    if 'populationModel' in schemaProperties:
      schemaProperties.pop('populationModel')
      self.__logAction("Removed 'populationModel' from form 'schema'.", 2)
      self.__logAction("Removed 'populationModel' from form 'definition'.", 2)
      dirty = True

    if 'harmonizationDesign' in schemaProperties:
      schemaProperties.pop('harmonizationDesign')
      self.__logAction("Removed 'harmonizationDesign' from form 'schema'.", 2)
      dirty = True

    config['schema'] = json.dumps(schema)

    if dirty and  self.__sendPutMicaRequest('config/harmonization-study/form-custom', config):
      self.__logAction("Saved initiative configuration form.", 2)

      stars = '*' * 3
      notice = """
%s Due to the complexity of the form 'definition' the following fields must be manually removed in Mica's administration\n%s section under 'Administration / Harmonization Initiative Configuration / Definition (TAB)':
%s - populations
%s - populationModel
%s - harmonizationDesign
""" % (stars, stars, stars, stars, stars)
      self.__logAction(notice, 0)

  def __cleanTaxonomy(self):
    self.__logAction("Cleaning up initiative taxonomy...", 0)
    taxonomy = self.__sendGetMicaRequest('config/study/taxonomy')
    vocabularies = taxonomy['vocabularies']
    before = len(vocabularies)
    vocabularies = list(filter(lambda x: x['name'] != 'harmonizationDesign', vocabularies))
    after = len(vocabularies)
    if before > after:
      taxonomy['vocabularies'] = vocabularies
      self.__logAction("Removed 'harmonizationDesign' vocabulary.", 2)

      if self.__sendPutMicaRequest('config/study/taxonomy', taxonomy):
        self.__logAction("Saved initiative taxonomy.", 2)


  def __cleanupInitiatives(self):
    self.__logAction("Cleaning up initiatives...", 0)
    initiatives = self.__sendGetMicaRequest('draft/harmonization-studies')
    if len(initiatives) > 0:
      publishables = self.__getPublishableInitiative(len(initiatives))
      
      for initiative in initiatives:
        dirty = False
        initiativeId = initiative['id']
        self.__logAction("Cleaning initiative %s..." % initiativeId, 2)

        if 'populations' in initiative:
          initiative.pop('populations')
          self.__logAction("Removed 'populations' from initiative document.", 4)
          dirty = True

        if 'content' in initiative:
          model = json.loads(initiative['content'])

          if 'populations' in model:
            model.pop('populations')
            self.__logAction("Removed 'populations' from model.", 4)
            dirty = True

          if 'populationModel' in model:
            model.pop('populationModel')
            self.__logAction("Removed 'populationModel' from model.", 4)
            dirty = True


          if 'harmonizationDesign' in model:
            model.pop('harmonizationDesign')
            self.__logAction("Removed 'harmonizationDesign' from model.", 4)
            dirty = True

          # Replace the content with the new changes
          initiative['content'] = json.dumps(model)

          if dirty and self.__sendPutMicaRequest('draft/harmonization-study/%s' % initiativeId, initiative):
            self.__logAction("Saved initiative %s." % initiativeId, 4)
            if publishables[initiativeId]:
              if self.__sendPutMicaRequest('draft/harmonization-study/%s/_publish' % initiativeId, None):
                self.__logAction("Published initiative %s." % initiativeId, 4)

  def _ensureValidMicaVersion(self):
    config = self.__sendGetMicaRequest("config")
    version = re.search(r"(\d+)\.(\d+)\.(\d+)", config['version'])
    [major, minor, patch] = list(map(int, version.groups()))
    if major < 4 or minor < 7:
      raise Exception('Mica Version must be >= 4.7.0')


  def process(self):
    self._ensureValidMicaVersion()
    self.__cleanupInitiatives()
    self.__cleanupInitiativeConfig()
    self.__cleanTaxonomy()



