## Latest
(may include items not yet merged)
<!-- List what's in open pull requests to be merged at an unknown date -->

- Fixes to [bash aliases](../Basic_setup/Docker.md#aliases).
- Timescaledb template fixed and public port now mapped to 5433.
<!-- PR-560 still a draft
- Documentation development made easier: [Writing documentation](
  ../Developers/index.md#writing-documentation) -->

## 2022-06-12

- Dockerfile based Zigbee2MQTT **deprecated**, requiring [migration](
  ../Containers/Zigbee2MQTT.md#update202204).
- New service: [Duckdns](../Containers/Duckdns.md), deprecates the
  `duck/duck.sh` script.
- New service: [Influxdb 2](../Containers/InfluxDB2.md), supported only on
  fully 64bit systems.
- Docker health checks added to Grafana and InfluxDB.

## 2022-04-26

- New service: [Syncthing](../Containers/Syncthing.md)
- Zigbee2MQTT: [Service definition change](
  ../Containers/Zigbee2MQTT.md#service-definition-change)
- Dropping support for Home Assistant Supervised. Home Assistant **Container**
  still available.
- [Homebridge](../Containers/Homebridge.md) is now on port 8581
- Documentation: Added: [Git Setup](../Developers/Git-Setup.md). Large changes
  to: [Updates](../Updates/index.md), [InfluxDB](../Containers//InfluxDB.md),
  [Grafana](../Containers/Grafana.md), [Pi-hole](../Containers/Pi-hole.md),
  [Docker Logging](../Basic_setup/Docker.md#logging).

## 2022-01-18

- Networking change **requiring** [migration](
  ../Updates/migration-network-change.md).
