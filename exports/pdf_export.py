from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, PageBreak, HRFlowable, Image)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.platypus import KeepTogether
import io
import os
from datetime import date
from calculator.roadmaps import get_roadmap

# ── Brand Colors ─────────────────────────────────────────────────
INSIGHT_BROWN = HexColor('#4A3728')
INSIGHT_PINK = HexColor('#C8006A')
DARK_BLUE = HexColor('#1F4E79')
MID_BLUE = HexColor('#2E75B6')
LIGHT_BLUE = HexColor('#DEEAF1')
LIGHT_GRAY = HexColor('#F5F5F5')
MID_GRAY = HexColor('#666666')
GREEN = HexColor('#70AD47')
ORANGE = HexColor('#ED7D31')
WHITE = white
BLACK = black

LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'assets', 'Insight.png')


def get_styles():
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        'CoverTitle',
        fontName='Helvetica-Bold',
        fontSize=32,
        textColor=INSIGHT_BROWN,
        spaceAfter=12,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        'CoverSubtitle',
        fontName='Helvetica',
        fontSize=16,
        textColor=MID_GRAY,
        spaceAfter=8,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        'SectionHeader',
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=DARK_BLUE,
        spaceBefore=16,
        spaceAfter=8,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        'SubHeader',
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=INSIGHT_PINK,
        spaceBefore=10,
        spaceAfter=6,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        'BodyText2',
        fontName='Helvetica',
        fontSize=10,
        textColor=BLACK,
        spaceAfter=6,
        leading=16,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        'BulletText',
        fontName='Helvetica',
        fontSize=10,
        textColor=BLACK,
        spaceAfter=4,
        leading=14,
        leftIndent=16,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        'SmallText',
        fontName='Helvetica',
        fontSize=8,
        textColor=MID_GRAY,
        spaceAfter=4,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        'MetricLabel',
        fontName='Helvetica',
        fontSize=9,
        textColor=MID_GRAY,
        spaceAfter=2,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        'MetricValue',
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=DARK_BLUE,
        spaceAfter=2,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        'PhaseTitle',
        fontName='Helvetica-Bold',
        fontSize=11,
        textColor=WHITE,
        spaceAfter=2,
        alignment=TA_CENTER,
    ))
    styles.add(ParagraphStyle(
        'Disclaimer',
        fontName='Helvetica-Oblique',
        fontSize=8,
        textColor=MID_GRAY,
        spaceAfter=4,
        alignment=TA_CENTER,
    ))

    return styles


def build_cover_page(elements, styles, customer_name, preparer_name, recommendation, years):
    """Build the cover page."""

    # Logo
    if os.path.exists(LOGO_PATH):
        logo = Image(LOGO_PATH, width=2.5*inch, height=1*inch)
        logo.hAlign = 'LEFT'
        elements.append(logo)
    elements.append(Spacer(1, 0.5*inch))

    # Accent line
    elements.append(HRFlowable(width="100%", thickness=4, color=INSIGHT_PINK))
    elements.append(Spacer(1, 0.3*inch))

    # Title
    elements.append(Paragraph("Private Cloud", styles['CoverTitle']))
    elements.append(Paragraph("ROI & TCO Analysis", styles['CoverTitle']))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(f"Prepared for: {customer_name}", styles['CoverSubtitle']))
    elements.append(Spacer(1, 0.1*inch))

    cell_style = ParagraphStyle(
        'CoverCell',
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=DARK_BLUE,
        alignment=TA_CENTER,
        leading=16,
    )

    rec_data = [
        [
            Paragraph("Recommended Platform", styles['MetricLabel']),
            Paragraph("Analysis Period", styles['MetricLabel']),
            Paragraph("Prepared By", styles['MetricLabel']),
            Paragraph("Date", styles['MetricLabel']),
        ],
        [
            Paragraph(recommendation, cell_style),
            Paragraph(f"{years} Years", cell_style),
            Paragraph(preparer_name or "Insight", cell_style),
            Paragraph(date.today().strftime("%b %d, %Y"), cell_style),
        ]
    ]

    rec_table = Table(rec_data, colWidths=[2.2*inch, 1.3*inch, 1.8*inch, 1.7*inch])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BLUE),
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWHEIGHT', (0, 0), (-1, 0), 20),
        ('ROWHEIGHT', (0, 1), (-1, 1), 55),
        ('BOX', (0, 0), (-1, -1), 1, MID_BLUE),
        ('GRID', (0, 0), (-1, -1), 0.5, MID_BLUE),
    ]))
    elements.append(Spacer(1, 0.3*inch))
    elements.append(rec_table)
    elements.append(Spacer(1, 0.4*inch))

    # Tagline
    elements.append(HRFlowable(width="100%", thickness=1, color=LIGHT_BLUE))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(
        "This analysis was prepared by Insight to help you understand the true cost of your current "
        "infrastructure, evaluate private cloud platform options, and build a clear roadmap to modernization. "
        "Our goal is to give you the data and confidence to make the right decision for your organization.",
        styles['BodyText2']
    ))
    elements.append(Spacer(1, 0.2*inch))
    elements.append(Paragraph(
        "Insight Proprietary and Confidential. Do Not Copy or Distribute. © 2025 Insight. All Rights Reserved.",
        styles['Disclaimer']
    ))
    elements.append(PageBreak())


