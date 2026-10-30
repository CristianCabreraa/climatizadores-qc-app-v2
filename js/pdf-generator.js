/**
 * Professional Industrial PDF Report Generator - GreenAir QC V2
 * Generates an executive-grade quality inspection sheet using jsPDF
 * Includes equipment metadata, CUADRO, CONFIGURACIÓN, checkpoints, optional components, personnel signatures, and adaptive photo gallery (0, 1, 2, 3+ photos).
 */

export const PDFGenerator = {
  /**
   * Generates the PDF document
   * @param {Object} data - Full form data
   * @returns {Promise<{doc: any, blob: Blob, fileName: string, objectUrl: string, sizeBytes: number}>}
   */
  async generateReport(data) {
    const { jsPDF } = window.jspdf || {};
    if (!jsPDF) {
      throw new Error('La librería jsPDF no está cargada.');
    }

    // Create A4 portrait document
    const doc = new jsPDF({
      orientation: 'portrait',
      unit: 'mm',
      format: 'a4',
      compress: true
    });

    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 14;
    const contentWidth = pageWidth - (margin * 2);

    const safeSerial = (data.serialNumber || 'SN-SIN-SERIE').replace(/[^a-zA-Z0-9_-]/g, '_');
    const fileName = `${safeSerial}_Ficha_Pruebas.pdf`;

    // ----------------------------------------------------
    // 1. HEADER & BRANDING
    // ----------------------------------------------------
    // Top banner background
    doc.setFillColor(15, 23, 42); // slate-900
    doc.rect(0, 0, pageWidth, 28, 'F');

    // Accent line
    doc.setFillColor(2, 132, 199); // sky-600
    doc.rect(0, 28, pageWidth, 2, 'F');

    // Brand title
    doc.setTextColor(255, 255, 255);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(14);
    doc.text('GREENAIR INDUSTRIAL - SISTEMAS DE CLIMATIZACIÓN', margin, 12);

    doc.setFont('helvetica', 'normal');
    doc.setFontSize(8.5);
    doc.setTextColor(148, 163, 184); // slate-400
    doc.text('CONTROL DE CALIDAD, ENSAYO Y CERTIFICACIÓN DE PUESTA EN MARCHA', margin, 18);
    doc.text(`DOC. REF: QC-CLIMA-${safeSerial}`, margin, 23);

    // Right-aligned status stamp
    doc.setFillColor(16, 185, 129); // emerald-500
    doc.roundedRect(pageWidth - margin - 38, 7, 38, 14, 2, 2, 'F');
    doc.setTextColor(255, 255, 255);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(9);
    doc.text('ENSAYO OK', pageWidth - margin - 19, 14, { align: 'center' });
    doc.setFontSize(6.5);
    doc.setFont('helvetica', 'normal');
    doc.text('CONFORME A NORMA', pageWidth - margin - 19, 18, { align: 'center' });

    let currentY = 35;

    // ----------------------------------------------------
    // 2. EQUIPMENT IDENTIFICATION CARD (CUADRO & CONFIGURACIÓN)
    // ----------------------------------------------------
    doc.setFillColor(241, 245, 249); // slate-100
    doc.roundedRect(margin, currentY, contentWidth, 34, 2, 2, 'F');
    doc.setDrawColor(203, 213, 225); // slate-300
    doc.setLineWidth(0.3);
    doc.roundedRect(margin, currentY, contentWidth, 34, 2, 2, 'S');

    // Card Title
    doc.setTextColor(15, 23, 42);
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(9.5);
    doc.text('DATOS DE IDENTIFICACIÓN DEL EQUIPO (PLACA Y CUADRO ELÉCTRICO)', margin + 4, currentY + 6);

    // Row 1: CUADRO & MODELO
    doc.setFontSize(8.5);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(71, 85, 105);
    doc.text('CUADRO:', margin + 4, currentY + 13.5);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(15, 23, 42);
    doc.text(data.cuadro || data.fabricante || 'GISER', margin + 30, currentY + 13.5);

    doc.setFont('helvetica', 'bold');
    doc.setTextColor(71, 85, 105);
    doc.text('MODELO DE MÁQUINA:', margin + 95, currentY + 13.5);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(2, 132, 199);
    doc.text(data.model || 'N/A', margin + 136, currentY + 13.5);

    // Row 2: Nº DE SERIE & FECHA DE FABRICACIÓN
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(71, 85, 105);
    doc.text('Nº DE SERIE:', margin + 4, currentY + 20.5);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(15, 23, 42);
    doc.text(data.serialNumber || 'N/A', margin + 30, currentY + 20.5);

    doc.setFont('helvetica', 'bold');
    doc.setTextColor(71, 85, 105);
    doc.text('FECHA FABRICACIÓN:', margin + 95, currentY + 20.5);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(15, 23, 42);
    doc.text(data.fabricationDate || 'N/A', margin + 136, currentY + 20.5);

    // Row 3: CONFIGURACIÓN DE LA MÁQUINA & FECHA ENSAYO
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(71, 85, 105);
    doc.text('CONFIGURACIÓN:', margin + 4, currentY + 27.5);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(16, 185, 129); // emerald-600
    doc.text(data.configuracion || 'Estándar', margin + 35, currentY + 27.5);

    doc.setFont('helvetica', 'bold');
    doc.setTextColor(71, 85, 105);
    doc.text('FECHA / HORA ENSAYO:', margin + 95, currentY + 27.5);
    doc.setFont('helvetica', 'normal');
    doc.setTextColor(15, 23, 42);
    const nowStr = new Date().toLocaleString('es-ES', { dateStyle: 'short', timeStyle: 'short' });
    doc.text(nowStr, margin + 136, currentY + 27.5);

    currentY += 39;

    // ----------------------------------------------------
    // 3. CHECKPOINTS TABLE
    // ----------------------------------------------------
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(9.5);
    doc.setTextColor(15, 23, 42);
    doc.text('CHECKPOINTS DE FUNCIONAMIENTO TÉCNICO', margin, currentY);
    currentY += 4;

    const checkpoints = [
      { name: 'Presostatos', checked: data.checkpoints?.presostatos, desc: 'Verificación de corte y rearme por presión diferencial' },
      { name: 'Ventilador de Impulsión', checked: data.checkpoints?.ventImpulsion, desc: 'Sentido de giro, vibraciones, consumo y caudal nominal' },
      { name: 'Ventilador de Retorno', checked: data.checkpoints?.ventRetorno, desc: 'Sentido de giro, balance dinámico y consumo eléctrico' },
      { name: 'Temperatura de Impulsión', checked: data.checkpoints?.tempImpulsion, desc: 'Sonda térmica calibrada y respuesta dinámica' },
      { name: 'Temperatura de Retorno', checked: data.checkpoints?.tempRetorno, desc: 'Sonda térmica calibrada y lectura en consola' },
    ];

    // Table Header
    doc.setFillColor(226, 232, 240); // slate-200
    doc.rect(margin, currentY, contentWidth, 6, 'F');
    doc.setFontSize(8);
    doc.setTextColor(51, 65, 85);
    doc.text('ELEMENTO INSPECCIONADO', margin + 4, currentY + 4.2);
    doc.text('CRITERIO DE ACEPTACIÓN', margin + 55, currentY + 4.2);
    doc.text('ESTADO', margin + 155, currentY + 4.2);
    currentY += 6;

    checkpoints.forEach((cp, idx) => {
      const rowY = currentY;
      const isEven = idx % 2 === 0;
      doc.setFillColor(isEven ? 255 : 248, isEven ? 255 : 250, isEven ? 255 : 252);
      doc.rect(margin, rowY, contentWidth, 6.5, 'F');
      doc.setDrawColor(226, 232, 240);
      doc.line(margin, rowY + 6.5, margin + contentWidth, rowY + 6.5);

      doc.setFont('helvetica', 'bold');
      doc.setFontSize(8);
      doc.setTextColor(15, 23, 42);
      doc.text(cp.name, margin + 4, rowY + 4.4);

      doc.setFont('helvetica', 'normal');
      doc.setFontSize(7.5);
      doc.setTextColor(100, 116, 139);
      doc.text(cp.desc, margin + 55, rowY + 4.4);

      // Status Badge
      if (cp.checked) {
        doc.setFillColor(209, 250, 229); // green-100
        doc.roundedRect(margin + 152, rowY + 1, 24, 4.5, 1, 1, 'F');
        doc.setTextColor(6, 95, 70); // green-800
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(7);
        doc.text('CORRECTO (OK)', margin + 164, rowY + 4.2, { align: 'center' });
      } else {
        doc.setFillColor(254, 226, 226); // red-100
        doc.roundedRect(margin + 152, rowY + 1, 24, 4.5, 1, 1, 'F');
        doc.setTextColor(153, 27, 27); // red-800
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(7);
        doc.text('NO CONFORME', margin + 164, rowY + 4.2, { align: 'center' });
      }

      currentY += 6.5;
    });

    currentY += 4;

    // ----------------------------------------------------
    // 4. OPTIONAL COMPONENTS
    // ----------------------------------------------------
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(9.5);
    doc.setTextColor(15, 23, 42);
    doc.text('COMPONENTES OPCIONALES', margin, currentY);
    currentY += 3.5;

    const optionals = [
      {
        name: 'Sonda de CO2',
        has: data.optionals?.sondaCo2?.has,
        working: data.optionals?.sondaCo2?.working,
        desc: 'Sensor ambiental de ppm de CO2 con salida 0-10V'
      },
      {
        name: 'Mando de Superficie',
        has: data.optionals?.mandoSuperficie?.has,
        working: data.optionals?.mandoSuperficie?.working,
        desc: 'Pantalla mural de control táctil / botonera de usuario'
      }
    ];

    optionals.forEach((opt) => {
      doc.setFillColor(248, 250, 252);
      doc.roundedRect(margin, currentY, contentWidth, 7.5, 1, 1, 'F');
      doc.setDrawColor(226, 232, 240);
      doc.roundedRect(margin, currentY, contentWidth, 7.5, 1, 1, 'S');

      doc.setFont('helvetica', 'bold');
      doc.setFontSize(8);
      doc.setTextColor(15, 23, 42);
      doc.text(opt.name, margin + 4, currentY + 4.8);

      doc.setFont('helvetica', 'normal');
      doc.setFontSize(7.5);
      doc.setTextColor(100, 116, 139);
      doc.text(opt.desc, margin + 50, currentY + 4.8);

      if (opt.has) {
        if (opt.working) {
          doc.setFillColor(209, 250, 229);
          doc.roundedRect(margin + 138, currentY + 1.5, 38, 4.5, 1, 1, 'F');
          doc.setTextColor(6, 95, 70);
          doc.setFont('helvetica', 'bold');
          doc.setFontSize(7);
          doc.text('INSTALADO - PRUEBA OK', margin + 157, currentY + 4.6, { align: 'center' });
        } else {
          doc.setFillColor(254, 243, 199);
          doc.roundedRect(margin + 138, currentY + 1.5, 38, 4.5, 1, 1, 'F');
          doc.setTextColor(146, 64, 14);
          doc.setFont('helvetica', 'bold');
          doc.setFontSize(7);
          doc.text('INSTALADO - PENDIENTE', margin + 157, currentY + 4.6, { align: 'center' });
        }
      } else {
        doc.setFillColor(241, 245, 249);
        doc.roundedRect(margin + 138, currentY + 1.5, 38, 4.5, 1, 1, 'F');
        doc.setTextColor(100, 116, 139);
        doc.setFont('helvetica', 'normal');
        doc.setFontSize(7);
        doc.text('NO INCLUIDO EN MODELO', margin + 157, currentY + 4.6, { align: 'center' });
      }

      currentY += 9;
    });

    currentY += 2;

    // ----------------------------------------------------
    // 5. OPERATIONS PERSONNEL / SIGNATURES (MONTADOR & ELECTRICISTA)
    // ----------------------------------------------------
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(9.5);
    doc.setTextColor(15, 23, 42);
    doc.text('PERSONAL DE OPERACIONES RESPONSABLE', margin, currentY);
    currentY += 3.5;

    const personnelBoxWidth = (contentWidth - 6) / 2;
    const personnelList = [
      { role: 'MONTADOR', subtitle: 'Armó la máquina completa', name: data.personnel?.montador || 'Sin asignar' },
      { role: 'ELECTRICISTA', subtitle: 'Cableó y probó la máquina', name: data.personnel?.electricista || 'Sin asignar' },
    ];

    personnelList.forEach((p, i) => {
      const boxX = margin + (i * (personnelBoxWidth + 6));
      doc.setFillColor(248, 250, 252);
      doc.roundedRect(boxX, currentY, personnelBoxWidth, 20, 1.5, 1.5, 'F');
      doc.setDrawColor(203, 213, 225);
      doc.roundedRect(boxX, currentY, personnelBoxWidth, 20, 1.5, 1.5, 'S');

      doc.setFont('helvetica', 'bold');
      doc.setFontSize(8);
      doc.setTextColor(2, 132, 199);
      doc.text(p.role, boxX + 4, currentY + 4.8);

      doc.setFont('helvetica', 'normal');
      doc.setFontSize(7);
      doc.setTextColor(100, 116, 139);
      doc.text(p.subtitle, boxX + 4, currentY + 8.5);

      doc.setFont('helvetica', 'bold');
      doc.setFontSize(8.5);
      doc.setTextColor(15, 23, 42);
      doc.text(p.name, boxX + 4, currentY + 14);

      // Signature line
      doc.setDrawColor(148, 163, 184);
      doc.setLineDashPattern([1, 1], 0);
      doc.line(boxX + 4, currentY + 17, boxX + personnelBoxWidth - 4, currentY + 17);
      doc.setLineDashPattern([], 0);
    });

    currentY += 25;

    // ----------------------------------------------------
    // 6. PHOTOGRAPHIC EVIDENCE (ADAPTIVE: 0, 1, 2, 3+ PHOTOS)
    // ----------------------------------------------------
    const photos = data.photos || [];
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(9.5);
    doc.setTextColor(15, 23, 42);
    doc.text(`EVIDENCIA FOTOGRÁFICA DE FUNCIONAMIENTO (${photos.length} ${photos.length === 1 ? 'FOTOGRAFÍA' : 'FOTOGRAFÍAS'})`, margin, currentY);
    currentY += 4;

    if (photos.length === 0) {
      // 0 photos: Clean placeholder, perfectly balanced layout
      doc.setFillColor(248, 250, 252);
      doc.roundedRect(margin, currentY, contentWidth, 16, 1.5, 1.5, 'F');
      doc.setDrawColor(226, 232, 240);
      doc.roundedRect(margin, currentY, contentWidth, 16, 1.5, 1.5, 'S');

      doc.setTextColor(100, 116, 139);
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(8);
      doc.text('No se adjuntaron fotografías adicionales. Comprobación conforme a inspección técnica visual en banco de pruebas.', margin + 6, currentY + 7);
      doc.setFontSize(7);
      doc.setTextColor(148, 163, 184);
      doc.text('Pruebas funcionales de presostatos, ventiladores y sondas térmicas validadas satisfactoriamente.', margin + 6, currentY + 11.5);
      currentY += 20;
    } else if (photos.length === 1) {
      // 1 photo: Centered large
      const pWidth = 84;
      const pHeight = 44;
      const pX = margin + (contentWidth - pWidth) / 2;
      try {
        doc.addImage(photos[0].dataUrl, 'JPEG', pX, currentY, pWidth, pHeight, undefined, 'FAST');
        doc.setDrawColor(15, 23, 42);
        doc.setLineWidth(0.3);
        doc.rect(pX, currentY, pWidth, pHeight, 'S');

        doc.setFillColor(15, 23, 42);
        doc.rect(pX, currentY + pHeight - 5, pWidth, 5, 'F');
        doc.setTextColor(255, 255, 255);
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(7);
        doc.text(`Foto 1: ${photos[0].caption || 'Prueba en servicio'}`, pX + 2, currentY + pHeight - 1.5);
      } catch (e) {
        console.warn('Error al incrustar foto 1 en PDF:', e);
      }
      currentY += pHeight + 6;
    } else if (photos.length === 2) {
      // 2 photos: Side-by-side
      const pWidth = (contentWidth - 6) / 2;
      const pHeight = 42;
      photos.slice(0, 2).forEach((photo, idx) => {
        const pX = margin + (idx * (pWidth + 6));
        try {
          doc.addImage(photo.dataUrl, 'JPEG', pX, currentY, pWidth, pHeight, undefined, 'FAST');
          doc.setDrawColor(15, 23, 42);
          doc.setLineWidth(0.3);
          doc.rect(pX, currentY, pWidth, pHeight, 'S');

          doc.setFillColor(15, 23, 42);
          doc.rect(pX, currentY + pHeight - 5, pWidth, 5, 'F');
          doc.setTextColor(255, 255, 255);
          doc.setFont('helvetica', 'bold');
          doc.setFontSize(7);
          doc.text(`Foto ${idx + 1}: ${photo.caption || 'Prueba en servicio'}`, pX + 2, currentY + pHeight - 1.5);
        } catch (e) {
          console.warn('Error al incrustar foto en PDF:', e);
        }
      });
      currentY += pHeight + 6;
    } else {
      // 3 or more photos: 3 in row
      const pWidth = (contentWidth - 8) / 3;
      const pHeight = 36;
      photos.slice(0, 3).forEach((photo, idx) => {
        const pX = margin + (idx * (pWidth + 4));
        try {
          doc.addImage(photo.dataUrl, 'JPEG', pX, currentY, pWidth, pHeight, undefined, 'FAST');
          doc.setDrawColor(15, 23, 42);
          doc.setLineWidth(0.3);
          doc.rect(pX, currentY, pWidth, pHeight, 'S');

          doc.setFillColor(15, 23, 42);
          doc.rect(pX, currentY + pHeight - 5, pWidth, 5, 'F');
          doc.setTextColor(255, 255, 255);
          doc.setFont('helvetica', 'bold');
          doc.setFontSize(6.5);
          doc.text(`Foto ${idx + 1}: ${photo.caption || 'Prueba'}`, pX + 2, currentY + pHeight - 1.5);
        } catch (e) {
          console.warn('Error al incrustar foto en PDF:', e);
        }
      });
      currentY += pHeight + 6;
    }

    // ----------------------------------------------------
    // 7. FOOTER & COMPLIANCE
    // ----------------------------------------------------
    const footerY = pageHeight - 11;
    doc.setDrawColor(203, 213, 225);
    doc.line(margin, footerY - 2, pageWidth - margin, footerY - 2);

    doc.setFont('helvetica', 'normal');
    doc.setFontSize(7);
    doc.setTextColor(148, 163, 184);
    doc.text('Documento oficial emitido por GreenAir Industrial — Departamento de Calidad y Electricidad.', margin, footerY + 2);
    doc.text(`Registro Electrónico Nº ${safeSerial} | Página 1 de 1`, pageWidth - margin, footerY + 2, { align: 'right' });

    // Output blob and base64
    const blob = doc.output('blob');
    if (!blob || blob.size < 500) {
      throw new Error('El documento PDF generado está vacío o no es válido.');
    }

    const objectUrl = URL.createObjectURL(blob);
    const sizeBytes = blob.size;

    return {
      doc,
      blob,
      fileName,
      objectUrl,
      sizeBytes
    };
  }
};
