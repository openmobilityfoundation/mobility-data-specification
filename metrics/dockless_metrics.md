## MDS Dockless Metrics

MDS dockless metrics are a set of defined metrics and compound metrics useful for measuring dockless vehicle activity with MDS data. Dockless metrics measure vehicle activity when they are in the public right of way, which means vehicles were in either available, unavailable, reserved, or trip state.

The table below represents supported MDS dockless metrics extension and definition. All metrics are aggregated by time interval and geographic areas. This [document](metrics_methodology.md) provides methodologies and sample calculations of MDS metrics. 

| No   | Metric                                     | Description                                                                                                     |
| ---- | ------------------------------------------ | --------------------------------------------------------------------------------------------------------------- |
| 2.1  | dockless.deployed.avg                      | The average number of vehicles in the public right of way.                                                      |
| 2.2  | dockless.deployed.avg.min                  | The minimum of the average number of vehicles in the public right of way.                                       |
| 2.3  | dockless.deployed.min                      | The minimum number of vehicles in the public right of way.                                                      |
| 2.4  | dockless.deployed.avg.max                  | The maximum average number of vehicles in the public right of way.                                              |
| 2.5  | dockless.deployed.max                      | The maximum number of vehicles in the public right of way.                                                      |
| 2.6  | dockless.active.avg                      | The average number of vehicles in the public right of way that have at least one trip during the interval, i.e. hourly. |
| 2.7  | dockless.inactive.avg                    | The average number of vehicles in the public right of way that have no trip during the interval.                        |
| 2.8  | dockless.utilization.idle.percent          | The percentage of time vehicles spent not in trip to the total time vehicles spent in the public right of way.  |
| 2.9  | dockless.utilization.active.percent        | The percentage of vehicles that had at least one trip during the interval.                                      |
| 2.10 | dockless.utilization.trips_per_vehicle.avg | The average number of trips for all vehicles in the public right of way during the interval.                    |
