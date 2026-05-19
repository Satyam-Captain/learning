"""Generate HLDD section draw.io diagrams (browser-safe, Word-readable)."""
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent

_spec = importlib.util.spec_from_file_location("gof_drawio", ROOT / "_generate_swimlane_drawio.py")
_mod = importlib.util.module_from_spec(_spec)
sys.modules["gof_drawio"] = _mod
_spec.loader.exec_module(_mod)
DrawioDoc = _mod.DrawioDoc

S_EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;strokeWidth=1;strokeColor=#333333;"
S_EDGE_D = S_EDGE.replace("#333333", "#666666;dashed=1;")
S_LEG = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333;align=left;spacingLeft=6;fontSize=9;"


def title(doc, text, w=1400):
    doc.box(text, "text;html=1;strokeColor=none;fillColor=none;fontSize=14;fontStyle=1;", 40, 12, w, 32, cid="title")


def legend(doc, text, y, w=520):
    doc.box(text, S_LEG, 40, y, w, 48, cid="leg")


def edge(doc, src, tgt, dashed=False):
    eid = doc.nid()
    doc.add(eid, "", S_EDGE_D if dashed else S_EDGE, edge=True, source=src, target=tgt)


def write_doc(doc, name):
    p = OUT / name
    p.write_text(doc.render(), encoding="utf-8")
    print("wrote", p.name)


def system_context():
    doc = DrawioDoc("hldd-02-context", "02 System Context", 1280, 820)
    title(doc, "<b>HLDD 2.1 / 4.1 — System Context</b>", 1200)
    legend(doc, "<b>Legend</b><br>Blue = GoF platform &nbsp;|&nbsp; White = users &nbsp;|&nbsp; Grey dashed = integrate (external authority)", 50)
    z_gof = doc.box(
        "GoF Platform Boundary",
        "swimlane;whiteSpace=wrap;html=1;startSize=28;fillColor=#E8F4FC;strokeColor=#005AAB;strokeWidth=2;fontStyle=1;",
        280, 110, 520, 420, cid="gof",
    )
    for cid, lbl, x, y in [
        ("d_data", "Governed Data", 20, 45),
        ("d_exp", "Experience", 200, 45),
        ("d_exec", "Execution", 360, 45),
        ("d_auto", "Automation", 20, 130),
        ("d_del", "Delivery", 200, 130),
        ("d_fed", "Federation", 360, 130),
        ("d_rt", "Runtime (horizontal)", 20, 215),
    ]:
        doc.box(lbl, "rounded=1;whiteSpace=wrap;html=1;fillColor=#B8D4EF;strokeColor=#005AAB;fontSize=10;", x, y, 150, 48, cid=cid, parent=z_gof)
    for cid, lbl, y in [
        ("u_eng", "Engineers", 130),
        ("u_dev", "Developers", 200),
        ("u_auto", "CI / workflows", 270),
    ]:
        doc.box(lbl, "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#666;", 40, y, 180, 44, cid=cid)
    for cid, lbl, y in [
        ("e_life", "SPDM / PLM", 130),
        ("e_id", "IAM / SSO", 200),
        ("e_hpc", "HPC scheduler", 270),
        ("e_stor", "Storage", 340),
        ("e_dom", "CAE / MDAO apps", 410),
        ("e_ci", "CI / registry", 480),
    ]:
        doc.box(lbl, "rounded=1;whiteSpace=wrap;html=1;fillColor=#EEEEEE;strokeColor=#666;dashed=1;fontSize=10;", 860, y, 180, 44, cid=cid)
    edge(doc, "u_eng", "gof")
    edge(doc, "d_data", "e_life", dashed=True)
    edge(doc, "d_exec", "e_hpc", dashed=True)
    edge(doc, "d_exec", "e_dom", dashed=True)
    write_doc(doc, "02_System_Context.drawio")