def build_executive_summary(elements, styles, customer_name, parsed, current_tco,
                             scenario_results, final_recommendation, years, discovery):
    """Build the executive summary page."""

    elements.append(Paragraph("Executive Summary", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=2, color=INSIGHT_PINK))
    elements.append(Spacer(1, 0.15*inch))

    # Opening narrative
    health = parsed.get('health', {})
    overall_health = health.get('overall', 'Needs Attention')
    vcpu_ratio = parsed.get('vcpu_pcpu_ratio', 0)
    powered_off = parsed.get('powered_off_vms', 0)
    total_vms = parsed.get('total_vms', 0)
    total_hosts = parsed.get('total_hosts', 0)

    # Dynamic narrative based on environment
    if overall_health == 'At Risk':
        health_narrative = (f"analysis reveals a {overall_health.lower()} infrastructure with "
                           f"a {vcpu_ratio}:1 vCPU overcommit ratio and {powered_off} powered-off VMs "
                           f"consuming unnecessary resources.")
    elif overall_health == 'Needs Attention':
        health_narrative = (f"analysis identifies several optimization opportunities across "
                           f"{total_vms} VMs running on {total_hosts} hosts, with a "
                           f"{vcpu_ratio}:1 vCPU ratio indicating room for consolidation.")
    else:
        health_narrative = (f"analysis shows a relatively healthy environment of {total_vms} VMs "
                           f"across {total_hosts} hosts, well-positioned for private cloud migration.")

    rec_result = scenario_results.get(final_recommendation, {})
    savings = rec_result.get('savings', 0)
    roi_pct = rec_result.get('roi_pct', 0)
    payback = rec_result.get('payback_months', 0)

    primary_driver = discovery.get('primary_driver', '-- Select --')
    driver_text = "" if primary_driver == "-- Select --" else f" driven by {primary_driver.lower()},"

    elements.append(Paragraph(
        f"{customer_name}'s infrastructure {health_narrative} "
        f"This engagement{driver_text} evaluated four private cloud platforms against your "
        f"environment profile, strategic direction, and total cost of ownership over {years} years.",
        styles['BodyText2']
    ))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        f"Based on a comprehensive analysis of your RVTools data, discovery findings, and financial modeling, "
        f"Insight recommends <b>{final_recommendation}</b> as the optimal private cloud platform for "
        f"{customer_name}. This recommendation delivers an estimated <b>${savings:,.0f} in {years}-year "
        f"savings</b> versus your current infrastructure costs, with a projected <b>{roi_pct}% ROI</b> "
        f"and payback within <b>{payback} months</b>.",
        styles['BodyText2']
    ))
    elements.append(Spacer(1, 0.15*inch))

    # Key metrics table
    elements.append(Paragraph("Key Financial Metrics", styles['SubHeader']))

    metrics_data = [
        ['Metric', 'Current State', final_recommendation, 'Difference'],
        [f'{years}-Year Total Cost',
         f"${current_tco['total']:,.0f}",
         f"${rec_result.get('total', 0):,.0f}",
         f"${savings:,.0f}"],
        ['Annual Average Cost',
         f"${current_tco['annual_average']:,.0f}",
         f"${rec_result.get('annual_average', 0):,.0f}",
         f"${current_tco['annual_average'] - rec_result.get('annual_average', 0):,.0f}"],
        ['ROI', '—', f"{roi_pct}%", '—'],
        ['Payback Period', '—', f"{payback} months", '—'],
    ]

    metrics_table = Table(metrics_data, colWidths=[2*inch, 1.5*inch, 1.8*inch, 1.2*inch])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT_GRAY, WHITE]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, MID_BLUE),
        ('ROWHEIGHT', (0, 0), (-1, -1), 22),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('BACKGROUND', (-1, 1), (-1, -1), HexColor('#E2EFDA')),
        ('FONTNAME', (-1, 1), (-1, -1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (-1, 1), (-1, -1), GREEN),
    ]))
    elements.append(metrics_table)
    elements.append(Spacer(1, 0.15*inch))

    # Why private cloud narrative
    elements.append(Paragraph("The Case for Private Cloud", styles['SubHeader']))
    elements.append(Paragraph(
        "Private cloud gives organizations the economics and agility of public cloud while maintaining "
        "the control, security, and predictability of on-premises infrastructure. Rather than simply "
        "reducing costs, the real value of private cloud is what you can build with the capacity you free up.",
        styles['BodyText2']
    ))
    elements.append(Paragraph(
        "The freed operational and financial capacity from modernizing your infrastructure creates a "
        "reinvestment opportunity across your most strategic initiatives — AI and machine learning, "
        "application modernization, DevSecOps automation, and edge computing expansion. "
        "Private cloud doesn't just save money. It funds your future.",
        styles['BodyText2']
    ))
    elements.append(PageBreak())


