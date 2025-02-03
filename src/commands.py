import inquirer, json
from pathlib import Path
from rich import print


def get_script_dir():
    return Path(__file__).resolve().parent


def get_data_path():
    return get_script_dir() / "data" / "data.json"


def check_configuration():
    data_path = get_data_path()
    if not data_path.exists():
        print("[bold red][ERROR][/bold red] Falta configuracin inicial")
        print(
            f"Ejecuta [bold blue]{Path(__file__).name} setup[/bold blue] para configurar el directorio de tus clases"
        )
        exit(1)


def setup_info(path: Path):
    question = inquirer.Text("full_name", message="Escribe tu nombre completo")
    answer = inquirer.prompt([question])

    data_path = get_data_path()

    data_path.parent.mkdir(parents=True, exist_ok=True)
    new_data = {"home": str(path), "my_name": answer["full_name"]}

    # Si el archivo ya existe, cargar su contenido y actualizar solo las propiedades necesarias
    if data_path.exists():
        with open(data_path, "r") as file:
            existing_data = json.load(file)
        existing_data.update(new_data)
        new_data = existing_data

    # Escribir los datos en el archivo JSON
    with open(data_path, "w") as file:
        json.dump(new_data, file, indent=4)

    print(f"Configuración guardada en: [bold blue]{data_path}[/bold blue]")


def add_class():
    check_configuration()

    questions = [
        inquirer.Text("class", message="Nombre de la clase"),
        inquirer.Text("id", message="ID para la clase, ej. Desarrollo Web -> dw"),
        inquirer.Text(
            "class_code", message="Código de la clase, ej. P2025_EAM154LN5 (opcional)"
        ),
        inquirer.Text("professor", message="Nombre del profesor"),
        inquirer.List(
            "prof_gender",
            message="Género del profesor",
            choices=["Male", "Female", "Other"],
        ),
        inquirer.Text(
            "path", message="Nombre del directorio de la clase (ej. desarrollo_web)"
        ),
    ]

    data_path = get_data_path()
    answers = inquirer.prompt(questions)

    answers["path"] = answers["path"].strip().replace("/", "").replace("\\", "")

    with open(data_path, "r") as file:
        data = json.load(file)

    if "courses" not in data:
        data["courses"] = []

    data["courses"].append(answers)

    with open(data_path, "w") as file:
        json.dump(data, file, indent=4)
