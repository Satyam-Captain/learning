"""
Generate GoF + OpenStack + Open OnDemand cloud stack architecture (draw.io).
Maps workshop capabilities to stack components; separates what OpenStack/OOD cannot solve.
Uses the same DrawioDoc as swimlane diagrams (browser-safe XML).
"""
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(r"c:\Users\satti\Desktop\GoF_Architecture_Workspace\10_diagrams\cloud_stack")

_spec = importlib.util.spec_from_file_location("gof_drawio", ROOT / "_generate_swimlane_drawio.py")
_gof_drawio = importlib.util.module_from_spec(_spec)
sys.modules["gof_drawio"] = _gof_drawio
_spec.loader.exec_module(_gof_drawio)
DrawioDoc = _gof_drawio.DrawioDoc
OUT.mkdir(parents=True, exist_ok=True)

# Styles
S_TITLE = "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=18;fontStyle=1"
S_SUB = "text;html=1;strokeColor=none;fillColor=none;align=center;fontSize=11;fontColor=#666666"
S_LAYER = "swimlane;whiteSpace=wrap;html=1;startSize=32;fillColor=#F5F5F5;strokeColor=#333333;fontStyle=1"
S_OOD = "rounded=1;whiteSpace=wrap;html=1;fillColor=#E3F2FD;strokeColor=#1565C0;fontStyle=1"
S_OSS = "rounded=1;whiteSpace=wrap;html=1;fillColor=#E8F5E9;strokeColor=#2E7D32;"
S_GOF = "rounded=1;whiteSpace=wrap;html=1;fillColor=#B8D4EF;strokeColor=#005AAB;fontStyle=1"
S_GOF_ORCH = "rounded=1;whiteSpace=wrap;html=1;fillColor=#B8E8E8;strokeColor=#2E8B8B;fontStyle=1"
S_EXT = "rounded=1;whiteSpace=wrap;html=1;fillColor=#EEEEEE;strokeColor=#666666;dashed=1;"
S_SEP = "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFF3E0;strokeColor=#E65100;strokeWidth=2;dashed=1;"
S_LEG = "rounded=1;whiteSpace=wrap;html=1;fillColor=#ffffff;strokeColor=#333;align=left;spacingLeft=8;fontSize=10;"
S_EDGE = "edgeStyle=orthogonalEdgeStyle;rounded=1;html=1;endArrow=classic;strokeWidth=1;"
S_EDGE_D = S_EDGE + "dashed=1;strokeColor=#666666;"
S_EDGE_G = S_EDGE + "strokeColor=#005AAB;"
S_EDGE_O = S_EDGE + "strokeColor=#2E7D32;"


def lane(doc, cid, title, x, y, w, h, fill="#F5F5F5"):
    sty = f"swimlane;whiteSpace=wrap;html=1;startSize=36;fillColor={fill};strokeColor=#333;fontStyle=1"
    return doc.box(title, sty, x, y, w, h, cid=cid)


def cell(doc, cid, val, sty, x, y, w, h, parent="1"):
    return doc.box(val, sty, x, y, w, h, cid=cid, parent=parent)


def add_edge(doc, src, tgt, dashed=False, color=None):
    eid = doc.nid()
    sty = S_EDGE_D if dashed else S_EDGE_G
    if color == "oss":
        sty = S_EDGE_O
    doc.add(eid, "", sty, edge=True, source=src, target=tgt)
    return eid


