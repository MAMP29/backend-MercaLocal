# Backend - Desarrollo de Software I
---

Este repositorio contiene el backend para la página web del proyecto de Desarrollo de Software I, desarrollado en Django.

## Pasos para configurar y ejecutar el proyecto

### 1. Crear y activar un entorno virtual de Python

Es recomendable crear un entorno virtual para gestionar las dependencias del proyecto y evitar conflictos con otras versiones de bibliotecas en el sistema.

- **En Linux/macOS:**

   ```bash
   python3 -m venv nombre-del-entorno
   source nombre-del-entorno/bin/activate
   ```

- **En Windows:**

   ```powershell
   python -m venv nombre-del-entorno
   nombre-del-entorno\Scripts\activate
   ```

### 2. Instalar las dependencias del proyecto

Con el entorno virtual activado, instala las dependencias necesarias listadas en el archivo `requirements.txt`:

   ```bash
   pip install -r requirements.txt
   ```
### 3. Clonar el repositorio

   ```bash
   git clone https://github.com/MAMP29/backend-proyecto.git
   cd backend-proyecto
   ```
   
### 4. Ejecutar el servidor de desarrollo

Para iniciar el servidor en el entorno local, usa el siguiente comando:

   ```bash
   python manage.py runserver
   ```

El servidor estará disponible en `http://127.0.0.1:8000/` de forma predeterminada.

---


## Datos existentes

La base de datos incluye los siguientes registros preconfigurados para realizar pruebas:

### Administrador

   - **First Name:** admin  
   - **Last Name:** project  
   - **Email Address:** admin@test.com  
   - **Username:** the-admin  
   - **Teléfono:** 6543210987  
   - **Ciudad:** Cali  
   - **Password:** admin-test  

### Usuarios

#### Usuario 1 - Cliente Normal

```json
{
   "email": "test@test.com",
   "username": "mauser",
   "first_name": "supra",
   "last_name": "test",
   "telefono": "3123456789",
   "ciudad": "Cali",
   "password": "test1234"
}
```

#### Usuario 2 - Cliente con Permisos de Vendedor

```json
{
   "email": "juan@google.com",
   "username": "jzjuan",
   "first_name": "juan",
   "last_name": "acer",
   "telefono": "3256416459",
   "ciudad": "Jamudi",
   "password": "juan1234"
}
```

---

## Notas adicionales

- **Actualizar dependencias:** Si se añaden nuevas bibliotecas, ejecute `pip freeze > requirements.txt` para mantener el archivo `requirements.txt` actualizado.

En caso de que al momento de utilizar el apartado de registro y se produzca un error con el correo electrónico, cree a nivel de la carpeta manage.py 
un archivo llamado .env y añada la siguiente línea:

```bash
EMAIL_HOST_USER=usuario@gmail.com
EMAIL_HOST_PASSWORD=contraseña
```

Para que el correo electrónico funcione correctamente, es necesario tener una cuenta de correo electrónico de Google, solo en entornos de desarrollo,
no olvide añadir el archivo .env a la lista de ignorados en el archivo .gitignore en caso de que no lo haga.