def build_environment_section(elements, styles, parsed, customer_name):
    """Build the current environment analysis section."""

    elements.append(Paragraph("Current Environment Analysis", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=2, color=INSIGHT_PINK))
    elements.append(Spacer(1, 0.15*inch))

    health = parsed.get('health', {})

    elements.append(Paragraph(
        f"The following analysis is based on RVTools data collected from {customer_name}'s environment. "
        f"This provides an objective baseline of the current infrastructure footprint, utilization patterns, "
        f"and areas of risk or opportunity.",
        styles['BodyText2']
    ))
    elements.append(Spacer(1, 0.1*inch))

    # Environment metrics table
    elements.append(Paragraph("Infrastructure Summary", styles['SubHeader']))

    env_data = [
        ['Metric', 'Value', 'Metric', 'Value'],
        ['Total VMs', str(parsed.get('total_vms', 0)),
         'Total Hosts', str(parsed.get('total_hosts', 0))],
        ['Powered On VMs', str(parsed.get('powered_on_vms', 0)),
         'Total Clusters', str(parsed.get('total_clusters', 0))],
        ['Powered Off VMs', str(parsed.get('powered_off_vms', 0)),
         'Total vCPU', str(parsed.get('total_vcpu', 0))],
        ['Total vRAM (GB)', str(parsed.get('total_vram_gb', 0)),
         'Total Storage (GB)', str(parsed.get('total_storage_gb', 0))],
        ['vCPU:pCPU Ratio', f"{parsed.get('vcpu_pcpu_ratio', 0)}:1",
         'VM Density', f"{parsed.get('vm_density', 0)}/host"],
        ['Windows VMs', str(parsed.get('windows_vms', 0)),
         'Linux VMs', str(parsed.get('linux_vms', 0))],
    ]

    env_table = Table(env_data, colWidths=[2*inch, 1.5*inch, 2*inch, 1.5*inch])
    env_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 1), (2, -1), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT_GRAY, WHITE]),
        ('GRID', (0, 0), (-1, -1), 0.5, MID_BLUE),
        ('ROWHEIGHT', (0, 0), (-1, -1), 20),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (1, 0), (1, -1), 'CENTER'),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
    ]))
    elements.append(env_table)
    elements.append(Spacer(1, 0.15*inch))

    # Health scorecard
    elements.append(Paragraph("Environment Health Scorecard", styles['SubHeader']))

    overall = health.get('overall', 'Unknown')
    overall_pct = health.get('overall_pct', 0)
    scores = health.get('scores', {})

    health_color = GREEN if overall == 'Healthy' else (ORANGE if overall == 'Needs Attention' else HexColor('#FF0000'))

    health_data = [['Overall Health', 'Score', 'VM Waste', 'CPU Ratio', 'OS Currency', 'Storage', 'VM Density']]
    score_icons = {'good': '✓ Good', 'warning': '⚠ Warning', 'critical': '✗ Critical'}
    health_data.append([
        overall,
        f"{overall_pct}%",
        score_icons.get(scores.get('vm_waste', 'good'), '—'),
        score_icons.get(scores.get('cpu_ratio', 'good'), '—'),
        score_icons.get(scores.get('os_currency', 'good'), '—'),
        score_icons.get(scores.get('storage', 'good'), '—'),
        score_icons.get(scores.get('density', 'good'), '—'),
    ])

    health_table = Table(health_data, colWidths=[1.1*inch, 0.7*inch, 1*inch, 1*inch, 1*inch, 0.9*inch, 1*inch])
    health_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, MID_BLUE),
        ('ROWHEIGHT', (0, 0), (-1, -1), 20),
        ('BACKGROUND', (0, 1), (0, 1), LIGHT_BLUE),
        ('FONTNAME', (0, 1), (0, 1), 'Helvetica-Bold'),
        ('TEXTCOLOR', (0, 1), (0, 1), health_color),
    ]))
    elements.append(health_table)
    elements.append(Spacer(1, 0.15*inch))

    # Flags and recommendations
    flags = health.get('flags', [])
    recs = health.get('recommendations', [])

    if flags:
        elements.append(Paragraph("Environment Flags", styles['SubHeader']))
        for flag in flags:
            elements.append(Paragraph(f"⚠  {flag}", styles['BulletText']))
        elements.append(Spacer(1, 0.1*inch))

    if recs:
        elements.append(Paragraph("Recommendations", styles['SubHeader']))
        for rec in recs:
            elements.append(Paragraph(f"→  {rec}", styles['BulletText']))

    elements.append(PageBreak())


