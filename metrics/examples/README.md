# Metrics Examples

This file represents a series of examples of [Metrics](/metrics) to use as templates. 

## Table of Contents

- [Metrics Discovery API](metrics-discovery-api)
- [Metrics Query API](metrics-query-api)

## Metrics Discovery API

Returns a discovery response describing the supported metrics, times, intervals, dimensions and filters.

#### Request

```js
GET /metrics
```

#### Response

```json
{
  "metrics": [
    {
      "measures": ["dockless.deployed.avg"],
      "since": "2019-01-01T00:00-07",
      "intervals": ["PT1H"]
    },
    {
      "measures": ["vehicles.available.count", "trips.end_loc.count"],
      "since": "2018-01-01T00:00-07",
      "intervals": ["PT15M", "PT1H", "P1D"]
    }
  ],
  "max_intervals": 10000,
  "dimensions": [
    "provider_id",
    "vehicle_type",
    "geography_id"
  ],
  "filters": [
    "provider_id",
    "vehicle_type",
    "geography_type",
    "geography_id"
  ]
}
```

## Metrics Query API

### Example: Activities

This metrics will pull daily vehicle deployment and the number of trips made by each vehicle type for all providers. 

File: [`activities.json`](activities.json) (request)

File: [`activities_response.json`](activities_response.json) (response)

#### Request

```js
POST /metrics
{
  "measures": ["dockless.deployed.avg","trips.end_loc.count"],
  "interval": "P1D",
  "start_date": "2019-10-21T00:00-07",
  "end_date": "2019-10-28T00:00-07",
  "dimensions": ["geography_id", "vehicle_type"],
  "filters": [
    {
      "name": "geography_type",
      "values": ["census_block"]
    }
  ]
}
```

#### Reponse

```json
{
  "id": "44428624-186b-4fc3-a7fb-124f487464a1",
  "query": {
    "measures": [
      "dockless.deployed.avg",
      "trips.end_loc.count"
    ],
    "interval": "P1D",
    "start_date": "2019-10-21T00:00-07",
    "end_date": "2019-10-28T00:00-07",
    "dimensions": ["vehicle_type"],
    "timezone": "UTC",
    "k_value": 10,
    "filters": []
  },
  "columns": [
    {
      "name": "interval_start",
      "column_type": "dimension",
      "data_type": "datetime"
    },
    {
      "name": "geography_id",
      "column_type": "dimension",
      "data_type": "uuid"
    },
    {
      "name": "vehicle_type",
      "column_type": "dimension",
      "data_type": "string"
    },
    {
      "name": "dockless.deployed.avg",
      "column_type": "measure",
      "data_type": "float"
    },
    {
      "name": "trips.end_loc.count",
      "column_type": "measure",
      "data_type": "integer"
    }
  ],
  "rows": [
    ["2019-10-21T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "bicycle", 456.12, 69],
    ["2019-10-22T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "bicycle", 235.23, 114],
    ["2019-10-23T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "bicycle", 124.13, 46],
    ["2019-10-24T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "bicycle", 123.45, 36],
    ["2019-10-25T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "bicycle", 223.56, -1],
    ["2019-10-26T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "bicycle", 1981.89, 10967],
    ["2019-10-27T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "bicycle", 4562.55, 25271],
    ["2019-10-21T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "scooter", 456.12, 69],
    ["2019-10-22T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "scooter", 235.23, 114],
    ["2019-10-23T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "scooter", 124.13, 46],
    ["2019-10-24T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "scooter", 123.45, 36],
    ["2019-10-25T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "scooter", 223.56, -1],
    ["2019-10-26T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "scooter", 1981.89, 10967],
    ["2019-10-27T00:00-07", "03db06d0-3998-406a-92c7-25a83fc2784a", "scooter", 4562.55, 25271],
    ["2019-10-21T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "bicycle", 456.12, 69],
    ["2019-10-22T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "bicycle", 235.23, 114],
    ["2019-10-23T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "bicycle", 124.13, 46],
    ["2019-10-24T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "bicycle", 123.45, 36],
    ["2019-10-25T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "bicycle", 223.56, -1],
    ["2019-10-26T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "bicycle", 1981.89, 10967],
    ["2019-10-27T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "bicycle", 4562.55, 25271],
    ["2019-10-21T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "scooter", 456.12, 69],
    ["2019-10-22T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "scooter", 235.23, 114],
    ["2019-10-23T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "scooter", 124.13, 46],
    ["2019-10-24T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "scooter", 123.45, 36],
    ["2019-10-25T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "scooter", 223.56, -1],
    ["2019-10-26T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "scooter", 1981.89, 10967],
    ["2019-10-27T00:00-07", "2b697fb4-5935-4d4a-88ea-0745e1ea9b29", "scooter", 4562.55, 25271]
  ]
}
```
