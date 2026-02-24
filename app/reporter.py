import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from app.database import get_recent_incidents, get_avg_mttr

def generate_report(output_path="data/incident_report.pdf"):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc    = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story  = []

    # Title
    story.append(Paragraph("InfraGuard — Incident Report", styles['Title']))
    story.append(Spacer(1, 20))

    # Summary
    incidents = get_recent_incidents(limit=50)
    total     = len(incidents)
    resolved  = sum(1 for i in incidents if i['resolved'])
    avg_mttr  = get_avg_mttr()

    summary = [
        ['Metric',          'Value'],
        ['Total Incidents',  str(total)],
        ['Resolved',         str(resolved)],
        ['Avg MTTR',         f"{avg_mttr}s"],
        ['Heal Rate',        f"{round(resolved/total*100 if total else 0, 1)}%"],
    ]
    t = Table(summary, colWidths=[200, 200])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR',  (0,0), (-1,0), colors.white),
        ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f0f0f0')]),
        ('GRID',  (0,0), (-1,-1), 0.5, colors.grey),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    # Incident log
    if incidents:
        story.append(Paragraph("Incident Log", styles['Heading2']))
        story.append(Spacer(1, 10))
        rows = [['Time', 'Type', 'Severity', 'Value', 'Action', 'MTTR']]
        for i in incidents:
            rows.append([
                str(i['timestamp'])[:16],
                i['type'],
                i['severity'],
                f"{i['metric_value']}%",
                i['action_taken'][:30],
                f"{i['mttr_seconds']}s" if i['mttr_seconds'] else 'Pending'
            ])
        t2 = Table(rows, colWidths=[90, 60, 60, 45, 150, 45])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#00d4ff')),
            ('FONTNAME',   (0,0), (-1,0), 'Helvetica-Bold'),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f5f5f5')]),
            ('GRID',    (0,0), (-1,-1), 0.3, colors.grey),
            ('FONTSIZE',(0,0), (-1,-1), 8),
            ('PADDING', (0,0), (-1,-1), 5),
        ]))
        story.append(t2)

    doc.build(story)
    print(f"[Reporter] PDF generated: {output_path}")
    return output_path
