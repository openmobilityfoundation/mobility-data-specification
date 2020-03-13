# Mobility Data Specification: **General information**

This document contains specifications that are shared between the various MDS APIs such as `agency`, `provider` and `policy`.

## Table of Contents

* [Versioning](#versioning)
* [Beta Features](#betafeatures)

## Versioning

MDS APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented through the use of a custom media-type, `application/vnd.mds.provider+json`, combined with a required `version` parameter.

The version parameter specifies the dot-separated combination of major and minor versions from a published version of the specification. For example, the media-type for version `0.2.1` would be specified as `application/vnd.mds.provider+json;version=0.2`

> Note: Normally breaking changes are covered by different major versions in semver notation. However, as this specification is still pre-1.0.0, changes in minor versions may include breaking changes, and therefore are included in the version string.

Clients must specify the version they are targeting through the `Accept` header. For example:

```http
Accept: application/vnd.mds.provider+json;version=0.3
```

> Since versioning was not available from the start, the following APIs provide a fallback version if the `Accept` header is not set as specified above:
> - The `provider` API must respond as if version `0.2` was requested.
> - The `agency` API must respond as if version `0.3` was requested.
> - The `policy` API must respond as if version `0.4` was requested.

If an unsupported or invalid version is requested, the API must respond with a status of `406 Not Acceptable`. If this occurs, a client can explicitly negotiate available versions.

A client negotiates available versions using the `OPTIONS` method to an MDS endpoint. For example, to check if `trips` supports either version `0.2` or `0.3` with a preference for `0.2`, the client would issue the following request:

```http
OPTIONS /trips/ HTTP/1.1
Host: provider.example.com
Accept: application/vnd.mds.provider+json;version=0.2,application/vnd.mds.provider+json;version=0.3;q=0.9
```

The response will include the most preferred supported version in the `Content-Type` header. For example, if only `0.3` is supported:

```http
Content-Type: application/vnd.mds.provider+json;version=0.3
```

The client can use the returned value verbatim as a version request in the `Accept` header.

## Beta Features
In some cases, features within MDS may be marked as "BETA." These are typically newly established endpoints or fields. Because beta features are new, they may not be fully mature and proven in real-world operation. The design of beta features may have undiscovered gaps, ambiguities, or inconsistencies. Implementations of those features are also likely new as well and are more likely to contain bugs or other problems. Beta features are likely to evolve more rapidly than other parts of the specification.

Despite this, MDS users are encouraged to use beta features. New features can only become proven and trusted through use and the learning that comes with it. Users should be thoughtful about the role of beta features in their operations. Beta features are suitable for enabling new tools and analysis, but may not be appropriate for mission-critical regulatory decisions where certainty and reliability are essential.

Users of beta features are strongly encouraged to share their experiences, learnings, and challenges with the broader MDS community via GitHub issues or pull requests. This will help the  community make the improvements that allow beta features to become proven, stable parts of the specification.

[Top](#table-of-contents)
