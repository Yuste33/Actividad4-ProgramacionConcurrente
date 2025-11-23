#  Sistema de Gestión Mágica del Ministerio (AOP-Python)

Este proyecto implementa un sistema modular de gestión de hechizos utilizando **FastAPI** y aplicando principios de **Programación Orientada a Aspectos (AOP)** y **Arquitectura Limpia**.

## Repositorio del Proyecto

**https://github.com/Yuste33/Actividad4-ProgramacionConcurrente**

---

##  Características Principales

* **AOP Implementado:** Auditoría automática de operaciones y medición de rendimiento mediante decoradores.
* **Seguridad:** Control de acceso basado en roles (`AUROR` vs. `APPRENTICE`) vía Inyección de Dependencias.
* **Interfaz:** Login funcional y Dashboard web (`Jinja2`) para la creación y consulta visual de hechizos.
* **Modularidad:** Separación de código en `core` (Aspectos), `services` (Lógica de Negocio) y `schemas` (Validación de datos).

---

##  Instalación y Uso

### 1. Requisitos

Asegúrate de tener Python 3.8+ instalado.

### 2. Instalación de Dependencias

```bash
pip install -r requirements.txt
