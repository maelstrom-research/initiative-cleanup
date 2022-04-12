# Maelstrom DB Exporter / Importer
Utility scripts permitting Opal and Mica administrators to export all associated network documents to a local folder and then import them to another Opal and Mica.

The Python-based commandline tool is the exporter and the BASH script is the importer.

Documents exported are:

**Mica**:
- Network
- Studies
- Datasets
- Files (Network, Studies, Datasets)
- Persons (Network, Studies)

> Person documents reference only the exported network and studies.

**Opal**:
- Projects
- Taxonomies

> Taxonomy documents only contain vocabularies and terms that were found in the network associated variables. 

## Depedencies
OBiBa Opal and Mica Python client packages and Python `requests` and `python3-pycurl` packages.
Use `apt` for `python3-pycurl`.

## Suggestions
Make sure to setup a Python virtual environment
```bash
pip install virtualenv
python -m venv venv # at the root of this project
source venv/bin/activate
```

Have `/usr/share/pyshared` added to `PYTHONPATH` so the Opal and Mica imports work. Here is a working example:

```
PYTHONPATH=/usr/share/pyshared:/usr/lib/python3/dist-packages
```

## Usage

#### To export Network associated documents:
```bash
python <SCRIPTS-PATH>/main.py --opal https://opal-staging.maelstrom-research.org --mica https://mica-staging.maelstrom-research.org --network near --output <EXPORT-OUTPUT-FOLDER> --user <UAERNAME> --password <PASSWORD> 
```

Including the ENV variables:
```bash
PYTHONPATH=/usr/share/pyshared:/usr/lib/python3/dist-packages python <SCRIPTS-PATH>/main.py --opal https://opal-staging.maelstrom-research.org --mica https://mica-staging.maelstrom-research.org --network near --output <EXPORT-OUTPUT-FOLDER> --user <UAERNAME> --password <PASSWORD> 
```
#### To import all Network associated documents:

```bash
bash import.sh -u USERNAME -p PASSWORD -o http://localhost:8080 -m http://localhost:8082 -s <IMPORT-SOURCE-FOLDER>
``` 
 If export/import is ran from the same location `IMPORT-SOURCE-FOLDER` is the same as `EXPORT-OUTPUT-FOLDER`.

## TODO
Remove the dependency to `requests` package once the `utf8` bug of `mica-python-client` is resolved. Needs more investigation.  
# initiative-populations-cleanup