def build_tco_section(elements, styles, current_tco, scenario_results,
                      selected_platforms, final_recommendation, years):
    """Build the TCO comparison section."""

    elements.append(Paragraph("Total Cost of Ownership Comparison", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=2, color=INSIGHT_PINK))
    elements.append(Spacer(1, 0.15*inch))

    elements.append(Paragraph(
        f"The following {years}-year TCO analysis compares your current infrastructure costs against "
        f"each evaluated private cloud platform. All costs include licensing, hardware refresh, "
        f"facilities, labor, and implementation. Savings are calculated against your current state baseline.",
        styles['BodyText2']
    ))
    elements.append(Spacer(1, 0.1*inch))

    # Current state breakdown
    elements.append(Paragraph("Current State Cost Breakdown", styles['SubHeader']))

    current_data = [
        ['Cost Category', f'{years}-Year Cost', '% of Total'],
        ['Hardware Refresh', f"${current_tco['hardware_refresh']:,.0f}",
         f"{round(current_tco['hardware_refresh']/current_tco['total']*100)}%"],
        ['Facilities & Power', f"${current_tco['facilities']:,.0f}",
         f"{round(current_tco['facilities']/current_tco['total']*100)}%"],
        ['Labor (FTE)', f"${current_tco['fte']:,.0f}",
         f"{round(current_tco['fte']/current_tco['total']*100)}%"],
        ['Licensing', f"${current_tco['licensing']:,.0f}",
         f"{round(current_tco['licensing']/current_tco['total']*100)}%"],
        ['Support & Maintenance', f"${current_tco['support']:,.0f}",
         f"{round(current_tco['support']/current_tco['total']*100)}%"],
        ['TOTAL', f"${current_tco['total']:,.0f}", '100%'],
    ]

    current_table = Table(current_data, colWidths=[3*inch, 2*inch, 1.5*inch])
    current_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -2), [LIGHT_GRAY, WHITE]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), LIGHT_BLUE),
        ('GRID', (0, 0), (-1, -1), 0.5, MID_BLUE),
        ('ROWHEIGHT', (0, 0), (-1, -1), 20),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    elements.append(current_table)
    elements.append(Spacer(1, 0.2*inch))

    # Platform comparison table
    elements.append(Paragraph("Platform Comparison Summary", styles['SubHeader']))

    col_widths = [2*inch] + [1.4*inch] * len(selected_platforms)
    headers = ['Metric'] + selected_platforms
    comp_data = [headers]

    rows = [
        (f'{years}-Year TCO', 'total'),
        ('Annual Average', 'annual_average'),
        ('Licensing', 'licensing'),
        ('Hardware', 'hardware_refresh'),
        ('Labor', 'fte'),
        ('Implementation', 'implementation'),
        ('Savings vs Current', 'savings'),
        ('ROI %', 'roi_pct'),
        ('Payback (months)', 'payback_months'),
    ]

    for label, key in rows:
        row = [label]
        for platform in selected_platforms:
            r = scenario_results[platform]
            val = r.get(key, 0)
            if key == 'roi_pct':
                row.append(f"{val}%")
            elif key == 'payback_months':
                row.append(f"{val} mo")
            else:
                row.append(f"${val:,.0f}")
        comp_data.append(row)

    comp_table = Table(comp_data, colWidths=col_widths)

    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT_GRAY, WHITE]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, MID_BLUE),
        ('ROWHEIGHT', (0, 0), (-1, -1), 18),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]

    # Highlight recommended platform column
    if final_recommendation in selected_platforms:
        rec_col = selected_platforms.index(final_recommendation) + 1
        table_style.append(('BACKGROUND', (rec_col, 0), (rec_col, 0), INSIGHT_PINK))
        table_style.append(('BACKGROUND', (rec_col, 1), (rec_col, -1), HexColor('#FFF0F7')))
        table_style.append(('FONTNAME', (rec_col, 1), (rec_col, -1), 'Helvetica-Bold'))

    comp_table.setStyle(TableStyle(table_style))
    elements.append(comp_table)
    elements.append(PageBreak())


