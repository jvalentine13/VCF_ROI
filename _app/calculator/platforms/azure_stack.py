def get_azure_stack_tco(parsed_data, overrides=None):
    """Azure Stack HCI-specific TCO adjustments and notes."""

    notes = [
        "Azure Stack HCI runs on-premises but is managed through Azure Arc",
        "Per-core host licensing plus Azure subscription for management services",
        "Strong hybrid story — consistent experience with Azure public cloud",
        "Good fit for organizations already invested in Microsoft ecosystem",
    ]

    strengths = [
        "Seamless hybrid cloud extension of Azure",
        "Strong Windows and SQL Server workload support",
        "Azure Arc provides unified management across on-prem and cloud",
        "Good disaster recovery story with Azure Site Recovery",
    ]

    considerations = [
        "Ongoing Azure subscription cost adds to TCO",
        "Requires Azure expertise in addition to on-prem skills",
        "Less mature than VCF or Nutanix for pure private cloud",
        "Vendor lock-in to Microsoft ecosystem",
    ]

    windows_ratio = parsed_data.get('windows_ratio', 0.5)
    total_hosts = parsed_data.get('total_hosts', 0)
    total_vms = parsed_data.get('total_vms', 1)

    fit_score = 0
    fit_reasons = []

    if windows_ratio > 0.7:
        fit_score += 35
        fit_reasons.append(f"High Windows ratio ({round(windows_ratio*100)}%) — strong Azure Stack fit")
    if total_hosts <= 16:
        fit_score += 20
        fit_reasons.append("Smaller footprint suits Azure Stack HCI entry licensing")
    if windows_ratio > 0.5:
        fit_score += 15
        fit_reasons.append("Microsoft-heavy environment aligns with Azure Stack ecosystem")

    fit_score = min(fit_score + 15, 100)

    return {
        'platform': 'Azure Stack HCI',
        'fit_score': fit_score,
        'fit_reasons': fit_reasons,
        'notes': notes,
        'strengths': strengths,
        'considerations': considerations,
    }