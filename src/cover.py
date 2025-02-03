import unicodedata, inquirer, json, os, re, platform

from commands import get_data_path
from docxtpl import DocxTemplate
from pathlib import Path
from today import Today
from rich import print


def normalizar_texto(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = re.sub(r"[^\w\s-]", "", texto).strip().lower()
    texto = re.sub(r"[-\s]+", "-", texto)
    return texto


def generate_cover(id: str = None, title: str = None):
    with open(get_data_path(), "r") as file:
        data = json.load(file)

    if id is None:
        questions = [
            inquirer.List(
                "class",
                message="Selecciona la clase",
                choices=[course["class"] for course in data["courses"]],
            )
        ]
        answers = inquirer.prompt(questions)
        course = next(
            course for course in data["courses"] if course["class"] == answers["class"]
        )
    else:
        course = next(course for course in data["courses"] if course["id"] == id)
        if course is None:
            print(f"[bold red]ERROR[/bold red] No se encontró la clase con id {id}")
            exit(1)

    if title is None:
        question = inquirer.Text("title", message="Título del trabajo")
        answers = inquirer.prompt([question])
        title = answers["title"]

    # change path to current directory
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    prefix = (
        "Profesor"
        if course["prof_gender"] == "Male"
        else "Profesora"
        if course["prof_gender"] == "Female"
        else "Docente"
    )

    doc_name = f"{Today.get_date_iso()}-{normalizar_texto(title)}.docx"

    info = {
        **course,
        "prefix": prefix,
        "my_name": data["my_name"],
        "title": title,
        "date": Today.get_date_str(),
    }

    # Generate the template
    doc = DocxTemplate("./templates/template.docx")
    doc.render(info)
    doc.save(doc_name)

    # Move the file to the course directory
    course_dir = Path(data["home"]) / course["path"]
    course_dir.mkdir(parents=True, exist_ok=True)
    os.rename(doc_name, course_dir / doc_name)

    print(f"Portada generada en: [bold blue]{course_dir / doc_name}[/bold blue]")

    # Open the document with the default application
    if platform.system().lower() == "windows":
        os.system(f'start "" "{course_dir / doc_name}"')

    elif platform.system().lower() == "darwin":
        os.system(f"open {course_dir / doc_name}")

    elif platform.system().lower() == "linux":
        # open the file without logs
        os.system(f"xdg-open {course_dir / doc_name} > /dev/null 2>&1")