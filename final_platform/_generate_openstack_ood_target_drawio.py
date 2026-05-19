"""Generate OpenStack + OOD + GoF target architecture (browser-safe draw.io)."""
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "final_platform"

_spec = importlib.util.spec_from_file_location("gof_drawio", ROOT / "_generate_swimlane_drawio.py")
_mod = importlib.util.module_from_spec(_spec)
sys.modules["gof_drawio"] = _mod
_spec.loader.exec_module(_mod)
DrawioDoc = _mod.DrawioDoc

# Styles
S_TITLE = "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=17;fontStyle=1"
S_SUB = "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=10;fontColor=#666666"
S_LEG = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333;align=left;spacingLeft=8;fontSize=9;"
S_USER = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#666666;"
S_OOD = "rounded=1;whiteSpace=wrap;html=1;fillColor=#C8E6C9;strokeColor=#2E7D32;fontStyle=1"
S_GOF = "rounded=1;whiteSpace=wrap;html=1;fillColor=#B8D4EF;strokeColor=#005AAB;fontStyle=1"
S_GOF_ORCH = "rounded=1;whiteSpace=wrap;html=1;fillColor=#B8E8E8;strokeColor=#2E8B8B;"
S_OSS = "rounded=1;whiteSpace=wrap;html=1;fillColor=#E1BEE7;strokeColor=#7B1FA2;"
S_LSF = "rounded=1;whiteSpace=wrap;html=1;fillColor=#E8EAF6;strokeColor=#3949AB;fontStyle=1"
S_EXT = "rounded=1;whiteSpace=wrap;html=1;fillColor=#EEEEEE;strokeColor=#666666;"
S_GAP = "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#E65100;dashed=1;"
S_OUT = "rounded=0;whiteSpace=wrap;html=1;fillColor=#FAFAFA;strokeColor=#999999;dashed=1;fontColor=#666666;"
S_LANE = "swimlane;whiteSpace=wrap;html=1;startSize=28;fillColor={fill};strokeColor=#333;fontStyle=1"
S_EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;strokeWidth=1;strokeColor=#333333;"
S_EDGE_D = S_EDGE.replace("strokeColor=#333333", "strokeColor=#666666;dashed=1;")


def lane(doc, cid, title, x, y, w, h, fill):
    return doc.box(title, S_LANE.format(fill=fill), x, y, w, h, cid=cid)


def edge(doc, src, tgt, dashed=False):
    eid = doc.nid()
    doc.add(eid, "", S_EDGE_D if dashed else S_EDGE, edge=True, source=src, target=tgt)
    return eid


