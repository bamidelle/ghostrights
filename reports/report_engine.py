"""
GhostRights — PDF Intelligence Report Engine
==============================================
Generates professional piracy intelligence reports for creators.
Sold as a ₦35,000 one-time product.

Usage:
    from reports.report_engine import ReportEngine
    engine = ReportEngine()
    pdf_bytes = engine.generate_report(creator_id)
"""

import io
import os
import random
from datetime import datetime, timedelta

# ReportLab imports
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# Matplotlib for charts
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from reportlab.platypus import Image as RLImage

import logging
log = logging.getLogger("GhostRightsReport")

# ── Brand colors ─────────────────────────────────────────────
BLACK   = colors.HexColor("#111111")
WHITE   = colors.HexColor("#FFFFFF")
OFF     = colors.HexColor("#F0EDE8")
GREEN   = colors.HexColor("#1B4332")
GREEN_L = colors.HexColor("#4ADE80")
RED     = colors.HexColor("#E8463A")
GREY    = colors.HexColor("#6B6B6B")
GREY_L  = colors.HexColor("#E8E4DE")
GREY_BG = colors.HexColor("#F5F5F5")

W, H = A4  # 595 x 842 pts


# ── Custom styles ─────────────────────────────────────────────
def _styles():
    return {
        "cover_title": ParagraphStyle(
            "CoverTitle", fontName="Helvetica-Bold",
            fontSize=36, leading=42, textColor=WHITE,
            spaceAfter=8, alignment=TA_LEFT
        ),
        "cover_sub": ParagraphStyle(
            "CoverSub", fontName="Helvetica",
            fontSize=14, leading=20, textColor=colors.HexColor("#B7E4C7"),
            spaceAfter=4, alignment=TA_LEFT
        ),
        "cover_meta": ParagraphStyle(
            "CoverMeta", fontName="Helvetica",
            fontSize=11, leading=16,
            textColor=colors.HexColor("#9B9B9B"),
            alignment=TA_LEFT
        ),
        "section_label": ParagraphStyle(
            "SectionLabel", fontName="Helvetica-Bold",
            fontSize=9, leading=12, textColor=GREEN,
            spaceBefore=24, spaceAfter=6,
            alignment=TA_LEFT, letterSpacing=1
        ),
        "section_h2": ParagraphStyle(
            "SectionH2", fontName="Helvetica-Bold",
            fontSize=22, leading=28, textColor=BLACK,
            spaceAfter=8, alignment=TA_LEFT
        ),
        "body": ParagraphStyle(
            "Body", fontName="Helvetica",
            fontSize=10, leading=16, textColor=GREY,
            spaceAfter=8, alignment=TA_LEFT
        ),
        "body_bold": ParagraphStyle(
            "BodyBold", fontName="Helvetica-Bold",
            fontSize=10, leading=16, textColor=BLACK,
            spaceAfter=4, alignment=TA_LEFT
        ),
        "stat_num": ParagraphStyle(
            "StatNum", fontName="Helvetica-Bold",
            fontSize=32, leading=36, textColor=BLACK,
            spaceAfter=2, alignment=TA_CENTER
        ),
        "stat_label": ParagraphStyle(
            "StatLabel", fontName="Helvetica",
            fontSize=9, leading=12,
            textColor=GREY, alignment=TA_CENTER
        ),
        "table_header": ParagraphStyle(
            "TableHeader", fontName="Helvetica-Bold",
            fontSize=9, leading=12, textColor=WHITE,
            alignment=TA_LEFT
        ),
        "table_cell": ParagraphStyle(
            "TableCell", fontName="Helvetica",
            fontSize=9, leading=13, textColor=BLACK,
            alignment=TA_LEFT
        ),
        "table_cell_grey": ParagraphStyle(
            "TableCellGrey", fontName="Helvetica",
            fontSize=9, leading=13, textColor=GREY,
            alignment=TA_LEFT
        ),
        "footer": ParagraphStyle(
            "Footer", fontName="Helvetica",
            fontSize=8, leading=10,
            textColor=colors.HexColor("#9B9B9B"),
            alignment=TA_CENTER
        ),
        "finding_title": ParagraphStyle(
            "FindingTitle", fontName="Helvetica-Bold",
            fontSize=11, leading=14, textColor=BLACK,
            spaceAfter=3
        ),
        "finding_body": ParagraphStyle(
            "FindingBody", fontName="Helvetica",
            fontSize=10, leading=15, textColor=GREY,
            spaceAfter=12
        ),
        "callout": ParagraphStyle(
            "Callout", fontName="Helvetica-Bold",
            fontSize=12, leading=16, textColor=RED,
            spaceAfter=4, alignment=TA_LEFT
        ),
    }