def build_recommendation_section(elements, styles, final_recommendation,
                                  scenario_results, discovery, years):
    """Build the platform recommendation section."""

    elements.append(Paragraph("Platform Recommendation", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=2, color=INSIGHT_PINK))
    elements.append(Spacer(1, 0.15*inch))

    rec = scenario_results[final_recommendation]
    fit = rec.get('fit', {})

    # Recommendation banner
    rec_data = [[Paragraph(f"Recommended: {final_recommendation}", ParagraphStyle(
        'RecBanner',
        fontName='Helvetica-Bold',
        fontSize=13,
        textColor=WHITE,
        alignment=TA_CENTER,
        leading=18,
    ))]]
    rec_table = Table(rec_data, colWidths=[7*inch])
    rec_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), INSIGHT_PINK),
        ('ROWHEIGHT', (0, 0), (-1, -1), 40),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    elements.append(rec_table)
    elements.append(Spacer(1, 0.15*inch))

    # Why this recommendation
    elements.append(Paragraph("Why We Recommend This Platform", styles['SubHeader']))

    fit_reasons = fit.get('fit_reasons', [])
    strengths = fit.get('strengths', [])
    considerations = fit.get('considerations', [])

    if fit_reasons:
        elements.append(Paragraph("Environment & Discovery Signals:", styles['BodyText2']))
        for reason in fit_reasons:
            elements.append(Paragraph(f"•  {reason}", styles['BulletText']))
        elements.append(Spacer(1, 0.08*inch))

    if strengths:
        elements.append(Paragraph("Platform Strengths for Your Environment:", styles['BodyText2']))
        for strength in strengths:
            elements.append(Paragraph(f"✓  {strength}", styles['BulletText']))
        elements.append(Spacer(1, 0.08*inch))

    if considerations:
        elements.append(Paragraph("Considerations to Plan For:", styles['BodyText2']))
        for consideration in considerations:
            elements.append(Paragraph(f"⚠  {consideration}", styles['BulletText']))

    elements.append(Spacer(1, 0.15*inch))

    # Fit score summary
    elements.append(Paragraph("Platform Fit Scores", styles['SubHeader']))

    fit_data = [['Platform', 'Fit Score', 'Assessment']]
    for platform, r in scenario_results.items():
        score = r.get('fit', {}).get('fit_score', 0)
        if score >= 70:
            assessment = 'Strong Fit'
        elif score >= 50:
            assessment = 'Good Fit'
        elif score >= 30:
            assessment = 'Moderate Fit'
        else:
            assessment = 'Limited Fit'
        marker = ' ◀ Recommended' if platform == final_recommendation else ''
        fit_data.append([f"{platform}{marker}", f"{score}/100", assessment])

    fit_table = Table(fit_data, colWidths=[3*inch, 1.5*inch, 2*inch])
    fit_style = [
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT_GRAY, WHITE]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('GRID', (0, 0), (-1, -1), 0.5, MID_BLUE),
        ('ROWHEIGHT', (0, 0), (-1, -1), 50),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]
    fit_table.setStyle(TableStyle(fit_style))
    elements.append(fit_table)
    elements.append(PageBreak())


