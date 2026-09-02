## ADDED Requirements

### Requirement: The existing Skill identity SHALL remain stable

The capability SHALL evolve the existing `.skills/yeisme/scaena/scaena-storyboard-breakdown` source。It MUST retain the `scaena-storyboard-breakdown` name/frontmatter identity and MUST NOT create a competing storyboard writer or operation Skill。

#### Scenario: Publish the evolved Skill

- **WHEN** the source passes validation and is synced to Scaena runtime
- **THEN** existing profile references SHALL continue to resolve the same Skill name
- **AND** no rename/deprecation migration SHALL be required

### Requirement: The Skill SHALL produce a bounded director route plan

For screenplay-to-storyboard work，the Skill SHALL set `phase=director_plan`、`artifact=storyboard_candidate`、`artifact_disposition=candidate`、`acceptance_state=unreviewed`、primary `ai-drama-director` and at most one `ai-drama-continuity-supervisor` constraint，with Scaena as owner binding。The operation Skill SHALL not claim the primary writer role。

#### Scenario: Route a vertical short-drama episode

- **WHEN** accepted project facts establish a vertical short-drama profile and exact source
- **THEN** the Skill SHALL return a ready director route with Scaena owner binding
- **AND** SHALL not include raw source、Prompt body or candidate content in the route plan

### Requirement: Format-changing ambiguity SHALL stop before model execution

If medium/profile、target duration or aspect is missing or conflicting and would change shot structure，the Skill SHALL return `needs_format_decision` and use the format-strategy path or ask the user。It MUST NOT infer the profile only from prose style。

#### Scenario: Script has no production profile

- **WHEN** a script could be vertical short drama、manga panel or ad microdrama and no accepted profile exists
- **THEN** the Skill SHALL request the minimum format decision
- **AND** provider/owner call count SHALL be zero

### Requirement: Episode boundary and owner limits SHALL be decided before paid execution

The Skill SHALL verify one exact episode plus current source、segment、request、token、delivery、scene and shot limit estimates from Scaena readiness。For unresolved multi-episode input or exceeded limits，it SHALL offer explicit split、direction or exact-model decisions and MUST NOT truncate、chunk、merge、loop-submit or silently fallback。

#### Scenario: A season script is supplied as one file

- **WHEN** Scaena reports `EPISODE_BOUNDARY_REQUIRED`
- **THEN** the Skill SHALL keep provider call count zero and request or route exact episode splitting
- **AND** SHALL not imitate a canonical batch by running an uncontrolled shell loop

### Requirement: Profile maturity SHALL be explicit

The Skill SHALL recognize `vertical-short-drama-v1` as the first-support target and `dialogue-dense-v1`、`manga-panel-v1`、`ad-microdrama-v1` as exploratory until their own evidence advances。It MUST present exploratory maturity before a live run。

#### Scenario: User selects manga-panel profile

- **WHEN** the user explicitly requests a manga storyboard
- **THEN** the Skill SHALL route to `manga-panel-v1` and label it exploratory
- **AND** SHALL not inherit vertical first-support status

### Requirement: Prompt selection SHALL use an exact PromptRepo address

The Skill SHALL prefer the immutable official PromptRepo address and SHALL run provider-free inspect/validate before live execution。Legacy `skill:scaena-storyboard-breakdown` version 1 MAY be accepted only as the documented compatibility mapping。The Skill MUST NOT copy the Prompt body into routine output。

#### Scenario: Official Prompt is current

- **WHEN** inspect/validate returns the expected address、digests、locale and readiness
- **THEN** the Skill SHALL pass the exact address to Scaena
- **AND** SHALL retain only safe snapshot refs/digests in its receipt

#### Scenario: Prompt is stale or missing

- **WHEN** the exact address cannot be resolved or its digest drifts
- **THEN** the Skill SHALL return a Prompt blocker and a real repository/catalog next action
- **AND** SHALL not call Dramaturge or a provider

### Requirement: The Skill SHALL perform provider-free capability preflight

Before a paid run/revise，the Skill SHALL verify actual CLI/tool availability、Scaena readiness、Prompt repository/contract、source/profile/direction identity and owner capability。It SHALL use real help/status/catalog commands and MUST NOT infer capability from docs or inventory alone。

#### Scenario: Foreground command is not installed

- **WHEN** current `--help` lacks `--foreground` or watch/diff commands
- **THEN** the Skill SHALL mark the convenience capability missing and use the real async run/show flow if otherwise available
- **AND** SHALL not invent the new flag or claim it executed

### Requirement: Local and remote execution modes SHALL be selected explicitly

In a verified local runtime，the Skill SHOULD use `run --foreground --events` and then watch on timeout。For remote/API/MCP，it SHALL use async run followed by status/resource polling and MUST NOT require a long-blocking MCP tool。

#### Scenario: Local foreground times out

- **WHEN** the command returns `WAIT_TIMEOUT` with a durable breakdown ref
- **THEN** the Skill SHALL watch the original ref
- **AND** SHALL not create a new idempotency key、resubmit or cancel implicitly

#### Scenario: MCP run is queued

