## Requerimientos

Se necesita tener instalado ```python``` y, por supuesto, word. Además, se necesita tener instalada la librería [docxtpl](https://docxtpl.readthedocs.io/en/latest/).
Instalación con pip:

```
pip install docxtpl
```

## Configuración

El script funciona gracias a la información del archivo clases.json, en donde se tiene que configurar el nombre del usuario y la ruta del directorio en dónde se guardan las materias.
Además, el json tiene un arreglo de cursos en donde se guardan los siguientes atributos:

- **id:** el identificador del curso, es utilizado como primer argumento a la hora de llamar al script.
- **professor:** El nombre del docente que imparte el curso.
- **class:** El nombre del curso.
- **class_code:** El código del curso.
- **prof_gender:** El género del docente.
- **path:** El directorio dentro de home en donde se encuentra el curso. (Importante terminar con /). Ejemplo: ruta_a_curso/

### Plantilla de portada

Para el correcto funcionamiento del script, se necesita de un archivo de word llamado ```template.docx```, el repositorio incluye un archivo, pero se puede modificar a voluntad, para que el script funcione necesita encontrar en el archivo diferentes placeholders para reemplazarlos por su valor en base al json y los argumentos de la función:

- {{ title }} - Es el título de el archivo y el segundo argumento a la hora de llamar al script.
- {{ my_name }} - Es el nombre completo del usuario.
- {{ prefix }} - Se calcula en base del género del docente, para escribir Profesor/Profesora/Docente
- {{ professor }} - El nombre completo del docente
- {{ class }} - El nombre del curso
- {{ class_code }} - El código del curso
- {{ date }} - Es la fecha de creación del archivo en formato "\<día\> de \<mes\> de \<año\>"

## Uso

Para utilizar este script, se necesita llamar al script y recibe dos argumentos, el id de la clase y el título del trabajo:
```python ./kiwi.py id "Título del trabajo"```
El script creará una copia de la plantilla, lo moverá a su respectivo directorio y lo nombrará de la siguiente forma:
```"%dia-%mes-%año <Título del trabajo>"```

Esta llamada creará el siguiente archivo 
```python ./kiwi.py id "Hola"``` > ```2023-10-06 Hola.docx```