def build_reinvestment_section(elements, styles, scenario_results,
                                final_recommendation, years):
    """Build the reinvestment strategy section."""

    elements.append(Paragraph("Reinvestment Strategy", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=2, color=INSIGHT_PINK))
    elements.append(Spacer(1, 0.15*inch))

    rec = scenario_results[final_recommendation]
    total_savings = rec.get('savings', 0)
    total_roi = rec.get('total', 0)

    elements.append(Paragraph(
        "Private cloud modernization isn't just about cutting costs — it's about redirecting "
        "investment toward the initiatives that drive competitive advantage. The operational "
        "efficiency and financial savings generated by this migration create a strategic "
        "reinvestment fund for your most important growth initiatives.",
        styles['BodyText2']
    ))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        f"Based on your {years}-year analysis, the freed capacity and cost savings of "
        f"<b>${total_savings:,.0f}</b> can be strategically allocated across five innovation "
        f"investment areas. This is not headcount reduction — this is budget and team capacity "
        f"redirected toward building the capabilities your business needs to compete.",
        styles['BodyText2']
    ))
    elements.append(Spacer(1, 0.15*inch))

    # Reinvestment allocation table
    allocations = [
        ('AI & Machine Learning', 0.30, 'Deploy private AI infrastructure for data-sovereign model training, '
         'inference workloads, and GPU-accelerated analytics. Keep sensitive data on-premises '
         'while leveraging enterprise AI capabilities.'),
        ('Application Modernization', 0.25, 'Containerize and modernize legacy applications, '
         'reduce technical debt, and accelerate time-to-market. Move from monolithic architectures '
         'to microservices and event-driven patterns.'),
        ('DevSecOps & Automation', 0.20, 'Build automated CI/CD pipelines with integrated security '
         'scanning, policy enforcement, and compliance automation. Reduce manual toil and '
         'accelerate software delivery velocity.'),
        ('Edge Computing Expansion', 0.15, 'Extend private cloud capabilities to edge locations, '
         'branch offices, and manufacturing environments. Bring compute closer to where data '
         'is generated for real-time processing.'),
        ('Innovation Reserve', 0.10, 'Maintain a strategic reserve for emerging opportunities, '
         'proof-of-concept initiatives, and technology evaluations. Stay agile as the '
         'technology landscape evolves.'),
    ]

    elements.append(Paragraph("Innovation Investment Allocation", styles['SubHeader']))

    alloc_data = [['Investment Area', 'Allocation', f'{years}-Year Budget', 'Strategic Focus']]
    for area, pct, focus in allocations:
        amount = total_savings * pct
        alloc_data.append([area, f"{int(pct*100)}%", f"${amount:,.0f}", focus[:60] + "..."])

    alloc_table = Table(alloc_data, colWidths=[1.8*inch, 0.8*inch, 1.2*inch, 2.8*inch])
    alloc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (3, 0), (3, -1), 'LEFT'),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [LIGHT_GRAY, WHITE]),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, MID_BLUE),
        ('ROWHEIGHT', (0, 0), (-1, -1), 22),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elements.append(alloc_table)
    elements.append(Spacer(1, 0.15*inch))

    # Detail cards for each investment area
    elements.append(Paragraph("Investment Area Detail", styles['SubHeader']))
    for area, pct, focus in allocations:
        amount = total_savings * pct
        card_data = [[
            Paragraph(f"{area}", ParagraphStyle('CardTitle', fontName='Helvetica-Bold',
                      fontSize=10, textColor=WHITE)),
            Paragraph(f"${amount:,.0f} ({int(pct*100)}%)", ParagraphStyle('CardAmount',
                      fontName='Helvetica-Bold', fontSize=10, textColor=WHITE,
                      alignment=TA_RIGHT)),
        ], [
            Paragraph(focus, ParagraphStyle('CardBody', fontName='Helvetica',
                      fontSize=8, textColor=BLACK, leading=12)),
            Paragraph(""),
        ]]
        card_table = Table(card_data, colWidths=[4.5*inch, 2*inch])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), MID_BLUE),
            ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BLUE),
            ('GRID', (0, 0), (-1, -1), 0.5, MID_BLUE),
            ('ROWHEIGHT', (0, 0), (-1, 0), 20),
            ('ROWHEIGHT', (0, 1), (-1, 1), 35),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('SPAN', (0, 1), (1, 1)),
        ]))
        elements.append(card_table)
        elements.append(Spacer(1, 0.05*inch))

    elements.append(PageBreak())


