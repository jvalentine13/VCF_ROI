import pandas as pd

def parse_rvtools(filepath):
    """Parse RVTools xlsx and extract infrastructure data with health scoring."""
    try:
        xl = pd.ExcelFile(filepath, engine="openpyxl")
        sheets = xl.sheet_names
        data = {}

        # vInfo sheet - VM details
        if 'vInfo' in sheets:
            vinfo = xl.parse('vInfo')
            data['total_vms'] = len(vinfo)
            data['powered_on_vms'] = len(vinfo[vinfo['Powerstate'] == 'poweredOn']) if 'Powerstate' in vinfo.columns else 0
            data['powered_off_vms'] = len(vinfo[vinfo['Powerstate'] == 'poweredOff']) if 'Powerstate' in vinfo.columns else 0
            data['total_vcpu'] = int(vinfo['CPUs'].sum()) if 'CPUs' in vinfo.columns else 0
            data['total_vram_gb'] = round(vinfo['Memory'].sum() / 1024, 2) if 'Memory' in vinfo.columns else 0

            # OS breakdown
            if 'OS' in vinfo.columns:
                os_counts = vinfo['OS'].value_counts().to_dict()
                data['os_breakdown'] = os_counts
                windows_vms = sum(v for k, v in os_counts.items() if 'windows' in str(k).lower())
                linux_vms = sum(v for k, v in os_counts.items() if any(x in str(k).lower() for x in ['linux', 'red hat', 'ubuntu', 'centos', 'suse']))
                data['windows_vms'] = windows_vms
                data['linux_vms'] = linux_vms
                data['windows_ratio'] = round(windows_vms / max(data['total_vms'], 1), 2)

            # Oversized VM detection (more than 8 vCPU or 32GB RAM with low utilization proxy)
            if 'CPUs' in vinfo.columns:
                data['large_vms'] = int(len(vinfo[vinfo['CPUs'] >= 8]))
                data['oversized_candidates'] = int(len(vinfo[vinfo['CPUs'] >= 16]))

            # Old OS detection
            if 'OS' in vinfo.columns:
                old_os_keywords = ['2008', '2003', '2012', 'windows 7', 'centos 6', 'rhel 6']
                old_os = vinfo[vinfo['OS'].str.lower().str.contains('|'.join(old_os_keywords), na=False)]
                data['old_os_vms'] = len(old_os)
                data['old_os_list'] = old_os['OS'].value_counts().to_dict() if len(old_os) > 0 else {}

        # vHost sheet - host details
        if 'vHost' in sheets:
            vhost = xl.parse('vHost')
            data['total_hosts'] = len(vhost)
            data['total_physical_cores'] = int(vhost['# Cores'].sum()) if '# Cores' in vhost.columns else 0
            data['total_physical_cpu'] = int(vhost['# CPU'].sum()) if '# CPU' in vhost.columns else 0
            data['total_host_ram_gb'] = round(vhost['Memory'].sum() / 1024, 2) if 'Memory' in vhost.columns else 0

            # vCPU to pCPU ratio
            if data.get('total_vcpu') and data.get('total_physical_cores'):
                data['vcpu_pcpu_ratio'] = round(data['total_vcpu'] / data['total_physical_cores'], 2)

            # VM density per host
            if data.get('total_vms') and data.get('total_hosts'):
                data['vm_density'] = round(data['total_vms'] / data['total_hosts'], 1)

        # vCluster sheet
        if 'vCluster' in sheets:
            vcluster = xl.parse('vCluster')
            data['total_clusters'] = len(vcluster)

        # vPartition sheet - storage
        if 'vPartition' in sheets:
            vpart = xl.parse('vPartition')
            data['total_storage_gb'] = round(vpart['Capacity MB'].sum() / 1024, 2) if 'Capacity MB' in vpart.columns else 0
            data['consumed_storage_gb'] = round(vpart['Consumed MB'].sum() / 1024, 2) if 'Consumed MB' in vpart.columns else 0
            if data.get('total_storage_gb', 0) > 0:
                data['storage_utilization'] = round(data['consumed_storage_gb'] / data['total_storage_gb'] * 100, 1)

        # Health scoring
        data['health'] = calculate_health_score(data)

        return data

    except Exception as e:
        return {"error": str(e)}


