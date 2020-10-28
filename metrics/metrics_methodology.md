# Metrics Methodology Documentation 

This section provides methodologies and sample calculations of [MDS metrics](https://github.com/lacuna-tech/mobility-data-specification/blob/c5d0092e80a62708efe4e23c8c4c64635b69ed5d/metrics/README.md). The Primary audience for this Guide is cities, mobility service providers, and third-party ecosystem services to have a standard way to consistently compute mobility metrics, while consumers of metrics may also find this document helpful to better understand metric parameters and assumptions.

**Assumptions:** Metrics calculations assume datasets are complete, received on time, and have valid state transitions unless noted otherwise. 

**Note 1:** Cities should consider whether they want to have a policy to exclude anomalous data (e.g. vehicles that do not have a state update after 48 hours or in trip for less than 10 seconds or longer than 5 hours). 

**Note 2:** While metrics are designed to be flexible, and allow calculations using any time interval (hourly, daily, monthly), samples in this document are aggregated into 15-mins intervals for simplicity and illustrative purposes. 


```
This document will be updated to match in accordance with MDS version 1.0.0
```


## Table of Contents
- [1. MDS Core Metrics](#1.-mds-core-metrics)
    - [1.1 vehicles.[state].avg](1.1-vehicles.[state].avg])
    - [1.2 vehicles.[state].min](1.2-vehicles.[state].min)
    - [1.3 vehicles.[state].max](1.3-vehicles.[state].max)
    - [1.4 vehicles.[state].duration.sum](1.4-vehicles.[state].duration.sum)
    - [1.5 events.[event_type].count](1.5-events.[event_type].count)
    - [1.6 trips.[start_loc/end_loc].count](1.6-trips.[start_loc/end_loc].count)
    - [1.7 trips.[start_loc/end_loc]_duration.avg](1.7-trips.[start_loc/end_loc]_duration.avg)
    - [1.8 trips.[start_loc/end_loc]_duration.sum](1.8-trips.[start_loc/end_loc]_duration.sum)
    - [1.9 trips.[start_loc/end_loc]_distance.avg](1.9-trips.[start_loc/end_loc]_distance.avg)
    - [1.10 trips.[start_loc/end_loc]_distance.sum](1.10-trips.[start_loc/end_loc]_distance.sum)
- [2. MDS Dockless Metrics](2.-MDS-Dockless-Metrics)
    - [2.1 dockless.deployed.avg](2.1-dockless.deployed.avg)
    - [2.2 dockless.deployed.avg.min](2.2-dockless.deployed.avg.min)
    - [2.3 dockless.deployed.min](2.3-dockless.deployed.min)
    - [2.4 dockless.deployed.avg.max](2.4-dockless.deployed.avg.max)
    - [2.5 dockless.deployed.max](2.5-dockless.deployed.max)
    - [2.6 dockless.active.count](2.6-dockless.active.count)
    - [2.7 dockless.inactive.count](2.7-dockless.inactive.count)
    - [2.8 dockless.utilization.idle.percent](2.8-dockless.utilization.idle.percent)
    - [2.9 dockless.utilization.active.percent](2.9-dockless.utilization.active.percent)
    - [2.10 dockless.utilization.trips_per_vehicle.avg](2.10-dockless.utilization.trips_per_vehicle.avg)
- [Compatibility with Mobility Data Collaborative Metrics](Compatibility-with-Mobility-Data-Collaborative-Metrics)

## 1. MDS Core Metrics

Reference to MDS Core Metrics specification in Github: [link](https://github.com/lacuna-tech/mobility-data-specification/blob/add_metrics_definitions/metrics/core_metrics.md) 


### 1.1 vehicles.[state].avg

The average number of vehicles in an [MDS state](https://github.com/openmobilityfoundation/mobility-data-specification/tree/release-0.4.1/agency#vehicle-events) during the interval within a geographic area. To calculate **vehicles.[state].avg**, we will take a snapshot of vehicle status every N-period, and  average the number of vehicles shown to be in status. The default for N is a 1-minute snapshot, with the goal to compute metrics at the largest interval where the least amount of change will occur. Although depending on use cases and computational capabilities, the snapshot frequency can be configurable.

**Sample**

We'll assume we have three vehicles registered in our system from one mobility provider. We received an event table, as shown in the table below. 

We modified the sample event table slightly, such that (1) we show event telemetry as geographical areas (Zone A and B) instead of lat/long, and (2) added the state column to highlight state transitions between event types.


<table>
  <tr>
   <td>device_id
   </td>
   <td>event_timestamp (as Time)
   </td>
   <td>event_type
   </td>
   <td>geography
   </td>
   <td>state
   </td>
  </tr>
  <tr>
   <td>vehicle_3
   </td>
   <td>10:01
   </td>
   <td>reserve
   </td>
   <td>Zone A
   </td>
   <td>reserved
   </td>
  </tr>
  <tr>
   <td>vehicle_2
   </td>
   <td>10:04
   </td>
   <td>provider_drop_off
   </td>
   <td>Zone A
   </td>
   <td>available
   </td>
  </tr>
  <tr>
   <td>vehicle_1
   </td>
   <td>10:07
   </td>
   <td>service_end
   </td>
   <td>Zone A
   </td>
   <td>unavailable
   </td>
  </tr>
  <tr>
   <td>vehicle_3
   </td>
   <td>10:06
   </td>
   <td>cancel_reservation
   </td>
   <td>Zone A
   </td>
   <td>available
   </td>
  </tr>
  <tr>
   <td>vehicle_2
   </td>
   <td>10:10
   </td>
   <td>reserve
   </td>
   <td>Zone A
   </td>
   <td>reserved
   </td>
  </tr>
</table>


The table below shows a sample of 1-minute snapshots of vehicles in the available state. 1 indicates vehicles are in an available state. 0  indicates vehicles in other (non-available) states. 


<table>
  <tr>
   <td>Time
   </td>
   <td>Vehicle 1
   </td>
   <td>Vehicle 2
   </td>
   <td>Vehicle 3
   </td>
   <td>Sum
   </td>
  </tr>
  <tr>
   <td>10:00
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>10:01
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>0
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>10:02
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>0
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>10:03
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>0
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>10:04
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>10:05
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>10:06
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>3
   </td>
  </tr>
  <tr>
   <td>10:07
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>10:08
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>10:09
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>10:10
   </td>
   <td>0
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>10:11
   </td>
   <td>0
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>10:12
   </td>
   <td>0
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>10:13
   </td>
   <td>0
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>10:14
   </td>
   <td>0
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
   <td><p style="text-align: right">
<strong>Sum</strong></p>

   </td>
   <td><strong>23</strong>
   </td>
  </tr>
</table>

The sample dataset above will return the following vehicles.available metric output. Some columns are omitted in this sample table for simplicity.

``` 
vehicles.available.avg = 23 / 15 = 1.53 
```

<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>vehicles.available.avg
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>1.53
   </td>
  </tr>
</table>



### 1.2 vehicles.[state].min

The minimum number of vehicles in a specified state during the interval within a geographical area. Similar to calculating **vehicles.[state].avg**, we will take a snapshot of the vehicle state every N-period, and find the minimum number of vehicles in the specified state during the interval.

**Sample**

Using the same sample dataset to calculate **vehicles.[state].avg**, the **vehicles.available.min** metric will return the following output. Some columns are omitted in this sample table for simplicity.

<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>vehicle.available.min
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>1
   </td>
  </tr>
</table>



### 1.3 vehicles.[state].max

The maximum number of vehicles in a specified state during the interval within a geographical area. Similar to calculating **vehicles.[state].avg**, we will take a snapshot of the vehicle state every N-period, and find the maximum number of vehicles in the specified state during the interval.

**Sample**

Using the same sample dataset to calculate **vehicles.[state].avg**, the vehicles.available.max metric will return the following output. Some columns are omitted in this sample table for simplicity.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>vehicle.available.max
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>3
   </td>
  </tr>
</table>



### 1.4 vehicles.[state].duration.sum

The total duration (in seconds) vehicles spent in a specified state within the time interval. The metric is grouped by the geographic area where vehicles start the state.

**Caveat:** The duration is 100% assigned to the geo-location where vehicles start the state. We do not currently factor in the fact that vehicles might traverse through multiple locations, i.e. when vehicles are on trips.


**Sample**

In this sample dataset, we assume there is only one vehicle from one mobility provider. We'll receive an event table that will look something like the table below. 

We modify the event information slightly, such that (1) we did point-in-polygon to show events' telemetry as geographical areas (Zone A, and B), and (2) added the state column to highlight state transitions between event types.


<table>
  <tr>
   <td>device_id
   </td>
   <td>event_timestamp (as Time)
   </td>
   <td>event_type
   </td>
   <td>geography
   </td>
   <td>state
   </td>
  </tr>
  <tr>
   <td>vehicle_1
   </td>
   <td>09:59
   </td>
   <td>reserve
   </td>
   <td>Zone A
   </td>
   <td>reserved 
   </td>
  </tr>
  <tr>
   <td>vehicle_1
   </td>
   <td>10:04
   </td>
   <td>trip_start
   </td>
   <td>Zone A
   </td>
   <td>trip
   </td>
  </tr>
  <tr>
   <td>vehicle_2
   </td>
   <td>10:06
   </td>
   <td>provider_drop_off
   </td>
   <td>Zone A
   </td>
   <td>available
   </td>
  </tr>
  <tr>
   <td>vehicle_1
   </td>
   <td>10:10
   </td>
   <td>trip_end
   </td>
   <td>Zone B
   </td>
   <td>available
   </td>
  </tr>
  <tr>
   <td>vehicle_1
   </td>
   <td>10:18
   </td>
   <td>reserve
   </td>
   <td>Zone B
   </td>
   <td>reserved
   </td>
  </tr>
  <tr>
   <td>vehicle_2
   </td>
   <td>10:20
   </td>
   <td>reserve
   </td>
   <td>Zone A
   </td>
   <td>reserved
   </td>
  </tr>
</table>


The sample dataset above will return **vehicles.[state].duration.sum** as shown in the table below. Some columns are omitted in this sample table for simplicity.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>vehicles.reserved.duration.sum
   </td>
   <td>09:45
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>60 
   </td>
  </tr>
  <tr>
   <td>vehicles.reserved.duration.sum
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>180
   </td>
  </tr>
  <tr>
   <td>vehicles.trip.duration.sum
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>360
   </td>
  </tr>
  <tr>
   <td>vehicles.available.duration.sum
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>540
   </td>
  </tr>
  <tr>
   <td>vehicles.available.duration.sum
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone B
   </td>
   <td>300
   </td>
  </tr>
</table>



### 1.5 events.[event_type].count

The number of [MDS events](https://github.com/openmobilityfoundation/mobility-data-specification/tree/release-0.4.1/agency#vehicle-events) received during the time interval within a geographical area.

**Sample**

Using the same sample dataset to calculate **vehicles.[state].duration.sum**, the **events.[event_type].count** metric will return the following information. Some columns are omitted in this sample table for simplicity.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>events.reserve.count
   </td>
   <td>09:45
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>events.trip_start.count
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>events.provider_drop_off.count
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>events.trip_end.count
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone B
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>events.reserve.count
   </td>
   <td>10:15
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>events.reserve.count
   </td>
   <td>10:15
   </td>
   <td>PT15M
   </td>
   <td>Zone B
   </td>
   <td>1
   </td>
  </tr>
</table>



### 1.6 trips.[start_loc/end_loc].count

The number of trips aggregated by geography areas of either trip_start or trip_enter, or trip_end or final trip_leave events during the time interval. 

**Sample**

Below is a sample of a restructured events table to a trips table


<table>
  <tr>
   <td>trip_id
   </td>
   <td>start_time
   </td>
   <td>end_time
   </td>
   <td>start_geography
   </td>
   <td>end_geography
   </td>
   <td>trip_duration (seconds)
   </td>
   <td>trip_distance (meter)
   </td>
  </tr>
  <tr>
   <td>123-456
   </td>
   <td>2019-09-17 10:00 AM
   </td>
   <td>2019-09-17 10:30 AM
   </td>
   <td>Historic Cultural
   </td>
   <td>Downtown
   </td>
   <td>1680
   </td>
   <td>987
   </td>
  </tr>
  <tr>
   <td>234-345
   </td>
   <td>2019-09-17 10:15 AM
   </td>
   <td>2019-09-17 10:30 AM
   </td>
   <td>Historic Cultural
   </td>
   <td>Downtown
   </td>
   <td>900
   </td>
   <td>321
   </td>
  </tr>
  <tr>
   <td>345-456
   </td>
   <td>2019-09-17 10:15 AM
   </td>
   <td>2019-09-17 10:30 AM
   </td>
   <td>Historic Cultural
   </td>
   <td>Downtown
   </td>
   <td>720
   </td>
   <td>365
   </td>
  </tr>
  <tr>
   <td>456-567
   </td>
   <td>2019-09-17 10:15 AM
   </td>
   <td>2019-09-17 10:45 AM
   </td>
   <td>Historic Cultural
   </td>
   <td>Downtown
   </td>
   <td>1080
   </td>
   <td>420
   </td>
  </tr>
  <tr>
   <td>567-678
   </td>
   <td>2019-09-17 10:30 AM
   </td>
   <td>2019-09-17 10:30 AM
   </td>
   <td>Historic Cultural
   </td>
   <td>Downtown
   </td>
   <td>600
   </td>
   <td>264
   </td>
  </tr>
</table>


A sample metric output table for trips.start.count Some columns are omitted in this sample table for simplicity.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography_type
   </td>
   <td>geography_key
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>trips.start_loc.count
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>trips.start_loc.count
   </td>
   <td>10:15
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>3
   </td>
  </tr>
  <tr>
   <td>trips.start_loc.count
   </td>
   <td>10:30
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>trips.end_loc.count
   </td>
   <td>10:30
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Downtown
   </td>
   <td>4
   </td>
  </tr>
  <tr>
   <td>trips.end_loc.count
   </td>
   <td>10:45
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Downtown
   </td>
   <td>1
   </td>
  </tr>
</table>



### 1.7 trips.[start_loc/end_loc]_duration.avg

The average duration (in seconds) of trips aggregated by geography areas of either trip_start or trip_enter, or trip_end or final trip_leave events during the time interval. 

**Sample**

A sample metric output table for **trips.[start_loc/end_loc]_duration.avg**.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography_type
   </td>
   <td>geography_key
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>trips.start_loc_duration.avg
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>1680
   </td>
  </tr>
  <tr>
   <td>trips.start_loc_duration.avg
   </td>
   <td>10:15
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>900
   </td>
  </tr>
  <tr>
   <td>trips.start_loc_duration.avg
   </td>
   <td>10:30
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>600
   </td>
  </tr>
  <tr>
   <td>trips.start_loc_duration.avg
   </td>
   <td>10:30
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Downtown
   </td>
   <td>975
   </td>
  </tr>
  <tr>
   <td>trips.end_loc_duration.avg
   </td>
   <td>10:45
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Downtown
   </td>
   <td>1080
   </td>
  </tr>
</table>



### 1.8 trips.[start_loc/end_loc]_duration.sum

The total duration (in seconds) of trips aggregated by geography areas of either trip_start or trip_enter, or trip_end or final trip_leave events during the time interval. 

**Sample**

A sample metric output table for **trips.[start_loc/end_loc]_duration.sum**. 


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography_type
   </td>
   <td>geography_key
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>trips.start_loc_duration.sum
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>1680
   </td>
  </tr>
  <tr>
   <td>trips.start_loc_duration.sum
   </td>
   <td>10:15
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>2700
   </td>
  </tr>
  <tr>
   <td>trips.start_loc_duration.sum
   </td>
   <td>10:30
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>600
   </td>
  </tr>
  <tr>
   <td>trips.end_loc_duration.sum
   </td>
   <td>10:30
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Downtown
   </td>
   <td>3900
   </td>
  </tr>
  <tr>
   <td>trips.end_loc_duration.sum
   </td>
   <td>10:45
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Downtown
   </td>
   <td>1080
   </td>
  </tr>
</table>



### 1.9 trips.[start_loc/end_loc]_distance.avg

The average distance (in meter) of trips aggregated by geography areas of either trip_start or trip_enter, or trip_end or final trip_leave events during the time interval. 

**Sample**

A sample metric output table for **trips.[start_loc/end_loc]_distance.avg**.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography_type
   </td>
   <td>geography_key
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>trips.start_loc.distance.avg
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>987
   </td>
  </tr>
  <tr>
   <td>trips.start_loc.distance.avg
   </td>
   <td>10:15
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>368.67
   </td>
  </tr>
  <tr>
   <td>trips.start_loc.distance.avg
   </td>
   <td>10:30
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>264
   </td>
  </tr>
  <tr>
   <td>trips.end_loc.distance.avg
   </td>
   <td>10:30
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Downtown
   </td>
   <td>484.25
   </td>
  </tr>
  <tr>
   <td>trips.end_loc.distance.avg
   </td>
   <td>10:45
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Downtown
   </td>
   <td>420
   </td>
  </tr>
</table>



### 1.10 trips.[start_loc/end_loc]_distance.sum

The total distance (in meter) of trips aggregated by geography areas of either trip_start or trip_enter, or trip_end or final trip_leave events during the time interval. 

**Sample**

A sample metric output table for **trips.[start_loc/end_loc]_distance.sum**.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography_type
   </td>
   <td>geography_key
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>trips.start_loc.distance.sum
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>987
   </td>
  </tr>
  <tr>
   <td>trips.start_loc.distance.sum
   </td>
   <td>10:15
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>1106
   </td>
  </tr>
  <tr>
   <td>trips.start_loc.distance.sum
   </td>
   <td>10:30
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Historical Cultural
   </td>
   <td>264
   </td>
  </tr>
  <tr>
   <td>trips.end_loc.distance.sum
   </td>
   <td>10:30
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Downtown
   </td>
   <td>1937
   </td>
  </tr>
  <tr>
   <td>trips.end_loc.distance.sum
   </td>
   <td>10:45
   </td>
   <td>PT15M
   </td>
   <td>neighborhood_council
   </td>
   <td>Downtown
   </td>
   <td>420
   </td>
  </tr>
</table>



## 2. MDS Dockless Metrics

Reference to MDS Dockless Metrics specification in Github: [link](https://github.com/lacuna-tech/mobility-data-specification/blob/add_metrics_definitions/metrics/dockless_metrics.md) 


### 2.1 dockless.deployed.avg

The average number of vehicles in the public right of way during the time interval and within the geographic area. Vehicles in the public right of way mean they were either in available, unavailable, reserved, or trip state. 

**Sample**

We'll assume we have three vehicles registered in our system from one mobility provider. We received an event table, as shown in the table below. 

We modified the sample event table slightly, such that (1) we show event telemetry as geographical areas (Zone A and B) instead of lat/long, and (2) added the state column to highlight state transitions between event types.


<table>
  <tr>
   <td>device_id
   </td>
   <td>event_timestamp (as Time)
   </td>
   <td>event_type
   </td>
   <td>geography
   </td>
   <td>state
   </td>
  </tr>
  <tr>
   <td>vehicle_1
   </td>
   <td>09:48
   </td>
   <td>trip_end
   </td>
   <td>Zone A
   </td>
   <td>available
   </td>
  </tr>
  <tr>
   <td>vehicle_2
   </td>
   <td>09:50
   </td>
   <td>provider_pick_up
   </td>
   <td>Zone A
   </td>
   <td>removed
   </td>
  </tr>
  <tr>
   <td>vehicle_3
   </td>
   <td>09:59
   </td>
   <td>reserve
   </td>
   <td>Zone A
   </td>
   <td>reserved
   </td>
  </tr>
  <tr>
   <td>vehicle_2
   </td>
   <td>10:04
   </td>
   <td>provider_drop_off
   </td>
   <td>Zone A
   </td>
   <td>available
   </td>
  </tr>
  <tr>
   <td>vehicle_3
   </td>
   <td>10:06
   </td>
   <td>cancel_reservation
   </td>
   <td>Zone A
   </td>
   <td>available
   </td>
  </tr>
  <tr>
   <td>vehicle_1
   </td>
   <td>10:07
   </td>
   <td>service_end
   </td>
   <td>Zone A
   </td>
   <td>unavailable
   </td>
  </tr>
  <tr>
   <td>vehicle_1
   </td>
   <td>10:10
   </td>
   <td>deregister
   </td>
   <td>Zone A
   </td>
   <td>inactive
   </td>
  </tr>
  <tr>
   <td>vehicle_2
   </td>
   <td>10:10
   </td>
   <td>reserve
   </td>
   <td>Zone A
   </td>
   <td>reserved
   </td>
  </tr>
  <tr>
   <td>vehicle_3
   </td>
   <td>10:12
   </td>
   <td>provider_pick_up
   </td>
   <td>Zone A
   </td>
   <td>removed
   </td>
  </tr>
  <tr>
   <td>vehicle_2
   </td>
   <td>10:16
   </td>
   <td>trip_start
   </td>
   <td>Zone A
   </td>
   <td>trip
   </td>
  </tr>
</table>


The table below shows a sample of a 1-minute snapshot of vehicles between 10:00 and 10:15 in Zone A. 1 indicates vehicles were in either available, unavailable, trip, or reserved state. 0 indicates vehicles were in neither of these states.


<table>
  <tr>
   <td>Time
   </td>
   <td>Vehicle 1
   </td>
   <td>Vehicle 2
   </td>
   <td>Vehicle 3
   </td>
   <td>Sum
   </td>
  </tr>
  <tr>
   <td>10:00
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>10:01
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>10:02
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>10:03
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>10:04
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>3
   </td>
  </tr>
  <tr>
   <td>10:05
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>3
   </td>
  </tr>
  <tr>
   <td>10:06
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>3
   </td>
  </tr>
  <tr>
   <td>10:07
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>3
   </td>
  </tr>
  <tr>
   <td>10:08
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>3
   </td>
  </tr>
  <tr>
   <td>10:09
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>3
   </td>
  </tr>
  <tr>
   <td>10:10
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>10:11
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>1
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>10:12
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>10:13
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>10:14
   </td>
   <td>0
   </td>
   <td>1
   </td>
   <td>0
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>
   </td>
   <td>
   </td>
   <td>
   </td>
   <td><p style="text-align: right">
<strong>Sum</strong></p>

   </td>
   <td><strong>33</strong>
   </td>
  </tr>
</table>


Some columns are omitted in this sample table for simplicity.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.avg
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>2.20
   </td>
  </tr>
</table>



### 2.2 dockless.deployed.avg.min

The minimum of the average number of vehicles in the public right of way, which is in the state available, unavailable, reserved, or trip during a time interval, and within the geographic area. The time interval for **dockless.deployed.min.avg** has to be larger than ones used for **dockless.deployed.avg**, such that if **dockless.deployed.avg** is calculated at 1-hour interval, **dockless.deployed.avg.min** can be the average of the 1-hour interval of a 4 hour peak time. 

```
dockless.deployed.avg.min = min(dockless.deployed.avg)
```

**Sample**

Below is an example of **dockless.deployed.avg** grouped into a 1-hour bin, and **dockless.deployed.avg.min** grouped into a 4-hour interval. 


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.avg
   </td>
   <td>06:00
   </td>
   <td>PT1H
   </td>
   <td>Zone A
   </td>
   <td>2.20
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.avg
   </td>
   <td>07:00
   </td>
   <td>PT1H
   </td>
   <td>Zone A
   </td>
   <td>4.10
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.avg
   </td>
   <td>08:00
   </td>
   <td>PT1H
   </td>
   <td>Zone A
   </td>
   <td>3.70
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.avg
   </td>
   <td>09:00
   </td>
   <td>PT1H
   </td>
   <td>Zone A
   </td>
   <td>1.80
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.avg.min
   </td>
   <td>06:00
   </td>
   <td>PT4H
   </td>
   <td>Zone A
   </td>
   <td>1.80
   </td>
  </tr>
</table>



### 2.3 dockless.deployed.min

The minimum number of vehicles in the public right of way, which is in the state available, unavailable, reserved, or trip during the time interval, and within the geographic area. 

**Sample**

Using the same sample dataset to calculate dockless.avg, the **dockless.deployed.min** metric will return the following output. Some columns are omitted in this sample table for simplicity.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>min
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.min
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>1
   </td>
  </tr>
</table>



### 2.4 dockless.deployed.avg.max

The maximum average number of vehicles in the public right of way, which is in the state available, unavailable, reserved, or trip during a time interval, and within the geographic area. The time interval for **dockless.deployed.avg.max** has to be larger than ones used for **dockless.deployed.avg**, such that if dockless.deployed.avg is calculated at 1-hour interval, **dockless.deployed.avg.max** can be the maximum of the 1-hour interval of a 4 hour peak time. 

```
dockless.deployed.avg.max = max(dockless.deployed.avg)
```


**Sample**

Below is an example of dockless.avg grouped into a 15 minutes bin, and dockless.avg.max grouped into 1-hour intervals. 


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.avg
   </td>
   <td>06:00
   </td>
   <td>PT1H
   </td>
   <td>Zone A
   </td>
   <td>2.20
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.avg
   </td>
   <td>07:00
   </td>
   <td>PT1H
   </td>
   <td>Zone A
   </td>
   <td>4.10
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.avg
   </td>
   <td>08:00
   </td>
   <td>PT1H
   </td>
   <td>Zone A
   </td>
   <td>3.70
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.avg
   </td>
   <td>09:00
   </td>
   <td>PT1H
   </td>
   <td>Zone A
   </td>
   <td>1.80
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.avg.max
   </td>
   <td>06:00
   </td>
   <td>PT4H
   </td>
   <td>Zone A
   </td>
   <td>4.10
   </td>
  </tr>
</table>



### 2.5 dockless.deployed.max

The maximum number of vehicles in the public right of way, which is in the state available, unavailable, reserved, or trip during the time interval, and within the geographic area. 

**Sample**

Using the same sample dataset to calculate** dockless.deployed.avg**, the **dockless.deployed**.**max** metric will return the following output. Some columns are omitted in this sample table for simplicity.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>Value
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.max
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>3
   </td>
  </tr>
</table>



### 2.6 dockless.active.count

The number of vehicles in the public right of way that have at least one trip during the interval, i.e. hourly. Metric is grouped by the geographic location of where the trip state started.

**Caveat:** The calculation method outlined above relies on the geographic area where vehicles started their status and do not take into account vehicles' movement traversing through different geographic areas.

**Sample**

In this sample dataset, we assume there were three vehicles from one mobility provider. We'll receive an event table that will look something like the table below. 

We modify the event information slightly, such that (1) we did point-in-polygon to show event telemetry as geographical areas (Zone A, and B), and (2) added the state column to highlight state transitions between event types.


<table>
  <tr>
   <td>device_id
   </td>
   <td>event_timestamp (as Time)
   </td>
   <td>event_type
   </td>
   <td>geography
   </td>
   <td>state
   </td>
  </tr>
  <tr>
   <td>vehicle_1
   </td>
   <td>10:04
   </td>
   <td>trip_start
   </td>
   <td>Zone A
   </td>
   <td>trip
   </td>
  </tr>
  <tr>
   <td>vehicle_2
   </td>
   <td>10:05
   </td>
   <td>trip_enter
   </td>
   <td>Zone A
   </td>
   <td>trip
   </td>
  </tr>
  <tr>
   <td>vehicle_3
   </td>
   <td>10:06
   </td>
   <td>provider_drop_off
   </td>
   <td>Zone B
   </td>
   <td>available
   </td>
  </tr>
  <tr>
   <td>vehicle_2
   </td>
   <td>10:07
   </td>
   <td>trip_leave
   </td>
   <td>Zone A
   </td>
   <td>elsewhere
   </td>
  </tr>
  <tr>
   <td>vehicle_1
   </td>
   <td>10:10
   </td>
   <td>trip_end
   </td>
   <td>Zone B
   </td>
   <td>available
   </td>
  </tr>
  <tr>
   <td>vehicle_2
   </td>
   <td>10:14
   </td>
   <td>trip_enter
   </td>
   <td>Zone A
   </td>
   <td>trip
   </td>
  </tr>
  <tr>
   <td>vehicle_3
   </td>
   <td>10:16
   </td>
   <td>reserve
   </td>
   <td>Zone B
   </td>
   <td>reserved
   </td>
  </tr>
</table>


**dockless.active** metric will return the following output. Some columns are omitted in this sample table for simplicity.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>dockless.active.count
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>2
   </td>
  </tr>
</table>



### 2.7 dockless.inactive.count

The number of vehicles in the public right of way that has no trip during the interval. Metric is grouped by the geographic location of where the vehicle state started.

**Caveat:** The calculation method outlined above relies on the geographic area where vehicles started their status and do not take into account vehicles' movement traversing through different geographic areas.

**Sample**

Using the same sample dataset to calculate dockless.active, the **dockless.inactive** metric will return the following output. Some columns are omitted in this sample table for simplicity.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>dockless.inactive.count
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>dockless.inactive.count
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone B
   </td>
   <td>1
   </td>
  </tr>
</table>



### 2.8 dockless.utilization.idle.percent

The percentage of time vehicles spent not on a trip to the total time vehicles spent in the public right of way (available, unavailable, in trip or reserved) within the geography area during the interval. 


**Sample**

Provided pre-calculated** vehicles.[state].duration.sum** metrics, the **dockless.utilization** metric will return the following output. Some columns are omitted in this sample table for simplicity.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>vehicles.available.duration.sum
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>3200
   </td>
  </tr>
  <tr>
   <td>vehicles.unavailable.duration.sum
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>1800
   </td>
  </tr>
  <tr>
   <td>vehicles.reserved.duration.sum
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>60
   </td>
  </tr>
  <tr>
   <td>vehicles.trip.duration.sum
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>120
   </td>
  </tr>
  <tr>
   <td>dockless.utilization.idle.percent
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>0.98
   </td>
  </tr>
</table>



### 2.9 dockless.utilization.active.percent

The percentage of vehicles that had at least one trip within the geography area during the interval. 


**Sample**

Provided pre-calculated **dockless.active** and **dockless.inactive**, the **dockless.utilization** metric will return the following output. Some columns are omitted in this sample table for simplicity.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>dockless.active.count
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>dockless.inactive.count
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>dockless.inactive.count
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone B
   </td>
   <td>1
   </td>
  </tr>
  <tr>
   <td>dockless.utilization.active.percent
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>0.50
   </td>
  </tr>
  <tr>
   <td>dockless.utilization.active.percent
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone B
   </td>
   <td>1.00
   </td>
  </tr>
</table>



### 2.10 dockless.utilization.trips_per_vehicle.avg

The average number of trips for all deployed vehicles during the interval. 

**Caveat:** The calculation method outlined above relies on the geographic area where vehicles started their status and do not take into account vehicles' movement traversing through different geographic areas.

Provided pre-calculated **trips.start.count** and **dockless.avg**, the **dockless.utilization.trips_per_vehicle.avg** metric will return the following output. Some columns are omitted in this sample table for simplicity.


<table>
  <tr>
   <td>name
   </td>
   <td>metric_start_time
   </td>
   <td>metric_time_interval
   </td>
   <td>geography
   </td>
   <td>value
   </td>
  </tr>
  <tr>
   <td>trips.start.count
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>20
   </td>
  </tr>
  <tr>
   <td>dockless.deployed.avg
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>2
   </td>
  </tr>
  <tr>
   <td>dockless.utilization.trips_frequency.avg
   </td>
   <td>10:00
   </td>
   <td>PT15M
   </td>
   <td>Zone A
   </td>
   <td>10
   </td>
  </tr>
</table>


## Compatibility with Mobility Data Collaborative Metrics

The table below maps MDS Metrics to Mobility Data Collaborative (MDC) [Glossary Metrics](https://github.com/openmobilityfoundation/mobility-data-specification/files/4659200/MDCGlossaryMetrics02202004.pdf).


<table>
  <tr>
   <td><strong>MDS Core Metrics </strong>
   </td>
   <td><strong>MDC Metrics</strong>
   </td>
  </tr>
  <tr>
   <td>1.1    vehicles.[state].avg
   </td>
   <td>6.1   Number of Vehicle of a Specified Status*
<p>
6.2   Average Number of Vehicles of a Specified Status*
   </td>
  </tr>
  <tr>
   <td>1.2    vehicles.[state].min	
   </td>
   <td>6.6   Absolute Minimum Number of Vehicles of a Specified Status*
   </td>
  </tr>
  <tr>
   <td>1.3    vehicles.[state].max	
   </td>
   <td>6.4   Absolute Maximum Number of Vehicles of a Specified Status*
   </td>
  </tr>
  <tr>
   <td>1.4    vehicles.[state].duration.sum
   </td>
   <td>5.x   Time Definitions
   </td>
  </tr>
  <tr>
   <td>1.5    events.[event_type].count
   </td>
   <td>-
   </td>
  </tr>
  <tr>
   <td>1.6    trips.[start_loc/end_loc].count	
   </td>
   <td>7.1   Number of Trips
   </td>
  </tr>
  <tr>
   <td>1.7    trips.[start_loc/end_loc]_duration.avg
   </td>
   <td>-
   </td>
  </tr>
  <tr>
   <td>1.8    trips.[start_loc/end_loc]_duration.sum
   </td>
   <td>-
   </td>
  </tr>
  <tr>
   <td>1.9    trips.[start_loc/end_loc]_distance.avg
   </td>
   <td>-
   </td>
  </tr>
  <tr>
   <td>1.10  trips.[start_loc/end_loc]_distance.sum
   </td>
   <td>-
   </td>
  </tr>
  <tr>
   <td><strong>MDS Dockless Metrics</strong>
   </td>
   <td><strong>MDC Metrics</strong>
   </td>
  </tr>
  <tr>
   <td>2.1    dockless.deployed.avg	
   </td>
   <td>6.1   Number of Vehicle of a Specified Status*
<p>
6.2   Average Number of Vehicles of a Specified Status*
   </td>
  </tr>
  <tr>
   <td>2.2    dockless.deployed.avg.min
   </td>
   <td>6.5   Minimum Average Number of Vehicles of a Specified Status*
   </td>
  </tr>
  <tr>
   <td>2.3    dockless.deployed.min	
   </td>
   <td>6.6   Absolute Minimum Number of Vehicles of a Specified Status*
   </td>
  </tr>
  <tr>
   <td>2.4    dockless.deployed.avg.max	
   </td>
   <td>6.3   Maximum Average Number of Vehicles of a Specific Status*
   </td>
  </tr>
  <tr>
   <td>2.5    dockless.deployed.max
   </td>
   <td>6.4   Absolute Maximum Number of Vehicles of a Specified Status*
   </td>
  </tr>
  <tr>
   <td>2.6    dockless.active.count
   </td>
   <td>-
   </td>
  </tr>
  <tr>
   <td>2.7    dockless.inactive.count	
   </td>
   <td>-
   </td>
  </tr>
  <tr>
   <td>2.8    dockless.utilization.idle_percent
   </td>
   <td>-
   </td>
  </tr>
  <tr>
   <td>2.9    dockless.utilization.active_percent
   </td>
   <td>-
   </td>
  </tr>
  <tr>
   <td>2.10  dockless.utilization.trips_per_vehicle.avg
   </td>
   <td>7.2   Utilization Rate of Vehicles of a Specified Status**
   </td>
  </tr>
</table>


_*MDC does not include a sample to handle geospatial aggregation for vehicles on the move, i.e. in trip status._

_**MDC glossary does not specify the status used to calculate utilization rate. Metrics API calculation is the average of trips per active vehicle, which is consistent with [SharedStreets metrics](https://github.com/sharedstreets/mobility-metrics#metrics)._