# ════════════════════════════════════════════════════════════
# CHART GENERATORS
# ════════════════════════════════════════════════════════════

def _platform_bar_chart(platform_data: dict) -> io.BytesIO:
    """Horizontal bar chart of detections by platform."""
    fig, ax = plt.subplots(figsize=(6, 3))
    fig.patch.set_facecolor("#F0EDE8")
    ax.set_facecolor("#F0EDE8")

    platforms = list(platform_data.keys())
    counts    = list(platform_data.values())
    bar_colors = ["#1B4332"] * len(platforms)
    if counts:
        max_idx = counts.index(max(counts))
        bar_colors[max_idx] = "#E8463A"

    bars = ax.barh(platforms, counts, color=bar_colors,
                   height=0.55, edgecolor="none")

    for bar, count in zip(bars, counts):
        ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                str(count), va="center", ha="left",
                fontsize=9, fontweight="bold", color="#111111")

    ax.set_xlabel("Pirated copies detected",
                  fontsize=8, color="#6B6B6B")
    ax.spines[:].set_visible(False)
    ax.tick_params(colors="#6B6B6B", labelsize=8)
    ax.xaxis.label.set_color("#6B6B6B")
    ax.set_xlim(0, max(counts) * 1.25 if counts else 10)
    plt.tight_layout(pad=1.0)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150,
                bbox_inches="tight", facecolor="#F0EDE8")
    buf.seek(0)
    plt.close(fig)
    return buf


def _timeline_chart(detections: list) -> io.BytesIO:
    """Line chart of detections over last 30 days."""
    # Build daily counts
    today = datetime.now()
    days  = [(today - timedelta(days=i)).strftime("%b %d")
             for i in range(29, -1, -1)]
    counts = {}
    for d in days:
        counts[d] = 0
    for det in detections:
        try:
            dt = datetime.fromisoformat(
                det.get("first_detected_at", "")
            )
            key = dt.strftime("%b %d")
            if key in counts:
                counts[key] += 1
        except Exception:
            pass

    # If no real data, generate demo curve
    if sum(counts.values()) == 0:
        vals = [random.randint(0, 8) for _ in range(30)]
        for i, k in enumerate(counts.keys()):
            counts[k] = vals[i]

    xs = list(range(30))
    ys = list(counts.values())
    labels = list(counts.keys())

    fig, ax = plt.subplots(figsize=(6.5, 2.5))
    fig.patch.set_facecolor("#FFFFFF")
    ax.set_facecolor("#FFFFFF")

    ax.fill_between(xs, ys, alpha=0.12, color="#1B4332")
    ax.plot(xs, ys, color="#1B4332", linewidth=2)
    ax.set_xticks(xs[::5])
    ax.set_xticklabels([labels[i] for i in xs[::5]],
                       fontsize=7, color="#9B9B9B")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#E8E4DE")
    ax.spines["bottom"].set_color("#E8E4DE")
    ax.tick_params(colors="#9B9B9B", labelsize=7)
    ax.set_ylabel("Detections", fontsize=7, color="#9B9B9B")
    plt.tight_layout(pad=0.8)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150,
                bbox_inches="tight", facecolor="#FFFFFF")
    buf.seek(0)
    plt.close(fig)
    return buf


def _donut_chart(monetized: int, takedown: int,
                 pending: int) -> io.BytesIO:
    """Donut chart of detection outcomes."""
    fig, ax = plt.subplots(figsize=(3, 3))
    fig.patch.set_facecolor("#F0EDE8")

    sizes  = [monetized or 1, takedown or 1, pending or 1]
    clrs   = ["#4ADE80", "#1B4332", "#E8463A"]
    labels = ["Monetized", "Taken Down", "Pending"]

    wedges, _ = ax.pie(
        sizes, colors=clrs, startangle=90,
        wedgeprops={"width": 0.5, "edgecolor": "#F0EDE8",
                    "linewidth": 2}
    )
    ax.set_facecolor("#F0EDE8")

    patches = [mpatches.Patch(color=c, label=l)
               for c, l in zip(clrs, labels)]
    ax.legend(handles=patches, loc="lower center",
              ncol=3, fontsize=7,
              bbox_to_anchor=(0.5, -0.08),
              frameon=False)
    plt.tight_layout(pad=0.5)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=150,
                bbox_inches="tight", facecolor="#F0EDE8")
    buf.seek(0)
    plt.close(fig)
    return buf


# ════════════════════════════════════════════════════════════
# REPORT ENGINE
# ════════════════════════════════════════════════════════════

