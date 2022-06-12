# Duck DNS

Duckdns is a free public DNS service that provides you with a domain name you
can update to match your dynamic IP-address.

This container automates the process to keep the duckdns.org domain updated
when your IP-address changes.

## Configuration

First, register an account, add your subdomain and get your token from
[http://www.duckdns.org/](http://www.duckdns.org/)

Either edit `~/IOTstack/docker-compose.yml` or create a file
`~/IOTstack/docker-compose.override.yml`. Place your Duckdns token and
subdomain name (without .duckdns.org) there:

``` yaml title="docker-compose.override.yml"
version: '3.6'
services:
  duckdns:
    environment:
      TOKEN: your-duckdns-token
      SUBDOMAINS: subdomain
```

Observe that at least the initial update is successful:

``` console
$ cd ~/IOTstack
$ docker-compose up -d duckdns
$ docker-compose logs -f duckdns
...SNIP...
duckdns    | Sat May 21 11:01:00 UTC 2022: Your IP was updated
...SNIP...
(ctrl-c to stop following the log)
```

If there is a problem, check that the resulting effective configuration of
'duckdns:' looks OK:
``` console
$ cd ~/IOTstack && docker-compose config
```

### Domain name for the private IP

!!! note inline end "Example public/private IP:s and domains"

    ``` mermaid
    flowchart
    I([Internet])
    G("Router\npublic IP: 52.85.51.71\nsubdomain.duckdns.org")
    R(Raspberry pi\nprivate IP: 192.168.0.100\nprivate_subdomain.duckdns.org)
    I --- |ISP| G --- |LAN| R
    ```

As a public DNS server, Duckdns is not meant to be used for private IPs. It's
recommended that for resolving internal LAN IPs you use the [Pi
Hole](Pi-hole.md) container or run a dedicated DNS server.

That said, it's possible to update a Duckdns subdomain to your private LAN IP.
This may be convenient if you have devices that don't support mDNS (.local) or
don't want to run Pi-hole. This is especially useful if you can't assign a
static IP to your RPi. No changes to your DNS resolver settings are needed.

First, as for the public subdomain, add the domain name to your Duckdns account
by logging in from their homepage. Then add a `PRIVATE_SUBDOMAINS` variable
indicating this subdomain:

``` yaml
version: '3.6'
services:
  duckdns:
    environment:
      TOKEN: ...
      SUBDOMAINS: ...
      PRIVATE_SUBDOMAINS: private_subdomain
```

## References

* uses ukkopahis' [fork](https://github.com/ukkopahis/docker-duckdns) based on
  the linuxserver
  [docker-duckdns](https://github.com/linuxserver/docker-duckdns) container