def logical_architecture():
    doc = DrawioDoc("hldd-04-logical", "04 Logical Architecture", 1400, 780)
    title(doc, "<b>HLDD 4.5 — TO-BE Logical Architecture</b>", 1320)
    legend(doc, "Blue = platform domains &nbsp;|&nbsp; Gold = cross-cutting services &nbsp;|&nbsp; Arrows = primary dependencies", 50, 600)
    xc = doc.box("Cross-cutting services", "swimlane;whiteSpace=wrap;html=1;startSize=24;fillColor=#FFF9E6;strokeColor=#CC9900;", 40, 108, 1320, 72, cid="xc")
    for cid, lbl, x in [("x1", "Run ID", 20), ("x2", "MDAC", 150), ("x3", "Lineage", 280), ("x4", "Observe", 410), ("x5", "Notify", 540)]:
        doc.box(lbl, "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFDE7;strokeColor=#CC9900;fontSize=10;", x, 38, 120, 32, cid=cid, parent=xc)
    z = doc.box("Platform domains (TO-BE)", "swimlane;whiteSpace=wrap;html=1;startSize=28;fillColor=#E8F4FC;strokeColor=#005AAB;fontStyle=1;", 40, 200, 1320, 320, cid="z")
    items = [
        ("lc1", "Governed Data &amp; Continuity", 20, 45, 400, 70),
        ("lc2", "Experience &amp; Access", 440, 45, 400, 70),
        ("lc3", "Execution Fabric", 860, 45, 420, 70),
        ("lc4", "Engineering Automation", 20, 140, 310, 70),
        ("lc5", "Software Delivery", 350, 140, 310, 70),
        ("lc6", "Global Federation", 680, 140, 300, 70),
        ("lc7", "Runtime Platforms", 1000, 140, 280, 70),
    ]
    for cid, lbl, x, y, w, h in items:
        doc.box(f"<b>{lbl}</b>", "rounded=1;whiteSpace=wrap;html=1;fillColor=#B8D4EF;strokeColor=#005AAB;fontSize=10;", x, y, w, h, cid=cid, parent=z)
    edge(doc, "lc4", "lc3")
    edge(doc, "lc3", "lc1")
    edge(doc, "lc5", "lc7", dashed=True)
    doc.box("AI/ML zone spans Execution + Automation + Data (same MDAC)", "text;html=1;strokeColor=none;fillColor=none;fontSize=10;", 40, 540, 1320, 24, cid="note")
    write_doc(doc, "04_Logical_Architecture.drawio")


def capability_view():
    doc = DrawioDoc("hldd-05-cap", "05 Capability View", 1700, 360)
    title(doc, "<b>HLDD 3.1 — Swimlanes S1–S7 to Platform Capabilities</b>", 1620)
    legend(doc, "Light blue = swimlane focus &nbsp;|&nbsp; Gold = shared spine (C1–C7)", 50, 400)
    swim = [
        ("S1", "Data &amp; compliance"),
        ("S2", "Dev &amp; deploy"),
        ("S3", "CAE execution"),
        ("S4", "Workflows"),
        ("S5", "MDAO"),
        ("S6", "AI / ML"),
        ("S7", "Global / EE"),
    ]
    x = 40
    for sid, title_s in swim:
        doc.box(f"<b>{sid}</b><br>{title_s}", "rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F4FC;strokeColor=#005AAB;align=center;fontSize=10;", x, 100, 210, 80, cid=f"sl_{sid}")
        x += 228
    doc.box(
        "<b>Shared spine</b><br>Refs · MDAC · Execution · Run ID · Runtime · Session",
        "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFD54F;strokeColor=#F9A825;fontStyle=1;align=center;fontSize=10;",
        480, 220, 740, 60, cid="hub",
    )
    for sid in ["S1", "S2", "S3", "S4", "S5", "S6", "S7"]:
        edge(doc, f"sl_{sid}", "hub", dashed=True)
    write_doc(doc, "05_Capability_View.drawio")


def integration_view():
    doc = DrawioDoc("hldd-06-integ", "06 Integration View", 1200, 620)
    title(doc, "<b>HLDD 4.1 — Integration View</b>", 1120)
    legend(doc, "Blue = GoF &nbsp;|&nbsp; Grey dashed = enterprise (authority external) &nbsp;|&nbsp; Dashed arrow = integrate", 50)
    doc.box("GoF Control Plane", "rounded=1;whiteSpace=wrap;html=1;fillColor=#B8D4EF;strokeColor=#005AAB;fontStyle=1;align=center;", 420, 180, 360, 280, cid="gof")
    for cid, lbl, x, y in [
        ("i1", "SPDM / PLM", 80, 140),
        ("i2", "IAM", 80, 240),
        ("i3", "HPC", 80, 340),
        ("i4", "Storage", 80, 440),
        ("i5", "CI / CD", 900, 140),
        ("i6", "Registry", 900, 240),
        ("i7", "Licenses", 900, 340),
    ]:
        doc.box(lbl, "rounded=1;whiteSpace=wrap;html=1;fillColor=#EEEEEE;strokeColor=#666;dashed=1;fontSize=11;", x, y, 160, 56, cid=cid)
        edge(doc, "gof", cid, dashed=True)
    write_doc(doc, "06_Integration_View.drawio")