def build():
    doc = DrawioDoc("gof-openstack-ood", "OpenStack + OOD + GoF", 2400, 1700)
    cell(doc, "t1", "<b>GoF on OpenStack-class cloud + Open OnDemand</b>", S_TITLE, 40, 10, 2320, 36)
    cell(
        doc,
        "t2",
        "Detailed reference stack for architects | Green = OpenStack (or Ceph-backed) | Blue = GoF owns | "
        "Orange dashed = outside stack | All arrows = interfaces",
        S_SUB,
        40,
        48,
        2320,
        28,
    )
    cell(
        doc,
        "leg",
        "<b>Legend</b><br>"
        "Blue = GoF platform (build) | Green = OpenStack services | Light blue = Open OnDemand<br>"
        "Teal = GoF orchestrates via APIs | Grey dashed = external (not replaced by OpenStack)<br>"
        "Solid arrows = primary interfaces | Dashed = integrate / optional",
        S_LEG,
        40,
        82,
        480,
        72,
    )

    # === LAYER 1: Access ===
    z_acc = lane(doc,"z_acc", "L1 - Access & experience", 40, 170, 1160, 200, "#E3F2FD")
    ood = cell(doc,
        "ood",
        "<b>Open OnDemand</b><br>"
        "<font style='font-size:9px'>HPC web portal: files, shell, jobs, "
        "interactive apps (Jupyter, VS Code, VNC)<br>"
        "Auth via Keystone/OIDC | Submit to Slurm/PBS adapters</font>",
        S_OOD,
        20,
        50,
        340,
        130,
        z_acc,
    )
    gof_sess = cell(doc,
        "gof_sess",
        "<b>GoF session broker</b> (OWN)<br>"
        "<font style='font-size:9px'>SSO to SPDM, OOD, tools | "
        "Engineering workspace context</font>",
        S_GOF,
        380,
        50,
        280,
        130,
        z_acc,
    )
    gof_api = cell(doc,
        "gof_api",
        "<b>GoF public APIs</b> (OWN)<br>"
        "<font style='font-size:9px'>Batch submit, refs, policy check, "
        "workflow run status</font>",
        S_GOF,
        680,
        50,
        280,
        130,
        z_acc,
    )
    vdi = cell(doc,
        "vdi",
        "<b>VDI / desktop</b> (INTEGRATE)<br>"
        "<font style='font-size:9px'>Citrix/Horizon - parallel path to OOD</font>",
        S_EXT,
        980,
        50,
        150,
        130,
        z_acc,
    )

    # === LAYER 2: Identity ===
    z_id = lane(doc,"z_id", "L2 - Identity & policy", 40, 390, 1160, 120, "#F5F5F5")
    keystone = cell(doc,
        "keystone",
        "<b>Keystone</b> (OpenStack IAM)<br>"
        "<font style='font-size:9px'>Projects, domains, roles, service catalog, "
        "OIDC/SAML federation</font>",
        S_OSS,
        20,
        48,
        260,
        60,
        z_id,
    )
    gof_mdac = cell(doc,
        "gof_mdac",
        "<b>GoF MDAC / policy engine</b> (OWN)<br>"
        "<font style='font-size:9px'>OPA-class ABAC on refs, data, deploy, runs | "
        "Uses Keystone claims + SPDM tags</font>",
        S_GOF,
        300,
        48,
        320,
        60,
        z_id,
    )
    corp_idp = cell(doc,
        "corp_idp",
        "<b>Corporate IdP</b> (EXTERNAL)<br>"
        "<font style='font-size:9px'>OneLogin/ADFS - federates to Keystone</font>",
        S_EXT,
        640,
        48,
        200,
        60,
        z_id,
    )
    barbican = cell(doc,
        "barbican",
        "<b>Barbican</b> (optional)<br>"
        "<font style='font-size:9px'>Secrets for VMs/containers</font>",
        S_OSS,
        860,
        48,
        160,
        60,
        z_id,
    )

    # === LAYER 3: GoF control plane ===
    z_gof = lane(doc,"z_gof", "L3 - GoF control plane (not a single OpenStack project)", 40, 530, 1160, 200, "#E8F4FC")
    gof_ref = cell(doc,"gof_ref", "<b>Reference &amp; lineage service</b><br>Immutable IDs", S_GOF, 20, 48, 200, 55, z_gof)
    gof_run = cell(doc,"gof_run", "<b>Run registry &amp; observability</b><br>Platform run ID", S_GOF, 240, 48, 200, 55, z_gof)
    gof_wf = cell(doc,"gof_wf", "<b>Workflow run engine</b><br>State, notify", S_GOF, 460, 48, 200, 55, z_gof)
    gof_env = cell(doc,"gof_env", "<b>Environment catalog</b><br>Guix/Spack/SIF refs", S_GOF, 680, 48, 200, 55, z_gof)
    gof_cache = cell(doc,
        "gof_cache",
        "<b>Data placement orchestrator</b><br>Cache policy near compute",
        S_GOF_ORCH,
        900,
        48,
        220,
        55,
        z_gof,
    )
    gof_note = cell(doc,
        "gof_note",
        "GoF control plane sits <b>above</b> OpenStack APIs (Nova, Manila, Neutron) and <b>beside</b> Slurm - "
        "it does not replace Heat or the scheduler",
        "text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=10;fontColor=#003366;",
        20,
        120,
        1100,
        30,
        z_gof,
    )

    # === LAYER 4: Orchestration ===
    z_orch = lane(doc,"z_orch", "L4 - Orchestration", 40, 750, 1160, 130, "#E8F5E9")
    heat = cell(doc,
        "heat",
        "<b>Heat</b> (OpenStack orchestration)<br>"
        "<font style='font-size:9px'>Templates for VMs, networks, volumes | "
        "Optional for infra bursts</font>",
        S_OSS,
        20,
        48,
        240,
        70,
        z_orch,
    )
    magnum = cell(doc,
        "magnum",
        "<b>Magnum</b> (K8s clusters)<br>"
        "<font style='font-size:9px'>ML/GPU pools on OpenStack</font>",
        S_OSS,
        280,
        48,
        200,
        70,
        z_orch,
    )
    slurm = cell(doc,
        "slurm",
        "<b>Slurm / LSF / PBS</b> (EXTERNAL to OpenStack)<br>"
        "<font style='font-size:9px'>Primary HPC scheduler - OOD and GoF submit here</font>",
        S_SEP,
        500,
        48,
        280,
        70,
        z_orch,
    )
    jenkins = cell(doc,
        "jenkins",
        "<b>CI (Jenkins/GitLab)</b> (EXTERNAL)<br>"
        "<font style='font-size:9px'>Triggers GoF workflow / batch</font>",
        S_EXT,
        800,
        48,
        200,
        70,
        z_orch,
    )

    # === LAYER 5: Compute ===
    z_comp = lane(doc,"z_comp", "L5 - Compute", 40, 900, 1160, 150, "#E8F5E9")
    nova = cell(doc,
        "nova",
        "<b>Nova</b> (VM compute)<br>"
        "<font style='font-size:9px'>Interactive nodes, workers, gateways</font>",
        S_OSS,
        20,
        48,
        200,
        85,
        z_comp,
    )
    ironic = cell(doc,
        "ironic",
        "<b>Ironic</b> (bare metal)<br>"
        "<font style='font-size:9px'>HPC-style dedicated nodes (where used)</font>",
        S_OSS,
        240,
        48,
        200,
        85,
        z_comp,
    )
    k8s = cell(doc,
        "k8s",
        "<b>Kubernetes workers</b><br>"
        "<font style='font-size:9px'>Via Magnum - GPU training class</font>",
        S_OSS,
        460,
        48,
        200,
        85,
        z_comp,
    )
    cae = cell(doc,
        "cae",
        "<b>CAE / solver jobs</b> (EXTERNAL apps)<br>"
        "<font style='font-size:9px'>Abaqus, Nastran, Star-CCM+ on compute nodes</font>",
        S_SEP,
        680,
        48,
        240,
        85,
        z_comp,
    )
    gpu = cell(doc,
        "gpu",
        "<b>GPU execution class</b><br>"
        "<font style='font-size:9px'>GoF routes by policy - may be Slurm or K8s</font>",
        S_GOF,
        940,
        48,
        180,
        85,
        z_comp,
    )

    # === LAYER 6: Storage ===
    z_stor = lane(doc,"z_stor", "L6 - Storage", 40, 1070, 1160, 150, "#E8F5E9")
    manila = cell(doc,
        "manila",
        "<b>Manila</b> (shared filesystem)<br>"
        "<font style='font-size:9px'>NFS shares per project | Maps S1 provisioning templates</font>",
        S_OSS,
        20,
        48,
        240,
        85,
        z_stor,
    )
    cinder = cell(doc,
        "cinder",
        "<b>Cinder</b> (block volumes)<br>"
        "<font style='font-size:9px'>VM disks, scratch volumes</font>",
        S_OSS,
        280,
        48,
        200,
        85,
        z_stor,
    )
    ceph = cell(doc,
        "ceph",
        "<b>Ceph / object (RGW)</b><br>"
        "<font style='font-size:9px'>Often under Manila/Cinder/Glance</font>",
        S_OSS,
        500,
        48,
        200,
        85,
        z_stor,
    )
    glance = cell(doc,
        "glance",
        "<b>Glance</b> (images)<br>"
        "<font style='font-size:9px'>VM/SIF base images</font>",
        S_OSS,
        720,
        48,
        160,
        85,
        z_stor,
    )
    spdm_stor = cell(doc,
        "spdm_stor",
        "<b>SPDM / PLM vault</b> (EXTERNAL)<br>"
        "<font style='font-size:9px'>Lifecycle truth - GoF stages copies to Manila</font>",
        S_SEP,
        900,
        48,
        220,
        85,
        z_stor,
    )

    # === LAYER 7: Network ===
    z_net = lane(doc,"z_net", "L7 - Network", 40, 1240, 1160, 100, "#E8F5E9")
    neutron = cell(doc,
        "neutron",
        "<b>Neutron</b> (SDN)<br>"
        "<font style='font-size:9px'>Networks, subnets, security groups, floating IPs | "
        "Geo/export segments via policy</font>",
        S_OSS,
        20,
        48,
        500,
        45,
        z_net,
    )
    egress = cell(doc,
        "egress",
        "<b>Egress / proxy</b> (EXTERNAL)<br>"
        "<font style='font-size:9px'>Netskope, corporate firewall</font>",
        S_EXT,
        540,
        48,
        200,
        45,
        z_net,
    )

    # === RIGHT COLUMN: Outside stack ===
    z_ext = lane(doc,"z_ext", "Outside OpenStack - keep separate (GoF integrates only)", 1220, 170, 1140, 1170, "#FFF3E0")
    ext_items = [
        ("SPDM / PLM (Teamcenter, Aras, 3DX)", "Lifecycle authority - GoF orchestrates stage/publish"),
        ("Engineering domain tools", "Eve, GEMSEO, Design Manager, Isight - compose via GoF"),
        ("Artifact registry (Harbor, Artifactory)", "Images/packages - GoF enforces MDAC on pull"),
        ("Enterprise ModelOps / cloud ML", "AWS SageMaker-class - policy routing only"),
        ("License servers (FlexLM, etc.)", "GoF pre-check before submit"),
        ("Archive / tape / cold tier", "Long retention beyond Manila - orchestrated retrieval"),
        ("Legal / export control (ACDS)", "Classification master - feeds MDAC"),
        ("Partner IT / EE networks", "Federation gateway - not OpenStack multi-site alone"),
        ("MDAO mathematics", "OpenMDAO/Dakota - external graphs call GoF batch API"),
    ]
    ey = 48
    ext_ids = []
    for i, (title, sub) in enumerate(ext_items):
        eid = cell(doc,
            f"ext{i}",
            f"<b>{title}</b><br><font style='font-size:9px'>{sub}</font>",
            S_SEP,
            15,
            ey,
            1110,
            58,
            z_ext,
        )
        ext_ids.append(eid)
        ey += 64

    cell(
        doc,
        "ext_note",
        "<b>Rule:</b> If OpenStack + OOD cannot solve it, it stays in this column - "
        "linked to GoF via APIs, not buried inside Nova",
        "text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=10;fontColor=#E65100;",
        15,
        ey + 10,
        1110,
        40,
        z_ext,
    )

    # === INTERFACE EDGES (all linked) ===
    # User access flow
    add_edge(doc, "ood", "keystone", dashed=True)
    add_edge(doc,"gof_sess", "keystone")
    add_edge(doc,"gof_api", "gof_mdac")
    add_edge(doc,"gof_sess", "ood", color="oss")
    add_edge(doc,"vdi", "gof_sess", dashed=True)

    add_edge(doc,"keystone", "corp_idp", dashed=True)
    add_edge(doc,"gof_mdac", "keystone", dashed=True)

    # GoF to orchestration
    add_edge(doc,"gof_api", "gof_run")
    add_edge(doc,"gof_run", "slurm")
    add_edge(doc,"gof_wf", "jenkins", dashed=True)
    add_edge(doc,"gof_wf", "heat", dashed=True)
    add_edge(doc,"gof_env", "glance", dashed=True)
    add_edge(doc,"gof_cache", "manila")
    add_edge(doc,"gof_ref", "spdm_stor", dashed=True)

    # OOD to scheduler and storage
    add_edge(doc,"ood", "slurm", color="oss")
    add_edge(doc,"ood", "manila", color="oss")

    # OpenStack internal typical
    add_edge(doc,"nova", "neutron", color="oss")
    add_edge(doc,"nova", "cinder", color="oss")
    add_edge(doc,"nova", "manila", color="oss")
    add_edge(doc,"nova", "glance", color="oss")
    add_edge(doc,"heat", "nova", color="oss")
    add_edge(doc,"magnum", "k8s", color="oss")
    add_edge(doc,"manila", "ceph", color="oss")
    add_edge(doc,"cinder", "ceph", color="oss")

    # Compute execution
    add_edge(doc,"slurm", "nova", dashed=True)
    add_edge(doc,"slurm", "ironic", dashed=True)
    add_edge(doc,"slurm", "cae")
    add_edge(doc,"gof_run", "cae", dashed=True)
    add_edge(doc,"gpu", "k8s", dashed=True)
    add_edge(doc,"gpu", "slurm", dashed=True)

    # External integrations from GoF
    add_edge(doc,"gof_ref", "ext0", dashed=True)
    add_edge(doc,"gof_wf", "ext1", dashed=True)
    add_edge(doc,"gof_env", "ext2", dashed=True)
    add_edge(doc,"gof_mdac", "ext6", dashed=True)
    add_edge(doc,"gof_cache", "ext0", dashed=True)
    add_edge(doc,"slurm", "ext4", dashed=True)
    add_edge(doc,"neutron", "egress", dashed=True)

    # Bottom narrative
    cell(
        doc,
        "flow",
        "<b>Typical engineer path:</b> Browser -&gt; Open OnDemand (auth via Keystone) -&gt; "
        "files on Manila / jobs to Slurm -&gt; GoF APIs add references, MDAC, run IDs, SPDM staging. "
        "<b>Typical automation path:</b> CI/MDAO -&gt; GoF workflow API -&gt; Slurm batch -&gt; "
        "results as references back to SPDM.",
        "rounded=0;whiteSpace=wrap;html=1;fillColor=#FFFDE7;strokeColor=#CC9900;fontSize=11;align=left;",
        40,
        1380,
        2320,
        55,
    )

    cell(
        doc,
        "map",
        "<b>Workshop mapping:</b> S1 data -&gt; Manila + GoF cache/MDAC | S2 dev -&gt; OOD + registry + GoF env | "
        "S3 runs -&gt; OOD/Slurm + GoF run API | S4 workflows -&gt; GoF engine + Heat optional | "
        "S5 MDAO -&gt; Slurm adapter (separate) | S6 ML -&gt; Magnum/K8s or Slurm GPU | S7 federation -&gt; separate column",
        "text;html=1;strokeColor=none;fillColor=none;align=left;fontSize=10;",
        40,
        1450,
        2320,
        45,
    )

    path = OUT / "GoF_OpenStack_OOD_Cloud_Architecture.drawio"
    path.write_text(doc.render(), encoding="utf-8")
    print("wrote", path)
    return path


if __name__ == "__main__":
    build()
