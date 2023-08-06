Quickbase API SDK for Synctivate server development

# Setup

## Installation
To install the SDK, run `pip install syncqb`.

## Initializing a `QuickbaseClient` object

You have two options for initializing your client object, utilizing `get_client()` or manual initialization.

To utilize `get_client`, you can first run `setqbinfo` in your terminal after installing to create default credentials, which will prompt you like this:
```bash
~$ setqbinfo
Quickbase URL (include https): https://yourrealm.quickbase.com
User Token: your_token
Username: your.username@mail.com
Password: 
```
Or you can create a dictionary if you haven't run `setqbinfo` or wish to override the default credentials, and enter your credentials there.

### Note: for better type hints and docstrings, use `get_json_client()` or `get_xml_client()` in place of `get_client()`

Then set up your code to something like this:
```python
from syncqb.qb_client import get_client

# if you are setting up your credentials with a dictionary, you must have the keys shown
credentials = {
    'QB_URL': 'https://yourrealm.quickbase.com',

    # This is only needed if you use the json client
    'QB_USERTOKEN': 'your_token',

    # This is only needed if you use the xml client
    'QB_USERNAME': 'your.username@mail.com',
    # This is only needed if you use the xml client
    'QB_PASSWORD': 'password'
}

# to initialize a json client object
json_client = get_client(True)

# to initialize an xml client object
# creds is the optional parameter whose argument is your credentials dictionary
xml_client = get_client(creds=credentials)
```

### Note:
Using `setqbinfo` will create a .env file that contains your credentials that you entered. You can modify this file by running `setqbinfo` again, running the python function `set_qb_info()` which you can import from `syncqb.qb_client`, or by manually modifying the file in an editor. The .env file will contain your sensitive information, DO NOT SHARE IT!



Or you can manually initialize your client object using code like the example below:
```python
from syncqb import json_quickbase, xml_quickbase

# to initialize a json QuickbaseClient object
json_client = json_quickbase.JsonQuickbaseClient(
    realmhost='yourrealm.quickbase.com', base_url="https://yourrealm.quickbase.com", user_token="your_token")

# to initialize an xml QuickbaseClient object
xml_client = xml_quickbase.XmlQuickbaseClient(
    base_url="https://yourrealm.quickbase.com", username='your.username@mail.com', password='password')
```

### Note: 
Using the JSON SDK is encouraged unless you are going to be sending requests with payloads larger than 10MB. Also note that the XML SDK functions a bit differently from the JSON SDK. Some features may not work or work differently.

# Usage
The quickbase `QuickbaseClient` object has many uses, the primary ones relating to finding, adding, editing, and deleting records

## Querying for Records

One of the primary uses of the quickbase `QuickbaseClient` is querying for records. Querying for records can be done using the `do_query()` method. 
Here is a basic example of querying for records:
```python

data = qb_client.do_query(query="{6.EX.'example'}", columns=[3,6,7], database='dbid')

for record in data:
    #do stuff
```
where query is a quickbase [query string](https://help.quickbase.com/api-guide/componentsquery.html),
columns is a list of field IDs that you want returned for each record
and database is the ID of the table that you would like to query from.

The other way to use the `do_query` method is by passing a report ID to the `qid` parameter instead.

Here is a slightly more advanced example of `do_query`, this time using `qid`:
```python
data = qb_client.do_query(qid=1, skip=3, max=50, sort=[3] database='dbid')

for record in data:
    #do stuff
```
where `skip` is the number of records to skip, `max` is the maximum amount of records to retrieve, 
and `sort` is a list of field IDs on which to sort in ascending order by default.
Order the field IDs in your `sort` list to the order that you want each field to be sorted. For example: 
`sort=[3,5]` will first sort by field ID 3, and then by field ID 5.

`skip` and `max` will only function when also using a `qid` parameter,
and `columns` will only function when also using a `query` parameter.

## Adding records

The `QuickbaseClient` object also has two methods to add new records: `add_record()` and `add_multiple_records()`*.

Heres an example of `add_record()`:
```python
# set fields and their values
fields = {
    '6':value,
    '8':value,
    '10':value
}

# add_record in try block to handle any errors
try:
    qb_client.add_record(fields=fields, database='dbid', safemode=True)
except Exception as e:
    print(e)
    #error handling code
```
The `fields` parameter is a dictionary of values with their keys being the respective field IDs, the `database` parameter is the the table ID, and the `safemode` parameter determines whether the code will check for the primary key field in `fields` and return an error if it is present; this parameter is also optional for `add_multiple_records()`. There is also an `uploads` parameter that takes a file upload.

Here is an example of `add_multiple_records()`*:
```python
data = [
    {
        '6': value
        '7': value
    },
    {
        '6': value
        '7': value
    },
]
response = qb_client.add_multiple_records(data=data, database='dbid', return_fields=[3,6,7])
# do stuff with response
```
`data` is a list of dicts as shown above, `database` is the table ID, and `return_fields` is an optional list of field id's that you want returned.

Along with adding records, there are also methods `edit_record()` and `edit_multiple_records()`* which function very similarly to their counterparts.

*The XML API does not have `add_multiple_records()` or `edit_multiple_records()`.

## Deleting Records

There are two methods for deleting records: `delete_record()` and `purge_records()`.
`delete_record()` takes two parameters, `database` and `record`, where `database` is the desired table ID, and `record` is the record ID. Example:
```python
qb_client.delete_record(database='dbid', record=100)
```
`purge_records()` takes at least two arguments, `database` which is the table ID, and either `query`, which is a quickbase [query string](https://help.quickbase.com/api-guide/componentsquery.html), or `rids` which is a list of record IDs. 
If both a `query` and a `rid` list is given, the list takes precedence. Example:
```python
qb_client.purge_records(database='dbid', rids=[100,101,102])
```

# Additional Usage

The `QuickbaseClient` object also has some other useful features such as file upload functionality,  `denest()` and `nest()` methods, and an `import_from_csv()` method.

## File Uploading and Downloading

The `get_file()` method retrieves file data from a given record. It can either take the `url` parameter where `url` is the complete file url extension, or it can take the following arguments: `database` which is the table ID, `record` which is the record ID, `field` which is the field ID, and `version` which is the version number.
Example:
```python
qb_client.get_file(database='dbid', record=100, field=8, version=1)
```
The `upload_file()` method takes three arguments: `rid` which is the record ID that the file is being uploaded to, `upload` which contains the required file data, and `database` which id the table ID.
Example:
```python
upload = {
    'filename':'test.txt',
    'value': 'b64_string',
    'field':7
}
qb_client.upload_file(rid=100, upload=upload, database=dbid)
```
The `add_record()` method also takes an optional `uploads` parameter which takes a list set up like this: 
```python
uploads = [{'field': fid, 'filename': filename, 'value': b64_data}]
```

## Other features

The `nest()` and `denest()` methods will convert data from `{fid:value}` to `{fid: {'value':value}}` and vice versa.
The `import_from_csv()` method will take a csv string and upload the records contained in the string.
The `round_ints()` method will take any returned data and change any unneeded floating-points to numbers. This method can be automatically called with an optional parameter `round_ints` in methods that return field data.

For more information on these additional features and other features, you can look at their individual documentation in src/json_quickbase.pyi or src/xml_quickbase.pyi.