def get_openshift_tco(parsed_data, overrides=None):
    """Red Hat OpenShift-specific TCO adjustments and notes."""

    notes = [
        "OpenShift Platform Plus includes RHEL, OpenShift, and Advanced Cluster Management",
        "Container-native platform — best for modern app development",
        "Strong CI/CD and DevSecOps integration",
        "Requires more operational expertise than traditional VM platforms",
    ]

    strengths = [
        "Best platform for container and microservices workloads",
        "Strong DevSecOps and automation story",
        "Good fit for Linux-heavy and developer-driven environments",
        "Red Hat ecosystem integration (Ansible, Satellite)",
    ]

    considerations = [
        "Steeper learning curve — requires container expertise",
        "Not ideal for legacy Windows workloads",
        "May require app modernization effort",
        "Higher operational complexity",
    ]

    windows_ratio = parsed_data.get('windows_ratio', 0.5)
    linux_vms = parsed_data.get('linux_vms', 0)
    total_vms = parsed_data.get('total_vms', 1)
    old_os_vms = parsed_data.get('old_os_vms', 0)

    fit_score = 0
    fit_reasons = []

    linux_ratio = linux_vms / max(total_vms, 1)
    if linux_ratio > 0.5:
        fit_score += 35
        fit_reasons.append(f"High Linux ratio ({round(linux_ratio*100)}%) — strong OpenShift fit")
    if windows_ratio < 0.4:
        fit_score += 25
        fit_reasons.append("Low Windows ratio — OpenShift containerization is viable")
    if old_os_vms > 10:
        fit_score += 15
        fit_reasons.append(f"{old_os_vms} legacy OS VMs — modernization opportunity with OpenShift")

    fit_score = min(fit_score + 10, 100)

    return {
        'platform': 'Red Hat OpenShift',
        'fit_score': fit_score,
        'fit_reasons': fit_reasons,
        'notes': notes,
        'strengths': strengths,
        'considerations': considerations,
    }