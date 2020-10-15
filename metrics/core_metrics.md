## MDS Core Metrics

The core metrics are a set of defined, consistent MDS metrics that provide building blocks for other MDS metrics, regardless of vehicle type. 

The table below represents supported MDS core metrics and definition. All metrics are aggregated by time interval and geographic areas. This [document](https://docs.google.com/document/d/1rOhnaKWPSZApfWhFd1lzurXMbWLuZTJAYCLoxT2PQ14/edit?usp=sharing) provides methodologies and sample calculations of MDS metrics. 


|No| Metric               | Description                                                                                                         |
|--| --| -- |
|1.1 | vehicles.[status].avg | The average number of vehicles in [MDS status](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-events). |
|1.2 | vehicles.[status].min | The minimum number of vehicles in [MDS status](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-events).   |
|1.3| vehicles.[status].max | The maximum number of vehicles in [MDS status](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-events). |
|1.4| vehicles.[status].duration.sum | The total duration (in seconds) vehicles spent in a specified [MDS status](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-events). |
|1.5| events.[event_type].count |The number of [MDS event type](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-events) received.  |
|1.6| trips.[start_loc/end_loc].count|The number of trips aggregated by either the start or first enter, or end or final leave locations.|
|1.7| trips.[start_loc/end_loc]_duration.avg|The average trip duration (in seconds) aggregated by either the start or first enter, or end or final leave locations.|
|1.8| trips.[start_loc/end_loc]_duration.sum| The total trip duration (in seconds) aggregated by either the start or first enter, or end or final leave locations. |
|1.9| trips.[start_loc/end_loc]_distance.avg| The average trip distance (in meter) aggregated by either the start or first enter, or end or final leave locations. |
|1.10| trips.[start_loc/end_loc]_distance.sum|The total trip distance (in meter) aggregated by either the start or first enter, or end or final leave locations.|

### Dimensions

The following represent the suggested MDS core metric dimensions:

| Dimension    | Description |
| ------------ | -------------------------------------------------------------------------------------------------------------------------- |
| provider_id  | Transportation provider id issued by OMF and [tracked here](https://github.com/openmobilityfoundation/mobility-data-specification/blob/dev/providers.csv)                              |
| [geography_type]   | [MDS Geography](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/geography) e.g. policy, jurisdictions, council_districts |
| vehicle_type | [Vehicle Type](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-type) defined by MDS                                                  |

### Filters

The following represent the suggested MDS core metric filters:

| Filter       | Description                                                                                                                |
| ------------ | -------------------------------------------------------------------------------------------------------------------------- |
| provider_id  | Transportation provider id issued by OMF and [tracked here](https://github.com/openmobilityfoundation/mobility-data-specification/blob/dev/providers.csv)                              |
| geography_id    | [MDS Geography](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/geography) |
| vehicle_type | [Vehicle Type](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-type) defined by MDS                                                      |


## Other MDS Metrics

- [MDS Dockless Metrics](dockless_metrics.md)
