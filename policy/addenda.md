# Mobility Data Specification: Policy (Addenda)

Notes about intent and interpretation of MDS Policy that are not part of the specification

- Authors: LADOT
- Date: 05 October 2019
- Version: beta

## Table of Contents

- [Authoring](#authoring)
- [Compliance](#compliance)
- [Rule Ordering](#rule-ordering)
- [Rule Evaluation](#rule-evaluation)

<a name="authoring"></a>

## Authoring

Creating, editing, and publishing policies may be performed via a variety of mechanisms, and are therefore not included in the Policy spec. Authoring tools would optionally provide schema extensions for tooling, including author, Provider-specificity, etc. We may add a specific instance of such extensions in a later revision of this document, but at present that’s TBD.

One mechanism may be via a source-control repository, where pull-requests to Policy objects are proposed, left open to public commentary, etc., and served as static content via flat files or the endpoints listed above.

Another possibility would be a policy-editing REST API, where drafts of Policy objects are mutable, pending publication. This would be the API for manual policy-creation with GUI tooling. LADOT will propose a specific policy-editing API in the future.

Certain policies could be fully dynamic, e.g. caps could be raised and lowered via algorithm on a day-to-day or even hour-to-hour basis. No-fly-zones could be created in quasi-real-time in response to emergencies or road-closures.

Dynamic caps can also be implemented by replacing the “maximum” integer with a URL to a source for dynamic data. This could be for provider-specific caps that go up and down, or for global caps e.g. “total 500 scooters at the coliseum”. Dynamic data sources would be required to have historical data so that validating prior information, and downloaded dynamic data would have a time-to-live.

<a name="compliance"></a>

## Compliance

A Compliance API will be described in a separate MDS specification. In brief, it will take as inputs the a snapshot of the MDS status at a particular time, the MDS geography data, and these MDS Policy objects and emit Compliance JSON measurements. MDS status can be generated from either Provider or Agency data.  This work is in draft form but is closely informed by the Policy specification.

<a name="rule-ordering"></a>

## Rule Ordering

Rules, being in a list, are implicitly ordered according to the JSON Specification. Rules are a very specific form of pattern matching; you specify the conditions for which a given rule is 'met', and a vehicle (or series of vehicles) may match with that specific rule. If a vehicle is matched with a rule, then it _will not_ be considered in the subsequent evaluation of rules within a given policy. This allows for expressing complex policies, such as a layer of 'valid' geographies in an earlier rule, with overarching 'invalid' geographies in later rules: see [LADOT Venice Beach Special Operations Example](./Examples.md#venice-beach-spec-ops)

<a name="rule-evaluation"></a>

## Rule Evaluation

The below example is intended to highlight the bucketing mechanisms of rule evaluation, and should not be considered a fully-fledged pseudocode representation of how to evaluate a policy. This is specifically for count maximum rules; evaluation for other rule types will be explained as part of the Compliance API.

```
let p = Policy object
let rules = p.rules
let S = set of vehicles to consider (e.g. all vehicles for a specific provider)

eval(rules, S) {
    let exclude = [] // Empty set
    let matched_not_bucketed = [] // Empty set
    for rule in rules {
        let result = eval_rule(rule, S \ exclude)
        let matched_vehicles = all (violation_vehicle || violation_vehicles) in result
        let bucketed_vehicles = matched_vehicles(accumulator, vehicle => {
            if (accumulator.length < rule.maximum) {
                accumulator.add(vehicle)
            }
        })
        matched_not_bucketed.add(matched_vehicles \ bucketed_vehicles)
        exclude.add(bucketed_vehicles)
        ...
    }
    ...
}
...
```
