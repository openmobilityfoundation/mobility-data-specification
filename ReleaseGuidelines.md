# MDS Release Guidelines

MDS will see regular updates and new [releases][mds-releases]. This document describes the general guidelines around how and when a new release is cut.

## Table of Contents

* [Versioning](#versioning)
* [Release Process](#process)
  * [Goals](#goals)
  * [Roles](#roles)
  * [Schedule](#schedule)
  * [Communication and Workflow](#communication-and-workflow)
* [Branch Mechanics](#branch-mechanics)
* [Checklist](#release-checklist)

## Versioning

MDS uses [Semantic Versioning][semver]. Each release is associated with a [`git tag`][mds-tags] of the form `X.Y.Z`.

Given that MDS is stabilizing under MAJOR version `0.x` right now, it should be assumed that MINOR version increments (e.g. `0.2.0` to `0.3.0`) are equivalent to MAJOR version increments and may contain breaking changes.

### Breaking vs. non-breaking changes

Since MDS is used by a broad ecosystem of both API consumers and implementers, it needs a strict definition of what changes are “non-breaking” and are therefore allowed in PATCH releases.

In the MDS spec, a breaking change is any change that requires either consumers or implementers to modify their code for it to continue to function correctly.

Examples of breaking changes include:

* Adding or removing a required endpoint or field
* Adding or removing a request parameter
* Changing the data type or semantics of an existing field, including clarifying previously-ambiguous requirements

Examples of non-breaking changes include:

* Adding or removing an optional endpoint or field
* Adding or removing enum values
* Modifying documentation or spec language that doesn't affect the behavior of the API directly

One implication of this policy is that clients should be prepared to ignore the presence of unexpected fields in responses and unexpected values for enums. This is necessary to preserve compatibility between PATCH versions within the same MINOR version range, since optional fields and enum values can be added as non-breaking changes.

### Ongoing version support

At this early stage, MDS will be moving relatively quickly with an eye toward stabilization rather than backwards-compatibility.

For now, MDS will maintain *two concurrent (MINOR) versions* (e.g. if `0.3.0` were the current version, the `0.2.x` series would continue to receive maintenance in addition to `0.3.x`).


## Release Process
The sections below define the release process itself, including timeline, roles, and communication best practices.

> **The process defined below currently being piloted with the MDS `provider` API only. Proposed changes to the `agency` API will be continue to be reviewed on an ad hoc basis.**

>**It is our intent to maintain a level of coordination between the technical direction of `agency` and `provider`. As such, proposed changes to either API will be reviewed to ensure they do not create unnecessary duplicative functionality, introduce confusion about which API should be used for a given purpose, or prevent the reconciliation of data between the two APIs (for example: using data from `provider` to cross-validate data received via `agency`).**

### Goals

* _Fast, regular releases to support rapid evolution of MDS_

* _Consensus-oriented with clear decision making process when consensus can't be reached_

* _Encourage involvement from all stakeholders, especially public agencies_

* _Frequent stakeholder communication on GitHub, web conference, and in-person_

* _Regular review of release process to ensure it is serving the needs of the community._


### Roles
* **contributors** - Anyone making pull requests, opening issues, or engaging in technical discussion around implementation of features.
* **maintainers** - Project maintainers have commit privileges in the main MDS repository and are responsible for implementing changes such as merging of pull requests and the creation of release branches.
* **release partner** - Review changes when consensus cannot be reached and make final release inclusion recommendations to maintainers for approval.

As of March 2019, LADOT and the City of Santa Monica are the project maintainers and Remix is the release partner.

### Schedule

MDS operates on a six-week release cycle for both major updates (0.x) and patches (0.x.y). In general, major updates (0.x) are expected no more than once per quarter. The release cycle is broken down as follows:

**week 1 - proposals**

Contributors submit proposals for inclusion in the release cycle in the form of pull requests and issues tagged. If known, note what release you intended a proposal for in its description. Maintainers will tag appropriate pull requests and issues with the Milestone for the upcoming release. Proposals should come with enough explanation to allow all stakeholders to understand intent and implementation strategy.

**weeks 2-4 - consensus building, refinement, and implementation**

Contributors will provide feedback on proposals. Where possible, discussion will happen via GitHub. Weekly calls will support dialog around more complex or controversial issues. By the end of week 4, all active proposals must be in the form of a pull request. Proposals can be withdrawn or split apart for inclusion in future releases.

**week 5 - decision making**

The week will start with an in-person/web conference work session for all contributors to review and discuss current proposals. Goal is to achieve consensus where possible, or to clearly articulate areas of disagreement where not. Minor changes may be accepted at this stage if they bring contributors to consensus.

At the conclusion of week 5, the release partner will review all items for which consensus was not reached and provide a recommended release plan to maintainers for approval. Any remaining approved pull requests will be merged, and a maintainer or release partner will open a pull request containing release notes for the proposed release.

**week 6 - release**

Documentation will be updated, release notes will be merged, a tag will be created and `master` updated to point to it, and the new version will be formally released. See [Release Checklist](#release-checklist) for details about the release process.

### Communication and Workflow
The release announcements and process schedule will be communicated via [`mds-announce`][mds-announce] Google Group. People wishing to stay informed should join the group for updates. Timing of web conference and in person work sessions will be communicated via mds-announce as well.

The following best practices are intended to create clarity around each release cycle:

* Categorize issues and PRs under an associated [Milestone][mds-milestones] for the release

* Assign a due date for said Milestone that aligns with proposed release date

* Pull requests and release notes should include a summary of the major changes / impacts associated with the change or release

* Proposed changes should come in the form of PRs to give the community ample awareness and time for feedback

## Branch Mechanics

The branching strategy we describe here is intended to handle ongoing maintenance changes in parallel with features for new releases.

### Primary branches

At a high-level, there are two primary branches:

* [`master`][mds-master] represents the latest release of MDS. It's only updated as part of the release process, and no pull requests should be based on or target it.

* [`dev`][mds-dev] contains all work that has happened since the last release, including both breaking and non-breaking changes.

### Feature branches

All development on changes to MDS should happen in branches cut from `dev` (with the exception of hotfixes to release branches, described below). When your work is ready for review, submit a PR against `dev`, ideally with any merge conflicts already resolved. `dev` serves as the collection point for all new feature work.

### Release branches

Whenever a MINOR version is released, a **release branch** will be created from `dev` to track any changes that should be included in subsequent PATCH versions. For example, at the time `0.4.0` is released, a branch called `0.4.x` will be created that initially points to the same commit as the `0.4.0` tag.

Release branches can be updated in two ways:

* When a non-breaking change has been merged to `dev`, a maintainer will usually [backport](#backporting-changes) it onto the newest release branch. This can be skipped if the change isn't relevant to the release branch (e.g., because it modifies language that was added after the last MINOR release) or if there are no plans to make another PATCH release with the same MINOR version.

* If a change needs to be made to spec language that exists in a release branch but is no longer relevant in `dev`, the contributor should create a feature branch based on the release branch and open a PR targeting the release branch directly. For example, if an endpoint was removed in `0.3.0` but needs to be modified for a `0.2.1` PATCH release, the contributor would create a PR based on the `0.2.x` release branch.

As stated earlier, at this time MDS will maintain *two concurrent MINOR versions*. This means that when a MINOR release is made (e.g. `0.4.0`), no further changes will be made to the outgoing series (`0.2.x`, in this case).

### Backporting changes

When non-breaking changes are merged to `dev`, it's generally necessary for a maintainer to backport these changes to the newest release branch so that they'll be included in any subsequent PATCH releases. There are a couple of different ways to do this:

* If the changes can be applied to the release branch without significant editing, the maintainer can use `git cherry-pick` to copy the changes from `dev` into the release branch (assuming the SHA of the merge commit on `dev` was `b70719b`):

  ```console
  git fetch
  git checkout 0.3.x
  git pull
  git cherry-pick -m 1 b70719b
  git push
  ```

  Note that the `-m 1` option is unnecessary if the PR was merged with the "Squash and merge" option instead of creating a merge commit.

* If backporting the change needs significant manual work (for example, if there were other changes to the relevant part of the spec in the last MINOR version), the maintainer can open a new PR for the backport targeting the relevant release branch.

  First, create a branch containing the backported change (again, assuming the SHA of the merge commit was `b70719b`):

  ```console
  git fetch
  git checkout 0.3.x
  git pull
  git checkout -b backport-helpful-change-to-0.3.x
  git cherry-pick -m 1 b70719b
  # Do any manual work needed to integrate the changes
  git push -u origin backport-helpful-change-to-0.3.x
  ```

  Next, create a PR with the release branch (in this case, `0.3.x`) as its `base`. Once that PR has been approved, merge the PR into the release branch as usual.


## Release Checklist

The following steps **must** be followed for **every** release of MDS:

1. Ensure the [Milestone][mds-milestones] for this release is at `100%`.

1. Update the [schema version regex][mds-schema-common].

1. Run the schema generator to ensure the schema files are up to date:

   ```console
   cd generate_schema/
   pipenv run python generate_provider_schema.py
   ```

1. [Open a PR][mds-pr-new] against `dev` that updates [`ReleaseNotes.md`](ReleaseNotes.md) using the following format:

    ```md
    ## 1.2.3

    > Released yyyy-MM-dd

    High level summary of the release.

    * Specific change referencing a PR [#555](https://github.com/CityofLosAngeles/mobility-data-specification/pull/555)

    * Another change summary referencing a PR [#777](https://github.com/CityofLosAngeles/mobility-data-specification/pull/777)
    ```

    The description of this PR should include a link to a GitHub compare page showing the changes that will be included in the release. This URL depends on the type of release:

    * For a PATCH release like 0.4.2, compare the previous version in the series to the current state of the release branch: https://github.com/CityOfLosAngeles/mobility-data-specification/compare/0.4.1...0.4.x

    * For a MINOR release like 0.5.0, compare the last release in the previous series to the current state of `dev`: https://github.com/CityOfLosAngeles/mobility-data-specification/compare/master...dev

    In the case of a new MINOR version, allow a minimum of 24 hours for community discussion and review of the current state of the release.

1. Once the PR has been sufficiently reviewed, merge it into `dev`.

1. Create a tag for this release on the tip of `dev` (for MINOR versions) or the relevant release branch (for PATCH versions). For example, for `0.5.0`:

    ```console
    git fetch
    git checkout origin/dev
    git tag 0.5.0
    git push --tags
    ```

    Or for `0.4.2`:

    ```console
    git fetch
    git checkout origin/0.4.x
    git tag 0.4.2
    git push --tags
    ```

1. If this release is a MINOR version, create a new [release branch](#release-branches). For example, if you've just created the `0.5.0` tag:

    ```console
    git push origin 0.5.0:0.5.x
    ```

1. Unless this is a maintenance release on an older branch (for example, releasing `0.3.2` after `0.4.0` has already come out), update `master` to point to the new tag:

    ```console
    git checkout master
    git reset --hard 0.5.0
    git push --force origin master
    ```

1. Publish a [new Release in GitHub][mds-releases-new] for the tag you just pushed. Copy in the [release notes](ReleaseNotes.md) created earlier.

1. Post a release announcement to [`mds-announce`](mailto:mds-announce@googlegroups.com), copying the [release notes](ReleaseNotes.md) created earlier and linking to the [GitHub release][mds-releases].

    ```email
    From:    mds-announce@googlegroups.com  
    To:      mds-announce@googlegroups.com  
    Subject: MDS 1.2.3 Release  

    MDS 1.2.3 has been released.

    <release notes>

    <link to GitHub release>
    ```

[mds-announce]: https://groups.google.com/forum/#!forum/mds-announce
[mds-dev]: https://github.com/CityOfLosAngeles/mobility-data-specification/tree/dev
[mds-master]: https://github.com/CityOfLosAngeles/mobility-data-specification/tree/master
[mds-milestones]: https://github.com/CityOfLosAngeles/mobility-data-specification/milestones
[mds-pr]: https://github.com/CityofLosAngeles/mobility-data-specification/pulls
[mds-pr-new]: https://github.com/CityOfLosAngeles/mobility-data-specification/compare
[mds-releases]: https://github.com/CityOfLosAngeles/mobility-data-specification/releases
[mds-releases-new]: https://github.com/CityOfLosAngeles/mobility-data-specification/releases/new
[mds-schema-common]: https://github.com/CityOfLosAngeles/mobility-data-specification/blob/master/generate_schema/common.json
[mds-tags]: https://github.com/CityOfLosAngeles/mobility-data-specification/tags
[semver]: https://semver.org/
