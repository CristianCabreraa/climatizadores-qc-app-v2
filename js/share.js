/**
 * Sharing & File Saving Engine - GreenAir QC V2
 * Handles:
 * - Real PDF file saving (via showSaveFilePicker on desktop / download fallback)
 * - Real PDF file sharing (via Web Share API with actual File object)
 * - WhatsApp & Gmail integrations with automatic PDF download and descriptive assistance
 */

export const ShareEngine = {
  /**
   * Prompts the user where to save the PDF (using File System Access API where available)
   * or downloads directly to the device.
   * @param {Blob} blob 
   * @param {string} fileName 
   * @returns {Promise<{success: boolean, cancelled?: boolean, method: string, message?: string}>}
   */
  async savePdf(blob, fileName) {
    // 1. Try File System Access API (Chromium Windows / Mac / Linux)
    if (window.showSaveFilePicker) {
      try {
        const handle = await window.showSaveFilePicker({
          suggestedName: fileName,
          types: [{
            description: 'Documento PDF (*.pdf)',
            accept: { 'application/pdf': ['.pdf'] }
          }]
        });
        const writable = await handle.createWritable();
        await writable.write(blob);
        await writable.close();
        return {
          success: true,
          method: 'file_picker',
          message: `Archivo guardado correctamente en: ${handle.name}`
        };
      } catch (err) {
        if (err.name === 'AbortError') {
          return { success: false, cancelled: true };
        }
        console.warn('showSaveFilePicker falló, usando método de descarga directa:', err);
      }
    }

    // 2. Standard Download Fallback (Android WebView / Firefox / Safari)
    try {
      this.downloadFile(blob, fileName);
      return {
        success: true,
        method: 'download',
        message: `Archivo descargado en tu carpeta de Descargas: ${fileName}`
      };
    } catch (err) {
      console.error('Error al descargar archivo:', err);
      return {
        success: false,
        method: 'failed',
        message: 'No se pudo guardar el archivo: ' + err.message
      };
    }
  },

  /**
   * Shares the actual PDF file using the native OS share sheet (WhatsApp, Gmail, Drive, etc.)
   * @param {Blob} blob 
   * @param {string} fileName 
   * @param {Object} meta 
   * @returns {Promise<{success: boolean, cancelled?: boolean, method: string, message?: string}>}
   */
  async sharePdfNative(blob, fileName, meta = {}) {
    try {
      const file = new File([blob], fileName, { type: 'application/pdf' });

      // Check if native sharing of files is supported
      if (navigator.canShare && navigator.canShare({ files: [file] })) {
        await navigator.share({
          files: [file],
          title: `Ficha Técnica QC - Nº ${meta.serialNumber || 'SN'}`,
          text: `Ficha de control de calidad y pruebas técnicas: ${meta.model || 'Equipo Climatizador'} (Nº Serie: ${meta.serialNumber || 'N/A'}, Cuadro: ${meta.cuadro || 'N/A'}).`
        });
        return { success: true, method: 'native_file_share' };
      }
    } catch (err) {
      if (err.name === 'AbortError') {
        return { success: false, cancelled: true };
      }
      console.warn('Error en navigator.share con archivos:', err);
    }

    return {
      success: false,
      method: 'unsupported',
      message: 'Tu navegador actual no admite compartir archivos directamente desde esta ventana. Se descargará el PDF para que lo adjuntes.'
    };
  },

  /**
   * WhatsApp share with pre-download of the actual PDF and pre-filled message
   */
  shareWhatsApp(meta = {}, fileName = '', blob = null) {
    if (blob) {
      this.downloadFile(blob, fileName);
    }

    const text = 
`*GREENAIR INDUSTRIAL - FICHA TÉCNICA DE CONTROL Y PRUEBAS*
━━━━━━━━━━━━━━━━━━━━━━
*Cuadro:* ${meta.cuadro || 'N/A'}
*Configuración:* ${meta.configuracion || 'Estándar'}
*Modelo:* ${meta.model || 'N/A'}
*Nº de Serie:* ${meta.serialNumber || 'N/A'}
*Fecha Fabricación:* ${meta.fabricationDate || 'N/A'}
*Fecha Ensayo:* ${new Date().toLocaleDateString('es-ES')}

*Personal Responsable:*
- Montador: ${meta.personnel?.montador || 'N/A'}
- Electricista: ${meta.personnel?.electricista || 'N/A'}

*Estado de Inspección:* ✅ PRUEBAS CONFORMES (OK)
${fileName ? `*Archivo PDF adjunto:* ${fileName}` : ''}
━━━━━━━━━━━━━━━━━━━━━━`;

    const encoded = encodeURIComponent(text);
    const whatsappUrl = `https://api.whatsapp.com/send?text=${encoded}`;
    window.open(whatsappUrl, '_blank');
  },

  /**
   * Gmail share with pre-download of the actual PDF and pre-filled subject/body
   */
  shareEmail(meta = {}, fileName = '', blob = null, useGmailWeb = true) {
    if (blob) {
      this.downloadFile(blob, fileName);
    }

    const subject = `Ficha Técnica Pruebas - Equipo Climatizador [Nº ${meta.serialNumber || 'SN'}] - ${meta.model || ''}`;
    const body = 
`Estimado equipo,

Adjunto la ficha técnica y reporte de pruebas de control de calidad del equipo:

DATOS DEL EQUIPO:
- Cuadro: ${meta.cuadro || 'N/A'}
- Configuración: ${meta.configuracion || 'Estándar'}
- Modelo: ${meta.model || 'N/A'}
- Nº de Serie: ${meta.serialNumber || 'N/A'}
- Fecha de Fabricación: ${meta.fabricationDate || 'N/A'}
- Fecha y Hora de Ensayo: ${new Date().toLocaleString('es-ES')}

PERSONAL ASIGNADO:
- Montador: ${meta.personnel?.montador || 'N/A'}
- Electricista: ${meta.personnel?.electricista || 'N/A'}

ESTADO: PRUEBAS TÉCNICAS COMPLETADAS CON ÉXITO (OK)
Archivo PDF generado: ${fileName || 'Ficha_Tecnica.pdf'}

Saludos cordiales,
Control de Calidad y Electricidad
GreenAir Industrial`;

    if (useGmailWeb) {
      const gmailUrl = `https://mail.google.com/mail/?view=cm&fs=1&su=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      window.open(gmailUrl, '_blank');
    } else {
      const mailtoUrl = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
      window.location.href = mailtoUrl;
    }
  },

  /**
   * Downloads the PDF file directly to device storage
   */
  downloadFile(blob, fileName) {
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = fileName;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    setTimeout(() => URL.revokeObjectURL(link.href), 1500);
  }
};