def build():
    doc = DrawioDoc("openstack-ood-gof-target", "OpenStack + OOD + GoF Target", 1900, 1280)
    doc.box(
        "<b>GISEH of Future — Target Architecture (OpenStack + Open OnDemand)</b>",
        S_TITLE,
        40,
        12,
        1820,
        40,
        cid="title",
    )
    doc.box(
        "Realistic placement: green = OOD | purple = OpenStack | blue = GoF build | grey = enterprise integrate | orange = gap/custom | dashed = out of scope",
        S_SUB,
        40,
        54,
        1820,
        24,
        cid="sub",
    )
    doc.box(
        "<b>Legend</b><br>"
        "<font color=#2E7D32>■</font> Open OnDemand &nbsp; "
        "<font color=#7B1FA2>■</font> OpenStack &nbsp; "
        "<font color=#005AAB>■</font> GoF control plane &nbsp; "
        "<font color=#3949AB>■</font> LSF/HPC/GISEH &nbsp; "
        "<font color=#666666>■</font> Enterprise &nbsp; "
        "<font color=#E65100>▢</font> Custom gap &nbsp; "
        "<font color=#999999>▢</font> Out of scope",
        S_LEG,
        40,
        82,
        560,
        52,
        cid="leg",
    )

    # LEFT — Users
    z_users = lane(doc, "z_users", "Users", 40, 150, 170, 680, "#F5F5F5")
    doc.box("Simulation engineers", S_USER, 15, 42, 140, 44, cid="u1", parent=z_users)
    doc.box("Software developers", S_USER, 15, 98, 140, 44, cid="u2", parent=z_users)
    doc.box("Workflow owners", S_USER, 15, 154, 140, 44, cid="u3", parent=z_users)
    doc.box("EE partners", S_USER, 15, 210, 140, 44, cid="u4", parent=z_users)
    doc.box("CI / automation", S_USER, 15, 266, 140, 44, cid="u5", parent=z_users)

    # CENTER — stacked zones
    cx, cw = 230, 720

    z_ood = lane(doc, "z_ood", "Open OnDemand Portal", cx, 150, cw, 150, "#E8F5E9")
    doc.box(
        "<b>Job submission UI</b><br><font style='font-size:9px'>Adapter to LSF | queues, scripts, array jobs</font>",
        S_OOD,
        15,
        42,
        160,
        95,
        cid="ood_jobs",
        parent=z_ood,
    )
    doc.box(
        "<b>Interactive apps</b><br><font style='font-size:9px'>Jupyter, VS Code, VNC, desktops</font>",
        S_OOD,
        185,
        42,
        160,
        95,
        cid="ood_apps",
        parent=z_ood,
    )
    doc.box(
        "<b>Terminal &amp; files</b><br><font style='font-size:9px'>Home/project browser on shared storage</font>",
        S_OOD,
        355,
        42,
        160,
        95,
        cid="ood_files",
        parent=z_ood,
    )
    doc.box(
        "<b>Visualization launch</b><br><font style='font-size:9px'>Post-processing app hooks</font>",
        S_OOD,
        525,
        42,
        175,
        95,
        cid="ood_viz",
        parent=z_ood,
    )

    z_gof = lane(doc, "z_gof", "GoF Control Plane (custom build)", cx, 320, cw, 200, "#E8F4FC")
    doc.box("Policy / MDAC", S_GOF, 15, 42, 130, 50, cid="gof_mdac", parent=z_gof)
    doc.box("Reference resolution", S_GOF, 155, 42, 130, 50, cid="gof_ref", parent=z_gof)
    doc.box("Run identity", S_GOF, 295, 42, 120, 50, cid="gof_run", parent=z_gof)
    doc.box("Lineage &amp; audit", S_GOF, 425, 42, 120, 50, cid="gof_lin", parent=z_gof)
    doc.box("Workflow state", S_GOF, 555, 42, 145, 50, cid="gof_wf", parent=z_gof)
    doc.box("SPDM stage/publish", S_GOF_ORCH, 15, 105, 165, 50, cid="gof_spdm", parent=z_gof)
    doc.box("Placement &amp; routing", S_GOF, 190, 105, 145, 50, cid="gof_place", parent=z_gof)
    doc.box("Notify / observe", S_GOF, 345, 105, 130, 50, cid="gof_obs", parent=z_gof)
    doc.box("Session broker APIs", S_GOF, 485, 105, 215, 50, cid="gof_api", parent=z_gof)
    doc.box(
        "<font style='font-size:9px'>OOD is UX only — GoF owns policy, refs, run IDs, digital thread</font>",
        "text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=9;fontColor=#003366;",
        15,
        165,
        680,
        22,
        cid="gof_note",
        parent=z_gof,
    )

    z_exec = lane(doc, "z_exec", "Execution &amp; Runtime", cx, 540, cw, 290, "#F3E5F5")
    doc.box(
        "<b>LSF / HPC production batch</b><br><font style='font-size:9px'>Queues, fairshare, license integration, large CAE</font>",
        S_LSF,
        15,
        42,
        220,
        75,
        cid="lsf",
        parent=z_exec,
    )
    doc.box(
        "<b>OpenStack private cloud</b><br><font style='font-size:9px'>Nova, Neutron, Cinder, Manila, Glance, Heat</font>",
        S_OSS,
        250,
        42,
        200,
        75,
        cid="oss",
        parent=z_exec,
    )
    doc.box(
        "<b>Dev / sandbox VMs</b><br><font style='font-size:9px'>Tenant-isolated engineering sandboxes</font>",
        S_OSS,
        465,
        42,
        120,
        75,
        cid="oss_dev",
        parent=z_exec,
    )
    doc.box(
        "<b>Runtime catalog</b><br><font style='font-size:9px'>Guix, Spack, modules, SIF refs</font>",
        S_GOF,
        15,
        130,
        155,
        60,
        cid="gof_env",
        parent=z_exec,
    )
    doc.box(
        "<b>Containers / Apptainer</b><br><font style='font-size:9px'>Executed on LSF or K8s workers</font>",
        S_GAP,
        180,
        130,
        155,
        60,
        cid="rt_cont",
        parent=z_exec,
    )
    doc.box(
        "<b>GPU execution classes</b><br><font style='font-size:9px'>Policy route: LSF GPU or Magnum/K8s</font>",
        S_GAP,
        345,
        130,
        155,
        60,
        cid="gpu_cls",
        parent=z_exec,
    )
    doc.box(
        "<b>Elastic service hosting</b><br><font style='font-size:9px'>Heat/Magnum for burst pools</font>",
        S_OSS,
        510,
        130,
        185,
        60,
        cid="oss_elastic",
        parent=z_exec,
    )
    doc.box(
        "<font style='font-size:9px'><b>Rule:</b> Production CAE at scale stays on LSF/HPC — OpenStack hosts sandboxes, gateways, and elastic pools, not solver logic</font>",
        "text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=9;",
        15,
        205,
        680,
        30,
        cid="exec_note",
        parent=z_exec,
    )

    # RIGHT — Enterprise
    z_ent = lane(doc, "z_ent", "Integrated Enterprise Systems", 970, 150, 380, 680, "#EEEEEE")
    ents = [
        ("ent_spdm", "<b>SPDM / PLM</b><br><font style='font-size:9px'>Lifecycle authority</font>"),
        ("ent_iam", "<b>IAM / SSO</b><br><font style='font-size:9px'>Corp IdP, claims</font>"),
        ("ent_stor", "<b>Storage tiers</b><br><font style='font-size:9px'>NAS, object, archive</font>"),
        ("ent_lic", "<b>License servers</b><br><font style='font-size:9px'>FlexLM, vendor</font>"),
        ("ent_ci", "<b>CI / CD</b><br><font style='font-size:9px'>Jenkins, GitLab</font>"),
        ("ent_art", "<b>Artifactory / Harbor</b><br><font style='font-size:9px'>Packages, images</font>"),
        ("ent_mo", "<b>ModelOps / ML</b><br><font style='font-size:9px'>Enterprise registry</font>"),
        ("ent_obs", "<b>Observability</b><br><font style='font-size:9px'>Splunk, Datadog-class</font>"),
        ("ent_cae", "<b>Domain CAE apps</b><br><font style='font-size:9px'>Abaqus, Nastran, Star-CCM+</font>"),
        ("ent_sky", "<b>Skywise / data platforms</b><br><font style='font-size:9px'>In-service data</font>"),
    ]
    ey = 42
    for cid, val in ents:
        doc.box(val, S_EXT, 15, ey, 345, 52, cid=cid, parent=z_ent)
        ey += 58

    # BOTTOM — Out of scope
    z_out = lane(doc, "z_out", "Explicitly out of scope (not GoF, not OpenStack, not OOD)", 40, 860, 1310, 110, "#FAFAFA")
    doc.box("SPDM/PLM product ownership", S_OUT, 15, 38, 200, 55, cid="out1", parent=z_out)
    doc.box("CAD authoring &amp; solver methodology", S_OUT, 225, 38, 200, 55, cid="out2", parent=z_out)
    doc.box("Legal / export classification ownership", S_OUT, 435, 38, 220, 55, cid="out3", parent=z_out)
    doc.box("Procurement &amp; license contracts", S_OUT, 665, 38, 200, 55, cid="out4", parent=z_out)
    doc.box("Partner internal IT", S_OUT, 875, 38, 180, 55, cid="out5", parent=z_out)
    doc.box("Datacenter / bare-metal lifecycle", S_OUT, 1065, 38, 220, 55, cid="out6", parent=z_out)

    # Arrows
    edge(doc, "u1", "ood_jobs")
    edge(doc, "u2", "ood_apps")
    edge(doc, "u3", "gof_api", dashed=True)
    edge(doc, "u4", "gof_mdac", dashed=True)
    edge(doc, "u5", "gof_wf", dashed=True)

    edge(doc, "ood_jobs", "gof_run")
    edge(doc, "ood_apps", "gof_api")
    edge(doc, "ood_files", "gof_ref")
    edge(doc, "ood_viz", "gof_place", dashed=True)

    edge(doc, "gof_run", "lsf")
    edge(doc, "gof_place", "lsf")
    edge(doc, "gof_place", "oss")
    edge(doc, "gof_env", "gof_run")
    edge(doc, "gof_spdm", "ent_spdm")
    edge(doc, "gof_mdac", "ent_iam")
    edge(doc, "gof_ref", "ent_stor", dashed=True)
    edge(doc, "gof_lin", "ent_obs", dashed=True)
    edge(doc, "gof_wf", "ent_ci", dashed=True)
    edge(doc, "gof_run", "ent_lic", dashed=True)
    edge(doc, "lsf", "ent_cae")
    edge(doc, "oss_dev", "oss")
    edge(doc, "gpu_cls", "lsf", dashed=True)
    edge(doc, "gpu_cls", "oss_elastic", dashed=True)
    edge(doc, "ent_spdm", "ent_stor", dashed=True)

    doc.box(
        "<b>SPDM remains lifecycle authority</b> — GoF stages governed copies; LSF executes; OOD is the engineer front door",
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFDE7;strokeColor=#CC9900;fontSize=10;align=center;",
        40,
        990,
        1310,
        36,
        cid="footer",
    )

    path = OUT / "OpenStack_OOD_GoF_Target_Architecture.drawio"
    path.write_text(doc.render(), encoding="utf-8")
    print("wrote", path)
    return path


if __name__ == "__main__":
    build()
