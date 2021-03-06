# Harmonization Initiative Cleanup Script

Mica 5.0 introduced several new changes to account for the new harmonization standards put forward by [Maelstrom Research](https://www.maelstrom-research.org/). The main changes are:

- Renaming of `Harmonization Study` to `Harmonization Initiative`.
- Addition of new fields to better describe a `Harmonization Initiative`.
- Removal of `Population` and `harmonizationDesign` fields from `Harmonization Initiative`.
- Renaming of `Harmonized Dataset` to `Harmonization Protocol`.
- Addition of new fields to better describe a `Harmonization Protocol`.

To minimize loss of data, Mica 5.0 migrates the old `populations` field as a new custom field in the `Harmonization Initiative` Form (see `Administration / Harmonization Initiative Configuration`). Any customization done for the old `populations` field are migrated under the new `populationModel` field in the same Form.

This utility aligns the new Mica installation with the new Maelstrom Research standards by removing the now _obsolete_ fields listed below:

> Mica administrators **should not** run the script if these fields are to be kept.

#### Harmonization Initiative Cleanup
- Remove references to `populations` from data and schema form.
- Remove references to `PopulationModel` from data and schema form.
- Remove references to `harmonizationDesign` from data, schema form and the `Mica_study` taxonomy.

> Due to the complexity of the form definition, the above fields must be manually removed in Mica's administration section under `Administration / Harmonization Initiative Configuration / Definition (TAB)`.  

> It is also recommended to remove the above obsolete fields from Mica public pages (`templates/study.ftl` and `templates/libs/study.ftl`).

## Dependencies
Python `requests` package.

## Suggestion
Use a virtual Python environment to prevent conflicts with current Python installation.

```bash
python3 -m venv venv  # create for the 1st time
source venv/bin/activate

deactivate # To exit the virtual environment 
````

## Usage

#### To run the cleanup script:
```bash
python3 <SCRIPTS-PATH>/main.py --mica <MICA-SERVER-URL> --user <UAERNAME> --password <PASSWORD> 
```
Example:

```bash
python3 ~/project/initiative-cleanup/src/main/python/main.py --mica http://localhost:8082 --user administrator --password password
```

