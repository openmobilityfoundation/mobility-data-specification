# Geography Examples

This file presents a series of example [Geography documents](/geography) to use as templates.

## Table of Contents

- [Municipal Boundary](#municipal-boundary)
- [Operating Area](#operating-area)

## Municipal Boundary

This Geography shows the muncipal boundaries of a regulating entity, which may be larger than the permitted operating area. 

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

This Geography shows the boundaries of a city's operating area for provider devices. 

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


