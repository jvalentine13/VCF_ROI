from pricing.defaults import HARDWARE, FTE, PLATFORMS

def calculate_current_tco(parsed_data, overrides=None):
    """Calculate current state TCO based on parsed RVTools data."""

    h = HARDWARE.copy()
    f = FTE.copy()
    if overrides:
        h.update(overrides.get('hardware', {}))
        f.update(overrides.get('fte', {}))

    hosts = parsed_data.get('total_hosts', 0)
    total_vms = parsed_data.get('total_vms', 0)
    years = overrides.get('years', 3) if overrides else 3
    fte_count = overrides.get('fte_count', 3) if overrides else 3

    # Hardware costs
    hardware_refresh = hosts * h['avg_host_cost'] * (years / h['refresh_cycle_years'])

    # Power and datacenter
    power_annual = hosts * h['power_per_host_kw'] * 8760 * h['power_cost_per_kwh']
    datacenter_annual = hosts * h['datacenter_cost_per_host']
    facilities_total = (power_annual + datacenter_annual) * years

    # FTE costs
    fte_total = fte_count * f['avg_fully_loaded_cost'] * years

    # Existing licensing (VMware vSphere assumed)
    vsphere_per_core_per_year = 50
    cores = parsed_data.get('total_physical_cores', hosts * 20)
    licensing_total = cores * vsphere_per_core_per_year * years

    # Support and maintenance (20% of hardware annually)
    support_total = hosts * h['avg_host_cost'] * 0.20 * years

    total = hardware_refresh + facilities_total + fte_total + licensing_total + support_total

    return {
        'hardware_refresh': round(hardware_refresh, 2),
        'facilities': round(facilities_total, 2),
        'fte': round(fte_total, 2),
        'licensing': round(licensing_total, 2),
        'support': round(support_total, 2),
        'total': round(total, 2),
        'years': years,
        'annual_average': round(total / years, 2),
    }


def calculate_platform_tco(parsed_data, platform_name, overrides=None):
    """Calculate TCO for a given private cloud platform."""

    platform = PLATFORMS[platform_name].copy()
    h = HARDWARE.copy()
    f = FTE.copy()

    if overrides:
        h.update(overrides.get('hardware', {}))
        f.update(overrides.get('fte', {}))
        if 'pricing' in overrides:
            platform.update(overrides['pricing'])

    hosts = parsed_data.get('total_hosts', 0)
    cores = parsed_data.get('total_physical_cores', hosts * 20)
    years = overrides.get('years', 3) if overrides else 3
    fte_count = overrides.get('fte_count', 3) if overrides else 3
    fte_reduction = overrides.get('fte_reduction', 0.40) if overrides else 0.40

    # Platform licensing
    if platform['model'] == 'per_core':
        license_units = max(cores, platform.get('min_cores', 0))
        licensing = license_units * platform['cost_per_core_per_year'] * years
    elif platform['model'] == 'per_node':
        license_units = max(hosts, platform.get('min_nodes', 0))
        licensing = license_units * platform['cost_per_node_per_year'] * years

    support = licensing * platform['support_percentage']

    # Hardware - private cloud typically improves density 20-30%
    hardware_efficiency = overrides.get('hardware_efficiency', 0.80) if overrides else 0.80
    effective_hosts = max(round(hosts * hardware_efficiency), 3)
    hardware_refresh = effective_hosts * h['avg_host_cost'] * (years / h['refresh_cycle_years'])

    # Power and datacenter (scaled to effective hosts)
    power_annual = effective_hosts * h['power_per_host_kw'] * 8760 * h['power_cost_per_kwh']
    datacenter_annual = effective_hosts * h['datacenter_cost_per_host']
    facilities_total = (power_annual + datacenter_annual) * years

    # FTE - reduced by automation
    effective_fte = fte_count * (1 - fte_reduction)
    fte_total = effective_fte * f['avg_fully_loaded_cost'] * years

    # Implementation/migration one-time cost
    implementation = hosts * 2500

    total = licensing + support + hardware_refresh + facilities_total + fte_total + implementation

    return {
        'platform': platform_name,
        'licensing': round(licensing, 2),
        'support': round(support, 2),
        'hardware_refresh': round(hardware_refresh, 2),
        'facilities': round(facilities_total, 2),
        'fte': round(fte_total, 2),
        'implementation': round(implementation, 2),
        'total': round(total, 2),
        'years': years,
        'annual_average': round(total / years, 2),
        'effective_hosts': effective_hosts,
    }


def calculate_roi(current_tco, platform_tco):
    """Calculate ROI comparing current state to a platform."""

    savings = current_tco['total'] - platform_tco['total']
    roi_pct = round(savings / max(platform_tco['total'], 1) * 100, 1)

    # Payback period in months
    monthly_savings = savings / max(current_tco['years'] * 12, 1)
    implementation_cost = platform_tco['implementation']
    payback_months = round(implementation_cost / max(monthly_savings, 1), 1) if monthly_savings > 0 else 999

    return {
        'savings': round(savings, 2),
        'roi_pct': roi_pct,
        'payback_months': payback_months,
        'is_positive': savings > 0,
    }