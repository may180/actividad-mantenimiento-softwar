from __future__ import annotations

import argparse
import subprocess
from datetime import date
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "docs" / "taller-mantenimiento.pdf"
REPO_URL = "https://github.com/may180/actividad-mantenimiento-softwar"


def register_fonts() -> tuple[str, str]:
    regular = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
    bold = Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("DejaVu", str(regular)))
        pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(bold)))
        return "DejaVu", "DejaVu-Bold"
    return "Helvetica", "Helvetica-Bold"


def read_commit_history() -> list[str]:
    try:
        output = subprocess.check_output(
            ["git", "-C", str(ROOT), "log", "-5", "--date=short", "--pretty=format:%h | %an | %ad | %s"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
        return output.splitlines() or ["No hay commits disponibles en el checkout."]
    except (OSError, subprocess.CalledProcessError):
        return ["No fue posible consultar el historial Git local."]


def build_report(dashboard: Path, commits: Path) -> None:
    if not dashboard.is_file():
        raise FileNotFoundError(f"No se encontró la captura del prototipo: {dashboard}")
    if not commits.is_file():
        raise FileNotFoundError(f"No se encontró la captura del historial Git: {commits}")

    regular, bold = register_fonts()
    palette = {
        "ink": colors.HexColor("#17343A"),
        "teal": colors.HexColor("#16796E"),
        "muted": colors.HexColor("#66777B"),
        "line": colors.HexColor("#DCE5E3"),
        "soft": colors.HexColor("#F2F7F6"),
    }
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="CoverTitle", parent=styles["Title"], fontName=bold, fontSize=25,
        leading=31, textColor=palette["ink"], alignment=TA_LEFT, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="Deck", parent=styles["Normal"], fontName=regular, fontSize=11,
        leading=17, textColor=palette["muted"], spaceAfter=14,
    ))
    styles.add(ParagraphStyle(
        name="Section", parent=styles["Heading2"], fontName=bold, fontSize=15,
        leading=20, textColor=palette["ink"], spaceBefore=8, spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="Subsection", parent=styles["Heading3"], fontName=bold, fontSize=10,
        leading=14, textColor=palette["teal"], spaceBefore=5, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="BodyTextCustom", parent=styles["BodyText"], fontName=regular,
        fontSize=9, leading=14, textColor=palette["ink"], spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="Small", parent=styles["BodyText"], fontName=regular,
        fontSize=7.5, leading=11, textColor=palette["muted"], spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="TableText", parent=styles["BodyText"], fontName=regular,
        fontSize=7.5, leading=11, textColor=palette["ink"],
    ))
    styles.add(ParagraphStyle(
        name="TableHeader", parent=styles["BodyText"], fontName=bold,
        fontSize=7.5, leading=10, textColor=colors.white,
    ))
    styles.add(ParagraphStyle(
        name="ShellCode", parent=styles["Code"], fontName="Courier",
        fontSize=8, leading=12, textColor=palette["ink"], leftIndent=7,
        backColor=palette["soft"], borderPadding=5, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="CenteredCaption", parent=styles["Small"], alignment=TA_CENTER,
    ))

    doc = SimpleDocTemplate(
        str(OUTPUT), pagesize=letter, rightMargin=0.68 * inch,
        leftMargin=0.68 * inch, topMargin=0.65 * inch, bottomMargin=0.65 * inch,
        title="Taller de mantenimiento de software — Manteni",
        author="Maikol Lozano",
        subject="Informe individual de GitHub y mantenimiento de software",
    )
    story = []
    story.extend([
        Spacer(1, 0.55 * inch),
        Paragraph("TALLER · MANTENIMIENTO DE SOFTWARE", styles["Small"]),
        Spacer(1, 0.18 * inch),
        Paragraph("Manteni", styles["CoverTitle"]),
        Paragraph("Control de mantenimiento · Informe de trabajo individual", styles["Deck"]),
        Spacer(1, 0.12 * inch),
    ])
    identity = [
        [Paragraph("ESTUDIANTE", styles["TableHeader"]), Paragraph("DATOS", styles["TableHeader"])],
        [Paragraph("Nombre", styles["TableText"]), Paragraph("Maikol Lozano", styles["TableText"])],
        [Paragraph("Correo informado", styles["TableText"]), Paragraph("maikollozano6@gmail.com", styles["TableText"])],
        [Paragraph("IdBanner", styles["TableText"]), Paragraph("may180", styles["TableText"])],
        [Paragraph("Repositorio", styles["TableText"]), Paragraph(f'<link href="{REPO_URL}" color="#16796E">{REPO_URL}</link>', styles["TableText"])],
    ]
    info_table = Table(identity, colWidths=[1.65 * inch, 5.35 * inch])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), palette["ink"]),
        ("BACKGROUND", (0, 1), (-1, -1), palette["soft"]),
        ("GRID", (0, 0), (-1, -1), 0.45, palette["line"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 9),
        ("RIGHTPADDING", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.extend([info_table, Spacer(1, 0.25 * inch)])
    story.extend([
        Paragraph("Resumen", styles["Section"]),
        Paragraph(
            "Se presenta Manteni, un prototipo web para consultar activos y órdenes de mantenimiento. "
            "El trabajo organiza cinco historias de usuario, implementa una interfaz estática con interacción "
            "en memoria y documenta el flujo de control de versiones usado en Git y GitHub.",
            styles["BodyTextCustom"],
        ),
        Paragraph("Alcance de la modalidad", styles["Subsection"]),
        Paragraph(
            "El enunciado original plantea una actividad grupal de hasta tres estudiantes. Este informe se "
            "estructura de forma individual a solicitud del estudiante; la aceptación de esta adaptación debe "
            "confirmarse con el docente-tutor. El historial y las capturas incluidos corresponden a evidencia "
            "real disponible en el repositorio, sin atribuir acciones no verificadas.",
            styles["BodyTextCustom"],
        ),
        Paragraph(f"Fecha de elaboración: {date.today().strftime('%d/%m/%Y')}", styles["Small"]),
        PageBreak(),
        Paragraph("1. Producto e historias de usuario", styles["Section"]),
        Paragraph(
            "Manteni organiza el trabajo de mantenimiento mediante un resumen de indicadores, inventario de "
            "activos, órdenes recientes y formularios de demostración.", styles["BodyTextCustom"]
        ),
    ])
    histories = [
        ("HU-01", "Consultar activos", "El panel muestra nombre, ubicación y estado para planificar mantenimiento."),
        ("HU-02", "Registrar activos", "El formulario valida campos obligatorios y agrega el activo a la lista."),
        ("HU-03", "Crear órdenes", "La orden muestra prioridad, activo asociado y estado inicial abierto."),
        ("HU-04", "Priorizar tareas", "La tabla distingue prioridad y estado; el indicador cuenta órdenes abiertas."),
        ("HU-05", "Revisar mi trabajo", "La interfaz presenta cinco historias y enlaza al repositorio individual."),
    ]
    rows = [[Paragraph("ID", styles["TableHeader"]), Paragraph("Objetivo", styles["TableHeader"]), Paragraph("Criterio de aceptación", styles["TableHeader"])]]
    rows.extend([[Paragraph(a, styles["TableText"]), Paragraph(b, styles["TableText"]), Paragraph(c, styles["TableText"])] for a, b, c in histories])
    table = Table(rows, colWidths=[0.55 * inch, 1.35 * inch, 5.1 * inch], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), palette["ink"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, palette["soft"]]),
        ("GRID", (0, 0), (-1, -1), 0.45, palette["line"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    story.extend([
        table,
        Spacer(1, 10),
        Paragraph("Implementación y límites", styles["Subsection"]),
        Paragraph(
            "La aplicación está construida con HTML, CSS y JavaScript sin dependencias de ejecución. Los "
            "activos y órdenes de ejemplo se manejan en memoria del navegador y se pierden al recargar; por "
            "tanto, la entrega es un prototipo funcional para el taller, no un sistema con persistencia ni una "
            "plataforma de producción.", styles["BodyTextCustom"]
        ),
        PageBreak(),
        Paragraph("2. Flujo de trabajo con Git y GitHub", styles["Section"]),
        Paragraph(
            "El repositorio remoto permite consultar el proyecto y el historial publicado. Los comandos "
            "siguientes resumen el flujo de trabajo documentado; los valores entre corchetes se reemplazan "
            "según la rama o el archivo trabajado.", styles["BodyTextCustom"]
        ),
    ])
    commands = [
        ("clone", "git clone " + REPO_URL + ".git", "Obtener una copia local del repositorio."),
        ("status", "git status", "Revisar cambios pendientes."),
        ("branch", "git switch -c mi-rama", "Crear y cambiar a una rama de trabajo."),
        ("add", "git add [archivo]", "Preparar cambios seleccionados."),
        ("commit", 'git commit -m "Describe el cambio"', "Registrar una unidad de trabajo."),
        ("remote", "git remote -v", "Consultar la dirección del repositorio remoto."),
        ("push", "git push -u origin mi-rama", "Publicar la rama en GitHub."),
        ("log", "git log --oneline --decorate", "Consultar el historial de commits."),
        ("ignore", "Agregar archivos locales a .gitignore", "Evitar versionar archivos generados o privados."),
    ]
    cmd_rows = [[Paragraph("Comando", styles["TableHeader"]), Paragraph("Ejemplo", styles["TableHeader"]), Paragraph("Propósito", styles["TableHeader"])]]
    cmd_rows.extend([[Paragraph(a, styles["TableText"]), Paragraph(f"<font name='Courier'>{b}</font>", styles["TableText"]), Paragraph(c, styles["TableText"])] for a, b, c in commands])
    cmd_table = Table(cmd_rows, colWidths=[0.72 * inch, 3.35 * inch, 2.93 * inch], repeatRows=1)
    cmd_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), palette["ink"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, palette["soft"]]),
        ("GRID", (0, 0), (-1, -1), 0.4, palette["line"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.extend([
        cmd_table,
        Spacer(1, 8),
        Paragraph("Historial visible en el checkout al generar este informe", styles["Subsection"]),
    ])
    for commit in read_commit_history():
        story.append(Paragraph(commit.replace("&", "&amp;"), styles["Small"]))
    story.extend([
        Paragraph(f"Rama de trabajo: v0/taller-mantenimiento · Repositorio: {REPO_URL}", styles["Small"]),
        PageBreak(),
        Paragraph("3. Evidencias", styles["Section"]),
        Paragraph("Figura 1. Interfaz del prototipo Manteni ejecutándose en navegador.", styles["BodyTextCustom"]),
    ])
    for image_path, max_height in [(dashboard, 3.1 * inch), (commits, 3.1 * inch)]:
        img = Image(str(image_path))
        img._restrictSize(7.0 * inch, max_height)
        story.append(img)
        if image_path == dashboard:
            story.append(Paragraph("Fuente: captura del prototipo local; los registros visibles son datos de demostración.", styles["CenteredCaption"]))
            story.append(Spacer(1, 8))
            story.append(Paragraph("Figura 2. Historial de commits publicado en GitHub.", styles["BodyTextCustom"]))
        else:
            story.append(Paragraph("Fuente: página pública de commits del repositorio y rama de trabajo.", styles["CenteredCaption"]))
    story.extend([
        Spacer(1, 8),
        Paragraph("Referencias", styles["Section"]),
        Paragraph(
            "Chacon, S., &amp; Straub, B. (2021). <i>Pro Git</i> (2.ª ed.). Apress. "
            "https://git-scm.com/book/es/v2",
            styles["Small"],
        ),
        Paragraph(
            "GitHub. (s. f.). <i>Acerca de GitHub y Git</i>. https://docs.github.com/es/get-started/start-your-journey/about-github-and-git",
            styles["Small"],
        ),
    ])

    def page_chrome(canvas, document):
        canvas.saveState()
        width, height = letter
        canvas.setStrokeColor(palette["line"])
        canvas.line(document.leftMargin, 0.48 * inch, width - document.rightMargin, 0.48 * inch)
        canvas.setFont(regular, 7)
        canvas.setFillColor(palette["muted"])
        canvas.drawString(document.leftMargin, 0.32 * inch, "Maikol Lozano · Taller de mantenimiento de software")
        canvas.drawRightString(width - document.rightMargin, 0.32 * inch, f"{canvas.getPageNumber()}")
        canvas.restoreState()

    doc.build(story, onFirstPage=page_chrome, onLaterPages=page_chrome)
    print(f"Informe generado: {OUTPUT}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Genera el informe individual del taller Manteni.")
    parser.add_argument("--dashboard", type=Path, default=Path("/tmp/v0-workspace/browser/screenshots/manteni-dashboard-solo.png"))
    parser.add_argument("--commits", type=Path, default=Path("/tmp/v0-workspace/browser/screenshots/manteni-github-commits.png"))
    args = parser.parse_args()
    build_report(args.dashboard, args.commits)
