# Harmonization Initiative Cleanup Script

Mica 4.7 introduced several new changes to account for the new harmonization standards put forward by [Maelstrom Research](https://www.maelstrom-research.org/). The main changes are:

- Renaming of `Harmonization Study` to `Harmonization Initiative`.
- Addition of new fields to better describe a `Harmonization Initiative`.
- Removal of `Population` and `harmonizationDesign` fields from `Harmonization Initiative`.
- Renaming of `Harmonized Dataset` to `Harmonization Protocol`.
- Addition of new fields to better describe a `Harmonization Protocol`.

To minimize loss of data, Mica 4.7 migrates the old `populations` field as a new custom field in the `Harmonization Initiative` Form (see `Administration / Harmonization Initiative Configuration`). As a consequence, all customization of the old `populations` field are added under the new `populationModel` field in the same Form.

To align the new Mica installation with the new Maelstrom Research standards, this utility removes the _obsolete_ fields listed below. Mica administrators **should not** run the script if these fields are to be kept.

#### Harmonization Initiative Cleanup
- Remove references to `populations` from data and schema form.
- Remove references to `PopulationModel` from data and schema form.
- Remove references to `harmonizationDesign` from data and schema form.
- Remove references to `harmonizationDesign` in the `Mica_study` taxonomy.

> Due to the complexity of the form definition, the following fields must be manually removed in Mica's administration section under `Administration / Harmonization Initiative Configuration / Definition (TAB)`:  
> - populations
> - populationModel
> - harmonizationDesign

## Dependencies
OBiBa Opal and Mica Python client packages and Python `requests`.

## Usage

#### To export Network associated documents:
```bash
python3 <SCRIPTS-PATH>/main.py --mica <MICA-SERVER-URL> --user <UAERNAME> --password <PASSWORD> 
```
Example:

```bash
python3 ~/project/initiative-cleanup/src/main/python/main.py --mica http://localhost:8082 --user administrator --password password
```