def calculate_health_score(data):
    """Generate a health scorecard from parsed data."""
    scores = {}
    flags = []
    recommendations = []

    total_vms = data.get('total_vms', 1)
    total_hosts = data.get('total_hosts', 1)

    # Powered off VM ratio
    powered_off_ratio = data.get('powered_off_vms', 0) / max(total_vms, 1)
    if powered_off_ratio > 0.20:
        scores['vm_waste'] = 'critical'
        flags.append(f"{data.get('powered_off_vms', 0)} powered-off VMs ({round(powered_off_ratio*100)}%) — significant waste")
        recommendations.append(f"Decommission or archive {data.get('powered_off_vms', 0)} powered-off VMs before migration")
    elif powered_off_ratio > 0.10:
        scores['vm_waste'] = 'warning'
        flags.append(f"{data.get('powered_off_vms', 0)} powered-off VMs ({round(powered_off_ratio*100)}%) — review before migration")
    else:
        scores['vm_waste'] = 'good'

    # vCPU to pCPU ratio
    ratio = data.get('vcpu_pcpu_ratio', 0)
    if ratio > 8:
        scores['cpu_ratio'] = 'critical'
        flags.append(f"vCPU:pCPU ratio of {ratio}:1 — overcommitted, performance risk")
        recommendations.append("Reduce vCPU overcommit ratio before private cloud migration")
    elif ratio > 4:
        scores['cpu_ratio'] = 'warning'
        flags.append(f"vCPU:pCPU ratio of {ratio}:1 — moderate overcommit")
    else:
        scores['cpu_ratio'] = 'good'

    # Old OS
    old_os_count = data.get('old_os_vms', 0)
    old_os_ratio = old_os_count / max(total_vms, 1)
    if old_os_ratio > 0.20:
        scores['os_currency'] = 'critical'
        flags.append(f"{old_os_count} VMs running end-of-life OS — licensing and security risk")
        recommendations.append(f"Plan OS modernization for {old_os_count} legacy VMs as part of migration")
    elif old_os_ratio > 0.05:
        scores['os_currency'] = 'warning'
        flags.append(f"{old_os_count} VMs on older OS versions — review for modernization")
    else:
        scores['os_currency'] = 'good'

    # Storage utilization
    storage_util = data.get('storage_utilization', 0)
    if storage_util > 85:
        scores['storage'] = 'critical'
        flags.append(f"Storage at {storage_util}% utilization — capacity risk")
        recommendations.append("Expand storage capacity or clean up unused data before migration")
    elif storage_util > 70:
        scores['storage'] = 'warning'
        flags.append(f"Storage at {storage_util}% utilization — monitor closely")
    else:
        scores['storage'] = 'good'

    # VM density
    density = data.get('vm_density', 0)
    if density > 30:
        scores['density'] = 'good'
    elif density > 15:
        scores['density'] = 'warning'
        flags.append(f"VM density of {density} VMs/host — consolidation opportunity")
        recommendations.append("Private cloud can improve VM density and reduce host count")
    else:
        scores['density'] = 'critical'
        flags.append(f"Low VM density of {density} VMs/host — significant consolidation potential")

    # Overall score
    score_map = {'good': 2, 'warning': 1, 'critical': 0}
    total = sum(score_map[v] for v in scores.values())
    max_score = len(scores) * 2
    overall_pct = round(total / max(max_score, 1) * 100)

    if overall_pct >= 75:
        overall = 'Healthy'
    elif overall_pct >= 50:
        overall = 'Needs Attention'
    else:
        overall = 'At Risk'

    return {
        'scores': scores,
        'flags': flags,
        'recommendations': recommendations,
        'overall': overall,
        'overall_pct': overall_pct,
    }