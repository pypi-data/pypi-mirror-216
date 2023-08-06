# HTTPie mauth

This is a plugin for the [HTTPie](https://github.com/jakubroztocil/httpie)
command line request library that allows it to send mauth-authenticated requests.

To use this, you will need:

* A MAuth App ID
* A MAuth private key whose corresponding public key is registered with the
MAuth server that the target service is using
* A MAuth config file in a supported location, one of:
    * `~/.mauth_config.yml`
    * `./config/mauth.yml`
    * `./mauth.yml`

The format of that file should be as follows:

```yaml
development:
  app_uuid: a36c9238-c9c8-4de9-a385-07dfe6dc1fc4
  private_key_file: /Users/mgup/.mauth_key
```

You can then issue signed requests as follows:

`http --auth-type mauth https://example.com`

You can pass the `-v` option to see the outgoing header. Validating the
signature of the response is not currently supported.
