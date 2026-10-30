/** Guardado y compartición de archivos reales: Android nativo / Web Share / navegador. */
const toBase64 = (blob) => new Promise((resolve, reject) => {
  const reader = new FileReader();
  reader.onerror = () => reject(new Error('No se pudo leer el PDF'));
  reader.onload = () => resolve(String(reader.result).split(',')[1]);
  reader.readAsDataURL(blob);
});

export const ShareEngine = {
  buildSummary(meta = {}, fileName = '') {
    const cp = meta.checkpoints || {};
    const results = [
      ['Presostatos', cp.presostatos],
      ['Ventilador de impulsión', cp.ventImpulsion],
      ['Ventilador de retorno', cp.ventRetorno],
      ['Temperatura de impulsión', cp.tempImpulsion],
      ['Temperatura de retorno', cp.tempRetorno]
    ].map(([name, ok]) => `${name}: ${ok ? 'CORRECTO' : 'INCORRECTO'}`).join('\n');
    return `*GREENAIR INDUSTRIAL — FICHA DE CONTROL Y PRUEBAS*\n` +
      `*Nº Pedido:* ${meta.orderNumber || 'SIN PEDIDO'}\n` +
      `*Nº Serie:* ${meta.serialNumber || 'N/A'}\n` +
      `*Modelo:* ${meta.model || 'N/A'}\n` +
      `*Cuadro:* ${meta.cuadro || 'N/A'}\n` +
      `*Configuración:* ${meta.configuracion || 'N/A'}\n` +
      `*Sonda CO2:* ${meta.optionals?.sondaCo2?.has ? (meta.optionals.sondaCo2.type || 'No especificada') : 'No instalada'}\n` +
      `*Montador:* ${meta.personnel?.montador || 'N/A'}\n` +
      `*Electricista:* ${meta.personnel?.electricista || 'N/A'}\n` +
      `*Verificaciones:*\n${results}\n` +
      `*PDF:* ${fileName}\n` +
      `Fecha: ${new Date().toLocaleString('es-ES')}`;
  },

  async savePdf(blob, fileName) {
    if (!(blob instanceof Blob) || !blob.size) return { success: false, message: 'PDF vacío o no válido.' };
    if (window.GreenAirNative?.savePdf) {
      try {
        // El éxito real se recibe después de que Android escriba el archivo.
        window.GreenAirNative.savePdf(await toBase64(blob), fileName);
        return { success: false, pending: true, method: 'android_picker', message: 'Elige dónde guardar el PDF.' };
      } catch (error) { return { success: false, message: error.message }; }
    }
    if (typeof window.showSaveFilePicker === 'function') {
      try {
        const handle = await window.showSaveFilePicker({
          suggestedName: fileName,
          types: [{ description: 'PDF', accept: { 'application/pdf': ['.pdf'] } }]
        });
        const writer = await handle.createWritable();
        await writer.write(blob);
        await writer.close();
        return { success: true, method: 'file_picker', message: 'PDF guardado correctamente.' };
      } catch (error) {
        if (error?.name === 'AbortError') return { success: false, cancelled: true };
        return { success: false, message: 'Error al guardar el PDF: ' + error.message };
      }
    }
    this.downloadFile(blob, fileName);
    return { success: false, pending: true, method: 'download', message: 'Descarga iniciada; verifica el archivo en Descargas.' };
  },

  async sharePdfNative(blob, fileName, meta = {}, preferred = '') {
    if (!(blob instanceof Blob) || !blob.size) return { success: false, message: 'No hay PDF para compartir.' };
    const summary = this.buildSummary(meta, fileName);
    if (window.GreenAirNative?.sharePdf) {
      try {
        window.GreenAirNative.sharePdf(await toBase64(blob), fileName, summary, preferred);
        return { success: false, pending: true, method: 'android_native', message: 'Preparando el selector nativo con PDF y texto.' };
      } catch (error) { return { success: false, message: error.message }; }
    }
    try {
      const file = new File([blob], fileName, { type: 'application/pdf' });
      if (navigator.canShare?.({ files: [file] }) && navigator.share) {
        await navigator.share({ title: `GreenAir QC — ${meta.orderNumber || meta.serialNumber || ''}`, text: summary, files: [file] });
        return { success: true, method: 'web_share', message: 'Archivo entregado al sistema de compartición; envío no confirmado.' };
      }
    } catch (error) {
      if (error?.name === 'AbortError') return { success: false, cancelled: true };
      return { success: false, message: 'No se pudo compartir: ' + error.message };
    }
    return { success: false, unsupported: true, message: 'Este navegador no permite adjuntar PDF automáticamente.' };
  },

  async shareWhatsApp(meta = {}, fileName = '', blob = null) {
    if (!blob) return { success: false, message: 'Genera antes el PDF.' };
    const result = await this.sharePdfNative(blob, fileName, meta, 'whatsapp');
    if (!result.unsupported) return result;
    this.downloadFile(blob, fileName);
    window.open(`https://api.whatsapp.com/send?text=${encodeURIComponent(this.buildSummary(meta, fileName))}`, '_blank');
    return { success: false, pending: true, message: 'Abierto WhatsApp con el resumen. Adjunta manualmente el PDF descargado.' };
  },

  async shareEmail(meta = {}, fileName = '', blob = null) {
    if (!blob) return { success: false, message: 'Genera antes el PDF.' };
    const result = await this.sharePdfNative(blob, fileName, meta);
    if (!result.unsupported) return result;
    this.downloadFile(blob, fileName);
    const subject = `GreenAir QC — Pedido ${meta.orderNumber || 'SIN PEDIDO'} — Serie ${meta.serialNumber || ''}`;
    window.open(`mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(this.buildSummary(meta, fileName))}`, '_self');
    return { success: false, pending: true, message: 'Correo preparado. Adjunta manualmente el PDF descargado.' };
  },

  downloadFile(blob, fileName) {
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = fileName;
    document.body.appendChild(anchor);
    anchor.click();
    anchor.remove();
    setTimeout(() => URL.revokeObjectURL(url), 30000);
  }
};
