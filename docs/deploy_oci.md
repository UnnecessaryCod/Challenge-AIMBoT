# Deploy en Oracle Cloud Infrastructure — AIMBOT Knowledge Agent

## Objetivo

Desplegar la aplicación Streamlit del AIMBOT Knowledge Agent usando al menos un servicio de OCI, dejando evidencia de funcionamiento para el challenge.

## Opción recomendada para el MVP

**OCI Compute Instance** (una VM pequeña es suficiente, p. ej. `VM.Standard.E2.1.Micro` del Always Free tier con Ubuntu 22.04).

## 1. Requisitos previos

- Cuenta en Oracle Cloud (https://cloud.oracle.com).
- Repositorio del proyecto publicado en GitHub.
- API key del proveedor de IA elegido (OpenAI, Gemini o Cohere).
- Par de llaves SSH.

## 2. Crear la instancia Compute

1. En la consola OCI: **Compute → Instances → Create Instance**.
2. Imagen: Ubuntu 22.04 (o similar). Shape pequeño es suficiente.
3. Asignar IP pública y cargar la llave SSH pública.
4. Crear la instancia y anotar la IP pública.

## 3. Abrir el puerto 8501

1. Ir a la **VCN → Security List** (o Network Security Group) de la subred de la instancia.
2. Agregar una regla de ingreso:
   - Source CIDR: `0.0.0.0/0`
   - Protocolo: TCP
   - Puerto destino: `8501`
3. En la instancia, abrir también el firewall local:

```bash
sudo iptables -I INPUT -p tcp --dport 8501 -j ACCEPT
```

## 4. Preparar el entorno

```bash
ssh ubuntu@<IP_PUBLICA>

sudo apt update && sudo apt install -y python3-pip python3-venv git
git clone https://github.com/usuario/challenge-aimtalent.git
cd challenge_aimtalent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 5. Configurar variables de entorno

```bash
cp .env.example .env
nano .env   # completar MODEL_PROVIDER y la API key correspondiente
```

Nunca subir `.env` al repositorio.

## 6. Ejecutar la aplicación

```bash
streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

Para dejarla corriendo tras cerrar la sesión SSH:

```bash
nohup streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0 &
```

## 7. Verificar

Abrir en el navegador:

```text
http://<IP_PUBLICA>:8501
```

Probar las preguntas obligatorias (ver README, sección 12) y verificar que:

- La app carga con branding AIMTALENT.
- AimBot responde con fuentes.
- La pregunta fuera de alcance activa el mensaje de fallback.

## 8. Evidencia final para el challenge

- Capturas de la app corriendo en OCI → `assets/screenshots/`
- Video corto de uso → `assets/demo/`
- URL pública (`http://<IP_PUBLICA>:8501`) o captura de la consola OCI mostrando la instancia activa.
