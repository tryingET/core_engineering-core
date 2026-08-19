---
summary: "Authority and freshness rules for checked-in engineering-core governance evidence."
read_when:
  - "Reading, regenerating, or reviewing a capability baseline or other governance evidence."
type: "reference"
---

# Governance evidence

Files in this directory are evidence snapshots, not runtime authority and not a substitute for current CI or release proof.

## Existing capability baseline

`engineering-core-capability-baseline.json` is a preserved **historical v0.7.0 snapshot**. It records the package/catalog version and host-local repository paths that were present when it was generated. Those paths are evidence from that run; they are not portable installation instructions, and the snapshot must not be interpreted as the current health of version 0.9.0 or later.

The current repository state is established by the checked-out source, `policy/engineering-lane.json`, `engineering-core check-self`, the required CI workflow, and release-lineage proof. A historical baseline may support comparison, but it cannot promote itself to current or verified status.

## Rules for new snapshots

A new checked-in governance snapshot should:

- state whether it is a historical fixture, current baseline, or generated projection;
- record the package version, catalog version, source commit, and generating command;
- include a UTC capture timestamp when time is material;
- avoid host-local paths in portable configuration fields;
- preserve host-local paths only when they are explicitly labeled as captured evidence;
- use a versioned or dated filename when more than one snapshot may coexist;
- document the owner and regeneration trigger;
- never claim CI, release, compliance, or doctrine authority beyond the schema's explicit authority statement.

When a current baseline is introduced, add a self-check that detects version/source drift. Until then, treat the existing file as a historical fixture only.
