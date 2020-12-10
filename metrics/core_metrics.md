# MDS Core Metrics

The core metrics are a set of defined, consistent MDS metrics definitions that provide building blocks for other MDS [metrics](/metrics), regardless of vehicle type. 

## Table of Contents

- [Metrics Definitions](#metrics-definitions)
  - [Dimensions](#dimensions)
  - [Filters](#filters)
- [Other MDS Metrics](#other-mds-metrics)

# Metrics Definitions

The table below represents supported MDS core metrics and definition. All metrics are aggregated by time interval and geographic areas. This [document](metrics_methodology.md) provides methodologies and sample calculations of MDS metrics. 

| Number | Metric                                 | Description                                                                                                                       |
| ------ | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 1.1    | vehicles.[status].avg                  | The average number of vehicles in [MDS status](/agency#vehicle-events).                                                           |
| 1.2    | vehicles.[status].min                  | The minimum number of vehicles in [MDS status](/agency#vehicle-events).                                                           |
| 1.3    | vehicles.[status].max                  | The maximum number of vehicles in [MDS status](/agency#vehicle-events).                                                           |
| 1.4    | vehicles.[status].duration.sum         | The total duration (in seconds) vehicles spent in a specified [MDS status](/agency#vehicle-events).                               |
| 1.5    | events.[event_type].count              | The number of [MDS event type](/agency#vehicle-events) received.                                                                  |
| 1.6    | trips.[start_loc/end_loc].count        | The number of trips aggregated by either the start or first enter, or end or final leave locations.                               |
| 1.7    | trips.[start_loc/end_loc].duration.avg | The average trip duration (in seconds) aggregated by either the start or first enter, or end or final leave locations.            |
| 1.8    | trips.[start_loc/end_loc].duration.med | The median trip duration (in seconds) aggregated by either the start or first enter, or end or final leave locations.             |
| 1.9    | trips.[start_loc/end_loc].duration.std | The standard deviation trip duration (in seconds) aggregated by either the start or first enter, or end or final leave locations. |
| 1.10   | trips.[start_loc/end_loc].duration.sum | The total sum of trip duration (in seconds) aggregated by either the start or first enter, or end or final leave locations.       |
| 1.11   | trips.[start_loc/end_loc].distance.avg | The average trip distance (in meters) aggregated by either the start or first enter, or end or final leave locations.             |
| 1.12   | trips.[start_loc/end_loc].distance.med | The median trip distance (in meters) aggregated by either the start or first enter, or end or final leave locations.              |
| 1.13   | trips.[start_loc/end_loc].distance.std | The standard deviation trip distance (in meters) aggregated by either the start or first enter, or end or final leave locations.  |
| 1.14   | trips.[start_loc/end_loc].distance.sum | The total sum of trip distance (in meters) aggregated by either the start or first enter, or end or final leave locations.        |

[Top][toc]

## Dimensions

The following represent the suggested MDS core metric dimensions:

| Dimension          | Description                                                                 |
| ------------------ | --------------------------------------------------------------------------- |
| provider_id        | Transportation provider id issued by OMF and [tracked here](/providers.csv) |
| geography_id       | [MDS Geography](/geography)                                                 |
| vehicle_type       | [Vehicle Type](/agency#vehicle-type) defined by MDS                         |

[Top][toc]

## Filters

The following represent the suggested MDS core metric filters:

| Filter             | Description                                                                                       |
| ------------------ | ------------------------------------------------------------------------------------------------- |
| provider_id        | Transportation provider id issued by OMF and [tracked here](/providers.csv)                       |
| geography_id       | [MDS Geography](/geography)                                                                       |
| geography_type     | [MDS Geography Type](/geography#geography-type) e.g. census_block, jurisdiction, council_district |
| vehicle_type       | [Vehicle Type](/agency#vehicle-type) defined by MDS                                               |

[Top][toc]

# Other MDS Metrics

- [MDS Dockless Metrics](dockless_metrics.md)

[Top][toc]

[toc]: #table-of-contents