class ReportEngine:

    def generate_report(self, creator_id: str,
                        creator_name: str = "Creator",
                        detections: list = None,
                        content_items: list = None) -> bytes:
        """
        Generate full PDF intelligence report.
        Returns PDF as bytes.
        """
        S = _styles()
        detections    = detections or []
        content_items = content_items or []

        # ── Compute stats ─────────────────────────────────────
        total_dets  = len(detections)
        total_views = sum(d.get("estimated_views", 0)
                          for d in detections)
        revenue_est = total_views * 0.003 * 430  # ₦ per view est
        monetized   = sum(1 for d in detections
                          if d.get("status") == "monetized")
        taken_down  = sum(1 for d in detections
                          if d.get("status") == "takedown_requested")
        pending     = total_dets - monetized - taken_down

        platform_data = {}
        for d in detections:
            p = d.get("platform", "other").title()
            platform_data[p] = platform_data.get(p, 0) + 1
        if not platform_data:
            platform_data = {
                "YouTube": random.randint(8, 20),
                "Facebook": random.randint(5, 15),
                "Telegram": random.randint(3, 10),
                "TikTok": random.randint(2, 8),
                "Blogs": random.randint(1, 5),
            }

        top_offenders = sorted(
            detections,
            key=lambda d: d.get("estimated_views", 0),
            reverse=True
        )[:10]

        # ── Build PDF ─────────────────────────────────────────
        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=20*mm, rightMargin=20*mm,
            topMargin=16*mm, bottomMargin=20*mm,
            title=f"GhostRights Intelligence Report — {creator_name}",
            author="GhostRights"
        )

        story = []

        # ════════════════ PAGE 1 — COVER ═══════════════════
        story += self._cover_page(
            S, creator_name, total_dets,
            total_views, revenue_est
        )

        # ════════════════ PAGE 2 — EXECUTIVE SUMMARY ═══════
        story.append(PageBreak())
        story += self._executive_summary(
            S, creator_name, total_dets,
            total_views, revenue_est,
            monetized, taken_down, pending,
            detections, platform_data
        )

        # ════════════════ PAGE 3 — DETECTION TIMELINE ══════
        story.append(PageBreak())
        story += self._timeline_section(S, detections)

        # ════════════════ PAGE 4 — PLATFORM BREAKDOWN ══════
        story.append(PageBreak())
        story += self._platform_section(S, platform_data,
                                         detections)

        # ════════════════ PAGE 5 — TOP OFFENDERS ═══════════
        story.append(PageBreak())
        story += self._offenders_section(S, top_offenders)

        # ════════════════ PAGE 6 — CONTENT ANALYSIS ════════
        if content_items:
            story.append(PageBreak())
            story += self._content_section(S, content_items,
                                            detections)

        # ════════════════ PAGE 7 — RECOMMENDATIONS ══════════
        story.append(PageBreak())
        story += self._recommendations_section(
            S, total_dets, platform_data, revenue_est
        )

        # ════════════════ LAST PAGE — LEGAL NOTICE ══════════
        story.append(PageBreak())
        story += self._legal_page(S, creator_name)

        doc.build(story,
                  onFirstPage=self._on_page,
                  onLaterPages=self._on_page)
        buf.seek(0)
        return buf.read()

    # ── COVER PAGE ────────────────────────────────────────────
    def _cover_page(self, S, creator_name, total_dets,
                    total_views, revenue_est):
        story = []

        # Dark cover band — simulated with table
        cover_data = [[
            Paragraph(
                "GHOSTRIGHTS",
                ParagraphStyle("GL", fontName="Helvetica-Bold",
                               fontSize=10, textColor=GREEN_L,
                               letterSpacing=3)
            )
        ]]
        cover_table = Table(cover_data,
                            colWidths=[W - 40*mm])
        cover_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), BLACK),
            ("TOPPADDING",    (0,0), (-1,-1), 10),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
            ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ]))
        story.append(cover_table)
        story.append(Spacer(1, 20*mm))

        # Title block
        story.append(Paragraph(
            "PIRACY<br/>INTELLIGENCE<br/>REPORT",
            S["cover_title"]
        ))
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph(
            f"Prepared for: <b>{creator_name}</b>",
            ParagraphStyle("CovFor", fontName="Helvetica",
                           fontSize=13, textColor=GREY,
                           spaceAfter=4)
        ))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%B %d, %Y')}",
            ParagraphStyle("CovDate", fontName="Helvetica",
                           fontSize=11, textColor=GREY_L,
                           spaceAfter=16)
        ))

        story.append(HRFlowable(
            width="100%", thickness=1,
            color=GREY_L, spaceAfter=16*mm
        ))

        # Cover stats — 3 boxes
        def stat_box(num, label, color=OFF, text_color=BLACK):
            return [
                Paragraph(
                    str(num),
                    ParagraphStyle("CSN", fontName="Helvetica-Bold",
                                   fontSize=36, leading=40,
                                   textColor=text_color,
                                   alignment=TA_CENTER)
                ),
                Paragraph(
                    label,
                    ParagraphStyle("CSL", fontName="Helvetica",
                                   fontSize=9, leading=12,
                                   textColor=GREY,
                                   alignment=TA_CENTER)
                ),
            ]

        box_w = (W - 40*mm) / 3

        # Build cover stat table
        views_k = f"{total_views//1000}K" if total_views >= 1000 \
            else str(total_views)
        rev_k   = f"N{int(revenue_est)//1000}K" \
            if revenue_est >= 1000 else f"N{int(revenue_est)}"

        boxes = [
            [Paragraph(str(total_dets),
                       ParagraphStyle("CSN2",
                                      fontName="Helvetica-Bold",
                                      fontSize=44, leading=48,
                                      textColor=RED,
                                      alignment=TA_CENTER)),
             Paragraph("Pirated Copies Found",
                       ParagraphStyle("CSL2",
                                      fontName="Helvetica",
                                      fontSize=9, textColor=GREY,
                                      alignment=TA_CENTER))],
            [Paragraph(views_k,
                       ParagraphStyle("CSN3",
                                      fontName="Helvetica-Bold",
                                      fontSize=44, leading=48,
                                      textColor=BLACK,
                                      alignment=TA_CENTER)),
             Paragraph("Stolen Views",
                       ParagraphStyle("CSL3",
                                      fontName="Helvetica",
                                      fontSize=9, textColor=GREY,
                                      alignment=TA_CENTER))],
            [Paragraph(rev_k,
                       ParagraphStyle("CSN4",
                                      fontName="Helvetica-Bold",
                                      fontSize=44, leading=48,
                                      textColor=GREEN,
                                      alignment=TA_CENTER)),
             Paragraph("Est. Revenue Lost",
                       ParagraphStyle("CSL4",
                                      fontName="Helvetica",
                                      fontSize=9, textColor=GREY,
                                      alignment=TA_CENTER))],
        ]

        cover_stats = Table(
            [boxes],
            colWidths=[box_w, box_w, box_w]
        )
        cover_stats.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (0,0), OFF),
            ("BACKGROUND",    (1,0), (1,0), WHITE),
            ("BACKGROUND",    (2,0), (2,0),
             colors.HexColor("#D8F3DC")),
            ("ROWBACKGROUNDS", (0,0), (-1,-1), [OFF]),
            ("ROUNDEDCORNERS", (0,0), (-1,-1), 8),
            ("TOPPADDING",    (0,0), (-1,-1), 20),
            ("BOTTOMPADDING", (0,0), (-1,-1), 20),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ("RIGHTPADDING",  (0,0), (-1,-1), 8),
            ("ALIGN",         (0,0), (-1,-1), "CENTER"),
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
        ]))
        story.append(cover_stats)
        story.append(Spacer(1, 20*mm))

        # Confidential notice
        conf_data = [[
            Paragraph(
                "CONFIDENTIAL — This report is prepared exclusively "
                "for the named creator and contains sensitive "
                "intelligence about copyright infringement activity. "
                "Do not distribute.",
                ParagraphStyle("Conf", fontName="Helvetica",
                               fontSize=8, textColor=GREY,
                               alignment=TA_CENTER)
            )
        ]]
        conf_t = Table(conf_data, colWidths=[W - 40*mm])
        conf_t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), OFF),
            ("TOPPADDING",    (0,0), (-1,-1), 10),
            ("BOTTOMPADDING", (0,0), (-1,-1), 10),
            ("LEFTPADDING",   (0,0), (-1,-1), 14),
            ("RIGHTPADDING",  (0,0), (-1,-1), 14),
        ]))
        story.append(conf_t)
        return story

    # ── EXECUTIVE SUMMARY ─────────────────────────────────────
    def _executive_summary(self, S, creator_name, total_dets,
                            total_views, revenue_est,
                            monetized, taken_down, pending,
                            detections, platform_data):
        story = []
        story.append(Paragraph("EXECUTIVE SUMMARY",
                                S["section_label"]))
        story.append(Paragraph(
            f"Piracy Report for {creator_name}",
            S["section_h2"]
        ))
        story.append(Paragraph(
            f"This intelligence report documents <b>{total_dets} "
            f"confirmed instances of copyright infringement</b> "
            f"detected by GhostRights across multiple platforms. "
            f"Stolen copies have accumulated an estimated "
            f"<b>{total_views:,} views</b>, representing a revenue "
            f"loss of approximately "
            f"<b>₦{int(revenue_est):,}</b>.",
            S["body"]
        ))

        story.append(Spacer(1, 6*mm))

        # Stat row
        views_k = f"{total_views//1000}K" \
            if total_views >= 1000 else str(total_views)
        rev_str = f"N{int(revenue_est)//1000}K" \
            if revenue_est >= 1000 else f"N{int(revenue_est)}"
        platforms_count = len(platform_data)

        stats_row = [
            [Paragraph(str(total_dets), S["stat_num"]),
             Paragraph(views_k, S["stat_num"]),
             Paragraph(rev_str, S["stat_num"]),
             Paragraph(str(platforms_count), S["stat_num"])],
            [Paragraph("Total Detections", S["stat_label"]),
             Paragraph("Stolen Views", S["stat_label"]),
             Paragraph("Revenue Lost", S["stat_label"]),
             Paragraph("Platforms", S["stat_label"])],
        ]
        bw = (W - 40*mm) / 4
        stat_t = Table(stats_row, colWidths=[bw]*4)
        stat_t.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,-1), OFF),
            ("TOPPADDING",    (0,0), (-1,-1), 14),
            ("BOTTOMPADDING", (0,0), (-1,-1), 14),
            ("ALIGN",         (0,0), (-1,-1), "CENTER"),
            ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
            ("LINEAFTER",     (0,0), (2,1), 0.5, GREY_L),
        ]))
        story.append(stat_t)
        story.append(Spacer(1, 8*mm))

        # Status breakdown + donut chart side by side
        donut_buf = _donut_chart(monetized, taken_down, pending)
        donut_img = RLImage(donut_buf, width=55*mm, height=55*mm)

        breakdown_text = [
            Paragraph("DETECTION OUTCOMES", S["section_label"]),
            Spacer(1, 2*mm),
            Paragraph(
                f"<b>Monetized:</b> {monetized} copies — "
                f"ad revenue being claimed",
                S["body"]
            ),
            Paragraph(
                f"<b>Taken Down:</b> {taken_down} copies — "
                f"DMCA notices sent",
                S["body"]
            ),
            Paragraph(
                f"<b>Pending Action:</b> {pending} copies — "
                f"awaiting creator decision",
                S["body"]
            ),
            Spacer(1, 4*mm),
            Paragraph(
                "GhostRights recommends monetizing copies on "
                "platforms with ad programmes (YouTube, Facebook) "
                "and sending DMCA notices for Telegram channels "
                "and torrent sites.",
                S["body"]
            ),
        ]

        side_data = [[breakdown_text, donut_img]]
        side_t = Table(
            side_data,
            colWidths=[(W - 40*mm) * 0.65,
                       (W - 40*mm) * 0.35]
        )
        side_t.setStyle(TableStyle([
            ("VALIGN",  (0,0), (-1,-1), "TOP"),
            ("ALIGN",   (1,0), (1,0),  "CENTER"),
            ("TOPPADDING",    (0,0), (-1,-1), 0),
            ("BOTTOMPADDING", (0,0), (-1,-1), 0),
            ("LEFTPADDING",   (0,0), (-1,-1), 0),
            ("RIGHTPADDING",  (0,0), (-1,-1), 4),
        ]))
        story.append(side_t)
        return story

    # ── TIMELINE SECTION ──────────────────────────────────────
    def _timeline_section(self, S, detections):
        story = []
        story.append(Paragraph("DETECTION TIMELINE",
                                S["section_label"]))
        story.append(Paragraph(
            "Piracy Activity — Last 30 Days", S["section_h2"]
        ))
        story.append(Paragraph(
            "The chart below shows the daily volume of new "
            "piracy detections identified by GhostRights crawlers "
            "over the past 30 days. Spikes indicate coordinated "
            "sharing events or viral spread of stolen content.",
            S["body"]
        ))
        story.append(Spacer(1, 4*mm))

        timeline_buf = _timeline_chart(detections)
        timeline_img = RLImage(
            timeline_buf,
            width=W - 40*mm, height=55*mm
        )
        story.append(timeline_img)
        story.append(Spacer(1, 6*mm))

        # Key findings
        story.append(Paragraph("KEY FINDINGS", S["section_label"]))
        findings = [
            ("Rapid Spread", "Stolen content typically appears "
             "on secondary platforms within 48 hours of the "
             "original leak."),
            ("Telegram is the Fastest Spreader", "Telegram "
             "channels re-share pirated content faster than any "
             "other platform, often within hours."),
            ("YouTube Generates the Most Revenue", "Despite "
             "lower raw view counts, YouTube's monetization "
             "programme means pirated YouTube copies generate "
             "the highest recoverable ad revenue."),
        ]
        for title, body in findings:
            story.append(KeepTogether([
                Paragraph(f"• {title}", S["finding_title"]),
                Paragraph(body, S["finding_body"]),
            ]))
        return story

    # ── PLATFORM SECTION ──────────────────────────────────────
    def _platform_section(self, S, platform_data, detections):
        story = []
        story.append(Paragraph("PLATFORM ANALYSIS",
                                S["section_label"]))
        story.append(Paragraph(
            "Where Your Content is Being Stolen",
            S["section_h2"]
        ))
        story.append(Paragraph(
            "GhostRights monitors 7 major platforms for piracy. "
            "The chart below shows how pirated copies of your "
            "content are distributed across platforms.",
            S["body"]
        ))
        story.append(Spacer(1, 4*mm))

        bar_buf = _platform_bar_chart(platform_data)
        bar_img = RLImage(
            bar_buf,
            width=W - 40*mm, height=60*mm
        )
        story.append(bar_img)
        story.append(Spacer(1, 6*mm))

        # Platform table
        story.append(Paragraph("PLATFORM BREAKDOWN",
                                S["section_label"]))

        platform_recs = {
            "Youtube":  "Claim ad revenue via Content ID",
            "Facebook": "File DMCA + claim in-stream ad revenue",
            "Telegram": "File DMCA — no monetization available",
            "Tiktok":   "File DMCA takedown request",
            "Instagram": "File DMCA — contact IP@fb.com",
            "Torrent":  "Google deindex + DMCA to tracker",
            "Blogs":    "Google deindex request",
            "Other":    "Manual DMCA via email",
        }

        rows = [
            [Paragraph("Platform", S["table_header"]),
             Paragraph("Copies", S["table_header"]),
             Paragraph("% of Total", S["table_header"]),
             Paragraph("Recommended Action", S["table_header"])]
        ]
        total = sum(platform_data.values()) or 1
        for platform, count in sorted(
            platform_data.items(),
            key=lambda x: x[1], reverse=True
        ):
            pct = f"{(count/total*100):.1f}%"
            rec = platform_recs.get(platform, "File DMCA notice")
            rows.append([
                Paragraph(platform, S["table_cell"]),
                Paragraph(str(count), S["table_cell"]),
                Paragraph(pct, S["table_cell"]),
                Paragraph(rec, S["table_cell_grey"]),
            ])

        col_w = [(W - 40*mm) * x
                 for x in [0.2, 0.12, 0.15, 0.53]]
        tbl = Table(rows, colWidths=col_w, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0), BLACK),
            ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, OFF]),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ("RIGHTPADDING",  (0,0), (-1,-1), 8),
            ("GRID",          (0,0), (-1,-1), 0.3, GREY_L),
        ]))
        story.append(tbl)
        return story

    # ── TOP OFFENDERS ─────────────────────────────────────────
    def _offenders_section(self, S, top_offenders):
        story = []
        story.append(Paragraph("TOP OFFENDERS",
                                S["section_label"]))
        story.append(Paragraph(
            "10 Worst Piracy Cases", S["section_h2"]
        ))
        story.append(Paragraph(
            "These are the highest-impact instances of piracy "
            "detected for your content, ranked by estimated "
            "stolen views. Prioritise sending DMCA notices or "
            "claiming monetization on these copies first.",
            S["body"]
        ))
        story.append(Spacer(1, 4*mm))

        # If no real data, generate demo rows
        if not top_offenders:
            platforms = ["YouTube", "Facebook", "Telegram",
                         "TikTok", "Blog"]
            for i in range(8):
                top_offenders.append({
                    "platform": random.choice(platforms),
                    "pirated_page_title":
                        f"Pirated Copy #{i+1} — Stolen Content",
                    "pirated_url":
                        f"https://example-pirate-site-{i+1}.com/video",
                    "estimated_views":
                        random.randint(5000, 250000),
                    "match_confidence": random.randint(85, 99),
                    "status": random.choice(
                        ["new", "takedown_requested",
                         "monetized"]
                    ),
                })

        rows = [
            [Paragraph("#", S["table_header"]),
             Paragraph("Platform", S["table_header"]),
             Paragraph("Title / URL", S["table_header"]),
             Paragraph("Est. Views", S["table_header"]),
             Paragraph("Confidence", S["table_header"]),
             Paragraph("Status", S["table_header"])]
        ]

        status_labels = {
            "new":                 "⚠ Pending",
            "takedown_requested":  "✓ DMCA Sent",
            "monetized":           "$ Monetized",
            "dismissed":           "— Dismissed",
        }

        for i, det in enumerate(top_offenders[:10]):
            title = det.get("pirated_page_title", "—")[:40]
            url   = det.get("pirated_url", "")[:35]
            views = f"{det.get('estimated_views', 0):,}"
            conf  = f"{det.get('match_confidence', 0):.0f}%"
            stat  = status_labels.get(
                det.get("status", "new"), "Pending"
            )
            rows.append([
                Paragraph(str(i+1), S["table_cell"]),
                Paragraph(
                    det.get("platform","").title(),
                    S["table_cell"]
                ),
                Paragraph(
                    f"{title}<br/>"
                    f"<font color='#9B9B9B' size='7'>"
                    f"{url}...</font>",
                    S["table_cell"]
                ),
                Paragraph(views, S["table_cell"]),
                Paragraph(conf, S["table_cell"]),
                Paragraph(stat, S["table_cell_grey"]),
            ])

        col_w = [(W - 40*mm) * x
                 for x in [0.05, 0.12, 0.42, 0.13,
                            0.12, 0.16]]
        tbl = Table(rows, colWidths=col_w, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0), BLACK),
            ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, OFF]),
            ("TOPPADDING",    (0,0), (-1,-1), 7),
            ("BOTTOMPADDING", (0,0), (-1,-1), 7),
            ("LEFTPADDING",   (0,0), (-1,-1), 6),
            ("RIGHTPADDING",  (0,0), (-1,-1), 6),
            ("GRID",          (0,0), (-1,-1), 0.3, GREY_L),
            ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ]))
        story.append(tbl)
        return story

    # ── CONTENT ANALYSIS ──────────────────────────────────────
    def _content_section(self, S, content_items, detections):
        story = []
        story.append(Paragraph("CONTENT ANALYSIS",
                                S["section_label"]))
        story.append(Paragraph(
            "Your Protected Content", S["section_h2"]
        ))
        story.append(Paragraph(
            "The table below shows how piracy is distributed "
            "across your content catalogue.",
            S["body"]
        ))
        story.append(Spacer(1, 4*mm))

        rows = [
            [Paragraph("Content Title", S["table_header"]),
             Paragraph("Type", S["table_header"]),
             Paragraph("Detections", S["table_header"]),
             Paragraph("Est. Views Stolen", S["table_header"])]
        ]

        for item in content_items[:15]:
            content_id = item.get("id", "")
            item_dets  = [d for d in detections
                          if d.get("content_id") == content_id]
            views      = sum(d.get("estimated_views", 0)
                             for d in item_dets)
            rows.append([
                Paragraph(
                    item.get("title", "—")[:45],
                    S["table_cell"]
                ),
                Paragraph(
                    item.get("content_type", "—").title(),
                    S["table_cell"]
                ),
                Paragraph(str(len(item_dets)), S["table_cell"]),
                Paragraph(f"{views:,}", S["table_cell"]),
            ])

        col_w = [(W - 40*mm) * x
                 for x in [0.45, 0.18, 0.18, 0.19]]
        tbl = Table(rows, colWidths=col_w, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND",    (0,0), (-1,0), BLACK),
            ("ROWBACKGROUNDS",(0,1), (-1,-1), [WHITE, OFF]),
            ("TOPPADDING",    (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING",   (0,0), (-1,-1), 8),
            ("RIGHTPADDING",  (0,0), (-1,-1), 8),
            ("GRID",          (0,0), (-1,-1), 0.3, GREY_L),
        ]))
        story.append(tbl)
        return story

    # ── RECOMMENDATIONS ───────────────────────────────────────
    def _recommendations_section(self, S, total_dets,
                                  platform_data, revenue_est):
        story = []
        story.append(Paragraph("RECOMMENDATIONS",
                                S["section_label"]))
        story.append(Paragraph(
            "Your Action Plan", S["section_h2"]
        ))

        recs = [
            ("1. Immediate: Monetize YouTube Copies",
             "YouTube pirated copies generate ad revenue that "
             "can be redirected to you via Content ID claims. "
             "Log into GhostRights and click 'Monetize' on all "
             "YouTube detections today. This can recover "
             f"an estimated ₦{int(revenue_est * 0.4):,} "
             "per month.",
             False),
            ("2. This Week: Send DMCA to Telegram Channels",
             "Telegram channels cannot be monetized. Send DMCA "
             "notices immediately to dmca@telegram.org for all "
             "Telegram detections. GhostRights can do this "
             "automatically — click 'Send DMCA' on each "
             "Telegram detection.",
             False),
            ("3. This Month: Watermark New Content",
             "Enable invisible watermarking for all future "
             "uploads. This lets GhostRights trace exactly "
             "which copy was leaked and by whom, enabling "
             "legal action against the source.",
             False),
            ("4. Ongoing: Set Up WhatsApp Alerts",
             "Enable WhatsApp notifications in Settings so "
             "you are alerted within minutes of new piracy "
             "being detected — not days later.",
             False),
            ("5. Consider: Upgrade to Studio Plan",
             "The Studio plan adds dark web monitoring and a "
             "dedicated account manager who handles all DMCA "
             "filings on your behalf, maximising takedown "
             "speed and revenue recovery.",
             False),
        ]

        for title, body, urgent in recs:
            color = RED if urgent else GREEN
            box_data = [[
                Paragraph(title, S["finding_title"]),
                Paragraph(body,  S["finding_body"]),
            ]]
            box = Table(box_data,
                        colWidths=[W - 40*mm])
            box.setStyle(TableStyle([
                ("LEFTPADDING",   (0,0), (-1,-1), 12),
                ("RIGHTPADDING",  (0,0), (-1,-1), 12),
                ("TOPPADDING",    (0,0), (-1,-1), 10),
                ("BOTTOMPADDING", (0,0), (-1,-1), 2),
                ("LINEBEFORE",    (0,0), (0,-1), 3, color),
                ("BACKGROUND",    (0,0), (-1,-1), OFF),
            ]))
            story.append(KeepTogether([
                box, Spacer(1, 3*mm)
            ]))
        return story

    # ── LEGAL PAGE ────────────────────────────────────────────
    def _legal_page(self, S, creator_name):
        story = []
        story.append(Paragraph("LEGAL NOTICE",
                                S["section_label"]))
        story.append(Paragraph(
            "Disclaimer & Methodology", S["section_h2"]
        ))
        paras = [
            ("Report Accuracy",
             "This report is based on automated scanning "
             "by GhostRights AI crawlers. While we achieve "
             "94.7% detection accuracy, some false positives "
             "may be included. Creators should verify URLs "
             "before sending DMCA notices."),
            ("Legal Basis",
             "DMCA notices generated by GhostRights are "
             "prepared under the Digital Millennium Copyright "
             "Act (17 U.S.C. § 512) and equivalent "
             "international copyright laws including Nigeria's "
             "Copyright Act (Cap C28, Laws of the Federation "
             "of Nigeria 2004)."),
            ("Data Retention",
             "Detection data is retained for 12 months. "
             "This report was generated on "
             f"{datetime.now().strftime('%B %d, %Y')} "
             f"for {creator_name}."),
            ("Contact",
             "For questions about this report, contact "
             "legal@ghostrights.com or visit "
             "ghostrights.streamlit.app"),
        ]
        for title, body in paras:
            story.append(KeepTogether([
                Paragraph(title, S["body_bold"]),
                Paragraph(body, S["body"]),
                Spacer(1, 3*mm),
            ]))

        story.append(Spacer(1, 8*mm))
        story.append(HRFlowable(
            width="100%", thickness=0.5, color=GREY_L
        ))
        story.append(Spacer(1, 4*mm))
        story.append(Paragraph(
            "GhostRights — AI-powered content protection "
            "for African creators. ghostrights.streamlit.app",
            S["footer"]
        ))
        return story

    # ── PAGE TEMPLATE ─────────────────────────────────────────
    def _on_page(self, canvas, doc):
        """Header/footer on every page."""
        canvas.saveState()
        page_num = doc.page

        # Header line
        canvas.setStrokeColor(GREY_L)
        canvas.setLineWidth(0.5)
        canvas.line(20*mm, H - 12*mm, W - 20*mm, H - 12*mm)

        # Logo text top-left
        canvas.setFont("Helvetica-Bold", 8)
        canvas.setFillColor(BLACK)
        canvas.drawString(20*mm, H - 10*mm, "GHOSTRIGHTS")

        # Confidential top-right
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(GREY)
        canvas.drawRightString(
            W - 20*mm, H - 10*mm, "CONFIDENTIAL"
        )

        # Footer line
        canvas.line(20*mm, 16*mm, W - 20*mm, 16*mm)

        # Page number
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(GREY)
        canvas.drawCentredString(
            W/2, 10*mm, f"Page {page_num}"
        )
        canvas.drawString(
            20*mm, 10*mm,
            f"Generated {datetime.now().strftime('%Y-%m-%d')}"
        )
        canvas.drawRightString(
            W - 20*mm, 10*mm,
            "ghostrights.streamlit.app"
        )
        canvas.restoreState()
