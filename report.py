"""PDF report for the diabetes risk app (English or Bahasa Melayu)."""
from datetime import datetime, timedelta, timezone

from fpdf import FPDF

from content import t, label

BAND_COLOUR = {"Low": (34, 139, 34), "Moderate": (204, 153, 0), "High": (200, 30, 30)}


def malaysia_now():
    # The cloud server runs on UTC; reports show Malaysia time (UTC+8).
    return datetime.now(timezone(timedelta(hours=8))).strftime("%d %b %Y, %I:%M %p (MYT)")


def pdf_safe(text):
    # The built-in PDF font covers Latin-1 only, so swap the few symbols outside it.
    text = str(text).replace("μ", "u").replace("–", "-").replace("’", "'").replace("²", "2")
    return text.encode("latin-1", "replace").decode("latin-1")


def _heading(pdf, text, size=12):
    pdf.set_font("Helvetica", "B", size)
    pdf.cell(0, 8 if size >= 12 else 7, pdf_safe(text), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)


def _bullets(pdf, items):
    for item in items:
        pdf.multi_cell(0, 6, pdf_safe(f"- {item}"), new_x="LMARGIN", new_y="NEXT")


def _table(pdf, header, rows, widths):
    with pdf.table(col_widths=widths, text_align=("LEFT", "LEFT"), line_height=7) as table:
        head = table.row()
        for h in header:
            head.cell(pdf_safe(h))
        for a, b in rows:
            r = table.row()
            r.cell(pdf_safe(a))
            r.cell(pdf_safe(b))


def make_pdf(rows, band, prob, model_name, tips, warning, plan=None, factors=(), lang="en"):
    """Build the PDF report and return its bytes."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(18, 18, 18)
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(0, 10, pdf_safe(t("rep_title", lang)), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(90, 90, 90)
    pdf.cell(0, 6, pdf_safe(t("rep_generated", lang, t=malaysia_now())),
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    pdf.set_text_color(*BAND_COLOUR[band])
    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(0, 9, pdf_safe(t("rep_risk", lang, band=label(band, lang), p=f"{prob:.0%}")),
             new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 6, pdf_safe(t("rep_model", lang, m=model_name)), new_x="LMARGIN", new_y="NEXT")
    if warning:
        pdf.set_font("Helvetica", "B", 10)
        pdf.multi_cell(0, 6, pdf_safe(warning), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    _heading(pdf, t("rep_details", lang))
    _table(pdf, (t("rep_measure", lang), t("rep_value", lang)), rows, (45, 55))
    pdf.ln(4)

    if factors:
        _heading(pdf, t("rep_why", lang))
        _bullets(pdf, factors)
        pdf.ln(4)

    _heading(pdf, t("what_you_can_do", lang))
    _bullets(pdf, tips)
    pdf.ln(4)

    if plan:
        days, food, note, health = plan
        _heading(pdf, t("weekly_plan", lang))
        _table(pdf, (t("day", lang), t("exercise", lang)), days, (25, 75))
        pdf.ln(3)
        _heading(pdf, t("food_guide", lang), size=10)
        _bullets(pdf, food)
        pdf.set_font("Helvetica", "I", 9)
        pdf.multi_cell(0, 5, pdf_safe(note), new_x="LMARGIN", new_y="NEXT")
        if health:
            pdf.ln(2)
            _heading(pdf, t("health_notes", lang), size=10)
            _bullets(pdf, health)
        pdf.ln(4)

    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(90, 90, 90)
    pdf.multi_cell(0, 5, pdf_safe(t("rep_footer", lang)))
    return bytes(pdf.output())
