# Platform roadmaps — 5-phase journey content for all four platforms

ROADMAPS = {
    "VMware VCF": {
        "tagline": "A practical journey from planning and setup to a fully operational private cloud platform.",
        "phases": [
            {
                "number": 1,
                "name": "Vision and Roadmap",
                "timeline": "4-8 Hours",
                "objective": "Establish business outcomes, maturity baseline, and an adoption roadmap.",
                "activities": [
                    "Private Cloud Maturity Assessment across vision & strategy, governance, people & tools, security, and operations",
                    "Executive alignment on outcomes, value case, funding approach, and program charter",
                    "High-level reference architecture and staged adoption plan covering management and workload domains, DR patterns, and security",
                ],
                "exit_criteria": [
                    "Approved roadmap and business case",
                    "Stakeholders aligned",
                    "Technical and organizational prerequisites captured",
                ],
            },
            {
                "number": 2,
                "name": "Essentials — VCF Stand-up and Readiness",
                "timeline": "Months 1-2",
                "objective": "Stand up the management domain and core operational capabilities.",
                "activities": [
                    "Cloud Builder deployment of the management domain (vCenter, NSX, vSAN, SDDC Manager) with initial security and operational hardening",
                    "Network, DNS/NTP, VLAN/MTU, and hardware/firmware baseline validation",
                    "Day-0 / Day-1 lifecycle configuration and operational readiness",
                    "As-built documentation, operations runbooks, and technical handoff",
                ],
                "exit_criteria": [
                    "Management domain healthy and operational",
                    "Backups tested and recoverable",
                    "LCM bundles reachable with offline workflow defined",
                    "Access controls and governance established",
                ],
            },
            {
                "number": 3,
                "name": "Foundation — Operate and Scale",
                "timeline": "Months 3-5",
                "objective": "Create initial workload domains and establish consistent operations and security baselines.",
                "activities": [
                    "Commission hosts and deploy initial workload domain(s)",
                    "Standardized clusters with NSX segmentation and micro-segmentation",
                    "DR strategy implemented using SRM and replication patterns",
                    "vSAN ESA design and storage policy baseline",
                    "Capacity and performance telemetry with showback / chargeback",
                    "Fleet-level lifecycle pipelines, compliance checks, and change governance",
                    "Expanded monitoring and AI-assisted operational insights",
                ],
                "exit_criteria": [
                    "At least one production workload domain in service",
                    "Security and compliance controls enforced",
                    "Lifecycle orchestration repeatedly successful",
                ],
            },
            {
                "number": 4,
                "name": "Private Cloud Services — Self-Service and Multi-Tenancy",
                "timeline": "Months 6-12",
                "objective": "Deliver cloud-like infrastructure consumption through VCF Automation.",
                "activities": [
                    "VCF Automation (Modern Cloud Interface) deployed and configured",
                    "Self-service catalog published for VMs, Kubernetes clusters, networks, volumes, and images",
                    "Projects, tenants, and policy models defined",
                    "Infrastructure-as-Code patterns using YAML and GitOps",
                    "Guardrails for RBAC, approvals, leases, and cost controls",
                    "Day-2 automation for scaling, patching, and lifecycle actions",
                    "Developer and platform engineering onboarding with enablement assets",
                ],
                "exit_criteria": [
                    "Catalog live for at least one project",
                    "Tenants actively consuming services",
                    "Governance and chargeback operational",
                    "SRE playbooks in use",
                ],
            },
            {
                "number": 5,
                "name": "Modernize and Innovate",
                "timeline": "Future State",
                "objective": "Evolve the platform to support modern applications, AI, and advanced resilience.",
                "activities": [
                    "GPU-capable workload mobility and Private AI enablement",
                    "Enhanced security operations with unified visibility and policy enforcement",
                    "Multi-site disaster recovery patterns and license portability strategies",
                    "On-prem to supported endpoint mobility with sovereign controls",
                    "Continuous optimization sprints focused on performance, capacity, and cost",
                    "Automated remediation and expansion of platform services such as DBaaS and data services",
                ],
                "exit_criteria": [
                    "Target modern workloads running in production",
                    "Resilience objectives met",
                    "Measurable efficiency and cost improvements",
                ],
            },
        ],
    },

    "Nutanix": {
        "tagline": "A streamlined journey to hyperconverged private cloud with simplified operations and self-service.",
        "phases": [
            {
                "number": 1,
                "name": "Vision and Roadmap",
                "timeline": "4-8 Hours",
                "objective": "Align on business outcomes, assess current infrastructure maturity, and define the Nutanix adoption roadmap.",
                "activities": [
                    "Infrastructure maturity assessment across compute, storage, networking, and operations",
                    "Executive alignment on HCI value case, funding approach, and migration priorities",
                    "High-level architecture design covering cluster sizing, network topology, and data protection strategy",
                ],
                "exit_criteria": [
                    "Approved roadmap and business case",
                    "Stakeholders aligned on HCI strategy",
                    "Migration priorities and prerequisites captured",
                ],
            },
            {
                "number": 2,
                "name": "Essentials — Nutanix Cluster Stand-up",
                "timeline": "Months 1-2",
                "objective": "Deploy and validate the Nutanix cluster foundation with AOS, AHV, and Prism Central.",
                "activities": [
                    "Nutanix cluster deployment with AOS and AHV hypervisor configuration",
                    "Prism Central deployment for unified management and analytics",
                    "Network configuration, VLAN setup, and storage policy baseline",
                    "Initial data protection policies, snapshots, and replication setup",
                    "Operational runbooks, as-built documentation, and team enablement",
                ],
                "exit_criteria": [
                    "Cluster healthy and passing NCC health checks",
                    "Prism Central operational with all nodes registered",
                    "Data protection policies active and tested",
                    "Team trained on day-to-day operations",
                ],
            },
            {
                "number": 3,
                "name": "Foundation — Migrate and Stabilize",
                "timeline": "Months 3-5",
                "objective": "Migrate initial workloads and establish operational stability on the Nutanix platform.",
                "activities": [
                    "Workload migration using Nutanix Move for VMware and physical workloads",
                    "Network segmentation and microsegmentation using Flow Network Security",
                    "Performance baseline and capacity planning using Prism Pro analytics",
                    "DR strategy implementation using Leap for cloud-based or on-prem failover",
                    "Cost governance with chargeback and resource quota policies",
                ],
                "exit_criteria": [
                    "Initial workload wave migrated and stable",
                    "Security microsegmentation enforced",
                    "DR runbooks tested and validated",
                ],
            },
            {
                "number": 4,
                "name": "Private Cloud Services — Automation and Self-Service",
                "timeline": "Months 6-12",
                "objective": "Enable self-service infrastructure consumption and developer agility through Nutanix automation.",
                "activities": [
                    "Nutanix Calm deployment for application lifecycle automation and blueprints",
                    "Self-service portal for VM, Kubernetes, and database provisioning",
                    "Role-based access control and approval workflows for governance",
                    "Infrastructure-as-Code integration with Terraform and Ansible",
                    "Kubernetes cluster provisioning via Nutanix Kubernetes Engine (NKE)",
                    "Showback and chargeback reporting by team and project",
                ],
                "exit_criteria": [
                    "Self-service catalog live and actively consumed",
                    "Kubernetes clusters provisioned on-demand",
                    "Governance and cost visibility operational",
                ],
            },
            {
                "number": 5,
                "name": "Modernize and Innovate",
                "timeline": "Future State",
                "objective": "Extend the platform to support AI workloads, multicloud operations, and continuous innovation.",
                "activities": [
                    "GPU node integration for AI/ML workloads and private AI initiatives",
                    "Nutanix Data Services for databases, files, and objects at scale",
                    "Multicloud management with Nutanix Cloud Manager across on-prem and public cloud",
                    "Advanced security with Nutanix Security Central and compliance automation",
                    "Continuous platform optimization sprints using AI-driven Prism insights",
                ],
                "exit_criteria": [
                    "AI/ML workloads running on private infrastructure",
                    "Multicloud visibility and governance operational",
                    "Measurable efficiency and cost improvements demonstrated",
                ],
            },
        ],
    },

    "Red Hat OpenShift": {
        "tagline": "A developer-first journey to container-native private cloud with integrated DevSecOps and AI-ready infrastructure.",
        "phases": [
            {
                "number": 1,
                "name": "Vision and Roadmap",
                "timeline": "4-8 Hours",
                "objective": "Define the container and DevSecOps strategy, assess application modernization readiness, and align on the OpenShift adoption roadmap.",
                "activities": [
                    "Application portfolio assessment — containerization candidates vs. lift-and-shift vs. retire",
                    "Developer and platform engineering team readiness assessment",
                    "Executive alignment on modernization outcomes, funding approach, and program charter",
                    "OpenShift cluster architecture design — bare metal, VM, or hyperconverged",
                ],
                "exit_criteria": [
                    "Application modernization roadmap approved",
                    "Platform architecture agreed upon",
                    "Developer and ops team readiness plan in place",
                ],
            },
            {
                "number": 2,
                "name": "Essentials — OpenShift Platform Stand-up",
                "timeline": "Months 1-2",
                "objective": "Deploy and harden the OpenShift cluster with core platform services and developer tooling.",
                "activities": [
                    "OpenShift cluster deployment on bare metal or virtualized infrastructure",
                    "Red Hat Advanced Cluster Management (ACM) for multi-cluster visibility",
                    "Core platform services: image registry, logging, monitoring, and alerting",
                    "Network policy baseline and ingress/egress configuration",
                    "RBAC model, namespaces, and project structure for multi-tenancy",
                    "Developer onboarding with initial toolchain integration (Git, CI/CD)",
                ],
                "exit_criteria": [
                    "Cluster healthy with all operators running",
                    "Platform services operational",
                    "Initial developer teams onboarded",
                    "Security policies and RBAC enforced",
                ],
            },
            {
                "number": 3,
                "name": "Foundation — Workload Onboarding and DevSecOps",
                "timeline": "Months 3-5",
                "objective": "Onboard initial applications and establish DevSecOps pipelines with integrated security.",
                "activities": [
                    "Initial application containerization and deployment to OpenShift",
                    "OpenShift Pipelines (Tekton) for CI/CD automation",
                    "OpenShift GitOps (Argo CD) for declarative application management",
                    "Red Hat Advanced Cluster Security (ACS) for container security and compliance",
                    "Service mesh deployment with OpenShift Service Mesh for observability",
                    "Developer self-service with Helm charts and application templates",
                ],
                "exit_criteria": [
                    "At least one production application running on OpenShift",
                    "CI/CD pipelines operational end-to-end",
                    "Security scanning integrated into pipelines",
                ],
            },
            {
                "number": 4,
                "name": "Platform Engineering — Internal Developer Platform",
                "timeline": "Months 6-12",
                "objective": "Build a fully operational internal developer platform with self-service, governance, and multi-tenancy.",
                "activities": [
                    "Developer portal deployment (Red Hat Developer Hub / Backstage)",
                    "Golden path templates for standardized application scaffolding",
                    "Multi-cluster management and workload placement policies via ACM",
                    "Resource quotas, limit ranges, and cost allocation by team and project",
                    "Automated compliance scanning and policy enforcement with ACS",
                    "Platform SRE practices — SLOs, error budgets, and runbook automation",
                ],
                "exit_criteria": [
                    "Developer portal live and actively used",
                    "Multiple teams self-serving on the platform",
                    "Governance, cost visibility, and compliance operational",
                ],
            },
            {
                "number": 5,
                "name": "Modernize and Innovate",
                "timeline": "Future State",
                "objective": "Extend the platform to support AI/ML workloads, edge computing, and continuous application modernization.",
                "activities": [
                    "OpenShift AI deployment for private AI/ML model training and serving",
                    "GPU operator configuration for AI workload scheduling",
                    "Edge cluster deployment with OpenShift at edge locations",
                    "Advanced application modernization — microservices, event-driven architecture",
                    "Multi-cluster federation and workload mobility across sites",
                    "Continuous platform evolution sprints aligned to developer and business needs",
                ],
                "exit_criteria": [
                    "AI/ML workloads running on private OpenShift infrastructure",
                    "Edge locations operational",
                    "Measurable developer productivity and deployment frequency improvements",
                ],
            },
        ],
    },

    "Azure Stack HCI": {
        "tagline": "A Microsoft-native journey to hybrid private cloud with seamless Azure integration and Arc-enabled management.",
        "phases": [
            {
                "number": 1,
                "name": "Vision and Roadmap",
                "timeline": "4-8 Hours",
                "objective": "Define the hybrid cloud strategy, assess Azure alignment, and establish the Azure Stack HCI adoption roadmap.",
                "activities": [
                    "Hybrid cloud maturity assessment across Azure usage, on-prem infrastructure, and operational practices",
                    "Executive alignment on hybrid outcomes, Azure Arc strategy, and funding approach",
                    "Azure Stack HCI cluster architecture design — node sizing, storage configuration, and Azure connectivity",
                    "Azure subscription and landing zone design for Arc-enabled management",
                ],
                "exit_criteria": [
                    "Hybrid cloud roadmap approved",
                    "Azure landing zone design agreed upon",
                    "Prerequisites and Azure subscription requirements captured",
                ],
            },
            {
                "number": 2,
                "name": "Essentials — Azure Stack HCI Cluster Stand-up",
                "timeline": "Months 1-2",
                "objective": "Deploy and register the Azure Stack HCI cluster with Azure Arc and core management services.",
                "activities": [
                    "Azure Stack HCI OS deployment and cluster creation on validated hardware",
                    "Azure Arc registration and Azure Portal integration",
                    "Storage Spaces Direct configuration and storage pool baseline",
                    "Network configuration with Software Defined Networking (SDN)",
                    "Azure Monitor and Azure Security Center integration",
                    "Windows Admin Center deployment for local management",
                ],
                "exit_criteria": [
                    "Cluster registered and visible in Azure Portal",
                    "Storage and networking validated",
                    "Azure Monitor collecting telemetry",
                    "Security baseline enforced",
                ],
            },
            {
                "number": 3,
                "name": "Foundation — Workload Migration and Azure Integration",
                "timeline": "Months 3-5",
                "objective": "Migrate initial workloads and establish deep Azure service integration for hybrid operations.",
                "activities": [
                    "VM workload migration using Azure Migrate for on-prem workloads",
                    "Azure Kubernetes Service (AKS) on HCI deployment for containerized workloads",
                    "Azure Site Recovery integration for hybrid DR and failover",
                    "Azure Backup for on-prem workload protection",
                    "Azure Policy enforcement across on-prem and cloud resources via Arc",
                    "Cost management and tagging strategy with Azure Cost Management",
                ],
                "exit_criteria": [
                    "Initial workload wave migrated and stable",
                    "AKS on HCI operational",
                    "DR runbooks tested with Azure Site Recovery",
                ],
            },
            {
                "number": 4,
                "name": "Hybrid Cloud Services — Arc-Enabled Everything",
                "timeline": "Months 6-12",
                "objective": "Extend Azure services to on-premises workloads and enable unified hybrid cloud governance.",
                "activities": [
                    "Azure Arc-enabled data services — SQL Managed Instance and PostgreSQL on-prem",
                    "Azure Arc-enabled application services for App Service and Functions on-prem",
                    "Unified identity with Azure Active Directory and hybrid join",
                    "Azure Defender for servers extended to on-prem via Arc",
                    "Self-service VM and AKS provisioning through Azure Portal",
                    "FinOps practices with unified cost visibility across on-prem and Azure",
                ],
                "exit_criteria": [
                    "Arc-enabled data services running on-prem",
                    "Unified governance and policy across hybrid estate",
                    "Self-service consumption active",
                ],
            },
            {
                "number": 5,
                "name": "Modernize and Innovate",
                "timeline": "Future State",
                "objective": "Leverage Azure innovation services on-premises for AI, advanced analytics, and sovereign cloud capabilities.",
                "activities": [
                    "Azure AI services extended on-prem for data sovereignty requirements",
                    "GPU-enabled nodes for private AI/ML model training",
                    "Azure Stack HCI stretched clusters for metro DR and always-on availability",
                    "Advanced threat protection with Microsoft Sentinel integration",
                    "Continuous platform optimization using Azure Advisor recommendations",
                    "Expansion to additional sites with consistent Arc-managed hybrid estate",
                ],
                "exit_criteria": [
                    "AI/ML workloads running on private HCI infrastructure",
                    "Stretched cluster or multi-site DR operational",
                    "Measurable hybrid efficiency and cost improvements demonstrated",
                ],
            },
        ],
    },
}


def get_roadmap(platform_name):
    """Return the roadmap for a given platform."""
    return ROADMAPS.get(platform_name, None)


def get_phase_summary(platform_name):
    """Return a simplified phase summary for proposal use."""
    roadmap = get_roadmap(platform_name)
    if not roadmap:
        return []
    return [
        {
            'number': p['number'],
            'name': p['name'],
            'timeline': p['timeline'],
            'objective': p['objective'],
        }
        for p in roadmap['phases']
    ]