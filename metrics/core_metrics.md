# MDS Core Metrics

The core metrics are a set of defined, consistent MDS metrics that provide building blocks for other MDS metrics, regardless of vehicle type. 

The table below represents supported MDS core metrics and definition. All metrics are aggregated by time interval and geographic areas. This [document](https://docs.google.com/document/d/1rOhnaKWPSZApfWhFd1lzurXMbWLuZTJAYCLoxT2PQ14/edit?usp=sharing) provides methodologies and sample calculations of MDS metrics. 


|Number| Metric                | Description    |
|------|-----------------------|----------------|
| 1.1  | vehicles.[status].avg                  | The average number of vehicles in [MDS status](/agency#vehicle-events). |
| 1.2  | vehicles.[status].min                  | The minimum number of vehicles in [MDS status](/agency#vehicle-events). |
| 1.3  | vehicles.[status].max                  | The maximum number of vehicles in [MDS status](/agency#vehicle-events). |
| 1.4  | vehicles.[status].duration.sum         | The total duration (in seconds) vehicles spent in a specified [MDS status](/agency#vehicle-events). |
| 1.5  | events.[event_type].count              | The number of [MDS event type](/agency#vehicle-events) received. |
| 1.6  | trips.[start_loc/end_loc].count        | The number of trips aggregated by either the start or first enter, or end or final leave locations. |
| 1.7  | trips.[start_loc/end_loc]_duration.avg | The average trip duration (in seconds) aggregated by either the start or first enter, or end or final leave locations. |
| 1.8  | trips.[start_loc/end_loc]_duration.med | The median trip duration (in seconds) aggregated by either the start or first enter, or end or final leave locations. |
| 1.9  | trips.[start_loc/end_loc]_duration.std | The standard deviation trip duration (in seconds) aggregated by either the start or first enter, or end or final leave locations. |
| 1.10 | trips.[start_loc/end_loc]_duration.sum | The total sum of trip duration (in seconds) aggregated by either the start or first enter, or end or final leave locations. |
| 1.11 | trips.[start_loc/end_loc]_distance.avg | The average trip distance (in meters) aggregated by either the start or first enter, or end or final leave locations. |
| 1.12 | trips.[start_loc/end_loc]_distance.med | The median trip distance (in meters) aggregated by either the start or first enter, or end or final leave locations. |
| 1.13 | trips.[start_loc/end_loc]_distance.std | The standard deviation trip distance (in meters) aggregated by either the start or first enter, or end or final leave locations. |
| 1.14 | trips.[start_loc/end_loc]_distance.sum | The total sum of trip distance (in meters) aggregated by either the start or first enter, or end or final leave locations. |

## Dimensions

The following represent the suggested MDS core metric dimensions:

| Dimension    | Description |
| ------------ | -------------------------------------------------------------------------------------------------------------------------- |
| provider_id  | Transportation provider id issued by OMF and [tracked here](/providers.csv)                              |
| [geography_type](/geography#geography-type)   | [MDS Geography](/geography) e.g. policy, jurisdictions, council_districts |
| vehicle_type | [Vehicle Type](/agency#vehicle-type) defined by MDS                                                  |
| special_group_type | [Special Group Type](#special-group-type) defined by MDS                                                  |

## Filters

The following represent the suggested MDS core metric filters:

| Filter       | Description                                                                                                                |
| ------------ | -------------------------------------------------------------------------------------------------------------------------- |
| provider_id  | Transportation provider id issued by OMF and [tracked here](/providers.csv)                              |
| geography_id    | [MDS Geography](/geography) |
| vehicle_type | [Vehicle Type](/agency#vehicle-type) defined by MDS                                                      |
| special_group_type | [Special Group Type](#special-group-type) defined by MDS                                                  |

## Special Group Type

Special groups of riders can be optionally queried and counts can be returned in aggregate.  

Here are the possible values for the `special_group_type` field:

| Name | Description |
|------|------|
| low_income | Trips where a low income discount is applied by the provider, e.g., a discount from a qualified provider equity plan. |

Other special group types may be added in future MDS releases as relevant agency and provider use cases are identified.

# Other MDS Metrics

- [MDS Dockless Metrics](dockless_metrics.md)
