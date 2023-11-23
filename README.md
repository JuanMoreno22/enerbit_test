# Prueba Técnica Enerbit

## Inicio Rápido

Sigue estas instrucciones para obtener una copia del proyecto en funcionamiento en tu máquina local.

### Prerrequisitos

Software necesario para ejecutar el proyecto

- Docker
- Docker Compose
- Power BI Desktop (para el reporte Power BI)

### Instalación

Un paso a paso de cómo poner en marcha un entorno de desarrollo en ejecución.

1. Clona el repositorio en tu máquina local.
   ```bash
   git clone https://github.com/JuanMoreno22/enerbit_test.git
   ```

2. Navega al directorio del proyecto y ejecuta Docker Compose para iniciar los servicios necesarios.
   ```bash
   cd ruta/a/tu/proyecto
   docker-compose up
   ```

3. En una nueva consola accede a la carpeta `src` del proyecto para configurar el entorno virtual y las dependencias:

    ####   IMPORTANTE:

    *Despues de activar VENV , verificar si vscode lo tomo como el interprete principal, puede hacerlo mediante el 	comando Ctrl + Shift + p, en el buscador digitar "Select Interpreter" y dar clic. Si no aparece en la lista venv, dar clic en  "Enter interpreter path", 
     Buscar y seleccionar el archivo en la siguiente ruta src\venv\Scripts\python.exe.
     Realizar de nuevo la verificación y si es exitosa proceder con la instalación de las librerías.*

   ```bash
   cd src
   python -m venv venv
   source venv/bin/activate # En Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. Inicia el servidor FastAPI:
   ```bash
   uvicorn app.main:app --reload
   ```

5. Visita `http://127.0.0.1:8000/docs` en tu navegador para ver la documentación interactiva de la API y comenzar a hacer peticiones.

## Uso del Reporte Power BI

Para visualizar y actualizar los datos del reporte en Power BI sigue estos pasos:

1. Asegúrate de tener Power BI Desktop instalado en tu máquina.

2. Abre el archivo de reporte Power BI proporcionado con el proyecto.

3. Una vez abierto el reporte y con todos los servicios en funcionamiento, utiliza el botón "Refresh" en Power BI para actualizar los datos del reporte. Esto conectará directamente con la base de datos y actualizará el reporte con los datos ingresados mediante la API.
