# Element Unify Connector Framework

The Unify Python Connector Framework is a library to develop connectors that interact
with Element Unify. This library is intended for developers who are building connectors to
ingest source input data to Element Unify or publish data from Element Unify to another
destination.

## User Information

This section is intended for users of the Unify Python Connector Framework. This includes
developers who are building connectors, integrations, and automation that interfaces
with Element Unify. For developers looking to contribute to the Connector Framework, see the
[Developer Information](#developer-information) section.

## Installation
You can install the Unify Connector Framework from [PyPI](pypi.org/project/unify-connector-framework):

`pip install unify-connector-framework`

### Using the Unify Connector Framework with virtualenv

This assumes you have installed an appropriate version virtualenv, python, and
other associated tools. This also assumes you have an existing python project
you'd like to import into, in this case `my-project`.

    mkdir path/to/my-project; cd path/to/my-project
    virtualenv venv
    source venv/bin/activate
    echo unify-connector-framework >> requirements.txt

Then, in your python import section add the following line:

    from unifyconnectorframework.organization_client import OrganizationClient

### Documentation
The Connector Framework developer guide is found in the Unify API Documentation Portal under the Unify Connector Framework section.

1. Navigate to your instance of Element Unify.
2. Log in and select your organization.
3. From the top-right menu, click on the Support icon and select API Documentation.

## Developer Information

This section is intended for developers working to extend the Unify Connector Framework.

### Developer Guide

1. Fork this repository.
2. Revise files with your contributions.
3. Follow styling guides. See [Python style guide](#python-style-guide).
4. Check for lint warnings. See [Lint checking](#lint-checking).
5. Create a pull request with description of your changes.

### Python style guide

Please use the following Python style guide
[Google Python Styling guide](https://google.github.io/styleguide/pyguide.html)
### Lint checking

We usy pylint to verify lint warnings, our build system requires a linter score
of >=9.0 to pass successfully.
 
To locally check you changes
```
pip install pylint
pylint dir/to/the/file.py
```
