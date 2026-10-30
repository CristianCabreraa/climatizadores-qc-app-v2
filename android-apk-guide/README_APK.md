# 📱 Guía de Compilación y Empaquetado APK para Android
## GreenAir QC - Control Técnico de Climatizadores y Recuperadores

Esta guía explica en detalle cómo compilar, empaquetar y generar el archivo instalable **`.apk`** nativo para teléfonos Android, así como las optimizaciones aplicadas para garantizar fluidez absoluta (**sin bloqueos ni congelamientos**) en el puesto de trabajo.

---

## 🚀 Método 1: Compilación Rápida Local con Capacitor y Android Studio

### Requisitos previos en tu PC
1. **Node.js** (v18 o superior) y **npm**.
2. **Android Studio** con SDK de Android (Android 11 a 14) instalado.
3. Java JDK 17.

### Pasos paso a paso para generar el APK:

```bash
# 1. Situarse en la carpeta del proyecto
cd climatizadores-qc-app

# 2. Instalar las dependencias de Capacitor
npm install

# 3. Añadir la plataforma Android nativa
npx cap add android

# 4. Sincronizar el código web, assets y configuración con Android nativo
npx cap sync android

# 5. Abrir el proyecto en Android Studio
npx cap open android
```

### En Android Studio:
1. Espera a que termine la sincronización de Gradle (barra inferior).
2. Ve al menú superior: **Build > Build Bundle(s) / APK(s) > Build APK(s)**.
3. Al finalizar la compilación (1-2 minutos), aparecerá una notificación abajo a la derecha:
   `APK(s) generated successfully for 1 module: Locate`.
4. Haz clic en **Locate**. Encontrarás tu archivo:
   📁 `android/app/build/outputs/apk/debug/app-debug.apk`.
5. Pásalo a cualquier teléfono Android por cable USB, WhatsApp o Google Drive e instálalo directamente.

---

## ⚡ Método 2: Compilación por Línea de Comandos (Sin abrir Android Studio)

Si ya tienes las variables de entorno de Android SDK (`ANDROID_HOME`) configuradas:

```bash
cd climatizadores-qc-app
npx cap sync android
cd android
./gradlew assembleDebug
```

El APK resultante se encontrará en:
`android/app/build/outputs/apk/debug/app-debug.apk`

---

## ☁️ Método 3: Compilación Automática en la Nube (GitHub Actions - ¡Sin instalar Android Studio!)

Hemos incluido el archivo `.github/workflows/build-apk.yml`. Si subes este proyecto a un repositorio de GitHub:
1. Cada vez que hagas `git push`, GitHub compilará el APK en sus servidores de forma 100% gratuita.
2. Ve a la pestaña **Actions** en tu repositorio en GitHub.
3. Entra en la ejecución más reciente y en la sección **Artifacts** podrás descargar el archivo listo:
   📦 `GreenAir-QC-Instalable.apk`.

---

## 📲 Método 4: Instalación Inmediata como PWA (Sin compilar APK)

La aplicación ya cuenta con `manifest.json` y Service Worker `sw.js`:
1. Inicia el servidor: `agy-node server.js`.
2. Desde el teléfono móvil Android, conéctate a la misma red Wi-Fi y abre en Chrome la dirección IP que muestra la consola (ej: `http://192.168.1.50:3000`).
3. En Google Chrome, presiona el menú de 3 puntos (⋮) y selecciona **"Instalar aplicación"** o **"Agregar a la pantalla principal"**.
4. Se instalará un acceso directo con ícono propio, pantalla completa y soporte para trabajar sin conexión a Internet (offline).

---

## 🛡️ Claves de Optimización de Rendimiento ("Que no se tilde en absoluto")

1. **Downscaling en Canvas antes de almacenar en memoria:**
   - Una fotografía directa de cámara Android pesa entre 5MB y 15MB y tiene resolución de 12 a 48 megapíxeles (descomprimida en memoria ocupa más de 50MB de RAM por foto).
   - El módulo `js/compressor.js` procesa la imagen en un Canvas offscreen inmediatamente tras la captura, reduciéndola a un tamaño máximo de 1280px con compresión JPEG al 78%.
   - **Resultado:** Cada foto pasa de 10MB a solo ~150KB, liberando el 98% de la memoria y evitando cierres forzados (*Out Of Memory* / Crash) en teléfonos de gama baja o media.

2. **Procesamiento Asíncrono no bloqueante:**
   - La lectura OCR y la generación del PDF se ejecutan mediante Web Workers y Promesas asíncronas, impidiendo que la interfaz táctil se congele mientras se procesan los datos.

3. **Pre-procesamiento Binarizado para OCR:**
   - Antes de enviar la imagen de la placa al motor OCR, se aplica un filtro de escala de grises y contraste adaptativo (`js/compressor.js`), eliminando reflejos metálicos habituales en las etiquetas de climatizadores para garantizar un reconocimiento inmediato.
