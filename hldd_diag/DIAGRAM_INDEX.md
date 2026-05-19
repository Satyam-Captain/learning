# HLDD Diagram Index

**HLDD Draft 0.3:** `06_architecture_synthesis/hldd/GoF_HLDD_Draft.md`  
**Word import (standalone):** `06_architecture_synthesis/hldd/GoF_HLDD_Word_Import.md`  

**Regenerate diagrams:** `python 10_diagrams/hldd/_generate_hldd_drawio.py`  
**Open:** [diagrams.net](https://app.diagrams.net/) → **Open Existing Diagram** (not Import)

| HLDD Section | Diagram File | Purpose | Source artifacts |
|--------------|--------------|---------|------------------|
| §1.1, §2.1, §4.1 | [02_System_Context.drawio](02_System_Context.drawio) | Users, GoF boundary, grouped enterprise systems | `target_architecture_view.md`, `what_gof_owns_vs_integrates.md` |
| §2.5, §3.1.2 | [05_Capability_View.drawio](05_Capability_View.drawio) | S1–S7 swimlanes → shared spine C1–C7 | `common_capabilities.md`, overlap diagrams |
| §3.5, §4.5 | [04_Logical_Architecture.drawio](04_Logical_Architecture.drawio) | Seven domains + cross-cutting strip | `domain_candidates.md`, `cross_cutting_services.md` |
| §4.1, §4.5.3 | [06_Integration_View.drawio](06_Integration_View.drawio) | GoF hub; dashed integrate to enterprise | `what_gof_owns_vs_integrates.md` |
| §3.2, §4.2, §4.5.4 | [07_Data_Policy_View.drawio](07_Data_Policy_View.drawio) | Reference → MDAC → SPDM → lineage → cache | `S1_capabilities.md`, CCS-02/03 |
| §4.5.4–5 | [08_Runtime_Execution_View.drawio](08_Runtime_Execution_View.drawio) | Session → workflow → execution → scheduler → lineage | `target_architecture_view.md` flows |
| §2.6, §5.3 | [09_Out_of_Scope_Boundary.drawio](09_Out_of_Scope_Boundary.drawio) | OWN / INTEGRATE / OUT | Boundary synthesis |

## Diagram design (second pass)

- **Title banner** on each page (HLDD section reference)  
- **Legend box** (colors: blue = GoF, grey dashed = integrate, gold = cross-cutting)  
- **Reduced clutter** in system context (six enterprise groups vs. ten boxes)  
- **Word export:** use 150–200 DPI PNG; width ~16 cm in Word for readability  

## Not diagrammed (by design)

| Item | Reason |
|------|--------|
| ArchiMate [HAG] formal views | CD / IMAC pass |
| Market alignment matrix | `04_market_mapping/` text tables |
| AS-IS [HAG] process maps | Narrative in HLDD §3.4, §4.4 |
| Per-scenario deployment | Single scenario selected §5.3 |
| Risks / open questions | HLDD §2.6–2.7 tables |

## Related platform diagrams

| Path | When to use |
|------|-------------|
| `10_diagrams/final_platform/GoF_Final_Future_Architecture.drawio` | Executive steerco overview |
| `10_diagrams/capability_overlap/S1_to_S7_common_capabilities.drawio` | Overlap workshop progression |