def build_roadmap_section(elements, styles, final_recommendation):
    """Build the 5-phase roadmap section."""

    elements.append(Paragraph("Your Private Cloud Journey", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=2, color=INSIGHT_PINK))
    elements.append(Spacer(1, 0.15*inch))

    roadmap = get_roadmap(final_recommendation)
    if not roadmap:
        return

    elements.append(Paragraph(roadmap['tagline'], styles['BodyText2']))
    elements.append(Spacer(1, 0.1*inch))

    # Phase timeline visual
    phase_colors = [DARK_BLUE, MID_BLUE, HexColor('#4472C4'), GREEN, ORANGE]
    phase_data = [[]]
    for i, phase in enumerate(roadmap['phases']):
        phase_data[0].append(
            Paragraph(
                f"Phase {phase['number']}\n{phase['name'].split('—')[0].strip()}\n{phase['timeline']}",
                ParagraphStyle('PhaseCell', fontName='Helvetica-Bold', fontSize=8,
                               textColor=WHITE, alignment=TA_CENTER, leading=11)
            )
        )

    phase_table = Table(phase_data, colWidths=[1.35*inch] * 5)
    phase_style = [
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ROWHEIGHT', (0, 0), (-1, -1), 45),
        ('GRID', (0, 0), (-1, -1), 1, WHITE),
    ]
    for i, color in enumerate(phase_colors):
        phase_style.append(('BACKGROUND', (i, 0), (i, 0), color))
    phase_table.setStyle(TableStyle(phase_style))
    elements.append(phase_table)
    elements.append(Spacer(1, 0.2*inch))

    # Phase detail
    for i, phase in enumerate(roadmap['phases']):
        color = phase_colors[i]

        # Phase header
        header_data = [[
            Paragraph(f"Phase {phase['number']} — {phase['name']}", ParagraphStyle(
                'PhaseHeader', fontName='Helvetica-Bold', fontSize=11,
                textColor=WHITE, alignment=TA_LEFT)),
            Paragraph(phase['timeline'], ParagraphStyle(
                'PhaseTimeline', fontName='Helvetica-Bold', fontSize=10,
                textColor=WHITE, alignment=TA_RIGHT)),
        ]]
        header_table = Table(header_data, colWidths=[5*inch, 2*inch])
        header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), color),
            ('ROWHEIGHT', (0, 0), (-1, -1), 24),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        # Objective
        obj_data = [[Paragraph(f"Objective: {phase['objective']}", ParagraphStyle(
            'PhaseObj', fontName='Helvetica-Oblique', fontSize=9,
            textColor=DARK_BLUE, leading=13))]]
        obj_table = Table(obj_data, colWidths=[7*inch])
        obj_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), LIGHT_BLUE),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('ROWHEIGHT', (0, 0), (-1, -1), 24),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        # Activities and exit criteria
        activities_text = '\n'.join([f"• {a}" for a in phase['activities']])
        exit_text = '\n'.join([f"✓ {e}" for e in phase['exit_criteria']])

        detail_data = [[
            Paragraph('<b>Key Activities & Outputs</b><br/>' +
                      '<br/>'.join([f"• {a}" for a in phase['activities']]),
                      ParagraphStyle('PhaseDetail', fontName='Helvetica', fontSize=8,
                                     leading=12, leftIndent=4)),
            Paragraph('<b>Exit Criteria</b><br/>' +
                      '<br/>'.join([f"✓ {e}" for e in phase['exit_criteria']]),
                      ParagraphStyle('PhaseDetail2', fontName='Helvetica', fontSize=8,
                                     leading=12, leftIndent=4)),
        ]]
        detail_table = Table(detail_data, colWidths=[3.5*inch, 3.5*inch])
        detail_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), WHITE),
            ('GRID', (0, 0), (-1, -1), 0.5, LIGHT_BLUE),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))

        elements.append(KeepTogether([
            header_table,
            obj_table,
            detail_table,
            Spacer(1, 0.1*inch),
        ]))

    elements.append(PageBreak())


