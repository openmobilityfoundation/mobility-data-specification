## MDS Core Metrics

The core metrics are a set of defined, consistent MDS metrics that provide building blocks for other MDS metrics, regardless of vehicle type.

The following represents supported MDS core metrics and definition:


| Metric               | Description                                                                                                         |
| -------------------- | ------------------------------------------------------------------------------------------------------------------- |
| vehicles.[status].avg | <img src="https://lh6.googleusercontent.com/E7yd_nf0KsVabWC_7J6L_2jn2KPOw9F0tA9T1jwFULHBrB-9H0uQ13GViSGKSd69JEUIBOhKM6O0eQY0GW84W5OromEQ0NduoDH1BuFzAsXJZicjA1UZxSojkTVKYb2uUx0lwZVk" title="" alt="" width="88"> where f(x) is the number of vehicles in [MDS status](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-events) at time x. Average number of vehicles in status over the interval (a to b). |
| vehicles.[status].min | Min number of vehicles in [MDS status](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-events) at any time during interval   |
| vehicles.[status].max | Max number of vehicles in [MDS status](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-events) at any time during interval   |
| events               | returns counts for each [MDS event_type](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-events) during interval |
| events.[event_type]  | Count of all `event_type` during interval                                                                            |
| trips                | Trips (count unique trip_id) with trip_end or **final** trip_leave event during interval                               |
| trips.duration       | Total time duration (in seconds)of all trips ending or leaving during interval                                     |
| trips.distance       | Total distance (in meters) traveled by trips ending or leaving during interval                                     |

### Dimensions

The following represent the suggested MDS core metric dimensions:

| Dimension    | Description                                                                                                                |
| ------------ | -------------------------------------------------------------------------------------------------------------------------- |
| provider_id  | Transportation provider id issued by OMF and [tracked here](https://github.com/openmobilityfoundation/mobility-data-specification/blob/dev/providers.csv)                              |
| geo.[type]   | [MDS Geography](https://github.com/openmobilityfoundation/mobility-data-specification/blob/dev/policy/README.md#geographies) e.g. geo.policy, geo.jurisdictions, geo.council_districts |
| vehicle_type | [Vehicle Type](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-type) defined by MDS                                                  |

### Filters

The following represent the suggested MDS core metric filters:

| Filter       | Description                                                                                                                |
| ------------ | -------------------------------------------------------------------------------------------------------------------------- |
| provider_id  | Transportation provider id issued by OMF and [tracked here](https://github.com/openmobilityfoundation/mobility-data-specification/blob/dev/providers.csv)                              |
| geography_id    | [MDS Geography](https://github.com/openmobilityfoundation/mobility-data-specification/blob/dev/policy/README.md#geographies) |
| vehicle_type | [Vehicle Type](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev/agency#vehicle-type) defined by MDS                                                      |


## Other MDS Metrics

- [MDS Dockless Metrics](dockless_metrics.md)
