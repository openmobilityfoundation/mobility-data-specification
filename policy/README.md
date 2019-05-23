# Mobility Data Specification: Policy

This specification contains a collection of RESTful APIs used to specify the digital relationship between *mobility as a service* Providers and the Agencies that regulate them.

* Authors: LADOT
* Date: 15 May 2019
* Version: alpha

## Table of Contents
* [Audience](#audience)
* [Background](#background)
* [Distribution](#distribution)
* [Schema](#schema)
* [Endpoints](#endpoints)
* [Authoring](#authoring)
* [Compliance](#compliance)
* [Open Topics](#open-topics)
* [Examples](#examples)

<a name="audience"></a>
## Audience

There are three intended audiences of this API: 

1. Agencies, as consumers in the form of automated compliance measurement, and as creators of policy
2. Providers, so that they can measure their compliance status independently
3. Tooling companies that want to create applications for policy-creation and editing

<a name="background"></a>
##Background

The goal of this specificiation is to enable Agencies to create, revise, and publish machine-readable micromobility policy, as set of rules for individual and collective micromobility device behavior exhibited by both providers and riders. Examples of policies include:

* City-wide and localized caps (e.g. “Minimum 500 and maximum 3000 scooters within city boundaries”)
* Exclusion zones (e.g. “No scooters are permitted in this district on weekends”)
* Cap allowances (e.g. “Up to 500 additional scooters are permitted near train stations”)
* Speed-limit restrictions (e.g. “15 mph outside of downtown, 10 mph downtown”)
* Idle-time and disabled-time limitations (e.g. “5 days idle while rentable, 12 hours idle while unrentable, per device”)

A machine-readable format will allow Providers to download policies and compute compliance for policies where it can be determined entirely by data obtained internally.  Providers can then continually measure their own compliance against policies without further API calls.

References to geography (areas, street segments, etc.) will be done via UUID.  Geographic data will be available as GeoJSON via the `/geographies` endpoint.  In a future revision of Agency, we will reconcile this with the existing `/service_areas` endpoint.  `/service_areas` currently only handles GeoJSON MultiPolygon and Polygon objects, and Policies might refer to street segments or points.  

This initial draft proposes a subset of possible policies for consideration, and should not be taken to be the a comprehensive enumeration of all possible policies.

<a name="distribution"></a>
## Distribution

Policies may be published by Agencies or their authorized delegates via JSON objects.

Each policy will have a unique ID (UUID).

Published policies should be treated as immutable data.  Obsoleting or otherwise changing policies is accomplished by publishing additional policies with a field named “prev_policies”, a list of UUID references to the previous policy or policies.  

Policies should be stored and accessible indefinitely so that the set of active policies at a given time in the past can be retrieved from the `/policies` endpoint.

Policies will typically be linked to one or more associated geographies.  Geography descriptions (e.g. geofences or lists of street segments) must also be maintained by the Agency indefinitely.  Policies without specific geographies (global policies) are assumed to apply to the entire service area managed by the Agency.

Policies should be re-fetched whenever (a) a Policy expires, or (b) at an interval specified by the Agency.


<a name="schema"></a>
## Schema

<a name="policy-fields"></a>
### Policy Fields

| Name            | Type      | R/O | Description |
| ---             | ---       | --- | --- |
| `name`          | String    | R   | Name of policy |
| `policy_id`     | UUID      | R   | Unique ID of policy |
| `description`   | String    | R   | Description of policy |
| `start_date`    | timestamp | R   | Beginning date/time of policy enforcement |
| `end_date`      | timestamp | O   | End date/time of policy enforcement |
| `prev_policies` | UUID[]    | O   | Unique IDs of prior policies replaced by this one |
| `rules`         | Rule[]    | R   | List of applicable rule elements (see [“rule fields”](#rule-fields)) |

Note that the provider-scope is at present not included.  A Provider should not be able to tell whether the policy is specific to them, or to a subset of Provider, or all Providers.

<a name="rule-types"></a>
### Rule Types 

| Name    | Description |
| ---     | --- |
| `count` | Fleet counts based on regions.  Rule max/min refers to number of devices. |
| `time`  | Individual limitations on time spent in one or more vehicle-states.  Rule max/min refers to number of minutes. |
| `speed` | Global or local speed limits.  Rule max/min refers to miles per hour. |
| `user`  | Information for users, e.g. about helmet laws.  Generally can't be enforced via events and telemetry. |

<a name="rule-units"></a>
### Rule Units 

| Name      | Description |
| ---       | --- |
| `seconds` | Seconds |
| `minutes` | Minutes |
| `hours`   | Hours |
| `mph`     | Miles per hour |
| `kph`     | Kilometers per hour |

<a name="rule-fields"></a>
### Rule Fields 

| Name         | Type     | R/O | Description      |
| ---          | ---      | --- | ---              |
| `name`       | String   | R   | Name of cap item |
| `rule_type`  | enum     | R   | Type of policy (see [“policy types”](#policy-types))|
| `rule_units` | enum     | O   | Measured units of policy (see [“policy units”](#policy-units))|
| `geographies`| UUID[]   | R   | List of Geography UUIDs (non-overlapping) specifying the covered geography |
| `statuses`   | Status[] | R   | Vehicle `status` to which this rule applies.  See [MDS Agency state diagram](https://github.com/CityOfLosAngeles/mobility-data-specification/blob/dev/agency/README.md#vehicle-events). |
| `vehicle_types` | VehicleType[] | O | Applicable vehicle categories, default “all”.  See MDS shared data types document.  (link forthcoming) |
| `minimum`    | integer | O | Minimum value, if applicable (default 0) |
| `maximum`    | integer | O | Maximum value, if applicable (default unlimited) |
| `start_time` | time    | O | Beginning time-of-day (hh:mm:ss) when the rule is in effect (default 00:00:00) |
| `end_time`   | time    | O | Ending time-of-day (hh:mm:ss) when the rule is in effect (default 23:59:59) |
| `days`       | day[]   | O | Days `["sun", "mon", "tue", "wed", "thu", "fri", "sat"]` when the rule is in effect (default all) |
| `messages`   | { string:string } | O | Message to rider user, if desired, in various languages, keyed by language tag (see [Messages](#messages))|
| `value_url ` | URL     | O | URL to an API endpoint that can provide dynamic information for the measured value (see [Value URL](#value-url)) |

### Order of Operations

Rules are ordered most-specific to most-general.  E.g. an “earlier” cap rule would take precedence over a “later” cap rule.  The internal mechanics of ordering are up to the Policy editing and hosting software.

<a name="messages"></a>
### Messages

Some Policies as established by the Agency may benefit from rider communication.  This optional field contains a map of languages to be (optionally?) shown to the user.  (Unanswered question: shown with what frequency?  At sign-up?  Once per day?)

Language tag values will be per [BCP 47](https://www.rfc-editor.org/rfc/bcp/bcp47.txt).

Example for a decreased speed-limit rule for Venice Beach on weekends:

```
	"messages": {
	            "en-US": "Remember to stay under 10 MPH on Venice Beach on weekends!”,
	            "es-US": "¡Recuerda permanecer menos de 10 millas por hora en Venice Beach los fines de semana!"
	        },
```

<a name="value-url"></a>
### Value URL

An Agency may wish to provide dynamic or global rules, e.g. "Within 300 yards of the stadium, 1000 total extra scooters may be deployed, across all Provider(s)."  In this case, compliance is not computable from the information available to a single Provider.  The Agency would provide a specified endpoint to get the current count of vehicles in the service-area, so that individual Providers could decide whether adding some number to those present can be done.  

There are potential complexities that are as-yet unaddressed, such as the latency between a Provider deciding to enter such an area, and the number of vehicles in the area when the scooters arrive.  As this specification is Alpha, feedback and refinements are welcome.

The payload returned from a GET call to the `value_url` will have the following immutable fields:

| Name         | Type      | R/O | Description |
| ----         | ----      | --- | ----------- |
| `value`      | integer   | R   | Value of whatever the rule measures |
| `timestamp`  | timestamp | R   | Timestamp the value was recorded |
| `policy_id`  | UUID      | R   | Relevant `policy_id` for reference |

MDS will likely include some sort of streaming mechanism in the upcoming releases that may supplant or replace this mechanism.

<a name="endpoints"></a>
## Endpoints

The provider-facing Policy API consists of the following two endpoints.

`GET /policies`

Parameters:

| Name         | Type      | R/O | Description |
| ----         | ----      | --- | ----------- |
| `start_time` | timestamp | O   | Earliest effective date, default=effective now |
| `end_time`   | timestamp | O   | Latest effective date, default=all future |

Note: provider_id is an implicit parameter and will be encoded in the authentication key

Returns: List of policy objects effective during the timespan described by greater than or equal to `start_time` and less than or equal to `end_time`

Policies will be returned in order of effective date (see Policy Schema, below), with pagination as in Agency or Provider.

`GET /policies/{id}`

Returns: One policy object whose id is `id`

Parameters: none

`GET /geographies/{id}`

Returns: One immutable GeoJSON FeatureCollection with an embedded UUID identifier property of `id`

Parameters: none

Note: Intentionally omitted `GET /geographies` until a compelling use-case can be identified.
 
<a name="authoring"></a>
## Authoring

Creating, editing, and publishing policies may be performed via a variety of mechanisms, and are therefore not specified here.  Authoring tools would optionally provide schema extensions for tooling, including author, Provider-specificity, etc.  We may add a specific instance of such extensions in a later revision of this document, but at present that’s TBD.

One mechanism may be via a source-control repository, where pull-requests to Policy objects are proposed, left open to public commentary, etc., and served as static content via the endpoints listed above.

Another possibility would be a policy-editing REST API, where drafts of Policy objects are mutable, pending publication.  This would be the API for manual policy-creation with GUI tooling.  LADOT may propose a specific separate policy-editing API in the future.

Certain policies could be fully dynamic, e.g. caps could be raised and lowered via algorithm on a day-to-day or even hour-to-hour basis.  No-fly-zones could be created in quasi-real-time in response to emergencies or road-closures. 

Dynamic caps can also be implemented by replacing the “maximum” integer with a URL to a source for dynamic data.  This could be for provider-specific caps that go up and down, or for global caps e.g. “total 500 scooters at the coliseum”.  Dynamic data sources would be required to have historical data so that validating prior information, and downloaded dynamic data would have a time-to-live.

<a name="compliance"></a>
## Compliance

A Compliance API will be described in a separate MDS specification.  In brief, it will take as inputs the MDS Agency data stream, the MDS geography data, and these MDS Policy objects and emit Compliance objects.  This work is in draft form but is closely informed by this Policy specification.

<a name="examples"></a>
## Examples

List of no policies as returned from `/policies`

```
{
    "policies": []
}
```

TODO add parking example that mixes time/count

Cap management in Los Angeles. One Policy object.  Greater LA has a cap of 3000, with an additional 5000 vehicles permitted in the San Fernando Valley DAC areas, and 2500 in the non-SFV DAC areas.  The statuses shown here are the "in the public right-of-way" statuses.

```
{
    "id": "f3c5a65d-fd85-463e-9564-fc95ea473f7d",
    "name": "Mobility Caps",
    "desc": "LADOT Mobility caps as described in the One-Year Permit",
    "type": "count",
    "start_date": 1552678594428,
    "end_date": null, 
    "prev_policy": null,
    "rules": [{
        "name": "Greater LA",
        "geographies": ["b4bcc213-4888-48ce-a33d-4dd6c3384bda"],
        "statuses": ["available", "unavailable", "reserved", "trip"],
        "vehicle_types": ["bicycle", "scooter"],
        "maximum": 3000,
        "minimum": 500
    }, {
        "name": "San Fernando Valley DAC",
        "geographies": ["ec551174-f324-4251-bfed-28d9f3f473fc"],
        "statuses": ["available", "unavailable", "reserved", "trip"],
        "vehicle_types": ["bicycle", "scooter"],
        "maximum": 5000
    }, {
        "name": "Non San Fernando Valley DAC",
        "geographies": ["4c2015c6-6702-48a6-ab58-94d963911182"],
        "statuses": ["available", "unavailable", "reserved", "trip"],
        "vehicle_types": ["bicycle", "scooter"],
        "maximum": 2500
    }]
}
```

Idle time limits example:

```
{
    "id": "a2c9a65f-fd85-463e-9564-fc95ea473f7d",
    "name": "Idle Times",
    "desc": "LADOT Idle Time Limitations",
    "type": "time",
    "effective": 1552678594428,
    "ends": null,
    "supersedes": null,
    "rules": [{
        "name": "Greater LA (rentable)",
        "geographies": ["b4bcc213-4888-48ce-a33d-4dd6c3384bda"],
        "statuses": ["available", "reserved"],
        "vehicle_types": ["bicycle", "scooter"],
        "maximum": 7200
    }, {
        "name": "Greater LA (non-rentable)",
        "geographies": ["12b3fcf5-22af-4b0d-a169-ac7ac903d3b9"],
        "statuses": ["unavailable", "trip"],
        "vehicle_types": ["bicycle", "scooter"],
        "limit": 720
    }]
}
```

Speed limits

```
{
    "id": "95645117-fd85-463e-a2c9-fc95ea47463e",
    "name": "Speed Limits",
    "desc": "LADOT Pilot Speed Limit Limitations",
    "type": "speed",
    "effective": 1552678594428,
    "ends": null,
    "supersedes": null,
    "rules": [{
        "name": "Greater LA",
        "geographies": ["b4bcc213-4888-48ce-a33d-4dd6c3384bda"],
        "states": ["trip"],
        "vehicle_types": ["bicycle", "scooter"],
        "maximum": 15
    }, {
        "name": "Venice Beach on weekend afternoons",
        "geographies": ["ec551174-f324-4251-bfed-28d9f3f473fc"],
        "states": ["trip"],
        "vehicle_types": ["bicycle", "scooter"],
        "days": ["sat", "sun"],
        "start_time": "12:00",
        "end_time": "23:59",
        "maximum": 10,
        "messages": {
            "en-US": "Remember to stay under 10 MPH on Venice Beach on weekends!”,
            "es-US": "¡Recuerda permanecer menos de 10 millas por hora en Venice Beach los fines de semana!"
        },
    }]
}
```

More examples coming