- **WHEN** an approved MCP run returns a queued breakdown
- **THEN** the Skill SHALL poll status/resources until review/terminal state or user stop
- **AND** SHALL not treat queued as a generated candidate

### Requirement: Paid mutations SHALL require a current explicit approval packet

Before run/revise，the Skill SHALL present source identity/classification、execution policy、direction、Prompt snapshot、owner readiness、provider retention/training/region facts and expiry、connection ref、exact model、fallbacks、attempts、cost cap and write/cost effect。It SHALL execute at most one mutation only after the current user confirms that packet。Confidential-source policy mismatch MUST NOT be bypassed by generic confirmation。

#### Scenario: User says only “continue” after preflight

- **WHEN** no current message explicitly approves the displayed cost-bounded mutation
- **THEN** the Skill MAY continue read-only status/review
- **AND** SHALL not infer run/revise approval

#### Scenario: Provider data policy is unknown

- **WHEN** the source remains confidential and readiness reports unknown or stale retention/training facts
- **THEN** the Skill SHALL show the typed blocker and a connection-policy next action
- **AND** SHALL not ask for or use a generic “proceed anyway” mutation approval

### Requirement: Review SHALL progress from safe summary to explicit detail

The Skill SHALL first show safe summary、direction summary and findings，then shots，and SHALL read literal dialogue or Prompt content only when the user explicitly needs that review。Routine receipts MUST remain refs/digests/counts/findings/actions only。

#### Scenario: Candidate has blocking findings

- **WHEN** a candidate reaches `review_required` with blockers
- **THEN** the Skill SHALL present finding codes、target refs and revise/patch/reject actions
- **AND** SHALL not offer accept as an allowed action

### Requirement: Revise and patch SHALL remain distinct

The Skill SHALL use Agent revise for structure、ordering、source/dialogue mapping、Prompt mapping、entity/continuity or profile changes，and typed patch only for the nine Scaena-supported local fields。After either mutation it SHALL reload current head and compare/diff before another decision。

#### Scenario: User changes only shot duration

- **WHEN** the requested edit is within the typed patch allowlist
- **THEN** the Skill SHALL use patch without an owner/provider call
- **AND** SHALL reload the immutable successor rather than editing the parent

#### Scenario: User asks to split one shot into three

- **WHEN** the change affects shot structure and source mapping
- **THEN** the Skill SHALL use an approved Agent revise
- **AND** SHALL not attempt unsupported patch paths

### Requirement: Acceptance SHALL require an explicit human direction review

Before accept，the Skill SHALL present story spine、shot beats、dialogue spine、visual baseline、duration contract、coverage/findings and current candidate identity。Only an explicit human approval MAY invoke Scaena accept；model/Skill/provider success MUST NOT imply acceptance。

#### Scenario: Candidate is structurally valid but unreviewed

- **WHEN** candidate validation passes but the user has not approved the presented direction
- **THEN** the Skill SHALL keep it in review-required
- **AND** SHALL not materialize ProductionGraph or start downstream paid generation

### Requirement: Reject、export and downstream generation SHALL have separate gates

Reject and export SHALL each require their own current explicit approval。Accepted storyboard handoff to image/video/audio SHALL be a later production gate；this Skill MUST NOT call Eikona or other generation providers。

#### Scenario: User accepts the storyboard

- **WHEN** Scaena returns an acceptance receipt and ProductionGraph ref
- **THEN** the Skill MAY offer an export or shot-planning handoff as the next action
- **AND** SHALL not automatically generate concept images

### Requirement: Stale、conflict and ambiguous outcomes SHALL not be hidden by retries

The Skill SHALL reload and explain `EXPECTED_VERSION_MISMATCH`/`CANDIDATE_NOT_HEAD`，compare intent on `IDEMPOTENCY_CONFLICT`，and reconcile/watch on ambiguous owner outcomes。It MUST NOT silently choose a new key、new model、higher budget or latest source/Prompt。

#### Scenario: Current candidate changes concurrently

- **WHEN** a mutation fails with expected-version mismatch
- **THEN** the Skill SHALL read/diff the new current head and ask for a new decision
- **AND** SHALL not auto-apply the old instruction to the new head

### Requirement: Skill output SHALL exclude private execution content

The Skill MUST NOT output or persist raw source、literal dialogue by default、rendered Prompt、provider options/payload、credential、Authorization、private path、tool arguments or full chain-of-thought。When explicit domain detail is shown，the final receipt SHALL still remain safe and refs-first。

#### Scenario: Owner run fails

- **WHEN** Scaena returns a typed owner/schema/cost error
- **THEN** the Skill SHALL report the code、safe refs/evidence and next action
- **AND** SHALL not include raw owner request/response content

### Requirement: Skill source and runtime copies SHALL follow repository governance

Maintainers SHALL edit only the source Skill/references in `.skills/yeisme` and run the scoped validators/sync。Generated `.agents/skills` and `.claude/skills` copies MUST NOT be hand-edited；this change SHALL not add or remove profile entries unless a separate need is proven。

#### Scenario: Source validation passes

- **WHEN** the source Skill is ready and runtime paths are quiescent
- **THEN** a single root sync owner SHALL run the narrow Scaena target sync and runtime validation
- **AND** generated copies SHALL match the source/profile exactly
