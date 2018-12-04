# MDS Release Guidelines

MDS will see periodic updates and new [releases][mds-releases] from time to time. This document describes the general guidelines around how and when a new release is cut.

## Table of Contents

* [Versioning](#versioning)
* [Branch Mechanics](#branch-mechanics)
* [Schedule](#schedule)
* [Checklist](#release-checklist)

## Versioning

MDS uses [Semantic Versioning][semver]. Each release is associated with a [`git tag`][mds-tags] of the form `X.Y.Z`.

Given that MDS is stabilizing under MAJOR version `0.x` right now, it should be assumed that MINOR version increments (e.g. `0.2.0` to `0.3.0`) are equivalent to MAJOR version increments and may contain breaking changes.

### Ongoing version support

At this early stage, MDS will be moving relatively quickly with an eye toward stabilization rather than backwards-compatibility.

For now, MDS will maintain *two concurrent (MINOR) versions* (e.g. if `0.3.0` were the current verison, the `0.2.x` series would continue to receive maintenace in addition to `0.3.x`).

## Branch Mechanics

Aside from using `git tags` as mentioned earlier, here we outline a branching strategy to handle ongoing maintenance changes in parallel with features for new releases.

### Primary branches

At a high-level, there are two primary branches:

* [`master`][mds-master] represents the current stable release (i.e. the most recent tag) of MDS. Development work generally *does not* happen here, but is rather merged from elsewhere.

* [`dev`][mds-dev] represents work on the next MINOR release, and is the *long-term* development branch.

### Feature branches

Work on new features for MDS happens in branches cut from `dev`. When the feature is ready for review, submit a PR against `dev`, ideally with any merge conflicts already resolved. `dev` serves as the collection point for all new feature work.

### Release branches

In anticipation of ongoing maintenance, a branch will be created for the current release series. For example, at the time `0.2.0` is released, a branch will be cut from `master` for `0.2.x`.

This *release branch* represents the current state of that release series. All maintenance/bugfix work for the series is collected in this branch. To work on a patch, cut a branch from the release branch. When ready, submit a PR against the release branch.

When a PATCH release is ready (e.g. `0.2.0` to `0.2.1`), the release branch (e.g. `0.2.x`) is merged to `master` (to make the release official) and `dev` is rebased onto `master` (to ensure the patch is incorporated with any new work).

As stated earlier, at this time MDS will maintain *two concurrent MINOR versions*. This means that when a MINOR release is made (e.g. `0.4.0`), work on the outgoing series (`0.2.x`, in this case) ceases and its release branch is removed.

## Schedule

MDS does not currently define a set release cadence or schedule. That being said, a MDS
release should not surprise anyone that wishes to be informed. To that end, releases will always:

* Categorize issues and PRs under an associated [Milestone][mds-milestones]

* Assign a due date for said Milestone that is *at least 24 hours ahead of planned release*

* Include a summary of the major changes / impacts associated with the release, if any

* Be PR-driven, to give the community ample awareness and time for feedback

* Be announced on the [`mds-announce`][mds-announce] Google Group

More detail on this can be read in the Release Checklist below.

## Release Checklist

The following steps **must** be followed for **every** release of MDS:

1. Ensure the [Milestone][mds-milestones] for this release is at `100%`.

1. Run the schema generator to ensure the schema files are up to date:

   ```console
   cd generate_schema/
   pipenv run python generate_provider_schema.py
   ```

1. Update [`ReleaseNotes.md`](ReleaseNotes.md) following the existing format:

    ```md
    ## 1.2.3

    > Released yyyy-MM-dd

    High level summary of the release.

    * Specific change referencing a PR [#555](https://github.com/CityofLosAngeles/mobility-data-specification/pull/555)

    * Another change summary referencing a PR [#777](https://github.com/CityofLosAngeles/mobility-data-specification/pull/777)
    ```

1. [Open a PR][mds-pr-new] against `master`, comparing either `dev` (for a MINOR release) or a release branch (e.g. `0.2.x`) for a PATCH release.

    In the case of a new MINOR version, allow a minimum of 24 hours for community discussion and review of the PR.

1. Once the PR has been sufficiently reviewed, `rebase merge` into `master`.

1. Create a tag on the tip of `master` for this release, e.g. for `0.3.0`:

    ```console
    git checkout master
    git fetch && git pull
    git tag 0.3.0
    git push --tags
    ```

1. Publish a [new Release in GitHub][mds-releases-new] for the tag you just pushed. Copy in the [release notes](ReleaseNotes.md) created earlier.

1. What kind of release was this?
   * **PATCH:** rebase `dev` onto `master` to incorporate the PATCH into `dev`

       *Caution: be aware that this may impact existing PRs open against `dev`!*

        ```console
        git checkout dev
        git rebase master
        git push --force origin dev
        ```

   * **MINOR:** cut a new branch for this release series from the tip of `master`

        Make this branch the default branch in GitHub. E.g. for `0.3.0`

        ```console
        git checkout master
        git checkout -b 0.3.x
        git push origin 0.3.x
        ```

       Remove any outgoing series' release branch (e.g. `0.1.x` when releasing `0.3.0`), if applicable.

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
[mds-tags]: https://github.com/CityOfLosAngeles/mobility-data-specification/tags
[semver]: https://semver.org/