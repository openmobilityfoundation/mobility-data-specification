# MDS Release Guidelines

MDS will see regular updates and new [releases][mds-releases]. This document describes the general guidelines around how and when a new release is cut.

## Table of Contents

* [Versioning](#versioning)
* [Release Process](#process)
  * [Goals](#goals)
  * [Project Meetings](#project-meetings)
  * [Roles](#roles)
  * [Schedule](#schedule)
  * [Approval by the Open Mobility Foundation](#approval-by-the-open-mobility-foundation)
  * [Communication and Workflow](#communication-and-workflow)
* [Branch Mechanics](#branch-mechanics)
* [Preparing a Release Candidate][prepare-rc]
* [Making an Official Release][make-release]
* [Hotfix Releases](#hotfix-releases)

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

Refer to the list of [Supported Releases](https://github.com/openmobilityfoundation/mobility-data-specification/wiki#supported-mds-releases) for more details.

[Top][toc]

## Release Process

The sections below define the release process itself, including timeline, roles, and communication best practices.

### Project Meetings

* Web conference work sessions will posted to the [MDS-Announce mailing list][mds-announce] and on the [MDS wiki](https://github.com/openmobilityfoundation/mobility-data-specification/wiki). Each working group typically meets every two weeks.

* The meeting organizer can use the [meeting template](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/Web-Conference-Template) to prepare for project meetings. Use the [template markup code](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/Web-Conference-Template/_edit) to create the next scheduled wiki meeting page before the meeting. Include the how to join the meeting and agenda details. Posting the agenda before the meeting has the added benefit that project contributors can propose agenda items.

### Goals

* _Fast, regular releases to support rapid evolution of MDS_

* _Consensus-oriented with clear decision making process when consensus can't be reached_

* _Encourage involvement from all stakeholders, especially public agencies_

* _Frequent stakeholder communication on GitHub, web conference, and in-person_

* _Regular review of release process to ensure it is serving the needs of the community._

### Roles

* **contributors** - Anyone making pull requests, opening issues, or engaging in technical discussion around implementation of features.

* **maintainers** - Project maintainers have commit privileges in the main MDS repository and are responsible for implementing changes such as merging of pull requests and the creation of release branches.

* **working group steering committees** - Review changes when consensus cannot be reached and make final release decision about what changes should be included in a release.

See the [MDS wiki](https://github.com/openmobilityfoundation/mobility-data-specification/wiki) for additional information on the working groups.

### Schedule

MDS operates on an approximately twelve-week release cycle for both major updates (0.x) and patches (0.x.y). In general, major updates (0.x) are expected no more than twice per year. The release cycle is broken down as follows:

#### Weeks 1-3: Proposals

Contributors submit proposals for inclusion in the release cycle in the form of pull requests and issues tagged. If known, note what release you intended a proposal for in its description. Maintainers will tag appropriate pull requests and issues with the Milestone for the upcoming release. Proposals should come with enough explanation to allow all stakeholders to understand intent and implementation strategy.

#### Weeks 4-9: Consensus building, refinement, and implementation

Contributors will provide feedback on proposals. Where possible, discussion will happen via GitHub. Weekly calls will support dialog around more complex or controversial issues. By the end of week 9, all active proposals must be in the form of a pull request. Proposals can be withdrawn or split apart for inclusion in future releases.

##### Weeks 10-11: Decision making

These weeks will start with an web conference work session for all contributors to review and discuss current proposals. Goal is to achieve consensus where possible, or to clearly articulate areas of disagreement where not. Minor changes may be accepted at this stage if they bring contributors to consensus.

During this period, the working group steering committees will review all items for which consensus was not reached and decide on a final release plan. Any remaining approved pull requests will be merged, and a maintainers or working group steering committees will open a pull request containing release notes for the proposed release.

#### Week 12: Release

Documentation will be updated, release notes will be merged and a tag will be created to point to it. At this point the new version will be formally considered a Release Candidate and begin the Open Mobility Foundation approval process described below. Subsequent sections describe how to [Prepare a Release Candidate][prepare-rc] and [Make an Official Release][make-release].

### Approval by the Open Mobility Foundation

Once a release is finalized by the working groups it will be considered a "Release Candidate" until it has been approved as an official deliverable by the Open Mobility Foundation. The OMF bylaws refer to this as a "Working Group Approved Deliverable (WGAD)."

The process for full OMF approval is detailed in Section 5.4 of the [OMF bylaws][omf-bylaws]. In summary:

1. The release candidate/WGAD will be provided to the OMF Technology Council for review and comment at least 75 days prior to the desired date of board approval.

1. The Technology Council will issue a report and/or recommendation for the Board of Directors within 60 days.

1. The Board of Directors will have a minimum of 30 days to review the Technology Council recommendation before taking a vote on the release candidate/WGAD.

1. Upon approval by the Board of Directors, the release will become an official deliverable of the OMF. It will be marked as such in GitHub and on the OMF web site, and it will be merged into the `master` branch on GitHub.

The approval status and anticipated timeline will be reflected in the [MDS wiki](https://github.com/openmobilityfoundation/mobility-data-specification/wiki). While it is the intent of the OMF to have concerns, questions, and issues addressed during the regular working group release process, it is possible that the Technology Council or Board of Directors may request modifications to a release candidate/WGAD prior to official approval. If this situation occurs, the release candidate will be sent back to the working group(s) for additional changes after which it can be resubmitted to the Technology Council and Board of Directors.

The OMF recommends that regulatory agencies do not formally adopt or require any versions of the spec that have not been fully approved by the OMF Board of Directors. However, release candidates/WGADs are considered stable enough to allow API producers and consumers to begin developing against in anticipation of formal approval.

### Communication and Workflow

The release announcements and process schedule will be communicated via [MDS-Announce mailing list][mds-announce]. People wishing to stay informed should join the group for updates. Timing of web conference and in person work sessions will be communicated via MDS-Announce as well.

The following best practices are intended to create clarity around each release cycle:

* Categorize issues and PRs under an associated [Milestone][mds-milestones] for the release

* Assign a due date for said Milestone that aligns with proposed release date

* Pull requests and release notes should include a summary of the major changes / impacts associated with the change or release

* Proposed changes should come in the form of PRs to give the community ample awareness and time for feedback

[Top][toc]

## Branch Mechanics

The branching strategy we describe here is intended to support ongoing maintenance changes in parallel with features for new releases. As mentioned earlier, MDS maintains two concurrent official MINOR releases.

Generally there are two major categories of branches: *Long-lived* and *Short-lived*:

### Long-lived branches

There are always two primary long-lived branches:

* [`master`][mds-master] represents the most recent official release of MDS. This branch is only updated as part of the release process, and pull requests should typically not target `master`.

* [`dev`][mds-dev] is an integration branch for all work since the last official release, including both breaking and non-breaking changes. `dev` is where Release Candidates come from.

If a hotfix is required for a prior release (e.g. a hotfix on top of the `0.3.x` line when the current release is in the `0.4.x` line), a new long-lived *Support branch* will be created from the corresponding tag in `master`. *Support branches* are named according to the version line (e.g. `0.3.x`).

### Short-lived branches

There are two types of short-lived branches, both always branched from `dev`:

* *Feature branches* are for new feature work, which should be submitted as PRs against `dev`, ideally with any merge conflicts already resolved. Rebasing a *Feature branch* onto `dev` before submitting a PR is a great way to avoid lengthy and complicated reviews. Typically a *Feature branch* is created in a fork of the MDS repository.

* *Release branches* are for preparing a new Release Candidate, and collecting any feedback before making an official release. A *Release branch* should be named like `release-x.y.z` where `x.y.z` is the intended version of the release.

[Top][toc]

## Preparing a Release Candidate

The following steps outline the process to prepare a Release Candidate of MDS. This process makes public the intention and contents of an upcoming release, while allowing work on the next release to continue as usual in `dev`.

1. Ensure the [Milestone][mds-milestones] for this release is at `100%`.

1. Create a *Release branch* from the tip of `dev` named `release-x.y.z`, where `x.y.z` is the intended version of the release. This branch will be used to prepare the Release Candidate. For example, to prepare a Release Candidate for `0.5.0`:

    ```bash
    git fetch
    git checkout origin/dev
    git checkout -b release-0.5.0
    git push -u origin release-0.5.0
    ```

    Changes generated by the steps below should be committed to this branch.

1. Update the [schema version regex][mds-schema-common].

1. Run the schema generator to ensure the schema files are up to date:

    ```bash
    cd schema/
    python generate_schemas.py
    ```

1. Update ReleaseNotes.md using the following format:

    ```md
    ## X.Y.Z

    > Release Candidate submitted yyyy-MM-dd

    High level summary of the release.

    ### CHANGES

    * Specific change referencing a PR [#555](https://github.com/openmobilityfoundation/mobility-data-specification/pull/555)

    * Another change summary referencing a PR [#777](https://github.com/openmobilityfoundation/mobility-data-specification/pull/777)
    ```

1. Create a tag like `x.y.z-rcN` for this Release Candidate. For example, for the first `0.5.0` Release Candidate:

    ```bash
    git fetch
    git checkout origin/release-0.5.0
    git tag 0.5.0-rc1
    git push --tags
    ```

1. Publish a [pre-Release in GitHub][mds-releases-new]:

    ```md
    Tag version: [tag you just pushed]
    Target: [release branch]
    Release title: [X.Y.Z Release Candidate N]
    Description: [copy in ReleaseNotes created earlier]
    This is a pre-release: Check
    ```

1. [Open an Issue][mds-issue-new] to start the Release Candidate review process, using the `Release Candidate review` template. Fill in the appropriate Release Candidate version/URL.

1. Post an announcement to the [MDS-announce Mailing List][mds-announce], copying the [release notes](ReleaseNotes.md) created earlier and linking to the [GitHub release][mds-releases] and Release Candidate review Issue:

    ```email
    From:    mds-announce@groups.openmobilityfoundation.org
    To:      mds-announce@groups.openmobilityfoundation.org
    Subject: MDS X.Y.Z Release Candidate

    A Release Candidate for MDS X.Y.Z has been submitted.

    [release notes]

    [link to GitHub pre-Release]

    The Release Candidate is now under OMF Review. Follow the progress here: https://github.com/openmobilityfoundation/mobility-data-specification/issues/XYZ
    ```

### Incorporating feedback from OMF review

The OMF review process may elicit further changes to a Release Candidate. Generally follow the same steps as above to prepare a subsequent Release Candidate, committing necessary changes to the release branch and incrementing the prior Release Candidate number where required.

For example, if the second Release Candidate for `0.5.0` is being prepared, after committing necessary changes, create a tag on the tip of the release branch like `0.5.0-rc2` and make a new [GitHub pre-Release][mds-releases-new] from there:

```bash
git fetch
git checkout origin/release-0.5.0
# more commits per OMF review
git tag 0.5.0-rc2
git push --tags
```

Communicate the new Release Candidate as usual, including in ReleaseNotes.md, on the MDS-Announce mailing list, and on the Release Candidate review Issue. Be sure to indicate that this is a *new Release Candidate* of the target version.

Repeat as-needed for subsequent Release Candidates.

[Top][toc]

## Making a Release

The following steps describe how to make an approved [Release Candidate][prepare-rc] an official release of MDS:

1. Ensure OMF review has been completed and the Issue created during the Release Candidate process has been closed.

1. In the release branch created earlier, update the ReleaseNotes.md with the new date of the release:

    ```diff
    ## X.Y.Z

    -> Release Candidate submitted yyyy-MM-dd
    +> Released yyyy-MM-dd

    etc...
    ```

1. [Open a Pull Request][mds-pr-new] from the release branch to `dev`. This ensures any changes to the Release Candidate during the review process make their way back into `dev`. Merge this PR.

1. [Open a Pull Request][mds-pr-new] from the release branch to `master`. Merge this PR to make the release official.

1. Create a tag in `master` for the new version. For example for `0.5.0`:

    ```bash
    get fetch
    git checkout master
    git tag 0.5.0
    git push --tags
    ```

1. Publish a [Release in GitHub][mds-releases-new]:

    ```md
    Tag version: [the tag you just pushed]
    Target: master
    Release title: [X.Y.Z]
    Description: [copy in ReleaseNotes created earlier]
    This is a pre-release: DO NOT check
    ```

1. Post an announcement to the [MDS-announce Mailing List][mds-announce], copying the [release notes](ReleaseNotes.md) created earlier and linking to the [GitHub release][mds-releases]:

    ```email
    From:    mds-announce@groups.openmobilityfoundation.org
    To:      mds-announce@groups.openmobilityfoundation.org
    Subject: MDS X.Y.Z Released

    MDS X.Y.Z has been released.

    [release notes]

    [link to GitHub pre-Release]
    ```

1. Finally, delete the release branch.

[Top][toc]

## Hotfix Releases

In rare cases, a hotfix for a prior release may be required out-of-phase with the normal release cycle. For example, if a critical bug is discovered in the `0.3.x` line after `0.4.0` has already been released.

1. Create a *Support branch* from the tag in `master` at which the hotfix is needed. For example if the bug was discovered in `0.3.2`, create a branch from this tag:

    ```bash
    git fetch
    git checkout 0.3.2
    git checkout -b 0.3.x
    git push -u origin 0.3.x
    ```

1. Merge (or commit directly) the hotfix work into this branch.

1. Update ReleaseNotes.md with the hotfix version details, following the existing format.

1. For fixes that impact the current cycle (e.g. updates to language that still exists and hasn't been changed in the current cycle), [open a Pull Request][mds-pr-new] to merge the support branch back into `dev`.

1. Tag the support branch with the hotfix version. For example if `0.3.2` is the version being hotfixed:

    ```bash
    git fetch
    git checkout 0.3.x
    git tag 0.3.3
    git push --tags
    ```

1. Create a [GitHub Release][mds-releases-new] from this tag and the support branch. For example if `0.3.3` is the new hotfix version:

    ```md
    Tag version: 0.3.3
    Target: 0.3.x
    Release title: 0.3.3
    Description: [copy in ReleaseNotes created earlier]
    This is a pre-release: DO NOT check
    ```

[Top][toc]

[make-release]: #making-a-release
[mds-announce]: https://groups.google.com/a/groups.openmobilityfoundation.org/forum/#!forum/mds-announce
[mds-dev]: https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev
[mds-issue-new]: https://github.com/openmobilityfoundation/mobility-data-specification/issues/new/choose
[mds-master]: https://github.com/openmobilityfoundation/mobility-data-specification/tree/master
[mds-milestones]: https://github.com/openmobilityfoundation/mobility-data-specification/milestones
[mds-pr]: https://github.com/openmobilityfoundation/mobility-data-specification/pulls
[mds-pr-new]: https://github.com/openmobilityfoundation/mobility-data-specification/compare
[mds-releases]: https://github.com/openmobilityfoundation/mobility-data-specification/releases
[mds-releases-new]: https://github.com/openmobilityfoundation/mobility-data-specification/releases/new
[mds-schema-common]: https://github.com/openmobilityfoundation/mobility-data-specification/blob/master/schema/templates/common.json
[mds-tags]: https://github.com/openmobilityfoundation/mobility-data-specification/tags
[omf-bylaws]: https://www.openmobilityfoundation.org/resources/
[prepare-rc]: #preparing-a-release-candidate
[semver]: https://semver.org/
[toc]: #table-of-contents
