import os, sys, json, platform, subprocess
from docxtpl import DocxTemplate
from datetime import date

def getDateStr():
    months = [
        "enero", "febrero", "marzo", "abril",
        "mayo", "junio", "julio", "agosto",
        "septiembre", "octubre", "noviembre", "diciembre"
    ]
    today = date.today()
    return f"{today.day} de {months[today.month - 1]} de {today.year}"

def getDateIso():
    today = date.today()
    return today.strftime("%Y-%m-%d")

def getInfo(id):
    with open("./clases.json", "r", encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
    
    for course in data["courses"]:
        if course["id"] == id:
            course["my_name"] = data["my_name"]
            course["home"] = data["home"]
            return course

    print("No se encontró la clase")
    exit()

def main():
    # Change path to current working directory
    os.chdir(sys.path[0])
    info = getInfo(sys.argv[1])
    title = sys.argv[2]
    date = getDateStr()

    path = info.pop("home")
    path += info.pop("path")
    info.pop("id")
    info["date"] = date
    info["title"] = title

    prefix = info.pop("prof_gender")
    if prefix == "M":
        info["prefix"] = "Profesor"
    elif prefix == "F":
        info["prefix"] = "Profesora"
    else:
        info["prefix"] = "Docente" 

    fileName = f'{getDateIso()} {title}.docx'
    doc = DocxTemplate("template.docx")
    doc.render(info)
    doc.save(fileName)
    
    system = platform.system().lower()
    if system == "windows":
        subprocess.run(["powershell", f"mv '{fileName}' '{path}'"])
        subprocess.run(["powershell", f"& '{path+fileName}'"])

    elif system == "darwin":
        subprocess.run(["zsh", f"mv '{fileName}' '{path}'"])
        subprocess.run(["zsh", f"open '{path+fileName}'"])
    else:
        print("Sistema operativo no compatible")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("El primer argumento es el id de la clase y el segundo el título")
        exit()
    main()