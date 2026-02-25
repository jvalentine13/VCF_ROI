import pandas as pd


def parse_liveoptics(filepath):
    """Parse a real LiveOptics VMware xlsx export."""
    try:
        xl = pd.ExcelFile(filepath, engine='openpyxl')
        sheets = xl.sheet_names
        sheets_lower = {s.lower().strip(): s for s in sheets}
        data = {}

        # ── VMs Sheet ─────────────────────────────────────────────
        vm_sheet = _find_sheet(sheets_lower, ['vms', 'virtual machines', 'vm inventory'])
        if vm_sheet:
            vms = xl.parse(vm_sheet)
            vms.columns = vms.columns.str.strip()

            data['total_vms'] = len(vms)

            # Power state — real LiveOptics uses poweredOn/poweredOff
            power_col = _find_col(vms, ['power state', 'powerstate', 'isrunning'])
            if power_col:
                col_lower = vms[power_col].astype(str).str.lower()
                data['powered_on_vms'] = int(col_lower.isin(['poweredon', 'on', 'true']).sum())
                data['powered_off_vms'] = int(col_lower.isin(['poweredoff', 'off', 'false']).sum())
            else:
                data['powered_on_vms'] = data['total_vms']
                data['powered_off_vms'] = 0

            # vCPU — real column is 'Virtual CPU'
            cpu_col = _find_col(vms, ['virtual cpu', 'vcpus', 'cpus', 'cpu count', 'num cpu', 'vcpu'])
            if cpu_col:
                data['total_vcpu'] = int(pd.to_numeric(vms[cpu_col], errors='coerce').fillna(0).sum())

            # Memory — real column is 'Provisioned Memory (MiB)'
            mem_col = _find_col(vms, ['provisioned memory (mib)', 'memory (mib)', 'provisioned memory',
                                       'memory (mb)', 'memory(mb)', 'memory mb', 'ram (mb)', 'memory'])
            if mem_col:
                mem_values = pd.to_numeric(vms[mem_col], errors='coerce').fillna(0)
                # Convert MiB to GB
                if mem_values.mean() > 1000:
                    data['total_vram_gb'] = round(mem_values.sum() / 1024, 2)
                else:
                    data['total_vram_gb'] = round(mem_values.sum(), 2)

            # OS — real column is 'VM OS'
            os_col = _find_col(vms, ['vm os', 'operating system', 'guest os', 'os type'])
            if os_col:
                os_counts = vms[os_col].value_counts().to_dict()
                data['os_breakdown'] = os_counts
                windows_vms = sum(v for k, v in os_counts.items()
                                  if 'windows' in str(k).lower())
                linux_vms = sum(v for k, v in os_counts.items()
                                if any(x in str(k).lower()
                                       for x in ['linux', 'red hat', 'ubuntu',
                                                  'centos', 'suse', 'rhel']))
                data['windows_vms'] = windows_vms
                data['linux_vms'] = linux_vms
                data['windows_ratio'] = round(windows_vms / max(data['total_vms'], 1), 2)

                # Old OS detection
                old_keywords = ['2008', '2003', '2012', 'windows 7', 'centos 6',
                                 'rhel 6', 'rhel6', 'windows 10']
                old_os = vms[vms[os_col].astype(str).str.lower().str.contains(
                    '|'.join(old_keywords), na=False)]
                data['old_os_vms'] = len(old_os)
                data['old_os_list'] = old_os[os_col].value_counts().to_dict() if len(old_os) > 0 else {}

            # Large VMs
            if cpu_col:
                cpu_numeric = pd.to_numeric(vms[cpu_col], errors='coerce')
                data['large_vms'] = int((cpu_numeric >= 8).sum())
                data['oversized_candidates'] = int((cpu_numeric >= 16).sum())

            # Cluster count from VM data
            cluster_col = _find_col(vms, ['cluster'])
            if cluster_col:
                data['total_clusters'] = vms[cluster_col].nunique()

        # ── ESX Hosts Sheet ───────────────────────────────────────
        host_sheet = _find_sheet(sheets_lower, ['esx hosts', 'esxi hosts', 'hosts',
                                                  'host inventory'])
        if host_sheet:
            hosts = xl.parse(host_sheet)
            hosts.columns = hosts.columns.str.strip()

            data['total_hosts'] = len(hosts)

            # CPU Sockets
            socket_col = _find_col(hosts, ['cpu sockets', 'sockets', 'num sockets'])
            if socket_col:
                data['total_physical_cpu'] = int(
                    pd.to_numeric(hosts[socket_col], errors='coerce').fillna(0).sum())

            # CPU Cores — real column is 'CPU Cores'
            cores_col = _find_col(hosts, ['cpu cores', 'total cores', 'cores',
                                           'num cores', 'cores per socket'])
            if cores_col:
                data['total_physical_cores'] = int(
                    pd.to_numeric(hosts[cores_col], errors='coerce').fillna(0).sum())

            # Memory — real column is 'Memory (KiB)' — convert to GB
            mem_col = _find_col(hosts, ['memory (kib)', 'memory(kib)', 'memory (kb)',
                                         'memory (gb)', 'memory(gb)', 'memory gb',
                                         'ram (gb)', 'total memory', 'memory'])
            if mem_col:
                mem_vals = pd.to_numeric(hosts[mem_col], errors='coerce').fillna(0)
                avg = mem_vals.mean()
                if avg > 1000000:
                    # KiB to GB
                    data['total_host_ram_gb'] = round(mem_vals.sum() / (1024 * 1024), 2)
                elif avg > 1000:
                    # MiB or MB to GB
                    data['total_host_ram_gb'] = round(mem_vals.sum() / 1024, 2)
                else:
                    data['total_host_ram_gb'] = round(mem_vals.sum(), 2)

            # VM density from host data
            vm_count_col = _find_col(hosts, ['guest vm count', 'number of vms',
                                              'vm count', 'vms'])
            if vm_count_col:
                total_vms_from_hosts = pd.to_numeric(
                    hosts[vm_count_col], errors='coerce').fillna(0).sum()
                if total_vms_from_hosts > 0:
                    data['vm_density'] = round(
                        total_vms_from_hosts / data['total_hosts'], 1)

            # vCPU to pCPU ratio
            if data.get('total_vcpu') and data.get('total_physical_cores'):
                data['vcpu_pcpu_ratio'] = round(
                    data['total_vcpu'] / data['total_physical_cores'], 2)

            # VM density fallback
            if not data.get('vm_density') and data.get('total_vms') and data.get('total_hosts'):
                data['vm_density'] = round(data['total_vms'] / data['total_hosts'], 1)

        # ── Host Devices / Storage Sheet ─────────────────────────
        storage_sheet = _find_sheet(sheets_lower, ['host devices', 'datastores',
                                                     'datastore inventory', 'storage'])
        if storage_sheet:
            ds = xl.parse(storage_sheet)
            ds.columns = ds.columns.str.strip()

            cap_col = _find_col(ds, ['capacity (gib)', 'capacity(gib)', 'capacity (gb)',
                                      'capacity(gb)', 'capacity gb', 'total capacity',
                                      'capacity'])
            used_col = _find_col(ds, ['used capacity (gib)', 'used (gib)',
                                       'used capacity (gb)', 'used (gb)',
                                       'used gb', 'used space', 'used'])

            if cap_col:
                cap_vals = pd.to_numeric(ds[cap_col], errors='coerce').fillna(0)
                # Check if GiB (values typically large) vs GB
                data['total_storage_gb'] = round(cap_vals.sum(), 2)

            if used_col:
                used_vals = pd.to_numeric(ds[used_col], errors='coerce').fillna(0)
                data['consumed_storage_gb'] = round(used_vals.sum(), 2)

            if data.get('total_storage_gb', 0) > 0 and data.get('consumed_storage_gb'):
                data['storage_utilization'] = round(
                    data['consumed_storage_gb'] / data['total_storage_gb'] * 100, 1)

        data['source'] = 'LiveOptics'

        from parser.rvtools import calculate_health_score
        data['health'] = calculate_health_score(data)

        return data

    except Exception as e:
        return {"error": str(e)}


def _find_sheet(sheets_lower, candidates):
    for candidate in candidates:
        if candidate.lower() in sheets_lower:
            return sheets_lower[candidate.lower()]
    return None


def _find_col(df, candidates):
    cols_lower = {c.lower().strip(): c for c in df.columns}
    # Exact match first
    for candidate in candidates:
        if candidate.lower() in cols_lower:
            return cols_lower[candidate.lower()]
    # Partial match — only if candidate is 4+ characters to avoid false matches
    for candidate in candidates:
        if len(candidate) >= 4:
            for col_lower, col_orig in cols_lower.items():
                if candidate.lower() in col_lower:
                    return col_orig
    return None