def build_next_steps_section(elements, styles, customer_name, final_recommendation,
                              scenario_results, preparer_name, discovery):
    """Build the next steps and call to action section."""

    elements.append(Paragraph("Recommended Next Steps", styles['SectionHeader']))
    elements.append(HRFlowable(width="100%", thickness=2, color=INSIGHT_PINK))
    elements.append(Spacer(1, 0.15*inch))

    renewal_urgency = discovery.get('renewal_urgency', 'low')
    time_horizon = discovery.get('time_horizon', '-- Select --')

    if renewal_urgency == 'high':
        urgency_text = ("Your VMware renewal is imminent. Acting now avoids automatic renewal "
                       "at significantly increased Broadcom pricing and preserves your ability "
                       "to negotiate from a position of strength.")
    elif renewal_urgency == 'medium':
        urgency_text = ("With a VMware renewal within 12 months, you have a strategic window "
                       "to begin migration planning now and avoid renewal lock-in.")
    else:
        urgency_text = ("Now is the ideal time to begin planning your private cloud journey. "
                       "Starting the assessment and architecture process positions you to "
                       "execute when the timing is right for your organization.")

    elements.append(Paragraph(urgency_text, styles['BodyText2']))
    elements.append(Spacer(1, 0.1*inch))

    # 3-step engagement
    elements.append(Paragraph("Insight's 3-Step Engagement Model", styles['SubHeader']))

    steps = [
        ("Step 1", "Vision & Roadmap Workshop", "4-8 Hours",
         f"Collaborate with your team to validate this analysis, align stakeholders, define "
         f"success criteria, and produce an approved roadmap and business case for {final_recommendation}. "
         f"This is a funded engagement available through Insight."),
        ("Step 2", "Architecture & Proof of Concept", "2-4 Weeks",
         f"Deploy a scoped proof of concept to validate {final_recommendation} against your "
         f"specific workloads and operational requirements. Produces a reference architecture "
         f"and go/no-go decision framework."),
        ("Step 3", "Full Deployment & Migration", "Per Roadmap",
         f"Execute the full {final_recommendation} deployment per the 5-phase roadmap, "
         f"including workload migration, operational enablement, and self-service activation. "
         f"Insight provides end-to-end delivery and knowledge transfer."),
    ]

    for step_num, step_name, timeline, description in steps:
        step_data = [[
            Paragraph(step_num, ParagraphStyle('StepNum', fontName='Helvetica-Bold',
                      fontSize=14, textColor=WHITE, alignment=TA_CENTER)),
            Paragraph(f"<b>{step_name}</b>  |  {timeline}", ParagraphStyle('StepTitle',
                      fontName='Helvetica-Bold', fontSize=11, textColor=WHITE)),
        ], [
            Paragraph(""),
            Paragraph(description, ParagraphStyle('StepDesc', fontName='Helvetica',
                      fontSize=9, textColor=BLACK, leading=13)),
        ]]
        step_table = Table(step_data, colWidths=[0.8*inch, 6.2*inch])
        step_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
            ('BACKGROUND', (0, 1), (-1, 1), LIGHT_BLUE),
            ('ROWHEIGHT', (0, 0), (-1, 0), 28),
            ('TOPPADDING', (0, 1), (-1, 1), 8),
            ('BOTTOMPADDING', (0, 1), (-1, 1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('SPAN', (0, 0), (0, 1)),
            ('BACKGROUND', (0, 0), (0, 1), INSIGHT_PINK),
            ('GRID', (0, 0), (-1, -1), 0.5, MID_BLUE),
        ]))
        elements.append(step_table)
        elements.append(Spacer(1, 0.08*inch))

    elements.append(Spacer(1, 0.2*inch))

    # Call to action
    cta_data = [[Paragraph(
        f"Ready to take the next step? Contact your Insight account team to schedule "
        f"your Vision & Roadmap Workshop and begin the journey to {final_recommendation}.",
        ParagraphStyle('CTA', fontName='Helvetica-Bold', fontSize=11,
                       textColor=WHITE, alignment=TA_CENTER, leading=16)
    )]]
    cta_table = Table(cta_data, colWidths=[7*inch])
    cta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), INSIGHT_PINK),
        ('ROWHEIGHT', (0, 0), (-1, -1), 60),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 20),
        ('RIGHTPADDING', (0, 0), (-1, -1), 20),
    ]))
    elements.append(cta_table)
    elements.append(Spacer(1, 0.2*inch))

    # Footer disclaimer
    elements.append(HRFlowable(width="100%", thickness=1, color=LIGHT_BLUE))
    elements.append(Spacer(1, 0.1*inch))
    elements.append(Paragraph(
        "This analysis is based on information provided by the customer and industry benchmarks. "
        "Actual costs and savings may vary based on specific environment details, vendor pricing "
        "changes, and implementation variables. Insight recommends validating all assumptions "
        "with current vendor quotes before making final investment decisions.",
        styles['Disclaimer']
    ))
    elements.append(Paragraph(
        "Insight Proprietary and Confidential. Do Not Copy or Distribute. © 2025 Insight. All Rights Reserved.",
        styles['Disclaimer']
    ))


def generate_pdf(customer_name, preparer_name, parsed, current_tco, scenario_results,
                 selected_platforms, final_recommendation, years, discovery,
                 sections=None):
    """Generate the full proposal PDF and return as bytes buffer."""

    if sections is None:
        sections = ['cover', 'executive_summary', 'environment', 'tco',
                   'recommendation', 'reinvestment', 'roadmap', 'next_steps']

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch,
    )

    styles = get_styles()
    elements = []

    if 'cover' in sections:
        build_cover_page(elements, styles, customer_name, preparer_name,
                        final_recommendation, years)
    if 'executive_summary' in sections:
        build_executive_summary(elements, styles, customer_name, parsed, current_tco,
                               scenario_results, final_recommendation, years, discovery)
    if 'environment' in sections:
        build_environment_section(elements, styles, parsed, customer_name)
    if 'tco' in sections:
        build_tco_section(elements, styles, current_tco, scenario_results,
                         selected_platforms, final_recommendation, years)
    if 'recommendation' in sections:
        build_recommendation_section(elements, styles, final_recommendation,
                                    scenario_results, discovery, years)
    if 'reinvestment' in sections:
        build_reinvestment_section(elements, styles, scenario_results,
                                  final_recommendation, years)
    if 'roadmap' in sections:
        build_roadmap_section(elements, styles, final_recommendation)
    if 'next_steps' in sections:
        build_next_steps_section(elements, styles, customer_name, final_recommendation,
                                scenario_results, preparer_name, discovery)

    doc.build(elements)
    buffer.seek(0)
    return buffer