# 🏭 GreenAir QC — Versión 2.0 (V2)
### Sistema de Control de Calidad, Ensayos Técnicos y Ficha PDF para Climatizadores y Recuperadores Industriales

Aplicación web progresiva (PWA) y aplicación móvil nativa Android para el registro, comprobación técnica y certificación en banco de pruebas de climatizadores y recuperadores de aire GreenAir.

---

## 🚀 Novedades y Mejoras Implementadas en la Versión V2

### 1. 🏠 Nueva Pantalla Principal (Home Screen)
- **Logotipo Oficial GreenAir:** Imagen corporativa auténtica extraída de los recursos de la empresa e integrada en el encabezado.
- **Botón "LOGÍSTICA":** Presenta modal informativo *"Módulo de Logística — Próximamente disponible"* con opción para regresar al menú principal.
- **Botón "ELECTRICIDAD":** Accede al formulario completo de ensayos técnicos sin perder datos al regresar al menú.
- **Navegación Intuitiva:** Botón superior `← Menú` para alternar entre el menú principal y el formulario de ensayos de forma segura.

### 2. 📷 Fotografías Completamente Opcionales (0, 1, 2, 3 o Más)
- Se **eliminó la restricción obligatoria de 3 fotografías** para poder finalizar la ficha técnica.
- Ahora el operario puede finalizar el registro con **0, 1, 2, 3 o más fotos**, según la disponibilidad en planta.
- La maquetación del documento PDF se adapta automáticamente:
  * **0 fotos:** Ficha balanceada y limpia con nota técnica de inspección visual en banco de ensayo.
  * **1 foto:** Fotografía ampliada y centrada con marco técnico y subtítulo.
  * **2 fotos:** Distribución simétrica en dos columnas.
  * **3+ fotos:** Cuadrícula de evidencia fotográfica con badges numerados.

### 3. ⚡ Campo "CUADRO" (Reemplazo de Fabricante)
- Renombrado visiblemente a **CUADRO** en todos los componentes:
  * Formulario principal.
  * Desplegable dinámico con persistencia local (`LocalStorage`).
  * Ventanas modales de alta y gestión (`+ Añadir Cuadro`, `Gestionar Lista`).
  * Ficha técnica del PDF generado.
  * Resúmenes y mensajes de compartición (WhatsApp y correo).
- Mantiene compatibilidad total con los datos previos.

### 4. ⚙️ Campo "CONFIGURACIÓN DE LA MÁQUINA" (Reemplazo de Pre-montador)
- Sustituye el antiguo campo de persona "Pre-montador" por **Configuración de la Máquina**.
- Permite seleccionar la configuración técnica del equipo, añadir nuevas configuraciones con el botón `+ Añadir` y eliminar las que no se utilicen.
- La configuración seleccionada queda registrada en la ficha de identificación del PDF y en el historial.
- Los campos de **Montador** y **Electricista** se conservan intactos como personas responsables con sus respectivas líneas de firma digital en el PDF.

### 5. 📄 Generación y Guardado Real del PDF
- Verificación de integridad del PDF generado con `jsPDF` antes de mostrar la pantalla de confirmación.
- **Pantalla Post-Generación Optimizada:**
  * Estado: **"Ficha generada correctamente"**
  * Nombre del archivo: `[Nº_Serie]_Ficha_Pruebas.pdf`
  * Botones de acción directos:
    1. **GUARDAR PDF:** Utiliza la API nativa `showSaveFilePicker()` en Windows/escritorio para permitir al usuario elegir la carpeta y el nombre exacto de guardado (o descarga directa en móviles).
    2. **COMPARTIR PDF:** Comparte el archivo PDF real usando `navigator.share({ files: [pdf] })`.
    3. **FINALIZAR:** Cierra el proceso y confirma la finalización del ensayo.

### 6. 📲 Compartición de Archivo PDF Real
- **Android / Dispositivos Móviles:** Al pulsar **COMPARTIR PDF**, se abre el menú nativo del sistema operativo adjuntando el documento PDF real para enviarlo a través de **WhatsApp**, **Gmail**, **Google Drive**, Bluetooth o Telegram.
- **WhatsApp Directo:** Descarga el archivo PDF y abre la conversación con el resumen técnico formateado para que el usuario pueda adjuntar el archivo recién descargado.
- **Gmail Directo:** Descarga el PDF y abre el compositor de correo con asunto y cuerpo pre-rellenados.

---

## 📦 Archivos del Proyecto y APK V2 Compilado

```
climatizadores-qc-app/
├── GreenAir-QC-v2.apk                  <-- ¡APK V2 INSTALABLE LISTO PARA ANDROID! (3.85 MB)
├── GreenAir-QC-v1.apk                  <-- APK V1 previo respaldado
├── index.html                          <-- Interfaz V2 (Home Screen + Formulario)
├── manifest.json                       <-- Manifiesto PWA
├── server.js                           <-- Servidor HTTP local con cero dependencias
├── compile_apk.ps1                     <-- Script de compilación y firma automática
├── js/
│   ├── app.js                          <-- Controlador V2 y navegación
│   ├── ocr.js                          <-- Motor OCR neuronal y parser de placas
│   ├── storage.js                      <-- Gestor LocalStorage (Cuadro, Configuración, Personal)
│   ├── pdf-generator.js                <-- Generador PDF maquetado V2 con fotos opcionales
│   ├── share.js                        <-- Motor de guardado nativo y compartición real
│   └── compressor.js                   <-- Compresor Canvas offscreen anti-bloqueos
├── css/
│   └── styles.css                      <-- Estilos táctiles industriales
├── assets/
│   ├── greenair-logo.png               <-- Logotipo corporativo oficial GreenAir
│   └── sample-plate.jpg                <-- Fotografía real de la etiqueta técnica GISER
└── android/                            <-- Proyecto Android nativo (Capacitor/Gradle)
```

---

## 🛠️ Cómo Probar la Aplicación V2

### Opción 1: Probar en el Navegador de la PC o Teléfono por Wi-Fi
El servidor local ya se encuentra en ejecución:
- **En tu computadora:** Abre `http://localhost:3000` en Chrome o Edge.
- **En tu teléfono celular:** Conéctate a la misma red Wi-Fi y abre en el navegador móvil la dirección `http://192.168.1.97:3000`.

### Opción 2: Instalar el APK V2 en tu Teléfono Android
1. El archivo instalable ya está compilado y firmado:
   📁 `C:\Users\GreenAir\Desktop\APP ELECTRICIDAD\climatizadores-qc-app\GreenAir-QC-v2.apk`
2. Pásalo a tu celular (por WhatsApp Web, cable USB o Google Drive).
3. En tu teléfono, pulsa sobre el archivo `GreenAir-QC-v2.apk` e instálalo directamente.
