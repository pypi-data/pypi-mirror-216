# Hefesto - Curation Toolkit: A Critical Step in the Workflow

**Preprocessing datatable toolkit for CDE semantic model data source requirements**

The implementation of the Common Data Element (CDE) Semantic Model for CSV data entails a meticulous and technically advanced workflow. By leveraging the power of the CDE YARRRML templates and incorporating the critical curation step executed by the Hefesto toolkit, this implementation achieves robustness, accuracy, and reliability in generating RDF-based CDE-oriented patient data.

Hefesto serves as a module dedicated to performing a curation step prior to the conversion of data into RDF. The primary transformations carried out by Hefesto include:

* Adding every domain specific ontological term required to define every instances of the model, these terms are specific for every data element.

* Splitting the column labeled as `value` into distinct datatypes. This enables YARRRML to interpret each datatype differently, facilitating the subsequent processing.

* Conducting a sanity check on the `stardate` and `enddate` columns to ensure data consistency and validity.

* Eliminating any input rows that lack of the minimal required data to minimize the generation of incomplete RDF transformations.

* Creation of the column called `uniqid` that assigns a unique identifier to each observation. This prevents the RDF instances from overlapping with one another, ensuring their distinctiveness and integrity.


##  Installation:

```bash
pip install Hefesto
```
## Usage:
**Requirements:**

- CSV datatable with your CDE data based on [CDE implementation glossary](https://github.com/ejp-rd-vp/CDE-semantic-model-implementations/blob/master/CDE_version_2.0.0/CSV_docs/glossary.md)

**Test:**

```py
from Hefesto.main import Hefesto
import yaml

test = Hefesto(datainput = "../data/preCDE.csv") # Use your own path for your CSV input data
transform = test.transform_Fiab()
transform.to_csv ("../data/CDE.csv", index = False, header=True) # Change this path to the location where your resulting data should be located
```

## Dockerized implementation:

There's a Docker-based implementation controlled via API (using FastAPI) that you can use for mounting this data transformation step as a part of your CDE implementation. Use our docker compose to control your Docker image, ports where its located and volumes in order to pass your CSV-based CDE patient data:

```yaml
version: "3.3"

services:
  api:
    image: pabloalarconm/hefesto_fiab:0.0.5
    ports:
      - "8000:8000"
    volumes:
      - ./data:/code/data
```