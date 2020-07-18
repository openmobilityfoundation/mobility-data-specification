# MDS Metrics API

An API for requesting **historical** calculated [metrics](core_metrics.md) and aggregations of MDS data. 

Objectives:
- Cities need a number of clearly defined best practice metrics for operating, measuring, and managing emerging micro mobility programs using MDS data.
- There is currently no standard counting methodology that mobility providers and cities have agreed upon. This consequently causes friction when establishing a new mobility program and evaluating its impact
- Cities need to rely upon trusted data sources upon which to perform longer term studies on citizen impact.
- Mobility providers would like consistent rules between each city deployment in order to make their operations more scalable.

Initial Design Use Cases:
- For cities to republish data ingested from MDS (Agency or Provider data) for use in visualization, analysis, or other applications
- For cities to publish calculated metrics back to providers allowing shared understanding of how policies are measured and enforced

## Date and Time Format

All dates and times (datetime) are [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format strings (YYYY-MM-DDTHHMM), with minute granularity supported and time zone as default UTC or included offset. 

All interval durations (duration) are [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) duration format strings (e.g. PT15M, PT1H, P1D).

## Metrics Discovery API

### Method

`GET /metrics`

Returns a discovery response describing the supported metrics, times, intervals, dimensions and filters.

### Parameters

None.

### Response

| Name              | Type       | Required | Comments                                                                                                  |
| ----------------- | ---------- | -------- | --------------------------------------------------------------------------------------------------------- |
| `metrics`         | metric[]   | Yes      | List of supported metrics.                                                                                |
| `metric.name`     | string[]   | Yes      | List of supported metric names. [See metric names](core_metrics.md)                                       |
| `metric.since`    | datetime   | Yes      | Earliest supported start date for fetching metrics.  Minute (MM) must be divisible by minimum `interval`. |
| `metric.interval` | duration[] | Yes      | A list of interval durations in ascending order.  Minimum (first) interval duration is the default.       |
| `max_intervals`   | integer    | Yes      | Maximum number intervals that can be returned.                                                            |
| `dimensions`      | string[]   | Yes      | List of supported dimensions. [See dimensions.](core_metrics.md#dimensions)                               |
| `filters`         | string[]   | Yes      | List of supported filters for metrics. [See filters.](core_metrics.md#filters)                            |

### Response Schema
```js
{
  "metrics": [
    {
      "name": [string],
      "since": datetime,
      "intervals": [duration]
    }
  ],
  "max_intervals": number,
  "dimensions": [string],
  "filters": [string]
}
```

### Example
#### Request
```js
GET /metrics
```
#### Response
```json
{
  "metrics": [
    {
      "name": ["dockless.utilization.avg"],
      "since": "2019-01-01T00:00-07",
      "intervals": ["PT1H"]
    },
    {
      "name": ["vehicles.available.count", "trips.count"],
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
    "geography_id"
  ]
}
```

## Metrics Query API

### Method

`POST /metrics`

Supports querying one or more metrics with the following parameters.

### Parameters

| Name            | Type     | Required | Comments                                                          |
| --------------- | -------- | -------- | ----------------------------------------------------------------- |
| `metrics`       | string[] | Yes      | list of metrics to return. [See metric names](core_metrics.md)    |
| `interval`      | duration | Yes      | Duration for metrics intervals.                                   |
| `start_date`    | datetime | Yes      | ISO 8601 formatted start date to fetch metrics.                   |
| `end_date`      | datetime | No       | ISI 8601 formatted end date to fetch metrics.                     |
| `timezone`      | timezone | No       | ISO 8601 time zone name (default: "UTC")                          |
| `dimensions`    | string[] | No       | List of dimension names. [See dimensions.](#dimensions)           |
| `filters`       | filter[] | No       | Filters for metrics to return of format. [See filters.](#filters) |
| `filter.name`   | string   | No       | Name of filter (e.g. 'vehicle_type')                              |
| `filter.values` | string[] | No       | List of values to filter for (e.g ['car', 'moped'])               |

Note: If `timezone` is specified then `start_date`, `end_date`, and all _datetime_ column values will be 
converted to the specified time zone. If not, parameters will be converted to and the results will be 
displayed in UTC.

Note: If `end_date` is specified, all intervals that *begin* between the specified `start_date` and the `end_date` *(inclusive)* are fetched. If `end_date` is not specified, only the interval that begins *on* the specified `start_date` is fetched. 

### Response

| Name                 | Type       | Comments                                                        |
| -------------------- | ---------- | --------------------------------------------------------------- |
| `id`                 | uuid       | Unique id for query                                             |
| `query.metrics`      | string[]   | From request.                                                   |
| `query.interval`     | duration   | From Request.                                                   |
| `query.start_date`   | datetime   | From Request.                                                   |
| `query.end_date`     | datetime   | From Request.                                                   |
| `query.dimensions`   | string[]   | From Request.                                                   |
| `query.filters`      | filter[]   | From Request.                                                   |
| `query.timezone`     | timezone   | From Request.                                                   |
| `columns`            | column[]   | Array of column information                                     |
| `column.name`        | string     | Name of metric or dimension column.                             |
| `column.column_type` | string     | ‘metric’ or ‘dimension’                                         |
| `column.data_type`   | string     | Data type of column.                                            |
| `rows`               | values[][] | Array of row arrays containing the dimension and metric values. |

### Response Schema
```js
{
  "id": string,
  "query": {
    "metrics": [string],
    "interval": duration,
    "start_date": datetime,
    "end_date": datetime,
    "dimensions": [string],
    "filters": [
      {
        "name": string,
        "values": [string]
      }
    ]
  },
  "columns": [
    {
      "name": string,
      "column_type": string,
      "data_type": string
    }
  ],
  "rows": [
    [string | number]
  ]
}
```

### Example
#### Request
```js
POST /metrics
{
  "metrics": ["dockless.utilization.avg","trips.count"],
  "interval": "P1D",
  "start_date": "2019-10-21T00:00-07",
  "end_date": "2019-10-28T00:00-07",
  "dimensions": ["vehicle_type"]
}
```
#### Reponse
```json
{
  "id": "44428624-186b-4fc3-a7fb-124f487464a1",
  "query": {
    "interval": "P1D",
    "start_date": "2019-10-21T00:00-07",
    "end_date": "2019-10-28T00:00-07",
    "metrics": [
      "dockless.utilization.avg",
      "trips.count"
    ],
    "dimensions": ["vehicle_type"],
    "filters": []
  },
  "columns": [
    {
      "name": "interval_start",
      "column_type": "dimension",
      "data_type": "datetime"
    },
    {
      "name": "vehicle_type",
      "column_type": "dimension",
      "data_type": "string"
    },
    {
      "name": "dockless.utilization.avg",
      "column_type": "metric",
      "data_type": "float"
    },
    {
      "name": "trips.count",
      "column_type": "metric",
      "data_type": "integer"
    }
  ],
  "rows": [
    ["2019-10-21T00:00-07", "bicycle", 0.09, 69],
    ["2019-10-22T00:00-07", "bicycle", 0.02, 114],
    ["2019-10-23T00:00-07", "bicycle", 0.04, 46],
    ["2019-10-24T00:00-07", "bicycle", 0, 36],
    ["2019-10-25T00:00-07", "bicycle", 0.01, 0],
    ["2019-10-26T00:00-07", "bicycle", 0.02, 10967],
    ["2019-10-27T00:00-07", "bicycle", 0.55, 25271],
    ["2019-10-21T00:00-07", "scooter", 0.09, 69],
    ["2019-10-22T00:00-07", "scooter", 0.02, 114],
    ["2019-10-23T00:00-07", "scooter", 0.04, 46],
    ["2019-10-24T00:00-07", "scooter", 0, 36],
    ["2019-10-25T00:00-07", "scooter", 0.01, 0],
    ["2019-10-26T00:00-07", "scooter", 0.02, 10967],
    ["2019-10-27T00:00-07", "scooter", 0.55, 25271]
  ]
}
```
