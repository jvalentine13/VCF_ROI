# Default pricing - last updated February 2025
# These are approximate list prices - always verify with current quotes

LAST_UPDATED = "February 2025"

PLATFORMS = {
    "VMware VCF": {
        "model": "per_core",
        "cost_per_core_per_year": 150,
        "support_percentage": 0.20,
        "min_cores": 16,
        "notes": "VCF Universal License. Includes vSphere, vSAN, NSX, Aria.",
    },
    "Nutanix": {
        "model": "per_node",
        "cost_per_node_per_year": 8000,
        "support_percentage": 0.20,
        "min_nodes": 3,
        "notes": "NCI Pro license. Includes AOS, AHV, Prism.",
    },
    "Red Hat OpenShift": {
        "model": "per_core",
        "cost_per_core_per_year": 120,
        "support_percentage": 0.20,
        "min_cores": 16,
        "notes": "OpenShift Platform Plus. Includes RHEL, OpenShift, Advanced Cluster Mgmt.",
    },
    "Azure Stack HCI": {
        "model": "per_core",
        "cost_per_core_per_year": 100,
        "support_percentage": 0.18,
        "min_cores": 16,
        "notes": "Azure Stack HCI host license. Azure subscription costs additional.",
    },
}

# Hardware refresh assumptions
HARDWARE = {
    "avg_host_cost": 35000,         # Per host, mid-range 2-socket server
    "refresh_cycle_years": 4,       # Typical refresh cycle
    "power_per_host_kw": 0.5,       # kW per host average
    "power_cost_per_kwh": 0.10,     # $/kWh datacenter rate
    "datacenter_cost_per_host": 2000, # Rack space, cooling per host per year
}

# FTE assumptions
FTE = {
    "avg_fully_loaded_cost": 150000,  # Annual fully loaded FTE cost
    "hours_per_year": 2080,
    "toil_percentage": 0.40,          # % of time spent on toil/undifferentiated work
}

# Soft benefit multipliers
SOFT_BENEFITS = {
    "deployment_speed_improvement": 0.75,  # 75% faster VM provisioning
    "incident_reduction": 0.30,            # 30% fewer incidents
    "automation_toil_reduction": 0.40,     # 40% reduction in manual toil
}

# Recommendation scoring weights
SCORING_WEIGHTS = {
    "vm_density": 0.20,          # How many VMs per host
    "os_mix": 0.15,              # Windows vs Linux ratio
    "container_readiness": 0.20, # Workload types suited for containers
    "budget_sensitivity": 0.20,  # TCO sensitivity
    "operational_complexity": 0.25, # FTE count, skill set
}