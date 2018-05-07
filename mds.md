# Mobility Data Standard

The Mobility Data Standard defines data standards for Mobility as a Service Providers in working with the LADOT to meet in order to ensure timely and shared access to data. 

* Authors: Hunter Owens, Jose Elias, Marcel Porras 

* Date: 3 May 2017 

* Version: ALPHA 

## Sections 

## Trip Data

A trip represents a journey taken by a Mobility as a Service customer with a geotagged start and stop point. The follow data to be provided via a RESTful API for Trip Data. The API should allow to query trips at least by ID, GeoFence for start or end, and time. The following fields to be provided. 

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| Company Name | String | Required | |
| Device Type | String | Required | | 
| Unique ID | UUID | Required | | 
| Trip Duration | Integer | Required | Time, in Seconds | 
| Trip Distance | Integer | Required | Trip Distance, in Meters | 
| Start Point | Point | Required | | 
| End Point | Point | Required | | 
| Route | Line | Optional | | 
| Device ID | UUID | Required | | 
| Start Time | Unix Timestamp | Required | | 
| End Time | Unix Timestamp | Required | |


## System Data / Avaliabity Data 

The following data standard is for avaliability data. The API should return the avaliabity for a system a time range. The API should allow queries at least by time period, geographical areas. 

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| Device Type | String | Required | | 
| Avaliability Start | Unix Timestamp | Required | | 
| Avaliability End | Unix Timestamp | Required |  | 
| Placement Reason | String | Required | Reason for placement (Rebalancing, Drop off, etc) | 
| Pickup Reason | String | Required | Reason for removal (matience, pick up) | 
| Associated Trips | UUID | Optional | list of associated trips | 




## Metrics 

