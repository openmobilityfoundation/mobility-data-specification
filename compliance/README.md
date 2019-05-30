# Mobility Data Specification: ** Compliance **

## Table of Contents

...

## Background

The Agency API is a fleet-data-intake mechanism (and for the moment, a source of geography from `/service_areas`). The Policy API expresses policy in a machine-readable fashion. For cities and providers to execute policies against fleet data, geographies, and policies, a Compliance API is required.

## Compliance Requirements

...

## Compliance Use-Cases

...

## Compliance Goals

### Provider Compliance

Many Policies require no global information, only data that is available to a provider (e.g. speed limits). Having Providers compute their own compliance status for these cases is desirable so as to prevent round-trip API calls to the city. However, the city must also compute compliance, for enforcement purposes. If the provider does not wish to compute this on their own, they can rely entirely on the city's computation.

### Global Compliance

Certain types of policy will be global across providerrs, e.g., instead of a per-provider fleet cap, a city might stipulate "the sum total of all permitted devices downtown may not exceed 2,000". This type of policy compliance cannot be computed without access to (anonymized) global knowledge. The compliance API will be required to provide whatever global state is needed, and the specific Policy will provide the paths to such endpoint(s). See the [Policy API](../policy/readme.md) for examples of such policies.

### Active Management

Some policies may be impractical or impossible to express in terms of _either_ provider-specific compliance or global-anonymous-information compliance. For cases such as these, the Policy will express "the provider _must_ submit certain types of events (with telemetry) to this endpoint for approval". E.g. "Is it okay if I end this trip at this location?"

## Compliance Architecture

...

## Compliance Endpoints

_GET /compliance/snapshot?timestamp=nnn_
