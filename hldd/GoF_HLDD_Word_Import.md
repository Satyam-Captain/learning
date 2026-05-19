# GISEH for eAction — High-Level Design Dossier (HLDD)

**Initiative:** GISEH of Future (GoF)  
**Document status:** Draft 0.3 — Word import (standalone, architecture-board level)  
**Format:** Complete HLDD for Microsoft Word (standalone).  
**Template:** HLDD_template.txt.txt.  
**Diagrams:** Export PNG from `10_diagrams/hldd/*.drawio` at each [Insert Diagram: …] marker.  
Open via diagrams.net → Open Existing Diagram (not Import).  
**Sources:** Architecture workspace synthesis (S1–S7, ~88 use cases); traceability in Reference Documents (§7)  

---

## TABLE OF CONTENTS

1. [Introduction](#1-introduction)  
2. [Context Analysis](#2-context-analysis)  
   - [2.6 Risks and Constraints](#26-risks-and-constraints)  
   - [2.7 Open Questions](#27-open-questions)  
3. [Business Architecture](#3-business-architecture)  
4. [Information System Architecture](#4-information-system-architecture)  
5. [Architecture Scenarios](#5-architecture-scenarios)  
6. [Transition Architectures and Roadmap](#6-transition-architectures-and-roadmap)  
7. [Reference Documents](#7-reference-documents)  
8. [Glossary](#8-glossary)  
- [Architecture Assumptions](#architecture-assumptions)  
- [Contributors](#contributors)  
- [Record of Revisions](#record-of-revisions)  

---

## 1 Introduction

### 1.1 Purpose of the document

This High-Level Design Dossier (HLDD) is the **Preliminary Design** record for **GISEH for eAction** (GISEH of Future — GoF). It is prepared for architecture board, IM Architecture Committee (IMAC), and program steerco review, and will inform Architecture Requirements Dossiers (ARDs) that decompose the design into implementable increments.

**Architectural intent.** GoF is defined as a **governed scientific computing platform**: the coherent layer where modeling and simulation data is referenced, policy is enforced, workloads are placed and executed, automation is orchestrated, and results are returned to enterprise lifecycle systems with auditable lineage. The HLDD explains **why** this layer is necessary, **what** it owns versus what it integrates, **how** major flows work, and **how** transition can be phased without contradicting existing enterprise systems of record.

**Transformation scope.** The initiative addresses ~**88 use cases** in swimlanes **S1–S7** (data and compliance, development and deployment, CAE execution, workflows, MDAO, AI/ML, global engineering). The transformation moves from:

- Fragmented engineer access (VDI, shares, ad hoc staging) to **unified session and API entry** with equal batch dignity.  
- Manual SPDM steps in certification loops to **orchestrated stage/publish** at the platform boundary.  
- Disconnected automation (scripts, multiple workflow products, CI without run correlation) to a **workflow run layer** with platform run identity.  
- Ungoverned cross-site copies and shadow ML paths to **MDAC-governed placement and routing**.

**What this HLDD contains:**

| Part | HLDD template chapter | Content |
|------|----------------------|---------|
| Context | §2 | Drivers, stakeholders, goals, vision, risks, open questions |
| Business | §3 | AS-IS/TO-BE business capabilities, requirements, deliverables |
| Information system | §4 | Logical domains, cross-cutting services, integration, data flows |
| Scenarios | §5 | Selected architecture and rejected alternatives with rationale |
| Transition | §6 | Work packages, dependencies, roadmap, adoption |
| References | §7–8 | Traceability to workshop artifacts |

A Concept Dossier (CD) may follow if IMAC requires extended multi-scenario scoring. Workshop synthesis already supports **one primary TO-BE pattern** (governed platform hub) with explicit OUT boundaries.

**Diagram:** [Insert Diagram: 02_System_Context.drawio]

### 1.2 ArchiMate Guidelines

Diagrams marked **[HAG]** in the HLDD template refer to ArchiMate modeling per enterprise HLDD guidelines (`HLDD_ArchiMate_Guidelines`).  

For this draft, **section-specific draw.io diagrams** in `10_diagrams/hldd/` provide workshop-ready views traceable to synthesis artifacts. Formal ArchiMate views may be produced in a subsequent pass for IMAC/DIAC submission.

---

## 2 Context Analysis

### 2.1 Context

GISEH for eAction (GoF) addresses a structural gap in how modeling and simulation is executed at Airbus scale. Approximately **88 workshop use cases** across swimlanes **S1–S7** describe needs that converge on the same architectural pressure: engineering computation must be **governed**, **automatable**, **globally lawful**, and **defensible over decades** — not merely faster on existing clusters.

#### Current operational reality (AS-IS context)

Engineering teams today operate through **multiple parallel access paths**:

- Interactive work via **VDI**, local staging, and desktop pre/post tools (S3).  
- Batch execution via **HPC schedulers** (LSF-class) with site-specific scripts and queue conventions (S3, S4, S5).  
- **Manual SPDM** staging and publish steps inside certification and load loops (S1, S4).  
- **CI pipelines** (Jenkins-class) that trigger compute but lack a unified platform run model (S4, S2).  
- **Regional file copies** and informal sync for global teams (S7).  
- **Separate ML estates** (cloud and on-prem) that bypass the same metadata and policy applied to simulation (S6).

This fragmentation is not a failure of HPC operations. Clusters, license integration, and queue management remain essential. The gap is the absence of a **platform layer at the M&S boundary** that binds identity, policy, references, run correlation, and lifecycle orchestration before and after scheduler execution.

#### Why HPC-only evolution is insufficient

An infrastructure-only program (more cores, new clusters, portal refresh without control plane) addresses **capacity and access** but leaves unresolved:

| Gap | Swimlane evidence | Architectural consequence |
|-----|-------------------|---------------------------|
| Ungoverned data copies | S1, S7 | Compliance and export-control exposure |
| No reference-first access | S1, S3 | Digital thread breaks at execution boundary |
| Manual SPDM in loops | S1, S4 | Certification velocity limited by human steps |
| Fragile nested automation | S4, S5 | Load loops and MDAO campaigns fail opaquely |
| Shadow ML paths | S6 | Policy bypass; duplicate data estates |
| File-based global collaboration | S7 | EE partners outside master-data model |

HPC remains the **execution engine**; GoF is the **governance and orchestration plane** above it.

#### Why governance and automation matter

**Governance (S1, S2, S7):** Metadata-driven access control (MDAC) must apply consistently when data is accessed, cached near compute, deployed across geographies, or exposed to partners. Fail-closed enforcement is an architectural property, not a storage feature.

**Automation (S4, S5):** eAction timelines depend on server-side workflow execution, batch-first APIs, and CI composition — not long-lived interactive sessions. The platform must own **workflow run state** while integrating external orchestrators (Jenkins, domain workflow products, MDAO tools).

#### Why digital thread continuity matters

SPDM/PLM remains lifecycle authority. GoF must issue **governed references**, record **lineage at platform use**, and **orchestrate stage/publish** without creating a second status truth. Use cases S1UC05, S4UC05, and cross-cutting concern CC1 (digital thread) require this binding.

#### Cross-site and extended-enterprise concerns (S7)

Global engineering is not solved by replicating files between regions. Architecture must enforce **placement policy** (execute in jurisdiction, lawful cache rules) and **EE access** through governed session and references — not email attachments or shadow repositories.

#### AI/ML concerns (S6)

S6 use cases demand GPU execution, hybrid routing, and ModelOps publication hooks. Architect tagging often assigns training estates to separate programs; synthesis nonetheless requires **classification routing**, **same MDAC**, and **lineage** on the GoF fabric to prevent a parallel ungoverned cloud.

**Global opportunity:** Reduce development and certification lead time through governed automation, digital thread continuity, and policy-aware execution — **without** replacing SPDM/PLM, corporate IAM, or domain solver methodology.

**Environment and scope of change:** Enterprise engineering IT, existing HPC/GISEH services, SPDM/PLM, IAM, storage, CI/CD, license infrastructure, domain CAE/MDAO applications, and optional portal/private-cloud integrations where already committed. HLDD scope is **platform behavior, boundaries, and integration contracts** — not datacenter greenfield, not PLM product replacement, not solver IP ownership.

### 2.2 Stakeholders

Stakeholders span **engineering domains**, **enterprise IT**, **data governance**, and **extended enterprise**. The HLDD does not alter organization structure; it defines how roles interact with the future platform. Full workshop roster remains in initiative records; the table below captures **architecturally relevant** stakeholders for decision and adoption.

| Stakeholder | Description (position, responsibilities) | Active / Represented | Action in initiative | Decision-maker | User | Sponsor |
|-------------|------------------------------------------|----------------------|----------------------|----------------|------|---------|
| SteerCo / HO domains (1A, 1G, 1P, 1Y, 1Z, Digital) | Program funding, scope approval, eAction alignment | Active / Represented | Approve HLDD pattern and phasing | X | | X |
| Use case owners (per domain) | CAE, MDAO, workflow, data UC owners | Active | Validate FR/NFR traceability; accept increments | | X | |
| GISEH / platform architecture | Target platform, HLDD, ARD, boundaries | Active | Author and maintain architecture | X | | |
| SPDM / PLM product owners | Lifecycle authority, metadata schema | Represented | API contracts; status semantics | X | | |
| Enterprise IAM / security | SSO, accreditation, corp security | Represented | Federation, attribute feeds | X | | |
| HPC / GISEH operations | Scheduler ops, capacity, license integration | Represented | Adapter operations; queue policy consult | | | |
| Data governance / compliance | Export control, classification (ACDS interface) | Represented | Policy axes; audit requirements | X | | |
| Engineering software developers | Business-owned BOTs, packaging (S2) | Active | DevSecOps templates; sandbox use | | X | |
| CI / automation owners | Jenkins-class pipelines (S4) | Active | Composition via GoF APIs | | X | |
| Extended-enterprise partners | Suppliers, partners (S7) | Represented | Governed access; no shadow IT | | X | |
| Corporate legal / export | Classification interpretation | Represented | Authority for rules; not platform build | X | | |

**Integration implication:** Users and sponsors are predominantly **engineering domains**; decision-makers include **SPDM, IAM, and program leadership**. HPC operations are **consulted and integrated**, not displaced — a key adoption constraint for §6.

### 2.3 Assessment

Stakeholder assessments (workshop synthesis, architect tagging review) are summarized below. These inform scenario selection and transition prioritization.

| SWOT | Assessment | Swimlane / source traceability |
|------|------------|-------------------------------|
| **Strengths** | Mature HPC estate and operational skill; enterprise SPDM investment; active automation in S4/S5; steerco alignment that GoF is a **platform** not a cluster | S3, S4, steerco messages |
| **Weaknesses** | Fragmented engineer access; manual SPDM steps; weak scheduler/solver semantics in generic metadata tools; nested job fragility; dual ML paths | S1, S3, S4, S6, market mapping |
| **Opportunities** | Reference-first data plane; single MDAC engine; workflow run layer; batch-first APIs; governed EE access; env catalog for replay | S1–S7, common capabilities C1–C7 |
| **Threats** | Everything-platform scope creep; duplicate SPDM status; orchestration sprawl (Jenkins + Eve + DDMS:Workflow + scripts); compliance incident via cache | CC3, architect review |

**Pain points by swimlane (architectural view):**

- **S1:** Data treated as paths not references; cache copies without policy; provisioning not mapped to classification templates.  
- **S2:** Deploy and codeshare without consistent MDAC; sandbox fragmentation.  
- **S3:** Interactive vs batch inconsistency; license checks not unified at submit boundary.  
- **S4:** No push notifications; fragile nested runs; CI lacks platform run correlation.  
- **S5:** MDAO loops depend on ad hoc batch glue.  
- **S6:** Training on copies outside governed fabric.  
- **S7:** Cross-site replication as workaround; EE outside digital thread.

**Diagram:** [Insert Diagram: 02_System_Context.drawio]

### 2.4 Motivation

#### Goals

| ID | Title | Description |
|----|-------|-------------|
| G1 | Governed scientific computing | Provide a platform where M&S data and runs are policy-bound, referenced, and auditable |
| G2 | Digital thread continuity | Link execution inputs/outputs to SPDM lifecycle without shadow file exchange |
| G3 | Automation at scale | Enable workflow and batch automation for eAction timelines (S4, S5) |
| G4 | Global engineering | Lawful cross-site and EE execution with placement policy (S7) |
| G5 | Reproducibility & replay | Support long-horizon reconstruction via environment catalog and lineage (S1, S3) |
| G6 | Converged AI/ML execution | Run ML on same fabric as simulation with classification routing (S6) |

#### Outcomes

| ID | Title | Description |
|----|-------|-------------|
| O1 | Reduced manual SPDM steps | Automated stage/publish orchestration at platform boundary |
| O2 | Single run correlation model | Platform run ID across interactive, batch, CI, MDAO |
| O3 | Fail-closed compliance | MDAC denies illegal replication and placement |
| O4 | Faster load-loop automation | Server-side workflow runs with notifications |
| O5 | EE digital thread | Partners access governed references, not email attachments |

#### High-Level Requirements (HLR)

| ID | Title | Description |
|----|-------|-------------|
| HLR1 | Reference-first data access | Engineers and automation use governed artifact references |
| HLR2 | Unified policy | Same MDAC semantics for data, deploy, cache, and run |
| HLR3 | SPDM-aligned lifecycle | Single authority for artifact status; GoF orchestrates |
| HLR4 | Batch-first parity | APIs equivalent dignity to interactive access |
| HLR5 | Integrated execution | Submit to existing schedulers under placement policy |
| HLR6 | Observable runs | Engineering observability exportable to enterprise sinks |

*Formal requirement baselining remains subject to architect validation and ARD decomposition.*

### 2.5 Vision

The transformation **adds** a governed platform layer and **impacts** how engineers and automation interact with data and execution. It does **not remove** SPDM, IAM, HPC operations, or domain applications.

| Category | Items |
|----------|--------|
| **Unchanged** | SPDM/PLM as lifecycle products; corporate IAM; solver binaries; legal classification ownership; HPC scheduler operations |
| **Impacted** | Engineer access patterns; staging/publish paths; CI/MDAO composition; cache placement; GPU routing |
| **Added** | GoF control plane: MDAC, references, run identity, workflow run state, env catalog, federation policy |
| **Removed** | Ad hoc ungoverned cross-site file sync as primary pattern (replaced by policy-aware staging) |

**Diagram:** [Insert Diagram: 05_Capability_View.drawio] — swimlane-to-capability vision.

### 2.6 Risks and Constraints

| Risk / constraint | Description | Mitigation (architectural) | Traceability |
|-------------------|-------------|---------------------------|--------------|
| **Scope creep** | Platform absorbs PLM, NAS design, or solver methodology | Explicit OUT boundaries; decision gates in §5 | `what_gof_owns_vs_integrates.md` |
| **Duplicated lifecycle ownership** | GoF stores SPDM-equivalent status | ORCH only; SPDM remains authority | S1UC05, architect review |
| **Orchestration sprawl** | Parallel workflow engines without composition model | GoF workflow **run state**; INTEG CI/domain WMs | S4, architect Q5–Q8 |
| **Compliance enforcement complexity** | MDAC must span data, deploy, cache, run, EE | Single Policy Decision Service (CCS-02) | S1, S2, S7 |
| **Metadata inconsistency** | Schema in SPDM vs enforcement at platform | Joint governance; GoF enforces profiles | S1UC02, architect Q2 |
| **Federated policy challenges** | Multi-site and EE rules conflict with cache | Federation domain + placement policy | S7 |
| **Replay / reproducibility** | 15–30 year reconstruction | Environment catalog + lineage binding | S1UC01, S3UC18 |
| **Epic vs architecture gap** | “Out of epic” read as “never” | Steerco boundary statement; phased roadmap | Architect review |
| **Operational adoption** | Engineers bypass platform if UX slower | Integrate existing portals/VDI; batch-first APIs | S3, S7 |
| **Performance constraints** | Data proximity drives behavior (filer latency) | Cache orchestration under MDAC — not ungoverned copy | S3UC31 |

Constraints that bound solution space:

- Must integrate **existing schedulers** (architect alignment: execution via integration).  
- Must not require **greenfield-only** cloud for production CAE.  
- Must respect **legal/export** classification authority external to GoF.  
- Market research informs **candidate ecosystems only** — no product selection in HLDD.

### 2.7 Open Questions

The following decisions remain open for architecture board or ARD resolution. They do not invalidate the selected scenario but must be closed before detailed design.

| ID | Topic | Question | Impact if unresolved | Suggested forum |
|----|-------|----------|---------------------|-----------------|
| OQ1 | Ownership | Single owner for platform run identity correlation (CCS-01)? | Broken automation debuggability | Architecture board |
| OQ2 | Workflow engine | Compose DDMS:Workflow, Eve, Jenkins vs converge? | Orchestration sprawl | S4 workshop |
| OQ3 | Metadata authority | RACI for schema vs enforcement (S1UC02)? | Inconsistent MDAC inputs | Data governance + GoF |
| OQ4 | Observability | Boundary between engineering run schema and enterprise SIEM? | Over- or under-instrumentation | IM/IT architecture |
| OQ5 | Federation onboarding | EE program separate vs GoF milestone (S7UC06)? | Duplicate partner gateways | S7 steerco |
| OQ6 | Runtime catalog | Central GoF catalog vs federated community modules? | Replay fragmentation | Runtime WP |
| OQ7 | Replay storage | Archive binding model for 15–30y retrieval | Certification defensibility | S1 + archive ops |
| OQ8 | ML routing | Matrix for ML Platform vs GoF GPU classes (S6)? | Shadow ML path | S6 architecture |
| OQ9 | Reference IDs | Issuer: GoF, SPDM, or joint service? | Digital thread breaks | S1 architecture |
| OQ10 | Phase 1 cut | eAction minimum vs long digital-thread horizon | Funding misalignment | Program steerco |

---

## 3 Business Architecture

### 3.1 Business Landscape

#### 3.1.1 Organization Landscape

Impacted organization units (internal) include engineering domains **1A** (airframe), **1G** (flight physics), **1P** (propulsion), **1Y** (systems), **1Z** (methods/tools), and digital/product architecture. Platform and integration roles include **GISEH**, enterprise **IAM/security**, **data governance**, and **HPC operations**. External interfaces include **extended-enterprise** partner organizations (S7) governed by contract and export rules — not by GoF owning partner IT.

**Architectural intent:** HLDD defines **ways of working** and system boundaries, not a reorganization. RACI for publish, policy, and scheduler operations is clarified in synthesis (`what_gof_owns_vs_integrates.md`): GoF is **responsible** for platform orchestration and policy enforcement at the M&S boundary; SPDM remains **accountable** for lifecycle status; HPC ops remains **accountable** for cluster operations.

Optional ArchiMate [HAG] organization diagrams may be added in CD for IMAC submission.

#### 3.1.2 Business Architecture Landscape

**Value stream (target):**

1. **Define engineering intent** — program, configuration, analysis campaign (often in PLM/SPDM context).  
2. **Prepare governed data** — resolve references, MDAC, stage from SPDM (S1).  
3. **Execute analysis** — interactive or batch, with run ID and env binding (S3, S4, S5).  
4. **Review results** — engineering judgment in domain tools.  
5. **Publish to lifecycle** — orchestrated publish-back to SPDM (S1, S4).  
6. **Reuse in program** — downstream consumers via SPDM authority, not ad hoc copies.

**Business capabilities by swimlane impact:**

| Business capability | S1 | S2 | S3 | S4 | S5 | S6 | S7 | Change type |
|---------------------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|-------------|
| Governed M&S data management | ● | ○ | ○ | ○ | ○ | ○ | ○ | **Impacted** — refs, MDAC, cache |
| Engineering computation execution | ○ | ○ | ● | ● | ● | ○ | ○ | **Impacted** — placement, classes |
| Engineering workflow automation | | ○ | ○ | ● | ● | ○ | ○ | **Impacted** — run state |
| Engineering software delivery | | ● | | ○ | | ○ | | **Impacted** — DevSecOps |
| Intelligent engineering (AI/ML) | | | ○ | ○ | ○ | ● | ○ | **Impacted** — routing zone |
| Global collaboration | ○ | | ○ | | ○ | ○ | ● | **Impacted** — federation |
| PLM/SPDM lifecycle | ● | ○ | ○ | ● | ○ | ○ | ○ | **Unchanged** — integrated |

● = strong influence · ○ = supporting

**Overlap insight (capability progression):** Shared spine capabilities (C1 references, C2 MDAC, C4 execution, C5 run ID, C6 runtime, C7 session) appear from **S1+S2** onward in overlap analysis — GoF must implement once, not per swimlane silo.

**Diagram:** [Insert Diagram: 05_Capability_View.drawio]

### 3.2 Business Deliverables Landscape

Key business objects (semantic, not physical schema):

| Business object | Sensitivity / notes |
|-----------------|---------------------|
| Governed artifact reference | Export control, program, EC tags |
| Engineering run record | Audit, lineage |
| Workflow run | Automation state |
| Environment definition | Replay, reproducibility |
| Staged work area | SPDM-aligned copy |
| Classification profile | MDAC input |
| Execution class | Batch, GPU, sandbox |

**Diagram:** [Insert Diagram: 07_Data_Policy_View.drawio] — reference and policy flow.

### 3.3 Business Requirements

#### Functional Requirements

| ID | Title | Description | Traceability |
|----|-------|-------------|--------------|
| FR1 | Governed data access | Engineers resolve artifact references; MDAC enforces access before IO | S1, all |
| FR2 | Proximity cache policy | Governed copies near compute; eviction on SPDM status change | S1, S3, S6 |
| FR3 | SPDM stage and publish | Orchestrate stage-in/out; no duplicate lifecycle state in GoF | S1, S4 |
| FR4 | Self-service provisioning templates | Map program/classification to storage access patterns | S1UC06 |
| FR5 | Unified engineering session | SSO context across SPDM, tools, compute entry points | S1, S3, S7 |
| FR6 | Batch submission API | Submit, monitor, cancel runs with platform contract | S3, S4, S5 |
| FR7 | Interactive workspace wrap | Interactive sessions register runs and policy same as batch | S3 |
| FR8 | Workflow run automation | Multi-step runs with state, notify, rerun, parent/child link | S4 |
| FR9 | CI composition | External CI triggers workflow/batch via GoF APIs | S4, S2 |
| FR10 | MDAO adapter contract | External optimizers invoke batch through platform API | S5 |
| FR11 | DevSecOps templates | Classification-aware build/deploy gates for business software | S2 |
| FR12 | Execution classes | Interactive, batch, campaign, GPU, sandbox classes with policy | S3, S6 |
| FR13 | ML classification routing | Route workloads to appropriate tier under MDAC | S6 |
| FR14 | Cross-site placement | Enforce geo and contract rules on placement and cache | S7 |
| FR15 | EE governed access | Partners use references on platform; no shadow file exchange | S7UC06 |
| FR16 | License pre-check | Gate submit using integrated entitlement check | S3, S4 |

#### Non-Functional Requirements

| ID | Title | Description | Rationale |
|----|-------|-------------|-----------|
| NFR1 | Fail-closed policy | Deny when MDAC cannot decide | Compliance (S1, € risk class in workshop) |
| NFR2 | Auditability | Lineage on every platform use | Digital thread, certification |
| NFR3 | Long-horizon replay | Env ID + refs for 15–30y reconstruction | S1UC01, incident defense |
| NFR4 | Scale | Campaign/array and nested runs | S4, S5, S3UC14–16 |
| NFR5 | Interoperability | Integrate schedulers, SPDM, IAM without fork | Architect review pattern |
| NFR6 | Observability | Engineering run schema exportable to enterprise sinks | S4UC01 gaps |
| NFR7 | Latency awareness | Placement respects data proximity | S3UC31 filer latency |
| NFR8 | Security egress | Controlled ingress/egress patterns | S1UC08, S7 |
| NFR9 | Evolutivity | Add execution classes without redesigning core | S6 GPU convergence |
| NFR10 | Operational clarity | Joint support model with HPC ops documented | Adoption §6 |

### 3.4 AS-IS Business Architecture

AS-IS business architecture is characterized by **capability fragmentation** at the M&S boundary:

**Data and compliance (S1):** Engineers and automation reference **paths and shares** more often than immutable IDs. Proximity copies exist for performance but **lack uniform policy** when SPDM status changes. Self-service provisioning is inconsistent across sites.

**Development and deployment (S2):** Business-owned software ships through heterogeneous pipelines. Sandboxes and dev nodes are **community-specific**. MDAC on deploy is not guaranteed to match data-access policy.

**CAE execution (S3):** Pre/post often on workspace; compute on HPC. Interactive and batch are **different operational models** with different support paths. License checks are scheduler-integrated but not correlated with a **platform run identity**.

**Workflows (S4):** Automation depends on **VDI-resident** orchestration, custom scripts, and multiple workflow products. Notifications are weak. Nested runs break on timeout or opaque child job failure.

**MDAO (S5):** Optimizer loops invoke batch through **adapters** without standard platform composition contract.

**AI/ML (S6):** Training and inference may occur on **separate estates** with weaker linkage to SPDM references and export rules.

**Global / EE (S7):** Collaboration relies on **file transfer** and informal process; co-simulation and partner access are not uniformly governed on-platform.

Logical capabilities exist in products (SPDM, scheduler, CI, domain apps) but **no pivot capability** unifies policy, references, and run correlation for all swimlanes.

### 3.5 TO-BE Business Architecture

TO-BE operational model: **all M&S entry points** (interactive portal class, VDI, APIs, CI, MDAO) pass through GoF **control-plane behaviors** before touching integrated execution and storage.

#### How engineers interact with GoF

1. **Authenticate** via corporate IAM; GoF session broker establishes engineering context.  
2. **Resolve** inputs as governed references; MDAC evaluates access and obligations.  
3. **Submit** work as platform runs (interactive session, batch job, or workflow step) with **run ID**.  
4. **Execute** on integrated scheduler/infrastructure per **placement policy**.  
5. **Record** lineage (tool, env ID, actor, inputs/outputs as refs).  
6. **Publish** or stage results via SPDM orchestration when lifecycle requires.

#### Batch vs interactive parity

HLR4 requires **batch-first APIs** with dignity equal to GUI paths. Architecturally:

- Interactive sessions still exist (S3) but are **wrapped** with same policy and run registration.  
- Automation and CI **must not** be second-class (S4UC01–02 architect alignment).

#### Workflow orchestration impacts

GoF owns **workflow run state** (schedule, notify, rerun, link prior runs). External engines (Jenkins, domain workflow products) **compose** via APIs — GoF does not rebuild their semantics.

#### Federation implications

Cross-site and EE runs consume **federation policy** before placement. Co-simulation gateway mediates protocols; partner IT remains external.

| Logical capability (pivot) | TO-BE role | Primary swimlanes |
|----------------------------|------------|-------------------|
| Governed data & continuity | Reference, MDAC, cache, SPDM orchestration | S1 (+ all consumers) |
| Experience & access | Session broker, public APIs | S1, S3, S7 |
| Execution fabric | Submit, placement, execution classes | S3, S4, S5, S6 |
| Engineering automation | Workflow run layer | S4, S5 |
| Software delivery | DevSecOps templates, gates | S2 |
| Global federation | Cross-site/EE policy, gateway | S7 |
| Runtime platforms | Environment catalog, replay | S1, S2, S3, S6 |

**Diagram:** [Insert Diagram: 04_Logical_Architecture.drawio]

### 3.6 Targeted Reuses & Gains

**Reuse (optimization — mandatory items become constraints in FR/NFR):**

| Reuse target | Architectural gain | Constraint if reused |
|--------------|-------------------|----------------------|
| Existing HPC/LSF estate | Preserves fairshare, license hooks, operational skill | Must provide scheduler adapter; no rip-and-replace |
| SPDM/PLM | Single lifecycle truth; audit alignment | GoF ORCH only; no status fork |
| Corporate IAM | No duplicate identity; accreditation path | MDAC consumes attributes |
| Enterprise storage tiers | No new vault product | GoF placement + cache policy only |
| CI controllers | Leverage existing pipeline investment | GoF workflow run layer, not new CI |
| Artifact registries | Portable images/packages (S2, S6) | MDAC on pull |
| Market patterns (OPA-class policy, OCI, portable env) | Accelerate ARD — **candidates only** | Selection in ARD, not HLDD |

**Gains (repository of reusable business/architecture elements for future programs):**

| Gain | Description |
|------|-------------|
| Common capability model C1–C7 | Repeatable spine for future swimlanes |
| Platform run identity standard | Reusable across CI, HPC, workflows |
| MDAC profile library | Classification templates per program |
| Headless CAE invocation profiles | Domain-agnostic execution contracts |
| Federation policy templates | Reusable EE/geo rules |

---

## 4 Information System Architecture

### 4.1 Information System Landscape

The TO-BE information system landscape introduces a **GoF application layer** (logical services) between engineering consumers and enterprise systems. The landscape is intentionally **hub-and-spoke**: GoF is the M&S control plane; enterprise products retain authority in their domains.

**Added (GoF platform):** Policy Decision (MDAC), Reference Resolution, Run Registry, Workflow Run Engine, Session Broker, Public APIs, Placement Engine, Environment Catalog, SPDM Orchestration Adapter, Federation Policy, Notification, Engineering Observability Export.

**Impacted (integration contracts strengthened):** Scheduler submit/status; SPDM stage/publish; IAM federation; storage mount/provision; CI webhooks; registry pull with MDAC.

**Unchanged (operated by owning teams):** Scheduler internals, SPDM/PLM product cores, IAM directory, physical storage arrays, solver binaries, legal classification systems.

| Logical application group | Representative enterprise apps | GoF relationship |
|---------------------------|-------------------------------|------------------|
| Lifecycle | SPDM, PLM | INTEG — orchestrate |
| Identity | Corp SSO, directory | INTEG — attributes |
| Execution | LSF-class scheduler, license servers | INTEG — execute / check |
| Data | NAS, object, archive | INTEG — tiers |
| Supply chain | Jenkins/GitLab, Artifactory/Harbor | INTEG — compose / pull |
| Domain | CAE, MDAO tools | INTEG — run |
| Observability | Enterprise log/analytics | INTEG — export sink |

**Diagram:** [Insert Diagram: 02_System_Context.drawio] · [Insert Diagram: 06_Integration_View.drawio]

### 4.2 Data Objects Landscape

High-level **data objects** (attributes omitted per HLDD convention) and relationships:

| Data object | Authority | Relationships |
|-------------|-----------|---------------|
| Governed artifact reference | GoF issues/resolves; SPDM aligns lifecycle | 1:N inputs/outputs per run |
| Platform run record | GoF | Maps to scheduler job, CI build |
| Workflow run | GoF | 1:N platform runs (steps) |
| Policy decision record | GoF | References actor, resource, action |
| Lineage record | GoF | Links runs, refs, env IDs |
| Environment definition | GoF catalog | Bound to runs for replay |
| Staged work area descriptor | GoF orchestration | Backed by storage mount |
| Classification profile | Enterprise + SPDM | Input to MDAC |
| SPDM artifact metadata | SPDM | Drives cache eviction rules |
| IAM claim set | IAM | Session context |
| Scheduler job record | HPC | External ID mapped by GoF |

**Sensitivity:** References and lineage carry **export control, program, military use/class** tags (S1UC04). Volume and rate requirements are workload-dependent — campaigns (S3, S5) drive placement and cache (NFR7), detailed in ARD.

**Diagram:** [Insert Diagram: 07_Data_Policy_View.drawio]

### 4.3 Information System Requirements

#### Functional (IM/IT)

| ID | Title | Description | Maps to FR |
|----|-------|-------------|------------|
| IS-FR1 | Policy API | MDAC allow/deny/obligations | FR1, FR14 |
| IS-FR2 | Reference API | Create, resolve, invalidate references | FR1 |
| IS-FR3 | Run API | Submit, status, cancel, list | FR6, FR7 |
| IS-FR4 | Workflow API | Define run, step state, notify | FR8 |
| IS-FR5 | SPDM adapter | Stage, publish, status subscription | FR3 |
| IS-FR6 | Scheduler adapter | Map platform run ↔ scheduler job | FR6 |
| IS-FR7 | Session broker | SSO context, launch attributes | FR5 |
| IS-FR8 | Placement service | Select execution class and site | FR12, FR14 |
| IS-FR9 | Environment catalog API | Register/bind environment IDs | FR3 replay |
| IS-FR10 | Observability export | Structured run events | NFR6 |
| IS-FR11 | Registry integration | MDAC-gated pull | FR11, S2 |
| IS-FR12 | License check integration | Pre-submit entitlement | FR16 |

#### Non-Functional (IM/IT)

| ID | Title | Description |
|----|-------|-------------|
| IS-NFR1 | Availability | Engineering SLA tiers per execution class (ARD) |
| IS-NFR2 | Security | Fail-closed; corp IAM; no shadow paths |
| IS-NFR3 | Performance | Cache hit rate and submit latency targets (ARD) |
| IS-NFR4 | Scalability | Horizontal control-plane scale; scheduler scale external |
| IS-NFR5 | Maintainability | Versioned APIs; adapter isolation |
| IS-NFR6 | Audit retention | Lineage retention aligned with compliance |
| IS-NFR7 | Portability | Adapter pattern for second site scheduler |

### 4.4 AS-IS Information System Architecture

AS-IS information systems expose **point integrations** without a shared control plane:

- Schedulers expose job IDs **not mapped** to engineering workflow or CI build IDs.  
- SPDM integrations are often **manual UI steps** at workflow boundaries.  
- IAM provides authentication but **not engineering ABAC** on artifacts and runs.  
- Metadata catalogs (where present) lack **scheduler/solver/environment semantics** (market mapping, OpenMetadata-class gap).  
- Observability is split between cluster ops and application logs **without** engineering run schema.

### 4.5 TO-BE Information System Architecture

TO-BE IS architecture introduces **GoF application services** (logical) as control plane over unchanged enterprise systems of record.

#### 4.5.1 Platform domains (detail)

**Governed Data & Continuity**  
Owns reference resolution, MDAC enforcement, proximity cache policy, SPDM stage/publish orchestration, provisioning templates. Consumes IAM attributes and SPDM status; does not own lifecycle state. *Leads:* C1, C2, C3.

**Engineering Experience & Access**  
Owns session broker, engineering workspace context, batch-first public APIs. Integrates portal-class UX and VDI as transport. *Leads:* C7.

**Execution Fabric**  
Owns submission contract, run lifecycle states, execution class catalog, placement policy (data + license + geo). Integrates scheduler for execute. *Leads:* C4.

**Engineering Automation**  
Owns workflow run state machine, notifications, composition contracts for CI/MDAO. Does not replace Jenkins or domain workflow products. *Supports:* S4, S5.

**Software Delivery & Lifecycle**  
Owns DevSecOps template model, mandatory compliance gates, packaging semantics. Integrates registry and CI. *Supports:* S2.

**Global Engineering Federation**  
Owns cross-site/BU placement rules, EE onboarding orchestration, co-simulation gateway policy. *Supports:* S7.

**Runtime Platforms (horizontal)**  
Owns environment catalog, replay binding, sandbox class definitions. Consumed by all execution paths. *Leads:* C6.

#### 4.5.2 Cross-cutting services

| Service | Purpose | Maps to scheduler/IAM/SPDM |
|---------|---------|---------------------------|
| Platform Run Identity | Correlate interactive, batch, CI, workflow | Maps LSF job IDs — does not replace |
| Policy Decision (MDAC) | Allow/deny/obligations | Consumes IAM + ACDS + SPDM tags |
| Lineage & Audit | Digital thread at use | Feeds enterprise audit |
| Engineering Observability | Run parameters, engineering metrics | Export to Splunk-class |
| Notification | Run/workflow events | Integrates mail/webhook |
| Reference Resolution | Stable IDs | Aligns with SPDM refs |
| Environment Binding | Env ID on every run | Supports replay |
| License pre-check | Gate before submit | Integrates FlexLM-class |
| Classification routing | ML/HPC/geo routing | S6 + S7 |

#### 4.5.3 Integration boundaries

Integration style: **reference-first, policy-wrapped, fail-closed**.

| Enterprise system | GoF boundary | Direction |
|-------------------|--------------|-----------|
| SPDM/PLM | Stage/publish APIs; read status | Bi-directional orchestration |
| IAM | OIDC/SAML; claims | Inbound attributes |
| HPC scheduler | Submit/status/cancel | Outbound execute |
| Storage | Mount/share provision | Outbound provision; policy on use |
| CI | Webhook/API trigger | Inbound compose |
| License | Check API | Outbound consult |
| ModelOps | Publish hook | Outbound after train |

#### 4.5.4 Data and policy flow

1. Actor presents identity and intent.  
2. References resolved; MDAC evaluates.  
3. If staging required, SPDM orchestration creates governed work area.  
4. Run registered; env ID bound; placement selects execution class.  
5. Scheduler executes; lineage captured.  
6. Outputs registered as references; publish orchestrated when required.

**Diagram:** [Insert Diagram: 07_Data_Policy_View.drawio]

#### 4.5.5 Run identity and lineage

**Run identity** is issued at platform boundary and **propagates** to nested and child runs (campaigns, sweeps, workflow steps). LSF job IDs and Jenkins build numbers are **mapped**, not replaced.

**Lineage** records inputs/outputs as references, tool IDs, environment IDs, actor, timestamps — supporting audit and long-horizon replay (S1UC01).

**Diagram:** [Insert Diagram: 04_Logical_Architecture.drawio] · [Insert Diagram: 08_Runtime_Execution_View.drawio] · [Insert Diagram: 06_Integration_View.drawio]

### 4.6 Candidate Architectures

| # | Scenario | Main features |
|---|----------|---------------|
| 1 | **Governed platform hub (recommended)** | GoF control plane; integrate SPDM, IAM, HPC, storage, CI; domain apps external |
| 2 | HPC-portal-only extension | Portal or VDI UX improvement only |
| 3 | SPDM-centric expansion | Extend SPDM to own execution and policy |
| 4 | Greenfield cloud-only | New cloud estate without HPC integration |

**Scenario 1** is the only candidate that satisfies HLR1–HLR6 without violating OUT boundaries. Alternatives are retained for IMAC traceability.

---

## 5 Architecture Scenarios

### 5.1 Introduction

Architecture scenario selection concludes the preliminary design. Workshop synthesis across S1–S7, architect tagging review, and domain model consolidation converge on **one recommended pattern**: a **governed platform hub** (Scenario 1) that adds GoF control-plane services and integrates existing enterprise and HPC systems.

Alternatives (portal-only, SPDM expansion, greenfield cloud-only) are documented for IMAC completeness. They fail one or more HLRs or violate OUT boundaries (SPDM ownership, legal authority, integrated scheduler assumption A3).

This chapter provides allocation matrix, narrative comparison, scoring summary, and formal decision record.

### 5.2 Alternate Scenario

#### 5.2.1 Synthesis of Architecture Scenarios

| Logical capability | Scenario 1 (selected) | Scenario 2 | Scenario 3 |
|--------------------|----------------------|------------|------------|
| Policy / MDAC | GoF service | Partial in portal | SPDM-only |
| References / lineage | GoF service | Paths | SPDM-only |
| Execution abstraction | GoF + HPC integrate | HPC only | Mixed |
| Workflow run state | GoF | External scripts | Domain WM |
| Engineer UX | Integrate portal class | Portal only | VDI-only |

#### 5.2.2 Description of Architecture Scenarios

**Scenario 1 — Governed platform hub (selected)**

- **Description:** GoF owns control-plane behavior; integrates enterprise systems; engineers access via integrated experience channels and APIs.  
- **Prerequisites:** SPDM API commitment, IAM federation, HPC API/adapter, architecture board boundary sign-off.  
- **Pros:** Meets compliance, automation, federation, ML routing; preserves investments.  
- **Cons:** Requires new platform build; strong governance needed to avoid scope creep.

**Scenario 2 — HPC portal only (rejected)**

- **Rationale for insufficiency:** A portal refresh improves file browsing and job submission UI but does not provide **MDAC**, **immutable references**, **workflow run state**, or **SPDM orchestration**. S1 and S4 requirements remain unmet; compliance risk on copies persists (S7). Architect comments position Giseh as orchestration, not portal-only (review summary §1).  
- **Operational continuity:** Keeps fragmented policy at storage and scheduler layers.  
- **Why rejected:** Fails digital thread and automation HLRs; steerco message “platform not cluster” is violated if portal is the only deliverable.

**Scenario 3 — SPDM-centric expansion (rejected)**

- **Ownership conflict:** SPDM/PLM teams own lifecycle semantics; expanding SPDM to own **execution placement**, **scheduler submit**, and **run correlation** creates **duplicate authority** and enterprise conflict (S1UC05 architect alignment).  
- **Weak execution abstraction:** Schedulers and GPU classes still require integration; SPDM is not designed as batch/HPC control plane.  
- **Why rejected:** High conflict risk, medium coverage of S3–S6; orchestration sprawl moves from Jenkins to SPDM customizations.

**Scenario 4 — Greenfield cloud-only (rejected)**

- **Operational continuity failure:** Production CAE at scale remains on **existing HPC** (architect tagging: HPC out of epic but integrated). Greenfield-only path abandons fairshare, license integration, and operational playbooks.  
- **Compliance integration:** Export control and accreditation assume **enterprise IAM and existing data** classifications — greenfield silo increases shadow-path risk (S6).  
- **Why rejected:** Does not meet HLR5; contradicts assumption A3 on integrated schedulers.

#### 5.2.3 Comparison of Architecture Scenarios

| Criteria | Weight | Scenario 1 | Scenario 2 | Scenario 3 |
|----------|--------|------------|------------|------------|
| Functional coverage (S1–S7) | High | Strong | Weak | Medium |
| Compliance / digital thread | High | Strong | Weak | Medium |
| Time to value (phased) | Medium | Medium | Fast short / weak long | Slow |
| Enterprise alignment | High | Strong | Medium | Conflict risk |
| Evolutivity | High | Strong | Weak | Medium |

### 5.3 Decision on Architecture Selection

**Decision:** Adopt **Scenario 1 — Governed platform hub** as the TO-BE information system pattern for GISEH of Future.

**Rationale:** Only scenario satisfying workshop HLRs without violating OUT boundaries (SPDM ownership, legal authority, solver methodology). Steerco messages 1–6 (platform not cluster, SPDM complement, metadata core, automation engine room, no shadow ML, federation not file copy) are structurally supported.

**Open:** Formal scoring session with IMAC/DIAC to be recorded in MoM when scheduled.

**Diagram:** [Insert Diagram: 09_Out_of_Scope_Boundary.drawio]

---

## 6 Transition Architectures and Roadmap

### 6.1 Business perspective

Prioritized transformation themes (architecture phasing — not committed project plan):

| # | Business process / activity | Business capability | Logical capability |
|---|----------------------------|---------------------|-------------------|
| 1 | Governed data access & staging | M&S data management | Governed data & continuity |
| 2 | Policy enforcement on runs | Compliance execution | MDAC + execution fabric |
| 3 | Workflow automation | Engineering automation | Workflow run engine |
| 4 | Batch-first engineer access | Computation execution | Experience + execution APIs |
| 5 | DevSecOps on platform | Software delivery | Delivery & lifecycle |
| 6 | Global / EE placement | Global collaboration | Federation |
| 7 | ML on governed fabric | AI-assisted engineering | Execution classes + routing |

### 6.2 Information Systems perspective

#### 6.2.1 Work Package identification

| # | Business capability | Logical capability | Description |
|---|---------------------|-------------------|-------------|
| WP1 | Governed data | References + MDAC | Foundation policy and ID model |
| WP2 | Governed data | SPDM orchestration | Stage/publish automation |
| WP3 | Execution | Execution fabric + HPC adapter | Submit/monitor abstraction |
| WP4 | Automation | Workflow run engine | S4 engine room |
| WP5 | Experience | Session broker + APIs | Unified access |
| WP6 | Delivery | DevSecOps templates | S2 governed ship |
| WP7 | Federation | EE / cross-site policy | S7 |
| WP8 | Runtime | Environment catalog | Replay track |

#### 6.2.2 Work Package definition

**WP1 — References + MDAC (foundation)**  
Application services: Reference API, Policy Decision API, policy audit log, classification profile enforcement.  
**Outcome:** Fail-closed gate for all downstream WPs.  
**Risks if delayed:** Every other WP lacks consistent policy.

**WP2 — SPDM orchestration**  
Services: Stage-in/out orchestrator, status-driven cache rules, SPDM adapter.  
**Depends on:** WP1 (refs + MDAC). **External:** SPDM API contract.

**WP3 — Execution fabric + HPC adapter**  
Services: Submit API, run lifecycle, placement engine, scheduler adapter, execution class registry.  
**Depends on:** WP1. **External:** HPC ops commitment.

**WP4 — Workflow run engine**  
Services: Workflow state store, notification, CI composition hooks.  
**Depends on:** WP1, WP3. **Addresses:** S4 engine room.

**WP5 — Session broker + public APIs**  
Services: SSO context, batch-first APIs, portal integration hooks.  
**Depends on:** WP1. **Parallel with:** WP3.

**WP6 — DevSecOps templates**  
Services: Template catalog, gate enforcement, deploy MDAC integration.  
**Depends on:** WP1. **Addresses:** S2.

**WP7 — Federation**  
Services: Placement policy for geo/EE, co-sim gateway mediation.  
**Depends on:** WP1, WP3. **Often later increment** per architect epic tagging.

**WP8 — Environment catalog**  
Services: Env registration, replay binding, sandbox class.  
**Depends on:** WP1, WP3. **Addresses:** S1 long-horizon, S3 legacy stacks.

**Dependency graph (logical):** WP1 → {WP2, WP3, WP5, WP6}; WP3 + WP1 → WP4; WP3 + WP1 → WP8; WP3 + WP1 → WP7.

#### 6.2.3 External dependencies identification

| Work package | External dependency |
|--------------|---------------------|
| WP1, WP2 | SPDM API and metadata profiles agreed |
| WP1, WP5 | IAM federation and attribute contract |
| WP3 | HPC scheduler integration commitment |
| WP2, WP3 | Storage tier and mount provisioning |
| WP6 | CI system and artifact registry access |
| WP7 | Legal/EE onboarding processes |

### 6.3 Change Management Inception

Transformation changes how engineers submit work, how automation correlates runs, and how data is staged — not only which cluster is used. Resistance typically appears when **VDI habits**, **manual SPDM shortcuts**, or **shadow ML paths** appear faster than governed paths.

#### 6.3.1 Communication Plan

| Audience | Message | Channel |
|----------|---------|---------|
| SteerCo / sponsors | GoF is platform, not HPC refresh; SPDM remains authority | SteerCo, written boundary statement |
| Domain engineers | Same science, better thread and automation; batch APIs matter | Domain workshops, S3/S4 owners |
| Developers (S2) | Templates accelerate compliant ship | Dev community |
| HPC ops | GoF adapts to scheduler; joint support model | Ops council |
| SPDM owners | Orchestration, not replacement | Architecture board |
| EE partners | Governed access replaces informal file exchange | S7 program |

Deliverables: initiative web page, increment release notes, FAQ on “out of epic vs out of architecture.”

#### 6.3.2 Training Plan

| Session | Audience | Content |
|---------|----------|---------|
| Awareness | HO, architects | Vision, boundaries, roadmap |
| Operational | CAE engineers | References, submit API, portal integration |
| Automation | Workflow/CI owners | Workflow API, run ID, notifications |
| Operations | Platform + HPC | Adapter ops, escalation, observability |
| Compliance | Data stewards | MDAC axes, fail-closed behavior |

### 6.4 Overall Roadmap

| Increment | Work packages | Capability outcome | Adoption / operational notes |
|-----------|---------------|-------------------|------------------------------|
| **Inc 1 — Foundation** | WP1, WP5 (partial) | References, MDAC, session/API baseline | Pilot domains on read-only policy; no production cutover |
| **Inc 2 — Execute & stage** | WP2, WP3 | SPDM orchestration + execution abstraction | Engineers submit via API; scheduler adapter in one site |
| **Inc 3 — Automate** | WP4 | Workflow run layer | CI teams migrate one pipeline as reference |
| **Inc 4 — Deliver & replay** | WP6, WP8 | DevSecOps templates + env catalog | Business BOT pilot; replay binding for one program |
| **Inc 5 — Federate** | WP7 | EE and cross-site policy | Requires legal/EE prerequisites (OQ5) |

**Phased rollout reasoning:** MDAC and references must precede execution scale-out to avoid **retrofitting policy** on ungoverned runs. Automation (Inc 3) depends on stable run IDs (Inc 2). Federation last because architect tagging marks many S7 UCs out of near epic — architecture enables without blocking Inc 1–4.

**Operational adoption concerns:** Joint support model between **platform team** and **HPC operations** (scheduler still operated by HPC). Training on references and APIs for engineers (S3/S4). Clear steerco message that **out of epic ≠ out of architecture** to avoid program conflict.

---

## 7 Reference Documents

| Index | Title | Reference / path |
|-------|-------|------------------|
| R1 | HLDD template | `00_raw_inputs/HLDD_template.txt.txt` |
| R2 | Swimlane use cases | `00_raw_inputs/swimlane_usecase.txt.txt` |
| R3 | Capability model | `02_capability_model/` |
| R4 | Domain model | `03_domain_model/` |
| R5 | Market mapping | `04_market_mapping/` |
| R6 | Architecture synthesis | `06_architecture_synthesis/` |
| R7 | Architect review | `07_questions_and_concerns/architect_review/` |
| R8 | Diagrams | `10_diagrams/` |
| R9 | HLDD diagrams index | `10_diagrams/hldd/DIAGRAM_INDEX.md` |

---

## 8 Glossary

| Term | Definition |
|------|------------|
| GoF | GISEH of Future — governed scientific computing platform |
| GISEH | Group / program context for engineering HPC and simulation estate |
| HLDD | High-Level Design Dossier |
| ARD | Architecture Requirements Dossier |
| CD | Concept Dossier |
| MDAC | Metadata-Driven Access Control |
| SPDM | Simulation Process Data Management (lifecycle) |
| EE | Extended enterprise (partners) |
| HPC | High-performance computing |
| MDAO | Multidisciplinary design analysis and optimization |

*Refer to LEXINET for enterprise standard terms.*

---

## Architecture Assumptions

| ID | Assumption | Architectural implication |
|----|------------|---------------------------|
| A1 | SPDM/PLM remains **lifecycle authority** | GoF must not persist competing status; publish orchestration only |
| A2 | GoF integrates **enterprise IAM/SSO** | MDAC consumes claims; no duplicate identity store |
| A3 | **Existing HPC/scheduler** remains execution backend | Execution Fabric is abstraction + adapter, not scheduler replacement |
| A4 | **Market tools** are candidates, not selections | ARD makes product choices; HLDD stays vendor-neutral |
| A5 | GoF owns **control-plane** OWN/ORCH behaviors | Nova/LSF/portal ops remain external operations |
| A6 | **Legal/export** authority external | Fail-closed MDAC from ACDS/legal feeds |
| A7 | **Solver methodology** external | Headless profiles only; no numerical ownership |
| A8 | **Architect epic tagging** may narrow delivery | Roadmap increments may not deliver all S7/S6 UCs immediately |
| A9 | **Per-UC validation** required | HLDD patterns hold; scope cut per ARD |
| A10 | Portal/cloud integrations optional | UX integrate layer; center of gravity is control plane |
| A11 | **Batch-first parity** is normative | API design precedes GUI-only features |
| A12 | **Single MDAC engine** | One policy service for data, deploy, cache, run, EE |

---

## Contributors

| Name | Function |
|------|----------|
| Architecture workspace synthesis | Draft HLDD content |
| *TBD* | Architecture board validation |

---

## Record of Revisions

| Issue | Date | Status | Modified by | Modified sections | Observations |
|-------|------|--------|-------------|-------------------|--------------|
| 0.1 | 2026-05-20 | Draft | Agent synthesis | All | Initial workshop synthesis |
| 0.2 | 2026-05-20 | Draft | Agent synthesis | All | Architecture-board expansion; §2.6–2.7 added |
| 0.3 | 2026-05-20 | Draft | Agent synthesis | All | Full section expansion; FR/NFR; Word parity |
