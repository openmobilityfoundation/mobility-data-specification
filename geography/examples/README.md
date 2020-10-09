# Geography Examples

This file presents a series of example [Geography documents](/geography) to use as templates.

## Table of Contents

- [Municipal Boundary](#municipal-boundary)
- [Operating Area](#operating-area)
- [Distribution Zone](#distribution-zone)
- [No Ride Zone](#no-ride-zone)
- [Slow Ride Zone](#slow-ride-zone)

## Municipal Boundary

Shows the muncipal boundaries of a regulating entity, which may be larger than the permitted operating area. 

**File with full geometry**: [`municipal-boundary.json`](municipal-boundary.json)

**GeoJSON part of file with preview**: [`municipal-boundary.geojson`](municipal-boundary.geojson)

```json
{
  "version": "1.0.0",
	"geography": {
		"geography_id": "e00535dd-d8ff-4b1b-920d-34e7404d0208",
		"geography_type": "municipal_boundary",
		"name": "Municipal Boundary",
		"description": "Full municipal jurisdiction for the combined city/county",
		"effective_date": 1570034561834,
		"publish_date": 1570035222868,
		"prev_geographies": [
			"40d78c83-493f-40ad-8aba-a1ef036c5ffa"
		],
    "geography_json": MUNICIPAL_BOUNDARY_GEOGRAPHY
  } 
}
```

[Top](#table-of-contents)

## Operating Area

Boundaries of a city's permitted operating area for provider vehicles. 

**File with full geometry**: [`operating-area.json`](operating-area.json)

**GeoJSON part of file with preview**: [`operating-area.geojson`](operating-area.geojson)

```json
{
  "version": "1.0.0",
  "geography": {
    "geography_id": "8ad39dc3-005b-4348-9d61-c830c54c161b",
    "geography_type": "operating_area",
    "name": "Operating Area",
    "description": "Municipal permitted operating area for devices",
    "effective_date": 1570034561834,
    "publish_date": 1570035222868,
    "prev_geographies": [
      "6100b029-a943-439c-b344-72bcc8e78d15",
      "5ce17f69-d869-4103-b414-9f213fd6347d"
    ],
    "geography_json": OPERATING_AREA_GEOGRAPHY
  } 
}
```

[Top](#table-of-contents)

## Distribution Zone

Boundaries of one of 9 areas in a city where vehicles can be distibuted and reblananced. 

**File with full geometry**: [`distribution-zone-8.json`](distribution-zone.json)

**GeoJSON part of file with preview**: [`distribution-zone-8.geojson`](distribution-zone.geojson)

```json
{
  "version": "1.0.0",
  "geography": {
    "geography_id": "70a91abc-0d9f-43a9-8e6a-763142dc6c94",
    "geography_type": "distribution_zone",
    "name": "Distribution Zone #8",
    "description": "Distribution area for reblancing vehicles. One of 9 zones in the city.",
    "effective_date": 1570034561834,
    "publish_date": 1570035222868,
    "prev_geographies": [
      "036e9c50-ae67-4135-a9e1-31df1f76f4a2",
      "3198dd92-749f-48e9-93ff-dd6ef4ec4149",
      "ba5ed96c-3d64-4bf7-a3ad-5e1b9fae5841"
    ],
    "geography_json": DISTRIBUTION_ZONE_GEOGRAPHY
  } 
}
```

[Top](#table-of-contents)

## No Ride Zone

Boundaries of areas in a city where vehicles are not allowed be ridden by riders. 

**File with full geometry**: [`no-ride-zone.json`](no-ride-zone.json)

**GeoJSON part of file with preview**: [`no-ride-zone.geojson`](no-ride-zone.geojson)

```json
{
  "version": "1.0.0",
  "geography": {
    "geography_id": "fc277865-79d3-4f0e-8459-53e9a647db99",
    "geography_type": "slow_ride_zone",
    "name": "Slow Ride Zones",
    "description": "Areas where vehicles are to be ridden at a reduced top speed",
    "effective_date": 1570034561834,
    "publish_date": 1570035222868,
    "geography_json": NO_RIDE_ZONE_GEOGRAPHY
  } 
}
```

[Top](#table-of-contents)

## Slow Ride Zone

Boundaries of areas in a city where vehicles are to be ridden at a slower top speed than what is allowed in the rest of the operating area.

**File with full geometry**: [`slow-ride-zone.json`](slow-ride-zone.json)

**GeoJSON part of file with preview**: [`slow-ride-zone.geojson`](slow-ride-zone.geojson)

```json
{
  "version": "1.0.0",
  "geography": {
    "geography_id": "8ad39dc3-005b-4348-9d61-c830c54c161b",
    "geography_type": "operating_area",
    "name": "Operating Area",
    "description": "Municipal permitted operating area for devices",
    "effective_date": 1570034561834,
    "publish_date": 1570035222868,
    "prev_geographies": [
      "6100b029-a943-439c-b344-72bcc8e78d15",
      "5ce17f69-d869-4103-b414-9f213fd6347d"
    ],
    "geography_json": SLOW_RIDE_ZONE_GEOGRAPHY
  } 
}
```

[Top](#table-of-contents)

