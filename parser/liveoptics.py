import pandas as pd


def parse_liveoptics(filepath):
    """Parse a LiveOptics xlsx export and extract key infrastructure data."""
    try:
        xl = pd.ExcelFile(filepath, engine='openpyxl')
        sheets = xl.sheet_names
        sheets_lower = {s.lower(): s for s in sheets}
        data = {}

        vm_sheet = _find_sheet(sheets_lower, ['vms', 'virtual machines', 'vm inventory'])
        if vm_sheet:
            vms = xl.parse(vm_sheet)
            vms.columns = vms.columns.str.strip()
            data['total_vms'] = len(vms)

            power_col = _find_col(vms, ['power state', 'powerstate', 'power'])
            if power_col:
                data['powered_on_vms'] = len(vms[vms[power_col].str.lower().isin(['on', 'poweredon'])])
                data['powered_off_vms'] = len(vms[vms[power_col].str.lower().isin(['off', 'poweredoff'])])
            else:
                data['powered_on_vms'] = data['total_vms']
                data['powered_off_vms'] = 0

            cpu_col = _find_col(vms, ['vcpus', 'cpus', 'cpu count', 'num cpu', 'vcpu'])
            if cpu_col:
                data['total_vcpu'] = int(pd.to_numeric(vms[cpu_col], errors='coerce').fillna(0).sum())

            mem_col = _find_col(vms, ['memory (mb)', 'memory(mb)', 'memory mb', 'ram (mb)', 'memory'])
            if mem_col:
                mem_values = pd.to_numeric(vms[mem_col], errors='coerce').fillna(0)
                if mem_values.mean() > 1000:
                    data['total_vram_gb'] = round(mem_values.sum() / 1024, 2)
                else:
                    data['total_vram_gb'] = round(mem_values.sum(), 2)

            os_col = _find_col(vms, ['operating system', 'os', 'guest os', 'os type'])
            if os_col:
                os_counts = vms[os_col].value_counts().to_dict()
                data['os_breakdown'] = os_counts
                windows_vms = sum(v for k, v in os_counts.items() if 'windows' in str(k).lower())
                linux_vms = sum(v for k, v in os_counts.items() if any(x in str(k).lower() for x in ['linux', 'red hat', 'ubuntu', 'centos', 'suse', 'rhel']))
                data['windows_vms'] = windows_vms
                data['linux_vms'] = linux_vms
                data['windows_ratio'] = round(windows_vms / max(data['total_vms'], 1), 2)

            if os_col:
                old_keywords = ['2008', '2003', '2012', 'windows 7', 'centos 6', 'rhel 6', 'rhel6']
                old_os = vms[vms[os_col].str.lower().str.contains('|'.join(old_keywords), na=False)]
                data['old_os_vms'] = len(old_os)
                data['old_os_list'] = old_os[os_col].value_counts().to_dict() if len(old_os) > 0 else {}

            if cpu_col:
                cpu_numeric = pd.to_numeric(vms[cpu_col], errors='coerce')
                data['large_vms'] = int(len(vms[cpu_numeric >= 8]))
                data['oversized_candidates'] = int(len(vms[cpu_numeric >= 16]))

        host_sheet = _find_sheet(sheets_lower, ['hosts', 'host inventory', 'esx hosts', 'esxi hosts'])
        if host_sheet:
            hosts = xl.parse(host_sheet)
            hosts.columns = hosts.columns.str.strip()
            data['total_hosts'] = len(hosts)

            cores_col = _find_col(hosts, ['total cores', 'cores', 'num cores', 'cpu cores'])
            if cores_col:
                data['total_physical_cores'] = int(pd.to_numeric(hosts[cores_col], errors='coerce').fillna(0).sum())

            socket_col = _find_col(hosts, ['cpu sockets', 'sockets', 'num sockets'])
            if socket_col:
                data['total_physical_cpu'] = int(pd.to_numeric(hosts[socket_col], errors='coerce').fillna(0).sum())

            host_mem_col = _find_col(hosts, ['memory (gb)', 'memory(gb)', 'memory gb', 'ram (gb)', 'total memory', 'memory'])
            if host_mem_col:
                mem_vals = pd.to_numeric(hosts[host_mem_col], errors='coerce').fillna(0)
                if mem_vals.mean() > 500:
                    data['total_host_ram_gb'] = round(mem_vals.sum() / 1024, 2)
                else:
                    data['total_host_ram_gb'] = round(mem_vals.sum(), 2)

            if data.get('total_vcpu') and data.get('total_physical_cores'):
                data['vcpu_pcpu_ratio'] = round(data['total_vcpu'] / data['total_physical_cores'], 2)

            if data.get('total_vms') and data.get('total_hosts'):
                data['vm_density'] = round(data['total_vms'] / data['total_hosts'], 1)

        cluster_sheet = _find_sheet(sheets_lower, ['clusters', 'cluster summary', 'cluster inventory'])
        if cluster_sheet:
            clusters_df = xl.parse(cluster_sheet)
            data['total_clusters'] = len(clusters_df)

        ds_sheet = _find_sheet(sheets_lower, ['datastores', 'datastore inventory', 'storage'])
        if ds_sheet:
            ds = xl.parse(ds_sheet)
            ds.columns = ds.columns.str.strip()

            cap_col = _find_col(ds, ['capacity (gb)', 'capacity(gb)', 'capacity gb', 'total capacity', 'capacity'])
            used_col = _find_col(ds, ['used (gb)', 'used(gb)', 'used gb', 'used space', 'used'])

            if cap_col:
                data['total_storage_gb'] = round(pd.to_numeric(ds[cap_col], errors='coerce').fillna(0).sum(), 2)
            if used_col:
                data['consumed_storage_gb'] = round(pd.to_numeric(ds[used_col], errors='coerce').fillna(0).sum(), 2)
            if data.get('total_storage_gb', 0) > 0 and data.get('consumed_storage_gb'):
                data['storage_utilization'] = round(data['consumed_storage_gb'] / data['total_storage_gb'] * 100, 1)

        data['source'] = 'LiveOptics'

        from parser.rvtools import calculate_health_score
        data['health'] = calculate_health_score(data)

        return data

    except Exception as e:
        return {"error": str(e)}


def _find_sheet(sheets_lower, candidates):
    """Find a sheet by trying multiple possible names."""
    for candidate in candidates:
        if candidate in sheets_lower:
            return sheets_lower[candidate]
    return None


def _find_col(df, candidates):
    """Find a column by trying multiple possible names."""
    cols_lower = {c.lower().strip(): c for c in df.columns}
    for candidate in candidates:
        if candidate.lower() in cols_lower:
            return cols_lower[candidate.lower()]
    for candidate in candidates:
        for col_lower, col_orig in cols_lower.items():
            if candidate.lower() in col_lower:
                return col_orig
    return None
