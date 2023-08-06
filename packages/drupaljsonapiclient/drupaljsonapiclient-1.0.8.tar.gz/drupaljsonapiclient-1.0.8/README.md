# drupaljsonapiclient: Drupal CMS JSON:API client for Python

## What is it?
**drupaljsonapiclient** is a powerful JSON:API client that helps to create and fect Drupal entities and resources via easy-to-use, pythonic, ORM-like abstraction layer.

## Features

* JSON:API write operations (POST, PATCH, and DELETE), including Drupal CMS specific implementation of uploading files.
* Optional asyncio implementation.
* Model schema definition and validation (required for creating/posting resources, optional for reading/fetching resources).
* Resource caching within session.

## Know Limitations

* Parsing meta data for entity reference fields is not supported. Meaning, it is not possible to retrive or post meta data added to entity reference fields used by such as modules as `drupal/image_field_caption`. It is recommended to store the required meta data directly as attributes of the referenced entity. For examply, by adding "Figure Caption" text field to Media entities as an alternative to using `drupal/image_field_caption`.

## Credits

* Based on JSON API Python client by [Tuomas Airaksinen](https://github.com/tuomas2/) for [Qvantel](http://qvantel.com/), 
see [JSON API Python client](https://github.com/qvantel/jsonapi-client/).