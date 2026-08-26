---
name: enterprise-multimodal-knowledge-router
description: Use when designing, implementing, reviewing, or routing the Inferrum-backed enterprise multimodal knowledge base, entity/subject library, ContextPack, source adapters, or cross-project knowledge integration across Inferrum, Scaena, Eikona, Pinax, Auctra, or Anatomia.
---

# Enterprise Multimodal Knowledge Router

Use this skill for the Yeisme enterprise knowledge-plane workflow. It keeps one shared Inferrum capability contract while preserving each project's canonical source, permission rules, business lifecycle, and local evidence.

## Core decision

Treat the target as **one knowledge platform with multiple domain owners**, not as one shared business database and not as an Inferrum importer.

- `cli/inferrum` owns the knowledge plane: resource catalog, representations, modality/profile/generation indexes, entity projections, principal-aware retrieval, `ContextPack`, receipts, rebuild and rollback.
- `cli/pinax` owns Markdown/vault truth and publishes note/chunk/source projections.
- `cli/eikona` owns image bytes, generation runs, visual memory, style packs, rights and asset lineage.
- `cli/auctra` owns Story World, characters, scenes, canonical text and revision/review.
- `agent/anatomia` owns video observations, shots/scenes, keyframes, transcripts and analysis evidence.
- `agent/scaena` owns project subjects, `SubjectVersion`, `ProductionGraph`, requirements, review and readiness; it consumes context and refs.
- `agent/ordo`, `agent/ordo` and Workbench consume typed context, tasks, receipts or safe projections; they do not become canonical knowledge owners.

Read [企业多模态知识与主体平台架构](../../../../docs/architecture/enterprise-multimodal-knowledge-platform.md) and the root change `openspec/changes/inferrum-enterprise-multimodal-knowledge-v1/` before proposing a new cross-project contract.

## When to route

Route through this skill when the request involves any of the following:

- enterprise internal RAG, multimodal search, entity library, subject library or shared ContextPack;
- adding a Pinax/Eikona/Auctra/Anatomia/Scaena source projection to Inferrum;
- connecting Scaena SubjectVersion or ProductionGraph readiness to retrieved entities/assets;
- changing representation profiles, index generations, permission-aware retrieval, citation, freshness or rollback;
- deciding whether a new knowledge feature belongs in Inferrum, a domain owner, Scaena, Ordo or Workbench.

Do not use it for a single product's ordinary note, image, screenplay, video-analysis or production behavior unless the work crosses the knowledge-plane contract.

## Routing workflow

1. **Classify the request** as source truth, source adapter, knowledge catalog/index, entity/subject, retrieval/ContextPack, production consumer, or operator/client surface.
2. **Find the canonical owner**. Keep source body, bytes, domain versions, review and business state in that owner. Inferrum receives only opaque refs, allowlisted metadata, safe representations, citations, digests and permission facts.
3. **Check the trust boundary**. Require authenticated principal/org/project scope and policy version. Never treat caller-supplied `allowed_ids` or an empty set as unrestricted. Never copy credentials, raw provider payloads, raw prompts, private paths or full unallowlisted content.
4. **Choose the implementation owner**:
   - root: cross-project architecture, owner matrix, OpenSpec and handoff;
   - `cli/inferrum`: catalog, representation, entity, retrieval, ContextPack, generation and shared SDK/API;
   - domain project: adapter and canonical-source projection;
   - `agent/scaena`: read-only ContextPack consumption, subject binding and production readiness;
   - Ordo/Workbench: consumer projection, run/receipt or operations UI only.
5. **Make the change additive**. Preserve `inferrum.sidecar.v1`, existing provider/Record/VectorStore contracts and domain CLI entrypoints. Add optional fields/methods or a new high-level contract; use an OpenSpec migration/deprecation/rollback plan for any stable-surface break.
6. **Define multimodal lineage**. Every representation names modality, profile, model, content digest and index generation. Video uses transcript/shot/keyframe/observation refs; image bytes stay with Eikona.
7. **Define entity review**. Candidate discovery may be automated; verify, merge, freeze and deprecate require owner or human evidence. Scaena adoption stores a version, scope, permission snapshot and receipt.
8. **Define retrieval evidence**. A `ContextPack` must include citation, source version/digest, permission snapshot, freshness, modality, index generation, redaction summary and pack digest.
9. **Split execution** into a root OpenSpec and owner OpenSpecs. Root does not claim subproject implementation is complete.

## Contract checklist

Before approving a design, verify:

- canonical owner and non-owner boundary are named;
- `KnowledgeResource`/`Representation`/`EntityVersion`/`ContextPack` refs are stable and versioned;
- permission scope is resolved before retrieval and included in cache/evidence keys;
- active/candidate/rollback generation behavior is explicit;
- stale, revoked, permission-denied, contract-mismatch and owner-outage states are explicit;
- no direct cross-project database access, private CLI parsing, raw payload copying or hidden prompt persistence;
- Scaena does not treat a retrieved candidate as a frozen subject or production acceptance;
- integration, component, system/e2e evidence follows the owning project's `temp/integration-test-runs/<run-id>/` contract.

## Real validation commands

Root documentation and Skill source:

```bash
openspec validate inferrum-enterprise-multimodal-knowledge-v1 --strict
scripts/skills.sh validate-custom
scripts/skills.sh validate-profiles
git diff --check -- docs/architecture docs/skills openspec/changes/inferrum-enterprise-multimodal-knowledge-v1
```

Inferrum implementation slice:

```bash
cd cli/inferrum
CGO_ENABLED=0 go test ./... -count=1
```

Scaena consumer slice:

```bash
cd agent/scaena
task test:architecture
task test:integration
```

Use the concrete owner OpenSpec and local `AGENTS.md` for Pinax, Eikona, Auctra and Anatomia commands. Do not invent a root-level command that reaches into another project's private state.

## Outputs

Produce a concise routing/design packet containing:

1. user scenario and readiness label (`exploratory`, `first-support`, or `mature`);
2. owner matrix and source-of-truth decision;
3. contract objects and data flow;
4. permission, redaction, citation, freshness and rollback rules;
5. root OpenSpec plus owner handoff changes;
6. validation commands and evidence paths;
7. non-goals and explicit unresolved decisions.

## Boundaries

- Do not create a parallel Inferrum importer for Pinax, Eikona, Auctra, Anatomia or Scaena.
- Do not merge domain stores into one business source or make LanceDB authoritative.
- Do not implement subproject business code from the root architecture session.
- Do not automatically merge/freeze entities, mutate ProductionGraph, or write owner content from retrieval.
- Do not write raw prompts, provider payloads, secrets, tokens, authorization headers, private paths or full chain-of-thought to docs, logs, receipts or evidence.
- Do not add this Skill to every target profile by default; root owns cross-project routing and domain owners load their local implementation skills.
