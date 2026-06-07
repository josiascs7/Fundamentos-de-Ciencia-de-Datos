# Fundamentos de Ciencias de Datos

Notebooks y prácticas del curso **Fundamentos de Ciencias de Datos** - TUIA.

## Estructura del proyecto

```
├── Unidad 2 - Manipulacion de Datos/
│   ├── Practica/                 # 9 ejercicios resueltos (limpieza, regex, formatos, etc.)
│   ├── Datasets/                 # Datasets de la unidad
│   └── *.ipynb                   # Notebooks de la unidad
├── Unidad 3 - Analisis Exploratorio de Datos/
│   ├── Práctica/                 # 7 ejercicios resueltos (vinos, titanic, etc.)
│   ├── Datasets/                 # Datasets de la unidad
│   └── *.ipynb                   # Notebooks de la unidad
├── Unidad 4 - Visualizaciones/
│   ├── Practica/                 # 6 ejercicios resueltos (gráficos, geodatos, etc.)
│   ├── Datasets/                 # Datasets de la unidad
│   └── *.ipynb                   # Notebooks de la unidad
├── Unidad 6 - Ajustes y Modelos/
│   ├── Ejemplo/                  # Notebook de ejemplo de regresión lineal
│   ├── Practica 1/               # Ejercicios: bacterias, esperanza de vida
│   ├── Practica 2/               # Ejercicios: student data, penguins, advertising, etc.
│   ├── Datasets/                 # Datasets organizados por práctica
│   └── *.ipynb                   # Notebooks de la unidad
├── Unidad 7 - Métodos avanzados/
│   ├── Datasets/                 # Datasets de la unidad
│   └── *.ipynb                   # Notebooks de la unidad
├── Parciales/
│   ├── Modelo de Examen 1/       # Recuperatorio: consumo energético (EDA + regresión)
│   └── Modelo de Examen 2/       # Parcial integrador: nacimientos (EDA + regresión múltiple)
├── pyproject.toml                # Dependencias del proyecto
└── .python-version               # Versión de Python requerida (3.11)
```

## Requisitos previos

- [Python 3.11](https://www.python.org/downloads/)
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — gestor de entornos y dependencias
- [Visual Studio Code](https://code.visualstudio.com/)
- Extensión de VS Code: **Python** (`ms-python.python`)
- Extensión de VS Code: **Jupyter** (`ms-toolsai.jupyter`)

## Configurar el entorno

1. Clonar o descargar el repositorio y abrirlo en VS Code:

   ```
   Archivo > Abrir carpeta... → seleccionar esta carpeta
   ```

2. Instalar las dependencias con `uv` desde la terminal integrada de VS Code
   (`Ctrl+ñ` o **Terminal > Nueva terminal**):

   ```powershell
   uv sync
   ```

   Esto crea automáticamente el entorno virtual en `.venv/` e instala todos los
   paquetes listados en `pyproject.toml`.

## Seleccionar el intérprete de Python en VS Code

Antes de ejecutar cualquier notebook hay que apuntar VS Code al entorno virtual
del proyecto:

1. Abrir la paleta de comandos: `Ctrl+Shift+P`
2. Escribir y seleccionar: **Python: Select Interpreter**
3. Elegir la opción que muestre la ruta `.venv` dentro de la carpeta del
   proyecto (`.venv\Scripts\python.exe`)

## Ejecutar un notebook

1. Abrir cualquier archivo `.ipynb` desde el explorador de archivos de VS Code.
2. En la esquina superior derecha del notebook, hacer clic en **Select Kernel**.
3. Elegir **Python Environments** y seleccionar el entorno `.venv` del proyecto.
4. Ejecutar celdas individualmente con `Shift+Enter` o todas con
   **Run All** (`Ctrl+F9` / botón ▶▶ en la barra del notebook).

## Dependencias

| Paquete        | Uso principal                                      |
|----------------|----------------------------------------------------|
| `jupyter`      | Entorno de notebooks                               |
| `pandas`       | Manipulación y análisis de datos                   |
| `matplotlib`   | Visualización de datos                             |
| `seaborn`      | Visualización estadística                          |
| `statsmodels`  | Modelos estadísticos y regresión                   |
| `scipy`        | Tests estadísticos y funciones científicas         |
| `openpyxl`     | Lectura/escritura de archivos Excel (`.xlsx`)      |
| `pyarrow`      | Lectura/escritura de archivos Parquet              |
| `lxml`         | Lectura de archivos HTML con pandas                |
| `rapidfuzz`    | Similitud de cadenas de texto (fuzzy matching)     |

## Agregar nuevas dependencias

```powershell
uv add <nombre-del-paquete>
```

Esto actualiza `pyproject.toml` y `uv.lock` automáticamente.
