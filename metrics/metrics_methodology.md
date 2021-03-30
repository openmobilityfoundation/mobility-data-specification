# Metrics Methodology Documentation

This section provides methodologies and sample calculations of [MDS metrics](/metrics/README.md). The Primary audience for this Guide is cities, mobility service providers, and third-party ecosystem services to have a standard way to consistently compute mobility metrics, while consumers of metrics may also find this document helpful to better understand metric parameters and assumptions.

**Assumptions:** Metrics calculations assume datasets are complete, received on time, and have valid state transitions unless noted otherwise. 

**Note 1:** Cities should consider whether they want to have a policy to exclude anomalous data (e.g. vehicles that do not have a state update after 48 hours or in trip for less than 10 seconds or longer than 5 hours). 

**Note 2:** While metrics are designed to be flexible, and allow calculations using any time interval (hourly, daily, monthly), samples in this document are aggregated into 15-mins intervals for simplicity and illustrative purposes. 

## Table of Contents

- [1. MDS Core Metrics](#1-mds-core-metrics)
  - [1.1 vehicles.[state].avg](#11-vehiclesstateavg)
  - [1.2 vehicles.[state].min](#12-vehiclesstatemin)
  - [1.3 vehicles.[state].max](#13-vehiclesstatemax)
  - [1.4 vehicles.[state].duration.sum](#14-vehiclesstatedurationsum)
  - [1.5 events.[event_type].count](#15-eventsevent_typecount)
  - [1.6 trips.[start_loc/end_loc].count](#16-tripsstart_locend_loccount)
  - [1.7 trips.[start_loc/end_loc]_duration.avg](#17-tripsstart_locend_loc_durationavg)
  - [1.8 trips.[start_loc/end_loc]_duration.sum](#18-tripsstart_locend_loc_durationsum)
  - [1.9 trips.[start_loc/end_loc]_distance.avg](#19-tripsstart_locend_loc_distanceavg)
  - [1.10 trips.[start_loc/end_loc]_distance.sum](#110-tripsstart_locend_loc_distancesum)
- [2. MDS Dockless Metrics](#2-mds-dockless-metrics)
  - [2.1 dockless.deployed.avg](#21-docklessdeployedavg)
  - [2.2 dockless.deployed.avg.min](#22-docklessdeployedavgmin)
  - [2.3 dockless.deployed.min](#23-docklessdeployedmin)
  - [2.4 dockless.deployed.avg.max](#24-docklessdeployedavgmax)
  - [2.5 dockless.deployed.max](#25-docklessdeployedmax)
  - [2.6 dockless.active.count](#26-docklessactivecount)
  - [2.7 dockless.inactive.count](#27-docklessinactivecount)
  - [2.8 dockless.utilization.idle.percent](#28-docklessutilizationidlepercent)
  - [2.9 dockless.utilization.active.percent](#29-docklessutilizationactivepercent)
  - [2.10 dockless.utilization.trips_per_vehicle.avg](#210-docklessutilizationtrips_per_vehicleavg)
- [Compatibility with Mobility Data Collaborative Metrics](#compatibility-with-mobility-data-collaborative-metrics)

## 1. MDS Core Metrics

Reference to MDS Core Metrics specification in Github: [link](/metrics/core_metrics.md) 

### 1.1 `vehicles.[state].avg`

The average number of vehicles in an [MDS state](../general-information.md#vehicle-states) during the interval within a geographic area. To calculate **vehicles.[state].avg**, we will take a snapshot of vehicle status every N-period, and  average the number of vehicles shown to be in status. The default for N is a 1-minute snapshot, with the goal to compute metrics at the largest interval where the least amount of change will occur. Although depending on use cases and computational capabilities, the snapshot frequency can be configurable.

**Sample**

We'll assume we have three vehicles registered in our system from one mobility provider. We received an event table, as shown in the table below. 

We modified the sample event table slightly, such that (1) we show event telemetry as geographical areas (Zone A and B) instead of lat/long, and (2) added the state column to highlight state transitions between event types.

| device_id | event_timestamp (as Time) | event_type         | geography | state       |
| --------- | ------------------------- | ------------------ | --------- | ----------- |
| vehicle_3 | 10:01                     | reserve            | Zone A    | reserved    |
| vehicle_2 | 10:04                     | provider_drop_off  | Zone A    | available   |
| vehicle_1 | 10:07                     | service_end        | Zone A    | unavailable |
| vehicle_3 | 10:06                     | cancel_reservation | Zone A    | available   |
| vehicle_2 | 10:10                     | reserve            | Zone A    | reserved    |

The table below shows a sample of 1-minute snapshots of vehicles in the available state. 1 indicates vehicles are in an available state. 0  indicates vehicles in other (non-available) states. 

| Time  | Vehicle 1 | Vehicle 2 | Vehicle 3 | Sum |
| ----- | --------- | --------- | --------- | --- |
| 10:00 | 1         | 0         | 1         | 2   |
| 10:01 | 1         | 0         | 0         | 1   |
| 10:02 | 1         | 0         | 0         | 1   |
| 10:03 | 1         | 0         | 0         | 1   |
| 10:04 | 1         | 1         | 0         | 2   |
| 10:05 | 1         | 1         | 0         | 2   |
| 10:06 | 1         | 1         | 1         | 3   |
| 10:07 | 0         | 1         | 1         | 2   |
| 10:08 | 0         | 1         | 1         | 2   |
| 10:09 | 0         | 1         | 1         | 2   |
| 10:10 | 0         | 0         | 1         | 1   |
| 10:11 | 0         | 0         | 1         | 1   |
| 10:12 | 0         | 0         | 1         | 1   |
| 10:13 | 0         | 0         | 1         | 1   |
| 10:14 | 0         | 0         | 1         | 1   |
|       |           |           | Sum       | 23  |

The sample dataset above will return the following vehicles.available metric output. Some columns are omitted in this sample table for simplicity.

```
vehicles.available.avg = 23 / 15 = 1.53 
```

| name                   | metric_start_time | metric_time_interval | geography | value |
| ---------------------- | ----------------- | -------------------- | --------- | ----- |
| vehicles.available.avg | 10:00             | PT15M                | Zone A    | 1.53  |

### 1.2 `vehicles.[state].min`

The minimum number of vehicles in a specified state during the interval within a geographical area. Similar to calculating **vehicles.[state].avg**, we will take a snapshot of the vehicle state every N-period, and find the minimum number of vehicles in the specified state during the interval.

**Sample**

Using the same sample dataset to calculate **vehicles.[state].avg**, the **vehicles.available.min** metric will return the following output. Some columns are omitted in this sample table for simplicity.

| name                  | metric_start_time | metric_time_interval | geography | value |
| --------------------- | ----------------- | -------------------- | --------- | ----- |
| vehicle.available.min | 10:00             | PT15M                | Zone A    | 1     |

### 1.3 `vehicles.[state].max`

The maximum number of vehicles in a specified state during the interval within a geographical area. Similar to calculating **vehicles.[state].avg**, we will take a snapshot of the vehicle state every N-period, and find the maximum number of vehicles in the specified state during the interval.

**Sample**

Using the same sample dataset to calculate **vehicles.[state].avg**, the vehicles.available.max metric will return the following output. Some columns are omitted in this sample table for simplicity.

| name                  | metric_start_time | metric_time_interval | geography | value |
| --------------------- | ----------------- | -------------------- | --------- | ----- |
| vehicle.available.max | 10:00             | PT15M                | Zone A    | 3     |

### 1.4 vehicles.[state].duration.sum

The total duration (in seconds) vehicles spent in a specified state within the time interval. The metric is grouped by the geographic area where vehicles start the state.

**Caveat:** The duration is 100% assigned to the geo-location where vehicles start the state. We do not currently factor in the fact that vehicles might traverse through multiple locations, i.e. when vehicles are on trips.

**Sample**

In this sample dataset, we assume there is only one vehicle from one mobility provider. We'll receive an event table that will look something like the table below. 

We modify the event information slightly, such that (1) we did point-in-polygon to show events' telemetry as geographical areas (Zone A, and B), and (2) added the state column to highlight state transitions between event types.

| device_id | event_timestamp (as Time) | event_type        | geography | state     |
| --------- | ------------------------- | ----------------- | --------- | --------- |
| vehicle_1 | 09:59                     | reserve           | Zone A    | reserved  |
| vehicle_1 | 10:04                     | trip_start        | Zone A    | trip      |
| vehicle_2 | 10:06                     | provider_drop_off | Zone A    | available |
| vehicle_1 | 10:10                     | trip_end          | Zone B    | available |
| vehicle_1 | 10:18                     | reserve           | Zone B    | reserved  |
| vehicle_2 | 10:20                     | reserve           | Zone A    | reserved  |

The sample dataset above will return **vehicles.[state].duration.sum** as shown in the table below. Some columns are omitted in this sample table for simplicity.

| name                            | metric_start_time | metric_time_interval | geography | value |
| ------------------------------- | ----------------- | -------------------- | --------- | ----- |
| vehicles.reserved.duration.sum  | 09:45             | PT15M                | Zone A    | 60    |
| vehicles.reserved.duration.sum  | 10:00             | PT15M                | Zone A    | 180   |
| vehicles.trip.duration.sum      | 10:00             | PT15M                | Zone A    | 360   |
| vehicles.available.duration.sum | 10:00             | PT15M                | Zone A    | 540   |
| vehicles.available.duration.sum | 10:00             | PT15M                | Zone B    | 300   |

### 1.5 `events.[event_type].count`

The number of [MDS events]../agency#vehicle---event) received during the time interval within a geographical area.

**Sample**

Using the same sample dataset to calculate **vehicles.[state].duration.sum**, the **events.[event_type].count** metric will return the following information. Some columns are omitted in this sample table for simplicity.

| name                           | metric_start_time | metric_time_interval | geography | value |
| ------------------------------ | ----------------- | -------------------- | --------- | ----- |
| events.reserve.count           | 09:45             | PT15M                | Zone A    | 1     |
| events.trip_start.count        | 10:00             | PT15M                | Zone A    | 1     |
| events.provider_drop_off.count | 10:00             | PT15M                | Zone A    | 1     |
| events.trip_end.count          | 10:00             | PT15M                | Zone B    | 1     |
| events.reserve.count           | 10:15             | PT15M                | Zone A    | 1     |
| events.reserve.count           | 10:15             | PT15M                | Zone B    | 1     |

### 1.6 `trips.[start_loc/end_loc].count`

The number of trips aggregated by geography areas of either trip_start or trip_enter, or trip_end or final trip_leave events during the time interval. 

**Sample**

Below is a sample of a restructured events table to a trips table

| trip_id | start_time          | end_time            | start_geography   | end_geography | trip_duration (seconds) | trip_distance (meter) |
| ------- | ------------------- | ------------------- | ----------------- | ------------- | ----------------------- | --------------------- |
| 123-456 | 2019-09-17 10:00 AM | 2019-09-17 10:30 AM | Historic Cultural | Downtown      | 1680                    | 987                   |
| 234-345 | 2019-09-17 10:15 AM | 2019-09-17 10:30 AM | Historic Cultural | Downtown      | 900                     | 321                   |
| 345-456 | 2019-09-17 10:15 AM | 2019-09-17 10:30 AM | Historic Cultural | Downtown      | 720                     | 365                   |
| 456-567 | 2019-09-17 10:15 AM | 2019-09-17 10:45 AM | Historic Cultural | Downtown      | 1080                    | 420                   |
| 567-678 | 2019-09-17 10:30 AM | 2019-09-17 10:30 AM | Historic Cultural | Downtown      | 600                     | 264                   |

A sample metric output table for trips.start.count Some columns are omitted in this sample table for simplicity.

| name                  | metric_start_time | metric_time_interval | geography_type       | geography_key       | value |
| --------------------- | ----------------- | -------------------- | -------------------- | ------------------- | ----- |
| trips.start_loc.count | 10:00             | PT15M                | neighborhood_council | Historical Cultural | 1     |
| trips.start_loc.count | 10:15             | PT15M                | neighborhood_council | Historical Cultural | 3     |
| trips.start_loc.count | 10:30             | PT15M                | neighborhood_council | Historical Cultural | 1     |
| trips.end_loc.count   | 10:30             | PT15M                | neighborhood_council | Downtown            | 4     |
| trips.end_loc.count   | 10:45             | PT15M                | neighborhood_council | Downtown            | 1     |

### 1.7 `trips.[start_loc/end_loc]_duration.avg`

The average duration (in seconds) of trips aggregated by geography areas of either trip_start or trip_enter, or trip_end or final trip_leave events during the time interval. 

**Sample**

A sample metric output table for **trips.[start_loc/end_loc]_duration.avg**.

| name                         | metric_start_time | metric_time_interval | geography_type       | geography_key       | value |
| ---------------------------- | ----------------- | -------------------- | -------------------- | ------------------- | ----- |
| trips.start_loc_duration.avg | 10:00             | PT15M                | neighborhood_council | Historical Cultural | 1680  |
| trips.start_loc_duration.avg | 10:15             | PT15M                | neighborhood_council | Historical Cultural | 900   |
| trips.start_loc_duration.avg | 10:30             | PT15M                | neighborhood_council | Historical Cultural | 600   |
| trips.start_loc_duration.avg | 10:30             | PT15M                | neighborhood_council | Downtown            | 975   |
| trips.end_loc_duration.avg   | 10:45             | PT15M                | neighborhood_council | Downtown            | 1080  |

### 1.8 `trips.[start_loc/end_loc]_duration.sum`

The total duration (in seconds) of trips aggregated by geography areas of either trip_start or trip_enter, or trip_end or final trip_leave events during the time interval. 

**Sample**

A sample metric output table for **trips.[start_loc/end_loc]_duration.sum**. 

| name                         | metric_start_time | metric_time_interval | geography_type       | geography_key       | value |
| ---------------------------- | ----------------- | -------------------- | -------------------- | ------------------- | ----- |
| trips.start_loc_duration.sum | 10:00             | PT15M                | neighborhood_council | Historical Cultural | 1680  |
| trips.start_loc_duration.sum | 10:15             | PT15M                | neighborhood_council | Historical Cultural | 2700  |
| trips.start_loc_duration.sum | 10:30             | PT15M                | neighborhood_council | Historical Cultural | 600   |
| trips.end_loc_duration.sum   | 10:30             | PT15M                | neighborhood_council | Downtown            | 3900  |
| trips.end_loc_duration.sum   | 10:45             | PT15M                | neighborhood_council | Downtown            | 1080  |

### 1.9 `trips.[start_loc/end_loc]_distance.avg`

The average distance (in meter) of trips aggregated by geography areas of either trip_start or trip_enter, or trip_end or final trip_leave events during the time interval. 

**Sample**

A sample metric output table for **trips.[start_loc/end_loc]_distance.avg**.

| name                         | metric_start_time | metric_time_interval | geography_type       | geography_key       | value  |
| ---------------------------- | ----------------- | -------------------- | -------------------- | ------------------- | ------ |
| trips.start_loc.distance.avg | 10:00             | PT15M                | neighborhood_council | Historical Cultural | 987    |
| trips.start_loc.distance.avg | 10:15             | PT15M                | neighborhood_council | Historical Cultural | 368.67 |
| trips.start_loc.distance.avg | 10:30             | PT15M                | neighborhood_council | Historical Cultural | 264    |
| trips.end_loc.distance.avg   | 10:30             | PT15M                | neighborhood_council | Downtown            | 484.25 |
| trips.end_loc.distance.avg   | 10:45             | PT15M                | neighborhood_council | Downtown            | 420    |

### 1.10 `trips.[start_loc/end_loc]_distance.sum`

The total distance (in meter) of trips aggregated by geography areas of either trip_start or trip_enter, or trip_end or final trip_leave events during the time interval. 

**Sample**

A sample metric output table for **trips.[start_loc/end_loc]_distance.sum**.

| name                         | metric_start_time | metric_time_interval | geography_type       | geography_key       | value |
| ---------------------------- | ----------------- | -------------------- | -------------------- | ------------------- | ----- |
| trips.start_loc.distance.sum | 10:00             | PT15M                | neighborhood_council | Historical Cultural | 987   |
| trips.start_loc.distance.sum | 10:15             | PT15M                | neighborhood_council | Historical Cultural | 1106  |
| trips.start_loc.distance.sum | 10:30             | PT15M                | neighborhood_council | Historical Cultural | 264   |
| trips.end_loc.distance.sum   | 10:30             | PT15M                | neighborhood_council | Downtown            | 1937  |
| trips.end_loc.distance.sum   | 10:45             | PT15M                | neighborhood_council | Downtown            | 420   |

## 2. MDS Dockless Metrics

Reference to MDS Dockless Metrics specification in Github: [link](../metrics/dockless_metrics.md) 

### 2.1 `dockless.deployed.avg`

The average number of vehicles in the public right of way during the time interval and within the geographic area. Vehicles in the public right of way mean they were either in available, unavailable, reserved, or trip state. 

**Sample**

We'll assume we have three vehicles registered in our system from one mobility provider. We received an event table, as shown in the table below. 

We modified the sample event table slightly, such that (1) we show event telemetry as geographical areas (Zone A and B) instead of lat/long, and (2) added the state column to highlight state transitions between event types.

| device_id | event_timestamp (as Time) | event_type         | geography | state       |
| --------- | ------------------------- | ------------------ | --------- | ----------- |
| vehicle_1 | 09:48                     | trip_end           | Zone A    | available   |
| vehicle_2 | 09:50                     | provider_pick_up   | Zone A    | removed     |
| vehicle_3 | 09:59                     | reserve            | Zone A    | reserved    |
| vehicle_2 | 10:04                     | provider_drop_off  | Zone A    | available   |
| vehicle_3 | 10:06                     | cancel_reservation | Zone A    | available   |
| vehicle_1 | 10:07                     | service_end        | Zone A    | unavailable |
| vehicle_1 | 10:10                     | deregister         | Zone A    | inactive    |
| vehicle_2 | 10:10                     | reserve            | Zone A    | reserved    |
| vehicle_3 | 10:12                     | provider_pick_up   | Zone A    | removed     |
| vehicle_2 | 10:16                     | trip_start         | Zone A    | trip        |

The table below shows a sample of a 1-minute snapshot of vehicles between 10:00 and 10:15 in Zone A. 1 indicates vehicles were in either available, unavailable, trip, or reserved state. 0 indicates vehicles were in neither of these states.

| Time  | Vehicle 1 | Vehicle 2 | Vehicle 3 | Sum |
| ----- | --------- | --------- | --------- | --- |
| 10:00 | 1         | 0         | 1         | 2   |
| 10:01 | 1         | 0         | 1         | 2   |
| 10:02 | 1         | 0         | 1         | 2   |
| 10:03 | 1         | 0         | 1         | 2   |
| 10:04 | 1         | 1         | 1         | 3   |
| 10:05 | 1         | 1         | 1         | 3   |
| 10:06 | 1         | 1         | 1         | 3   |
| 10:07 | 1         | 1         | 1         | 3   |
| 10:08 | 1         | 1         | 1         | 3   |
| 10:09 | 1         | 1         | 1         | 3   |
| 10:10 | 0         | 1         | 1         | 2   |
| 10:11 | 0         | 1         | 1         | 2   |
| 10:12 | 0         | 1         | 0         | 1   |
| 10:13 | 0         | 1         | 0         | 1   |
| 10:14 | 0         | 1         | 0         | 1   |
|       |           |           | Sum       | 33  |

Some columns are omitted in this sample table for simplicity.

| name                  | metric_start_time | metric_time_interval | geography | value |
| --------------------- | ----------------- | -------------------- | --------- | ----- |
| dockless.deployed.avg | 10:00             | PT15M                | Zone A    | 2.20  |

### 2.2 dockless.deployed.avg.min

The minimum of the average number of vehicles in the public right of way, which is in the state available, unavailable, reserved, or trip during a time interval, and within the geographic area. The time interval for **dockless.deployed.min.avg** has to be larger than ones used for **dockless.deployed.avg**, such that if **dockless.deployed.avg** is calculated at 1-hour interval, **dockless.deployed.avg.min** can be the average of the 1-hour interval of a 4 hour peak time. 

```
dockless.deployed.avg.min = min(dockless.deployed.avg)
```

**Sample**

Below is an example of **dockless.deployed.avg** grouped into a 1-hour bin, and **dockless.deployed.avg.min** grouped into a 4-hour interval. 

| name                      | metric_start_time | metric_time_interval | geography | value |
| ------------------------- | ----------------- | -------------------- | --------- | ----- |
| dockless.deployed.avg     | 06:00             | PT1H                 | Zone A    | 2.20  |
| dockless.deployed.avg     | 07:00             | PT1H                 | Zone A    | 4.10  |
| dockless.deployed.avg     | 08:00             | PT1H                 | Zone A    | 3.70  |
| dockless.deployed.avg     | 09:00             | PT1H                 | Zone A    | 1.80  |
| dockless.deployed.avg.min | 06:00             | PT4H                 | Zone A    | 1.80  |

### 2.3 `dockless.deployed.min`

The minimum number of vehicles in the public right of way, which is in the state available, unavailable, reserved, or trip during the time interval, and within the geographic area. 

**Sample**

Using the same sample dataset to calculate dockless.avg, the **dockless.deployed.min** metric will return the following output. Some columns are omitted in this sample table for simplicity.

| name                  | metric_start_time | metric_time_interval | geography | min |
| --------------------- | ----------------- | -------------------- | --------- | --- |
| dockless.deployed.min | 10:00             | PT15M                | Zone A    | 1   |

### 2.4 `dockless.deployed.avg.max`

The maximum average number of vehicles in the public right of way, which is in the state available, unavailable, reserved, or trip during a time interval, and within the geographic area. The time interval for **dockless.deployed.avg.max** has to be larger than ones used for **dockless.deployed.avg**, such that if dockless.deployed.avg is calculated at 1-hour interval, **dockless.deployed.avg.max** can be the maximum of the 1-hour interval of a 4 hour peak time. 

```
dockless.deployed.avg.max = max(dockless.deployed.avg)
```

**Sample**

Below is an example of dockless.avg grouped into a 15 minutes bin, and dockless.avg.max grouped into 1-hour intervals. 

| name                      | metric_start_time | metric_time_interval | geography | value |
| ------------------------- | ----------------- | -------------------- | --------- | ----- |
| dockless.deployed.avg     | 06:00             | PT1H                 | Zone A    | 2.20  |
| dockless.deployed.avg     | 07:00             | PT1H                 | Zone A    | 4.10  |
| dockless.deployed.avg     | 08:00             | PT1H                 | Zone A    | 3.70  |
| dockless.deployed.avg     | 09:00             | PT1H                 | Zone A    | 1.80  |
| dockless.deployed.avg.max | 06:00             | PT4H                 | Zone A    | 4.10  |

### 2.5 `dockless.deployed.max`

The maximum number of vehicles in the public right of way, which is in the state available, unavailable, reserved, or trip during the time interval, and within the geographic area. 

**Sample**

Using the same sample dataset to calculate **dockless.deployed.avg**, the **dockless.deployed.max** metric will return the following output. Some columns are omitted in this sample table for simplicity.

| name                  | metric_start_time | metric_time_interval | geography | Value |
| --------------------- | ----------------- | -------------------- | --------- | ----- |
| dockless.deployed.max | 10:00             | PT15M                | Zone A    | 3     |

### 2.6 dockless.active.count

The number of vehicles in the public right of way that have at least one trip during the interval, i.e. hourly. Metric is grouped by the geographic location of where the trip state started.

**Caveat:** The calculation method outlined above relies on the geographic area where vehicles started their status and do not take into account vehicles' movement traversing through different geographic areas.

**Sample**

In this sample dataset, we assume there were three vehicles from one mobility provider. We'll receive an event table that will look something like the table below. 

We modify the event information slightly, such that (1) we did point-in-polygon to show event telemetry as geographical areas (Zone A, and B), and (2) added the state column to highlight state transitions between event types.

| device_id | event_timestamp (as Time) | event_type        | geography | state     |
| --------- | ------------------------- | ----------------- | --------- | --------- |
| vehicle_1 | 10:04                     | trip_start        | Zone A    | trip      |
| vehicle_2 | 10:05                     | trip_enter        | Zone A    | trip      |
| vehicle_3 | 10:06                     | provider_drop_off | Zone B    | available |
| vehicle_2 | 10:07                     | trip_leave        | Zone A    | elsewhere |
| vehicle_1 | 10:10                     | trip_end          | Zone B    | available |
| vehicle_2 | 10:14                     | trip_enter        | Zone A    | trip      |
| vehicle_3 | 10:16                     | reserve           | Zone B    | reserved  |

**dockless.active** metric will return the following output. Some columns are omitted in this sample table for simplicity.

| name                  | metric_start_time | metric_time_interval | geography | value |
| --------------------- | ----------------- | -------------------- | --------- | ----- |
| dockless.active.count | 10:00             | PT15M                | Zone A    | 2     |

### 2.7 `dockless.inactive.count`

The number of vehicles in the public right of way that has no trip during the interval. Metric is grouped by the geographic location of where the vehicle state started.

**Caveat:** The calculation method outlined above relies on the geographic area where vehicles started their status and do not take into account vehicles' movement traversing through different geographic areas.

**Sample**

Using the same sample dataset to calculate dockless.active, the **dockless.inactive** metric will return the following output. Some columns are omitted in this sample table for simplicity.

| name                    | metric_start_time | metric_time_interval | geography | value |
| ----------------------- | ----------------- | -------------------- | --------- | ----- |
| dockless.inactive.count | 10:00             | PT15M                | Zone A    | 1     |
| dockless.inactive.count | 10:00             | PT15M                | Zone B    | 1     |

### 2.8 `dockless.utilization.idle.percent`

The percentage of time vehicles spent not on a trip to the total time vehicles spent in the public right of way (available, unavailable, in trip or reserved) within the geography area during the interval. 

**Sample**

Provided pre-calculated **vehicles.[state].duration.sum** metrics, the **dockless.utilization** metric will return the following output. Some columns are omitted in this sample table for simplicity.

| name                              | metric_start_time | metric_time_interval | geography | value |
| --------------------------------- | ----------------- | -------------------- | --------- | ----- |
| vehicles.available.duration.sum   | 10:00             | PT15M                | Zone A    | 3200  |
| vehicles.unavailable.duration.sum | 10:00             | PT15M                | Zone A    | 1800  |
| vehicles.reserved.duration.sum    | 10:00             | PT15M                | Zone A    | 60    |
| vehicles.trip.duration.sum        | 10:00             | PT15M                | Zone A    | 120   |
| dockless.utilization.idle.percent | 10:00             | PT15M                | Zone A    | 0.98  |

### 2.9 `dockless.utilization.active.percent`

The percentage of vehicles that had at least one trip within the geography area during the interval. 

**Sample**

Provided pre-calculated **dockless.active** and **dockless.inactive**, the **dockless.utilization** metric will return the following output. Some columns are omitted in this sample table for simplicity.

| name                                | metric_start_time | metric_time_interval | geography | value |
| ----------------------------------- | ----------------- | -------------------- | --------- | ----- |
| dockless.active.count               | 10:00             | PT15M                | Zone A    | 2     |
| dockless.inactive.count             | 10:00             | PT15M                | Zone A    | 1     |
| dockless.inactive.count             | 10:00             | PT15M                | Zone B    | 1     |
| dockless.utilization.active.percent | 10:00             | PT15M                | Zone A    | 0.50  |
| dockless.utilization.active.percent | 10:00             | PT15M                | Zone B    | 1.00  |

### 2.10 `dockless.utilization.trips_per_vehicle.avg`

The average number of trips for all deployed vehicles during the interval. 

**Caveat:** The calculation method outlined above relies on the geographic area where vehicles started their status and do not take into account vehicles' movement traversing through different geographic areas.

Provided pre-calculated **trips.start.count** and **dockless.avg**, the **dockless.utilization.trips_per_vehicle.avg** metric will return the following output. Some columns are omitted in this sample table for simplicity.

| name                                     | metric_start_time | metric_time_interval | geography | value |
| ---------------------------------------- | ----------------- | -------------------- | --------- | ----- |
| trips.start.count                        | 10:00             | PT15M                | Zone A    | 20    |
| dockless.deployed.avg                    | 10:00             | PT15M                | Zone A    | 2     |
| dockless.utilization.trips_frequency.avg | 10:00             | PT15M                | Zone A    | 10    |

## Compatibility with Mobility Data Collaborative Metrics

The table below maps MDS Metrics to Mobility Data Collaborative (MDC) [Glossary Metrics](https://github.com/openmobilityfoundation/mobility-data-specification/files/4659200/MDCGlossaryMetrics02202004.pdf).[**](#footnotes)   

| MDS Core Metrics                                 | MDC Metrics                                                                                            |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------ |
| 1.1    vehicles.[state].avg                      | 6.1   Number of Vehicle of a Specified Status[*](#footnotes),  6.2   Average Number of Vehicles of a Specified Status[*](#footnotes)  |
| 1.2    vehicles.[state].min                      | 6.6   Absolute Minimum Number of Vehicles of a Specified Status[*](#footnotes)                                       |
| 1.3    vehicles.[state].max                      | 6.4   Absolute Maximum Number of Vehicles of a Specified Status[*](#footnotes)                                        |
| 1.4    vehicles.[state].duration.sum             | 5.x   Time Definitions                                                                                 |
| 1.5    events.[event_type].count                 | -                                                                                                      |
| 1.6    trips.[start_loc/end_loc].count           | 7.1   Number of Trips                                                                                  |
| 1.7    trips.[start_loc/end_loc]_duration.avg    | -                                                                                                      |
| 1.8    trips.[start_loc/end_loc]_duration.sum    | -                                                                                                      |
| 1.9    trips.[start_loc/end_loc]_distance.avg    | -                                                                                                      |
| 1.10  trips.[start_loc/end_loc]_distance.sum     | -                                                                                                      |

| MDS Dockless Metrics                             | MDC Metrics                            |
| ------------------------------------------------ | -------------------------------------- |
| 2.1    dockless.deployed.avg                     | 6.1   Number of Vehicle of a Specified Status[*](#footnotes), 6.2   Average Number of Vehicles of a Specified Status[*](#footnotes)  |
| 2.2    dockless.deployed.avg.min                 | 6.5   Minimum Average Number of Vehicles of a Specified Status[*](#footnotes)                                       |
| 2.3    dockless.deployed.min                     | 6.6   Absolute Minimum Number of Vehicles of a Specified Status[*](#footnotes)                                        |
| 2.4    dockless.deployed.avg.max                 | 6.3   Maximum Average Number of Vehicles of a Specific Status[*](#footnotes)                                          |
| 2.5    dockless.deployed.max                     | 6.4   Absolute Maximum Number of Vehicles of a Specified Status[*](#footnotes)                                        |
| 2.6    dockless.active.count                     | -                                                                                                      |
| 2.7    dockless.inactive.count                   | -                                                                                                      |
| 2.8    dockless.utilization.idle_percent         | -                                                                                                      |
| 2.9    dockless.utilization.active_percent       | -                                                                                                      |
| 2.10  dockless.utilization.trips_per_vehicle.avg | 7.2   Utilization Rate of Vehicles of a Specified Status                                               |

### Footnotes

* _MDC does not include a sample to handle geospatial aggregation for vehicles on the move, i.e. in trip status._

** _MDC glossary does not specify the status used to calculate utilization rate. Metrics API calculation is the average of trips per active vehicle, which is consistent with [SharedStreets metrics](https://github.com/sharedstreets/mobility-metrics#metrics)._
