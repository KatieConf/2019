# katieconf.xyz

Source code for KatieConf.xyz

## Testing

Requires: 

  * Ruby
  * Jekyll

```shell
make serve
```

## Updating

Add to the `_data` files, as required, 

You can also use the import helper, `import_speakers.py`

Requires: 

 * Read access to "KatieConf 2019 - Call for Proposals (Responses)"
 * Python 3.8+ in a virtualenv with installed `requirements.txt`

```shell
make import # appends import to _data

make testimport # Shows the data that would be imported
```


