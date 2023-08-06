MS Jira hours imputed services
=============================
This repository is a suite of methods necessary to extract and calculate information about the allocated hours of employees and their work agreements.


Hours agreement
========================
The hours that an employee must do are recorded in a Google Sheet where the hours needed by office are indicated for each day.


## How to use the agreements service?
----------------------------------

In order for us to connect to Google services, we need to register a series of environment variables:


```bash
export GOOGLE_SHEET_CREDENTIALS=<SERVICE_ACCOUNT_BASE64_CONTENT>
```
where we will store in Base64 the content of the JSON of our Google service account that has the credentials to authenticate us.


```bash
export GOOGLE_SHEET_AGREEMENTS_SPREADSHEET_ID=<ID_FOR_GOOGLE_SHEET>
```
It will be the Google sheet ID where the work agreements will be.

### Usage example

#### Getting agreement hours for a month
```python
from ms_imputedhours_core.agreements import Agreement

month = 9
year = 2022
sheet_name = 'Sheet 1'
spreadsheet_id = '111111'

service = Agreements(spreadsheet_id)

service.get_hours_by_month(month, year, sheet_name)
```

#### Getting agreement hours by a dates range
```python
from ms_imputedhours_core.agreements import Agreement

spreadsheet_id = '111111'
from_date = datetime.strptime('12/09/2022', '%d/%m/%Y')
to_date = datetime.strptime('17/09/2022', '%d/%m/%Y')
sheet_name = 'SHEET_NAME_TEST'

service = Agreements(spreadsheet_id)

service.get_hours_by_range(from_date, to_date, sheet_name)
```

#### Getting all office names
```python
from ms_imputedhours_core.agreements import Agreement

spreadsheet_id = '111111'

service = Agreements(spreadsheet_id)

service..get_all_office_names()
```

# How to contribute
After clone repository

## 1.- Install dependencies
```bash
poetry install
```

## 2.- Run test
```bash
make test
```

## 3.- Run lint
```bash
make lint && make isort
```

## How to publish new version
Once we have done a merge of our Pull request and we have the updated master branch we can generate a new version. For them we have 3 commands that change the version of our library and generate the corresponding tag so that the Bitbucket pipeline starts and publishes our library automatically.

```bash
make release-patch
```

```bash
make release-minor
```

```bash
make release-major
```
