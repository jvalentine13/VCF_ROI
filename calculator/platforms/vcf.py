from pricing.defaults import PLATFORMS

def get_vcf_tco(parsed_data, overrides=None):
    """VCF-specific TCO adjustments and notes."""

    notes = [
        "VCF includes vSphere, vSAN, NSX, and Aria Suite — no separate licensing needed",
        "Existing VMware admins can manage VCF with minimal retraining",
        "Best fit for environments already running VMware infrastructure",
        "vSAN eliminates need for separate SAN/NAS storage licensing",
    ]

    strengths = [
        "Lowest operational disruption — familiar tooling",
        "Strong VM density and performance",
        "Integrated networking (NSX) and storage (vSAN)",
        "Best for Windows-heavy workloads",
    ]

    considerations = [
        "Broadcom licensing changes — verify current terms",
        "Higher per-core cost than some alternatives",
        "Less container-native than OpenShift",
    ]

    # VCF specific scoring factors
    windows_ratio = parsed_data.get('windows_ratio', 0.5)
    vm_density = parsed_data.get('vm_density', 0)
    vcpu_ratio = parsed_data.get('vcpu_pcpu_ratio', 4)

    fit_score = 0
    fit_reasons = []

    if windows_ratio > 0.6:
        fit_score += 30
        fit_reasons.append(f"High Windows VM ratio ({round(windows_ratio*100)}%) — VCF licensing advantage")
    if vm_density > 20:
        fit_score += 25
        fit_reasons.append("High VM density suits VCF's mature hypervisor")
    if vcpu_ratio < 6:
        fit_score += 20
        fit_reasons.append("Healthy vCPU ratio — good fit for VCF performance profile")

    fit_score = min(fit_score + 25, 100)  # Base score

    return {
        'platform': 'VMware VCF',
        'fit_score': fit_score,
        'fit_reasons': fit_reasons,
        'notes': notes,
        'strengths': strengths,
        'considerations': considerations,
    }