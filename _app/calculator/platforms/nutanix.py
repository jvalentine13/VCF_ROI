def get_nutanix_tco(parsed_data, overrides=None):
    """Nutanix-specific TCO adjustments and notes."""

    notes = [
        "Nutanix NCI includes AOS, AHV hypervisor, and Prism management",
        "AHV is a free KVM-based hypervisor — no separate hypervisor licensing",
        "Prism Central provides single-pane-of-glass management",
        "Strong HCI story — converged compute and storage",
    ]

    strengths = [
        "Simple node-based licensing — easy to budget",
        "Strong automation and self-service via Prism",
        "Good Linux and mixed workload support",
        "Competitive TCO for mid-market environments",
    ]

    considerations = [
        "AHV migration effort if coming from VMware",
        "Smaller ecosystem than VMware",
        "Per-node pricing can be expensive at scale",
    ]

    windows_ratio = parsed_data.get('windows_ratio', 0.5)
    linux_vms = parsed_data.get('linux_vms', 0)
    total_vms = parsed_data.get('total_vms', 1)
    total_hosts = parsed_data.get('total_hosts', 0)

    fit_score = 0
    fit_reasons = []

    linux_ratio = linux_vms / max(total_vms, 1)
    if linux_ratio > 0.4:
        fit_score += 25
        fit_reasons.append(f"Good Linux VM ratio ({round(linux_ratio*100)}%) — strong AHV fit")
    if total_hosts <= 20:
        fit_score += 25
        fit_reasons.append("Mid-size environment — Nutanix node licensing scales well")
    if windows_ratio < 0.7:
        fit_score += 20
        fit_reasons.append("Mixed OS environment suits Nutanix's flexible hypervisor")

    fit_score = min(fit_score + 20, 100)

    return {
        'platform': 'Nutanix',
        'fit_score': fit_score,
        'fit_reasons': fit_reasons,
        'notes': notes,
        'strengths': strengths,
        'considerations': considerations,
    }