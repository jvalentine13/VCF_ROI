def validate_parsed_data(parsed):
    """Validate parsed RVTools data and return warnings and errors."""
    errors = []
    warnings = []

    total_vms = parsed.get('total_vms', 0)
    total_hosts = parsed.get('total_hosts', 0)
    total_vcpu = parsed.get('total_vcpu', 0)
    total_cores = parsed.get('total_physical_cores', 0)
    vcpu_ratio = parsed.get('vcpu_pcpu_ratio', 0)
    storage = parsed.get('total_storage_gb', 0)

    # Hard errors — will break calculations
    if total_vms == 0:
        errors.append("No VMs found in the uploaded file. Please verify this is a valid RVTools export.")
    if total_hosts == 0:
        errors.append("No hosts found. The vHost sheet may be missing or empty.")

    # Warnings — won't break but may skew results
    if total_vms > 0 and total_hosts == 0:
        warnings.append("Host data is missing — TCO calculations will use estimated host counts.")
    if vcpu_ratio > 16:
        warnings.append(f"vCPU:pCPU ratio of {vcpu_ratio}:1 is extremely high — verify host data is complete.")
    if vcpu_ratio == 0 and total_vcpu > 0 and total_cores > 0:
        warnings.append("Could not calculate vCPU ratio — check that host core data is present.")
    if storage == 0:
        warnings.append("No storage data found — vPartition sheet may be missing.")
    if parsed.get('powered_off_vms', 0) > total_vms * 0.5:
        warnings.append("More than 50% of VMs are powered off — verify this is accurate before using for sizing.")
    if total_vms > 0 and parsed.get('windows_vms', 0) == 0 and parsed.get('linux_vms', 0) == 0:
        warnings.append("OS data not detected — platform fit scoring will use neutral defaults.")

    return errors, warnings


def validate_tco_inputs(fte_count, fte_cost, host_cost, years):
    """Validate TCO input assumptions."""
    errors = []
    warnings = []

    if fte_count <= 0:
        errors.append("FTE count must be at least 1.")
    if fte_cost < 50000:
        warnings.append(f"FTE cost of ${fte_cost:,} seems low — fully loaded cost typically includes salary, benefits, and overhead.")
    if fte_cost > 500000:
        warnings.append(f"FTE cost of ${fte_cost:,} seems high — verify this is the fully loaded annual cost.")
    if host_cost < 5000:
        warnings.append(f"Host cost of ${host_cost:,} seems low — typical 2-socket servers run $25,000-$50,000.")
    if host_cost > 200000:
        warnings.append(f"Host cost of ${host_cost:,} seems high — verify this is per-host not total.")
    if years not in [1, 2, 3, 5]:
        errors.append("Analysis period must be 1, 2, 3, or 5 years.")

    return errors, warnings


def validate_quote_inputs(quotes, parsed):
    """Validate vendor quote inputs."""
    warnings = []
    cores = parsed.get('total_physical_cores', 0)
    hosts = parsed.get('total_hosts', 0)

    for platform, quote in quotes.items():
        value = quote.get('value', 0)
        if value == 0:
            continue

        quote_type = quote.get('type', '')

        if 'Total Contract Value' in quote_type:
            if value < 10000:
                warnings.append(f"{platform}: Total contract value of ${value:,} seems very low — did you mean per-unit pricing?")
            if value > 50000000:
                warnings.append(f"{platform}: Total contract value of ${value:,.0f} is very high — verify this is correct.")
        else:
            # Per unit pricing
            if platform in ['VMware VCF', 'Red Hat OpenShift', 'Azure Stack HCI']:
                if value < 10:
                    warnings.append(f"{platform}: Per-core price of ${value} seems very low.")
                if value > 1000:
                    warnings.append(f"{platform}: Per-core price of ${value} seems very high — verify this is annual per-core, not total.")
            elif platform == 'Nutanix':
                if value < 1000:
                    warnings.append(f"{platform}: Per-node price of ${value:,} seems very low.")
                if value > 100000:
                    warnings.append(f"{platform}: Per-node price of ${value:,} seems very high.")

    return warnings


def validate_discovery(discovery):
    """Check discovery completeness and return a completion score."""
    if not discovery:
        return 0, ["Discovery questionnaire not completed — recommendation is based on environment data only."]

    key_fields = [
        'primary_driver', 'app_strategy', 'kubernetes', 'current_hypervisor',
        'microsoft_investment', 'team_skillset', 'change_appetite', 'vmware_renewal'
    ]

    answered = sum(1 for f in key_fields
                   if discovery.get(f) and discovery.get(f) != '-- Select --')
    completion_pct = round(answered / len(key_fields) * 100)

    warnings = []
    if completion_pct < 50:
        warnings.append(f"Discovery questionnaire is only {completion_pct}% complete — consider answering more questions for a stronger recommendation.")
    elif completion_pct < 80:
        warnings.append(f"Discovery questionnaire is {completion_pct}% complete — a few more answers would improve recommendation accuracy.")

    return completion_pct, warnings