def data_policy_view():
    doc = DrawioDoc("hldd-07-data", "07 Data Policy", 1300, 480)
    title(doc, "<b>HLDD 4.2 — Data &amp; Policy Flow</b>", 1220)
    legend(doc, "Blue = GoF behavior &nbsp;|&nbsp; Grey = external authority", 50)
    doc.box("User / Automation", "rounded=1;whiteSpace=wrap;html=1;fillColor=#fff;strokeColor=#666;", 40, 130, 140, 50, cid="actor")
    chain = [("r", "References"), ("m", "MDAC"), ("s", "SPDM stage"), ("l", "Lineage"), ("c", "Cache policy")]
    x = 220
    prev = "actor"
    for cid, lbl in chain:
        doc.box(f"<b>{lbl}</b>", "rounded=1;whiteSpace=wrap;html=1;fillColor=#B8D4EF;strokeColor=#005AAB;fontSize=11;", x, 125, 150, 60, cid=cid)
        edge(doc, prev, cid)
        prev = cid
    doc.box("SPDM authority", "rounded=1;whiteSpace=wrap;html=1;fillColor=#EEEEEE;strokeColor=#666;dashed=1;", 520, 280, 180, 50, cid="spdm")
    doc.box("Storage tiers", "rounded=1;whiteSpace=wrap;html=1;fillColor=#EEEEEE;strokeColor=#666;dashed=1;", 760, 280, 180, 50, cid="stor")
    edge(doc, "s", "spdm", dashed=True)
    edge(doc, "c", "stor", dashed=True)
    write_doc(doc, "07_Data_Policy_View.drawio")


def runtime_execution_view():
    doc = DrawioDoc("hldd-08-runtime", "08 Runtime Execution", 1300, 420)
    title(doc, "<b>HLDD 4.5 — Runtime / Execution Path</b>", 1220)
    legend(doc, "Solid = platform path &nbsp;|&nbsp; Last box = integrated scheduler (not owned)", 50, 480)
    steps = [
        ("e1", "Session / API"),
        ("e2", "Workflow (opt.)"),
        ("e3", "Execution fabric"),
        ("e4", "Env bind"),
        ("e5", "Scheduler"),
        ("e6", "Lineage + refs"),
    ]
    x = 40
    prev = None
    for cid, lbl in steps:
        sty = "rounded=1;whiteSpace=wrap;html=1;fillColor=#B8D4EF;strokeColor=#005AAB;fontSize=10;"
        if cid == "e5":
            sty = "rounded=1;whiteSpace=wrap;html=1;fillColor=#EEEEEE;strokeColor=#666;dashed=1;fontSize=10;"
        doc.box(lbl, sty, x, 120, 170, 55, cid=cid)
        if prev:
            edge(doc, prev, cid)
        prev = cid
    write_doc(doc, "08_Runtime_Execution_View.drawio")


def out_of_scope():
    doc = DrawioDoc("hldd-09-oos", "09 Out of Scope", 1100, 520)
    title(doc, "<b>HLDD 5.3 — Boundary View</b>", 1020)
    legend(doc, "Blue OWN &nbsp;|&nbsp; Grey INTEG &nbsp;|&nbsp; Dashed OUT", 50, 420)
    doc.box("<b>OWN</b><br>Policy, refs, runs, workflows, env catalog", "rounded=1;whiteSpace=wrap;html=1;fillColor=#B8D4EF;strokeColor=#005AAB;align=center;fontSize=11;", 80, 120, 260, 100, cid="own")
    doc.box("<b>INTEGRATE</b><br>SPDM, IAM, HPC, storage, CI, CAE", "rounded=1;whiteSpace=wrap;html=1;fillColor=#EEEEEE;strokeColor=#666;align=center;fontSize=11;", 420, 120, 260, 100, cid="integ")
    doc.box("<b>OUT</b><br>PLM ownership, solver IP, legal, partner IT", "rounded=0;whiteSpace=wrap;html=1;fillColor=#FAFAFA;strokeColor=#999;dashed=1;align=center;fontSize=11;", 760, 120, 260, 100, cid="out")
    write_doc(doc, "09_Out_of_Scope_Boundary.drawio")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    system_context()
    logical_architecture()
    capability_view()
    integration_view()
    data_policy_view()
    runtime_execution_view()
    out_of_scope()


if __name__ == "__main__":
    main()
