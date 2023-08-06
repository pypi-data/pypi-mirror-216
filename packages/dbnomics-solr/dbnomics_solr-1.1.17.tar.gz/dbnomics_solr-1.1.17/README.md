# DBnomics Solr

Index DBnomics data into Apache Solr for full-text and faceted search.

Requirements:

- a running instance of [Apache Solr](http://lucene.apache.org/solr/); at the time this documentation is written, we use the version 7.3.

See [dbnomics-docker](https://git.nomics.world/dbnomics/dbnomics-docker) to run a local DBnomics instance with Docker that includes a service for Apache Solr.

## Configuration

Environment variables:

- `DEBUG_PYSOLR`: display pysolr DEBUG logging messages (cf <https://github.com/django-haystack/pysolr>)

## Index a provider

Replace `wto` by the real provider slug in the following command:

```bash
dbnomics-solr index-provider /path/to/wto-json-data
```

### Full mode vs incremental mode

When data is stored in a regular directory, the script always indexes all datasets and series of a provider. This is called _full mode_.

When data is stored in a Git repository, the script runs by default in _incremental mode_: it indexes only the datasets modified since the last indexation.

It is possible to force the _full mode_ with the `--full` option.

### Bare repositories

The script has an option `--bare-repo-fallback` which tries to add `.git` at the end of the storage dir name, if not found.

## Remove all data from a provider

To remove all the documents related to a provider (`type:provider`, `type:dataset` and `type:series`):

```bash
dbnomics-solr --debug delete-provider --code <provider_code>
dbnomics-solr --debug delete-provider --slug <provider_slug>

# Examples:
dbnomics-solr --debug delete-provider --code WTO
dbnomics-solr --debug delete-provider --slug wto
```
