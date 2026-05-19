# GoF on OpenStack + Open OnDemand — Cloud Stack Architecture

**Diagram:** [GoF_OpenStack_OOD_Cloud_Architecture.drawio](GoF_OpenStack_OOD_Cloud_Architecture.drawio)  
**Regenerate:** `python 10_diagrams/cloud_stack/_generate_cloud_stack_drawio.py`

### Opening in diagrams.net (browser)

1. Go to [https://app.diagrams.net/](https://app.diagrams.net/)
2. **Open Existing Diagram** → choose `GoF_OpenStack_OOD_Cloud_Architecture.drawio` from this folder  
   (or drag the file onto the page)
3. Do **not** use **File → Import** — that menu is for CSV/images, not `.drawio` files, and can show `d.setId is not a function`
4. If you still see an old error, hard-refresh the tab (Ctrl+F5) or open in a private window

This is the **infrastructure reference stack** your architects likely mean when they say “something like OpenStack”: a layered cloud with **Open OnDemand** as the science gateway, **OpenStack services** for IAM/compute/storage/network, and **GoF** as the governed platform control plane on top — with everything OpenStack **cannot** replace kept **separate** (orange column) and **linked by interfaces** (arrows).

---

## Why OpenStack + Open OnDemand (not “GoF = OpenStack”)

| Idea | Meaning |
|------|--------|
| **OpenStack** | Private-cloud **IaaS**: VMs, networks, volumes, shared filesystems, images, identity. |
| **Open OnDemand (OOD)** | **HPC web portal** on top: browser access to files, shells, job submission, Jupyter/VS Code — standard in research/HPC. |
| **GoF** | **Governed engineering platform**: references, MDAC, run IDs, SPDM staging, workflow state — **not** a replacement for Nova or Slurm. |
| **Slurm / LSF** | Still the **batch authority** on most HPC sites — sits **beside** OpenStack, connected to OOD and GoF. |

GoF is closer to **“platform services on an OpenStack-class cloud”** than to “another OpenStack project.”

---

## Layer model (read diagram top → bottom)

| Layer | Components | GoF / workshop link |
|-------|------------|-------------------|
| **L1 Access** | Open OnDemand, GoF session broker, GoF APIs, VDI | S7 experience, S1 SSO, S3 interactive |
| **L2 Identity** | Keystone, GoF MDAC, corp IdP, Barbican | S1 MDAC, S2 deploy policy |
| **L3 GoF control plane** | References, run registry, workflow engine, env catalog, data placement | Overlap spine (OWN) |
| **L4 Orchestration** | Heat, Magnum, **Slurm (separate)**, CI | S4 workflows, S5 MDAO, S6 K8s |
| **L5 Compute** | Nova, Ironic, K8s workers, CAE jobs, GPU class | S3, S5, S6 execution |
| **L6 Storage** | Manila, Cinder, Ceph/Glance, **SPDM (separate)** | S1 data, provisioning |
| **L7 Network** | Neutron, egress proxy | S7 geo, export control |

**Right column (orange):** capabilities that **must not** be drawn inside Nova — SPDM, PLM, solvers, ModelOps, licenses, legal, partners.

---

## OpenStack service → GoF capability mapping

| OpenStack service | Typical use in GoF context | GoF role |
|-------------------|---------------------------|----------|
| **Keystone** | Projects, users, OIDC to corp IdP | **INTEGRATE** — tokens for OOD & APIs |
| **Nova** | Interactive VMs, gateways, some workers | **INTEGRATE** — compute placement |
| **Ironic** | Bare-metal HPC nodes (where deployed) | **INTEGRATE** |
| **Neutron** | Networks, security groups, floating IPs | **INTEGRATE** — segments + policy |
| **Manila** | NFS home/project shares | **INTEGRATE** — governed provisioning templates (S1UC06) |
| **Cinder** | Block scratch for VMs | **INTEGRATE** |
| **Ceph / RGW** | Object + often backs Manila/Cinder | **INTEGRATE** |
| **Glance** | Base images / SIF sources | **INTEGRATE** |
| **Heat** | Infra stacks (optional burst pools) | **INTEGRATE** — not primary workflow engine |
| **Magnum** | Kubernetes for GPU/ML pools | **INTEGRATE** — S6 routing |
| **Barbican** | Secrets | **INTEGRATE** (optional) |

| Open OnDemand | Typical use | GoF role |
|---------------|-------------|----------|
| **OOD core** | Files, shell, job adapter to Slurm | **INTEGRATE** — primary engineer UX |
| **OOD apps** | Jupyter, VS Code, VNC | **INTEGRATE** |
| **OOD auth** | Keystone/OIDC | **INTEGRATE** via session broker |

---

## Kept separate (cannot be “solved” by OpenStack alone)

| Capability | Why separate | Interface to stack |
|------------|--------------|-------------------|
| **SPDM / PLM** | Lifecycle & configuration truth | GoF stage/publish API → Manila copies |
| **Slurm / LSF / PBS** | HPC scheduler, not an OpenStack project | OOD adapter + GoF submit API |
| **CAE solvers** | Domain binaries & licenses | Run on compute nodes via batch |
| **CI (Jenkins/GitLab)** | Engineering supply chain | Triggers GoF workflow / batch |
| **MDAO tools** | GEMSEO, Design Manager, OpenMDAO | Call GoF batch API |
| **Artifact registry** | Harbor, Artifactory | Pull via MDAC; not Glance-only |
| **Enterprise ModelOps** | Cloud ML platforms | Policy routing; not in Nova |
| **License servers** | FlexLM etc. | Pre-check before submit |
| **Legal / export (ACDS)** | Classification authority | Feeds GoF MDAC |
| **Archive / tape** | 15–30 year retention | Beyond Manila; orchestrated retrieve |
| **Partner / EE networks** | Federation & contracts | Gateway; not Neutron alone |

---

## Interface list (arrows on diagram)

| From | To | Interface |
|------|-----|-----------|
| Engineer browser | Open OnDemand | HTTPS |
| Open OnDemand | Keystone | OIDC / SAML |
| GoF session broker | Keystone | Token claims for MDAC |
| GoF session broker | Open OnDemand | Launch context / deep links |
| GoF public APIs | GoF MDAC | Policy check |
| GoF run registry | Slurm | Submit / status / cancel |
| Open OnDemand | Slurm | Job submission (adapter) |
| Open OnDemand | Manila | Home/project files |
| GoF data placement | Manila | Provision share / mount policy |
| GoF references | SPDM | Stage in / publish back |
| Nova | Neutron / Cinder / Manila / Glance | Standard OpenStack attachments |
| Heat | Nova | Stack orchestration (optional) |
| Magnum | Kubernetes | Cluster API |
| Slurm | Nova or Ironic | Runs on cloud nodes (site-specific) |
| GoF MDAC | Corporate classification | Attribute enrichment |
| Neutron | Egress proxy | Controlled internet |

---

## Typical flows (for workshops)

**Engineer (interactive)**  
Browser → OOD (Keystone login) → browse Manila → submit job to **Slurm** → GoF records **run ID** + **references** → results staged toward **SPDM**.

**Automation (CI / workflow)**  
Jenkins → **GoF workflow API** → batch via Slurm → lineage to SPDM → notifications.

**ML (hybrid)**  
GoF policy router → **Magnum/K8s** or **Slurm GPU** queue → ModelOps publish hook (external registry).

---

## Relation to other workspace diagrams

| Artifact | Relationship |
|----------|--------------|
| `GoF_Final_Future_Architecture.drawio` | Logical platform domains (what GoF is) |
| **This diagram** | Physical/logical **cloud stack** (what to deploy on) |
| `S*_market_mapping.md` | Market tools mapped to layers (iRODS, OPA, etc.) |
| Overlap diagrams | Shared GoF services that sit in **L3** |

---

## Architect talking points

1. **“We need OpenStack”** → Clarify: **IaaS + storage + identity**, not SPDM or batch semantics.  
2. **“We need Open OnDemand”** → Yes for **portal UX**; GoF still owns **policy and digital thread**.  
3. **“Can OpenStack replace Slurm?”** → **No** on typical HPC — keep Slurm separate, integrate.  
4. **“Can Heat replace GoF workflows?”** → **No** — Heat is infra; GoF owns **engineering run state**.  
5. **“Where does GoF code run?”** → Control plane services (L3) + APIs (L1); workloads run on Slurm/Nova/K8s.
