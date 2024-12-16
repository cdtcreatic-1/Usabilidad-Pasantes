import jsPDF from 'jspdf'; // Librería para la creación de archivos PDF.
import 'jspdf-autotable'; // Extensión de jsPDF que permite crear tablas automáticas en el PDF.
import { Chart } from 'chart.js/auto'; // Librería para generar gráficos dentro de un canvas.
import axios from 'axios';

const marginX = 14; // Margen horizontal usado en el documento PDF.


/* Limpia y ajusta la URL del prototipo de Figma para la captura del iframe.
Elimina el subdominio 'embed.' y el parámetro 'embed-host'. */
const cleanFigmaUrl = (url) => {
    let cleanUrl = url.replace('embed.', '').replace('&embed-host=share', '');
    return cleanUrl;
};

/* Formatea una fecha en una cadena con el formato 'día de mes de año' en español. */
const formatDate = (dateString) => {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
};

/* Configuración predeterminada de estilos para las tablas que se generarán en el PDF.
Incluye propiedades de color, tamaño de fuente, grosor de líneas, entre otros. */
const defaultTableStyles = {
    theme: 'grid', // Tipo de tema de tabla, 'grid' aplica un estilo de cuadrícula.
    styles: {
        lineColor: [0, 0, 0], // Color de las líneas de las tablas (negro).
        lineWidth: 0.2, // Grosor de las líneas de las tablas.
        fontSize: 11, // Tamaño de la fuente del texto dentro de las celdas.
        textColor: '#000', // Color del texto dentro de las celdas (negro).
    },
    headStyles: {
        fillColor: '#BEC0BD', // Color de fondo de la cabecera de la tabla.
        textColor: '#000', // Color del texto de la cabecera (negro).
        fontStyle: 'bold', // Estilo de la fuente de la cabecera (negrita).
    },
};

/* Genera la primera página del PDF, que incluye el título, la información del test de diseño y una tabla con los detalles del mismo. */
const firstPage = async (doc, design_test) => {
    // Obtiene el ID del test de diseño.
    const testId = design_test.test_id;
    let numQuestions = 0;

    try {
        // Realiza una petición para obtener el número de preguntas de diseño asociadas al test.
        const response = await axios.get(`http://127.0.0.1:8000/api/designtest/${testId}/designquestions/`);
        if (response.status === 200) {
            // Si la petición es exitosa, almacena el número de preguntas.
            numQuestions = response.data.length;
        }
    } catch (error) {
        console.error('Error al obtener las preguntas de diseño:', error);
    }

    // Carga la imagen de cabecera para la primera página del PDF.
    const imageSrc = '/src/assets/lading/imagen2.png';
    const img = new Image();
    img.src = imageSrc;

    // Espera hasta que la imagen se haya cargado completamente para redimensionarla.
    await new Promise((resolve) => {
        img.onload = function () {
            const imgWidth = img.width;
            const imgHeight = img.height;
            const maxWidth = 60;
            const maxHeight = 60;
            let width, height;

            // Redimensiona la imagen manteniendo la proporción de aspecto.
            if (imgWidth > imgHeight) {
                width = maxWidth;
                height = (imgHeight * maxWidth) / imgWidth;
            } else {
                height = maxHeight;
                width = (imgWidth * maxHeight) / imgHeight;
            }

            // Añade la imagen redimensionada al documento PDF.
            doc.addImage(img, 'PNG', 10, 5, width, height);
            resolve();
        };
    });

    // Añade el título principal del documento PDF.
    doc.setFont('helvetica', 'bold');
    doc.setFontSize(22);
    doc.text('INFORME DETALLADO DE LA PRUEBA DE DISEÑO', doc.internal.pageSize.width / 2, 40, { align: 'center' });
    doc.setFontSize(20);
    doc.text(`${design_test.name}`, doc.internal.pageSize.width / 2, 50, { align: 'center' });

    // Añade una sección con los datos principales del test de diseño.
    doc.setFontSize(18);
    doc.text('Datos de la prueba de diseño', marginX, 70);
    doc.setFont('helvetica', 'normal');

    // Tabla que contiene la información de la prueba de diseño.
    const DesignInfoTable = [
        ['Creado en', formatDate(design_test.created_at)],
        ['Propietario', design_test.user_name],
        ['Nombre', design_test.name],
        ['URL', cleanFigmaUrl(design_test.url)],
        ['Descripción', design_test.description],
        ['Tipo de prueba', design_test.test_type === 'Movil' ? 'Móvil' : 'Web'],
        ['Heurísticas', design_test.has_heuristics ? 'Sí' : 'No'],
        ['Pantallas', numQuestions.toString()],
    ];

    // Genera una tabla con la información del test de diseño en el PDF.
    doc.autoTable({
        ...defaultTableStyles,
        startY: 75, // Posición vertical donde comenzará la tabla.
        body: DesignInfoTable, // Cuerpo de la tabla con los datos del test.
        columnStyles: {
            0: { cellWidth: 40, valign: 'middle', halign: 'right', fillColor: [210, 210, 210] },
            1: { cellWidth: 140 }
        }
    });

    // Si el test tiene heurísticas, añade una tabla adicional con las mediciones.
    if (design_test.has_heuristics) {
        doc.setFont('helvetica', 'bold');
        doc.setFontSize(16);
        doc.text('Mediciones', marginX, doc.autoTable.previous.finalY + 10);

        doc.setFont('helvetica', 'normal');
        doc.setFontSize(12);
        doc.text('Las mediciones que dan valor a los heurísticos siguen el siguiente patrón:', marginX, doc.autoTable.previous.finalY + 20);

        // Definición de los valores de medición.
        const MedicionTable = [
            ['1 - 2', 'Se da la mínima expresión del heurístico en las páginas evaluadas'],
            ['3 - 4', 'Se da una expresión baja del heurístico en las páginas evaluadas'],
            ['5 - 6', 'Se da una expresión media del heurístico en las páginas evaluadas'],
            ['7 - 8', 'Se da una expresión alta del heurístico en las páginas evaluadas'],
            ['9 - 10', 'Se da la máxima expresión del heurístico en las páginas evaluadas']
        ];

        // Genera una tabla con las descripciones de las mediciones.
        doc.autoTable({
            ...defaultTableStyles,
            startY: doc.autoTable.previous.finalY + 25, // Comienza después de la tabla anterior.
            head: [['Valor', 'Observaciones']], // Cabecera de la tabla.
            body: MedicionTable, // Cuerpo de la tabla con los valores.
            theme: 'grid',
            columnStyles: {
                0: { cellWidth: 20, halign: 'center' },
                1: { cellWidth: 160 }
            },
            headStyles: {
                halign: 'center',
                fillColor: '#BEC0BD',
            }
        });
    }
};

/* Función principal que genera un informe en PDF basado en los datos de las pruebas de diseño y evaluadores.
Este PDF incluye múltiples páginas con tablas, respuestas, y en algunos casos gráficos o capturas.
@param {Object} data - Datos del test de diseño y evaluadores.
@param {Function} onStart - Callback que se ejecuta al comenzar la generación del PDF.
@param {Function} onEnd - Callback que se ejecuta al finalizar la generación del PDF. */
export const exportFullReportPDF = async (data, onStart, onEnd) => {
    onStart(); // Callback para indicar el inicio del proceso.
    const { design_test, evaluators } = data; // Extrae los datos del test de diseño y evaluadores.
    const doc = new jsPDF(); // Crea una nueva instancia del documento PDF.

    // Genera la primera página del informe.
    await firstPage(doc, design_test);
    doc.addPage(); // Añade una nueva página al PDF para el contenido posterior.

    // Itera sobre cada evaluador para agregar su información y respuestas al PDF.
    for (const evaluator of evaluators) {
        const evaluatorInfo = [
            [evaluator.username, evaluator.email] // Información del evaluador (nombre y correo).
        ];

        // Genera una tabla con el nombre y correo del evaluador.
        doc.autoTable({
            ...defaultTableStyles,
            startY: 15, // La tabla comienza en la coordenada Y 15.
            head: [['Nombre del evaluador', 'Correo del evaluador']], // Encabezado de la tabla.
            body: evaluatorInfo, // Cuerpo de la tabla con la información del evaluador.
            columnStyles: {
                0: { cellWidth: 60 }, // Ancho de la columna de nombre.
                1: { cellWidth: 120 }, // Ancho de la columna de correo.
            }
        });

        let startY = doc.autoTable.previous.finalY + 10; // Define la posición Y inicial para la siguiente tabla.

        if (design_test.has_heuristics) {
            // Si el test tiene heurísticas, genera tablas detalladas por cada respuesta y heurística.
            evaluator.responses.forEach(response => {
                // Tabla con el título y la descripción de la pregunta.
                const questionTableData = [
                    [response.title, response.description]
                ];

                doc.autoTable({
                    ...defaultTableStyles,
                    startY, // Comienza en la posición Y calculada.
                    head: [['Título', 'Descripción']], // Encabezado de la tabla.
                    body: questionTableData, // Datos de la pregunta.
                    columnStyles: {
                        0: { cellWidth: 40 }, // Ancho de la columna de título.
                        1: { cellWidth: 140 }, // Ancho de la columna de descripción.
                    }
                });

                startY = doc.autoTable.previous.finalY + 10; // Actualiza la posición Y para la siguiente tabla.

                // Genera tablas con subprincipios y puntajes de las heurísticas.
                response.heuristics.forEach(heuristic => {
                    const subprincipleTableData = heuristic.subprinciples.map(subprinciple => [
                        subprinciple.subprinciple_subtitle, // Subtítulo del subprincipio.
                        subprinciple.response_value, // Valor de la respuesta.
                    ]);

                    doc.autoTable({
                        ...defaultTableStyles,
                        startY, // Comienza en la posición Y calculada.
                        head: [[heuristic.heuristic_title, 'Puntaje']], // Encabezado con el título de la heurística.
                        body: subprincipleTableData, // Datos de los subprincipios.
                        columnStyles: {
                            0: { cellWidth: 160 }, // Ancho de la columna del subtítulo.
                            1: { cellWidth: 20, halign: 'center' } // Puntaje centrado.
                        }
                    });

                    // Calcula la suma total de los puntajes obtenidos en la heurística.
                    const totalHeuristicScore = heuristic.subprinciples.reduce((sum, subprinciple) => sum + subprinciple.response_value, 0);

                    // Genera una fila que muestra la suma total de los puntajes.
                    doc.autoTable({
                        ...defaultTableStyles,
                        startY: doc.autoTable.previous.finalY, // Comienza justo después de la tabla anterior.
                        body: [['Total de puntajes', totalHeuristicScore.toFixed(2)]], // Fila con la suma total de los puntajes.
                        columnStyles: {
                            0: { cellWidth: 160, halign: 'right' }, // Alineación a la derecha para la descripción.
                            1: { cellWidth: 20, halign: 'center' }, // Alineación centrada para el puntaje.
                        },
                        headStyles: { fillColor: '#d1e7dd' } // Resalta la fila con un color de fondo.
                    });

                    startY = doc.autoTable.previous.finalY + 10; // Actualiza la posición Y para la siguiente tabla.
                });
            });

        } else {
            // Si el test no tiene heurísticas, genera tablas estándar para las preguntas y respuestas.
            evaluator.responses.forEach(response => {
                // Tabla con el título y la descripción de la pregunta.
                const questionTableData = [
                    [response.question.title, response.question.description]
                ];

                doc.autoTable({
                    ...defaultTableStyles,
                    startY,
                    head: [['Título', 'Descripción']],
                    body: questionTableData,
                    columnStyles: {
                        0: { cellWidth: 40 },
                        1: { cellWidth: 140 },
                    }
                });

                // Tabla con el tipo de respuesta, puntaje y comentarios.
                const responseData = [
                    [response.response.response_type, response.response.response_value, response.response.comment],
                ];

                doc.autoTable({
                    ...defaultTableStyles,
                    startY: doc.autoTable.previous.finalY + 10,
                    head: [['Tipo', 'Puntaje', 'Comentario']],
                    body: responseData,
                    columnStyles: {
                        0: { cellWidth: 27 },
                        1: { cellWidth: 19, halign: 'center' }, // Centrado el puntaje.
                        2: { cellWidth: 134 },
                    },
                });

                startY = doc.autoTable.previous.finalY + 10; // Actualiza la posición Y.
            });
        }
        doc.addPage(); // Añade una nueva página para el siguiente evaluador.
    }

    // Si el test incluye heurísticas, genera tablas de usabilidad heurística.
    if (design_test.has_heuristics) {
        const questionResponses = evaluators.flatMap(evaluator =>
            evaluator.responses.map(response => ({
                question_id: response.question_id,
                title: response.title,
                description: response.description,
                heuristics: response.heuristics
            }))
        );

        await generateHeuristicUsabilityTable(doc, questionResponses); // Genera la tabla de usabilidad heurística.
    }
    
    // Genera resumen de heurísticas si están presentes.
    if (design_test.has_heuristics) {
        const questionResponses = evaluators.flatMap(evaluator =>
            evaluator.responses.map(response => ({
                question_id: response.question_id,
                title: response.title,
                description: response.description,
                heuristics: response.heuristics.map(heuristic => ({
                    heuristic_code: heuristic.heuristic_code,
                    heuristic_title: heuristic.heuristic_title,
                    comments: evaluators.map(evaluator => ({
                        evaluator_name: evaluator.username,
                        text: evaluator.responses.find(r => r.question_id === response.question_id)?.heuristics
                            .find(h => h.heuristic_code === heuristic.heuristic_code)?.comment || 'Sin comentario'
                    }))
                })),
                url_frame: response.url_frame
            }))
        );
    
        await generateHeuristicSummaryTable(doc, questionResponses); // Genera la tabla resumen de heurísticas.
    }

    // Si no hay heurísticas, genera gráficos y tablas de usabilidad.
    if (!design_test.has_heuristics) {
        const globalScores = {
            calificacion: { total: 0, count: 0, max: 10 },
            coherencia: { total: 0, count: 0, max: 10 },
            legibilidad: { total: 0, count: 0, max: 5 },
        };

        // Suma las respuestas de todos los evaluadores.
        evaluators.forEach(evaluator => {
            evaluator.responses.forEach(response => {
                const tipoRespuesta = response.response.response_type.toLowerCase();
                const valorRespuesta = response.response.response_value || 0;
                if (globalScores[tipoRespuesta]) {
                    globalScores[tipoRespuesta].total += valorRespuesta;
                    globalScores[tipoRespuesta].count++;
                }
            });
        });

        const totalUsabilidadPosible = Object.values(globalScores)
            .reduce((acc, { count, max }) => acc + (count * max), 0);
        const usabilidadObtenida = Object.values(globalScores)
            .reduce((acc, { total }) => acc + total, 0);
        const faltaUsabilidad = totalUsabilidadPosible - usabilidadObtenida;
        const totalPercentage = (usabilidadObtenida / totalUsabilidadPosible) * 100;

        generateUsabilityTable(doc, globalScores, faltaUsabilidad, totalPercentage); // Genera la tabla de usabilidad.

        const totalScores = Object.values(globalScores).map(({ total }) => total);
        const labels = Object.keys(globalScores).map(tipo => tipo.charAt(0).toUpperCase() + tipo.slice(1));

        if (!labels.includes('Falta de Usabilidad')) {
            totalScores.push(faltaUsabilidad);
            labels.push('Falta de Usabilidad');
        }

        await exportEvaluatorGraphsPDF(doc, totalScores, labels, 'General', totalPercentage); // Exporta los gráficos de evaluación.
        doc.addPage(); // Añade una nueva página.
    }

    // Si no hay heurísticas, genera la tabla de preguntas y capturas de pantalla.
    if (!design_test.has_heuristics) {
        const uniqueQuestions = new Set();
        evaluators.forEach(evaluator => {
            evaluator.responses.forEach(response => uniqueQuestions.add(JSON.stringify(response.question)));
        });
        const questionsArray = Array.from(uniqueQuestions).map(q => JSON.parse(q));

        for (const question of questionsArray) {
            const comentarios = evaluators.flatMap(evaluator =>
                evaluator.responses
                    .filter(response => response.question.question_id === question.question_id)
                    .map(response => [evaluator.username, response.response.comment])
            );

            const questionUrl = cleanFigmaUrl(question.url_frame) + '&scaling=scale-down&content-scaling=fixed';
            const questionTableData = [
                ['Título de la Pregunta', question.title],
                ['URL del Prototipo', questionUrl]
            ];

            doc.autoTable({
                ...defaultTableStyles,
                startY: 15, // Comienza en la coordenada Y 15.
                head: [['Campo', 'Valor']],
                body: questionTableData,
                columnStyles: {
                    0: { cellWidth: 50 },
                    1: { cellWidth: 130 },
                },
            });

            const comentariosTableData = comentarios.map(([username, comment]) => [username, comment]);
            doc.autoTable({
                ...defaultTableStyles,
                startY: doc.autoTable.previous.finalY + 10, // Posiciona después de la tabla anterior.
                head: [['Evaluador', 'Comentario']],
                body: comentariosTableData,
                columnStyles: {
                    0: { cellWidth: 40 },
                    1: { cellWidth: 140 },
                },
            });

            const screenshot = await captureIframeScreenshot(questionUrl, design_test.has_heuristics); // Captura la pantalla del prototipo.
            if (screenshot) {
                const img = new Image();
                img.src = screenshot;
                await new Promise((resolve) => {
                    img.onload = function () {
                        const imgWidth = img.width;
                        const imgHeight = img.height;
                        const maxWidth = 180;
                        const maxHeight = 100;
                        let width, height;
                        if (imgWidth > imgHeight) {
                            width = maxWidth;
                            height = (imgHeight * maxWidth) / imgWidth;
                        } else {
                            height = maxHeight;
                            width = (imgWidth * maxHeight) / imgHeight;
                        }

                        doc.addImage(img, 'PNG', marginX, doc.autoTable.previous.finalY + 10, width, height); // Añade la imagen.
                        resolve();
                        doc.addPage(); // Añade una nueva página.
                    };
                });
            }
        }
    }

    doc.save(`Informe detallado de ${design_test.name}.pdf`); // Guarda el PDF con el nombre del test.
    onEnd(); // Callback para indicar el final del proceso.
};

/* Genera la tabla resumen de heurísticas para cada pregunta y añade capturas de pantalla.
@param {Object} doc - Documento PDF en el que se generan las tablas.
@param {Array} questionResponses - Respuestas de las preguntas evaluadas. */
const generateHeuristicSummaryTable = async (doc, questionResponses) => {
    const uniqueQuestions = new Set();
    
    // Paso 1: Asegurarse de no repetir preguntas.
    questionResponses.forEach(response => uniqueQuestions.add(JSON.stringify(response)));

    const questionsArray = Array.from(uniqueQuestions).map(q => JSON.parse(q));

    // Paso 2: Generar tablas por cada pregunta (sin duplicar).
    for (const response of questionsArray) {
        doc.addPage(); // Añade una nueva página para cada pregunta.

        // 1. Tabla con el título de la pregunta y la URL del prototipo.
        const questionTableData = [
            ['Título de la Pregunta', response.title],
            ['URL del Prototipo', response.url_frame]
        ];

        // Genera la tabla con la información de la pregunta.
        doc.autoTable({
            ...defaultTableStyles,
            startY: 15, // La tabla comienza en la coordenada Y 15.
            head: [['Campo', 'Valor']], // Encabezado de la tabla.
            body: questionTableData, // Cuerpo de la tabla.
            columnStyles: {
                0: { cellWidth: 50 }, // Ancho de la columna del campo.
                1: { cellWidth: 130 }, // Ancho de la columna del valor.
            },
        });

        // 2. Generar tabla de comentarios agrupados por heurística.
        const heuristicsCommentsData = [];

        // Agrupa los comentarios de los evaluadores por cada heurística.
        response.heuristics.forEach(heuristic => {
            // Añade el título de la heurística.
            heuristicsCommentsData.push([`${heuristic.heuristic_title}`, '']); 

            // Añade los comentarios de cada evaluador para esta heurística.
            heuristic.comments.forEach(comment => {
                if (comment.text) {
                    heuristicsCommentsData.push([comment.evaluator_name, comment.text]); 
                }
            });
        });

        // Genera la tabla con los comentarios agrupados por heurística.
        doc.autoTable({
            ...defaultTableStyles,
            startY: doc.autoTable.previous.finalY + 10, // Posiciona después de la tabla anterior.
            head: [['Heurística', 'Comentario']],
            body: heuristicsCommentsData, // Comentarios agrupados por heurística.
            columnStyles: {
                0: { cellWidth: 60 }, // Ancho de la columna de la heurística.
                1: { cellWidth: 120 }, // Ancho de la columna de comentarios.
            },
        });

        // 3. Generar la captura de pantalla de la URL del prototipo.
        const screenshot = await captureIframeScreenshot(response.url_frame, true); // Usa la URL para capturar la pantalla.

        if (screenshot) {
            // Añade la captura de pantalla debajo de la tabla en la misma página.
            const img = new Image();
            img.src = screenshot;

            await new Promise((resolve) => {
                img.onload = function () {
                    const imgWidth = img.width;
                    const imgHeight = img.height;
                    const maxWidth = 180;
                    const maxHeight = 100;
                    let width, height;

                    // Redimensiona la imagen manteniendo la proporción.
                    if (imgWidth > imgHeight) {
                        width = maxWidth;
                        height = (imgHeight * maxWidth) / imgWidth;
                    } else {
                        height = maxHeight;
                        width = (imgWidth * maxHeight) / imgHeight;
                    }
                    doc.addPage();
                    doc.addImage(img, 'PNG', marginX, 10, width, height); // Añade la imagen al documento.
                    resolve();
                };
            });
        }
    }
};

/*  Genera una tabla de usabilidad basada en las heurísticas evaluadas.
 @param {Object} doc - Documento PDF en el que se generan las tablas.
 @param {Array} questionResponses - Respuestas con las heurísticas evaluadas. */
const generateHeuristicUsabilityTable = async (doc, questionResponses) => {
    const heuristicsMap = {};

    // Recorre las respuestas para organizar los datos de las heurísticas por cada pregunta.
    questionResponses.forEach(response => {
        response.heuristics.forEach(heuristic => {
            if (!heuristicsMap[response.question_id]) {
                heuristicsMap[response.question_id] = {};
            }
            if (!heuristicsMap[response.question_id][heuristic.heuristic_code]) {
                heuristicsMap[response.question_id][heuristic.heuristic_code] = {
                    title: heuristic.heuristic_title,
                    totalScore: 0,
                    maxScore: 0,
                    evaluators: 0
                };
            }

            const heuristicData = heuristicsMap[response.question_id][heuristic.heuristic_code];
            heuristic.subprinciples.forEach(subprinciple => {
                heuristicData.totalScore += subprinciple.response_value;
                heuristicData.maxScore += 10; // Puntaje máximo por subprincipio es 10.
            });
            heuristicData.evaluators++;
        });
    });

    // Genera la tabla por cada pregunta.
    for (const questionId of Object.keys(heuristicsMap)) {
        const heuristics = heuristicsMap[questionId];

        let totalPuntosObtenidos = 0;
        let totalPuntosMaximos = 0;

        // Calcula el total de puntos obtenidos y máximos para todas las heurísticas.
        Object.values(heuristics).forEach(heuristicData => {
            totalPuntosObtenidos += heuristicData.totalScore;
            totalPuntosMaximos += heuristicData.maxScore;
        });

        const nivelDeUsabilidad = (totalPuntosObtenidos / totalPuntosMaximos) * 100;

        // Genera los datos para la tabla de cada heurística.
        const tableData = Object.values(heuristics).map(heuristicData => {
            const { title, totalScore, maxScore } = heuristicData;
            const porcentajeObtenido = (totalScore / totalPuntosObtenidos) * nivelDeUsabilidad;

            return [
                title,
                totalScore.toFixed(2),  // Puntaje obtenido.
                maxScore.toFixed(2),     // Puntaje máximo.
                `${porcentajeObtenido.toFixed(2)}%` // Porcentaje obtenido.
            ];
        });

        // Añade una fila para la "Falta de Usabilidad".
        const faltaDeUsabilidad = (100 - nivelDeUsabilidad).toFixed(2) + '%';
        tableData.push(['Falta de Usabilidad', '-', '-', faltaDeUsabilidad]);

        // Añade una nueva página antes de cada tabla.
        doc.addPage(); 

        // Genera la tabla de usabilidad para la pregunta actual.
        doc.autoTable({
            ...defaultTableStyles,
            startY: 15, // Comienza la tabla al principio de la página.
            head: [['Heurística', 'Puntaje Obtenido', 'Puntaje Máximo', 'Porcentaje Obtenido']],
            body: tableData,
            columnStyles: {
                0: { cellWidth: 60 },
                1: { cellWidth: 40, halign: 'center' },
                2: { cellWidth: 40, halign: 'center' },
                3: { cellWidth: 40, halign: 'center' }
            }
        });

        // Genera datos para la gráfica de pastel con el porcentaje de usabilidad obtenido.
        const heuristicData = Object.values(heuristics).map(heuristic => ({
            title: heuristic.title,
            percentageObtained: (heuristic.totalScore / totalPuntosObtenidos) * nivelDeUsabilidad 
        }));

        const totalUsabilidad = heuristicData.reduce((acc, h) => acc + h.percentageObtained, 0);
        const pieChartImage = await createHeuristicPieChartImage(heuristicData, totalUsabilidad);

        // Añade la gráfica de pastel si está disponible.
        if (pieChartImage) {
            doc.addImage(pieChartImage, 'PNG', 15, doc.autoTable.previous.finalY + 10, 180, 100);
        }
        
        // Genera el gráfico de medidor de riesgo para la usabilidad.
        const riskMeterImage = createHeuristicRiskMeterImage(nivelDeUsabilidad); 
        
        if (riskMeterImage) {
            // Añade el medidor de riesgo justo después de la gráfica de pastel.
            doc.addImage(riskMeterImage, 'PNG', 15, doc.autoTable.previous.finalY + 120, 180, 60);
        }
    }
};

/*  Crea una gráfica de pastel basada en los datos de heurísticas y usabilidad total.
 @param {Array} heuristicsData - Datos de las heurísticas evaluadas.
 @param {number} usabilidadTotal - Porcentaje total de usabilidad calculado.
 @returns {Promise<string>} - Imagen de la gráfica en formato base64. */
const createHeuristicPieChartImage = (heuristicsData, usabilidadTotal) => {
    const heuristicLabels = heuristicsData.map(item => item.title);
    const heuristicScores = heuristicsData.map(item => item.percentageObtained);

    // Calcula la falta de usabilidad como porcentaje restante.
    const faltaDeUsabilidad = 100 - usabilidadTotal;
    heuristicLabels.push("Falta de Usabilidad");
    heuristicScores.push(faltaDeUsabilidad); 

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 800;
    canvas.height = 600;
    ctx.scale(2, 2);

    // Crea la gráfica de pastel.
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: heuristicLabels,
            datasets: [{
                data: heuristicScores, 
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
            }]
        },
        options: {
            responsive: false,
            plugins: {
                legend: { position: 'top' },
                title: { display: true, text: `Gráfica de Usabilidad por Heurísticas` },
            }
        }
    });

    return new Promise((resolve) => {
        setTimeout(() => resolve(canvas.toDataURL('image/png', 0.9)), 1000);
    });
};

/*  Crea un medidor de riesgo basado en el porcentaje de usabilidad.
 @param {number} usabilityPercentage - Porcentaje de usabilidad calculado.
 @returns {string} - Imagen del gráfico en formato base64. */
const createHeuristicRiskMeterImage = (usabilityPercentage) => {
    usabilityPercentage = usabilityPercentage || 0;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 400;
    canvas.height = 200;
    const meterWidth = 360;
    const meterHeight = 40;

    // Gradiente de color para representar el nivel de riesgo.
    const gradient = ctx.createLinearGradient(20, 0, meterWidth + 20, 0);
    gradient.addColorStop(0, '#F44336');  // Rojo para baja usabilidad.
    gradient.addColorStop(0.5, '#FFC107'); // Amarillo para media usabilidad.
    gradient.addColorStop(1, '#4CAF50');  // Verde para alta usabilidad.

    ctx.fillStyle = gradient;
    ctx.fillRect(20, 100, meterWidth, meterHeight);

    let riskLevel;
    if (usabilityPercentage <= 33) {
        riskLevel = (usabilityPercentage / 33) * (meterWidth * 0.33);
    } else if (usabilityPercentage <= 66) {
        riskLevel = ((usabilityPercentage - 33) / 33) * (meterWidth * 0.33) + (meterWidth * 0.33);
    } else {
        riskLevel = ((usabilityPercentage - 66) / 34) * (meterWidth * 0.34) + (meterWidth * 0.66);
    }

    // Dibuja el marcador de nivel de riesgo.
    ctx.beginPath();
    ctx.moveTo(20 + riskLevel, 100);
    ctx.lineTo(20 + riskLevel - 5, 70);
    ctx.lineTo(20 + riskLevel + 5, 70);
    ctx.closePath();
    ctx.fillStyle = '#000000';
    ctx.fill();

    // Dibuja el círculo en el nivel de riesgo.
    ctx.beginPath();
    ctx.arc(20 + riskLevel, 100, 5, 0, Math.PI * 2);
    ctx.fillStyle = '#000000';
    ctx.fill();

    // Texto que muestra el porcentaje de usabilidad.
    const usabilityText = `Usabilidad: ${usabilityPercentage.toFixed(2)}%`;
    ctx.font = '16px Arial';
    ctx.fillText(usabilityText, (400 - ctx.measureText(usabilityText).width) / 2, 40);

    return canvas.toDataURL('image/png', 1.0); // Retorna la imagen en base64.
};

/* Función para crear tabla de usabilidad (sin heurísticas)
Genera una tabla de usabilidad basada en los puntajes globales de las respuestas, sin heurísticas.
 @param {Object} doc - El documento PDF en el que se generan las tablas.
 @param {Object} globalScores - Los puntajes globales por tipo de respuesta (calificación, coherencia, legibilidad, etc.). */
const generateUsabilityTable = (doc, globalScores) => {
    // Inicializa el total de puntos obtenidos y los puntos máximos posibles.
    const totalPuntosObtenidos = Object.values(globalScores).reduce((acc, { total }) => acc + total, 0);
    const totalPuntosMaximos = Object.values(globalScores).reduce((acc, { count, max }) => acc + (count * max), 0);

    // Evita cálculos incorrectos si no se han obtenido puntos.
    if (totalPuntosObtenidos === 0) {
        console.error('Error: totalPuntosObtenidos es 0, lo que causa NaN en los porcentajes.');
        return;
    }

    // Calcula el porcentaje de usabilidad total.
    const porcentajeUsabilidadTotal = (totalPuntosObtenidos / totalPuntosMaximos) * 100;

    // Calcula el porcentaje de cada tipo de respuesta en relación al porcentaje total de usabilidad.
    const calculoPromediosFinal = Object.entries(globalScores).map(([tipo, { total }]) => {
        const porcentajeEnUsabilidad = ((total / totalPuntosObtenidos) * porcentajeUsabilidadTotal).toFixed(2) + '%';
        const puntajeMaximo = totalPuntosMaximos;

        return [
            tipo.charAt(0).toUpperCase() + tipo.slice(1),  // Tipo de respuesta (Calificación, Coherencia, etc.).
            total.toFixed(2),                              // Puntaje obtenido.
            puntajeMaximo.toFixed(2),                      // Puntaje máximo posible.
            porcentajeEnUsabilidad                         // Porcentaje dentro del total de usabilidad.
        ];
    });

    // Agrega una fila adicional para la "Falta de Usabilidad".
    const faltaUsabilidadPorcentaje = (100 - porcentajeUsabilidadTotal).toFixed(2) + '%';
    calculoPromediosFinal.push([
        'Falta de Usabilidad', 
        '-', 
        '-', 
        faltaUsabilidadPorcentaje
    ]);

    // Genera la tabla de cálculo de porcentajes.
    doc.autoTable({
        ...defaultTableStyles,
        startY: 15, // Comienza la tabla en la coordenada Y 15.
        head: [['Tipo de Respuesta', 'Puntaje Obtenido', 'Puntaje Máximo', 'Porcentaje Obtenido']], // Encabezado.
        body: calculoPromediosFinal, // Cuerpo de la tabla.
        columnStyles: {
            0: { cellWidth: 60 }, // Ancho de la columna del tipo de respuesta.
            1: { cellWidth: 40, halign: 'center' }, // Columna del puntaje obtenido.
            2: { cellWidth: 40, halign: 'center' }, // Columna del puntaje máximo.
            3: { cellWidth: 40, halign: 'center' }, // Columna del porcentaje obtenido.
        },
    });
};

/* Función para crear gráfica de pastel (sin heurísticas)
 Genera una gráfica de pastel basada en los puntajes obtenidos para cada pregunta.
 @param {Array} preguntaScores - Puntajes obtenidos por cada pregunta.
 @param {Array} preguntaLabels - Etiquetas para cada pregunta.
 @param {string} evaluatorName - Nombre del evaluador.
 @returns {Promise<string>} - Imagen de la gráfica de pastel en formato base64. */
const createPieChartImage = (preguntaScores, preguntaLabels, evaluatorName) => {
    const totalScore = preguntaScores.reduce((acc, score) => acc + score, 0);
    const maxPossibleScore = preguntaScores.length * 10; // Puntaje máximo posible.
    const missingUsability = maxPossibleScore - totalScore;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 800;
    canvas.height = 600;
    ctx.scale(2, 2);

    const finalScores = [...preguntaScores];
    const finalLabels = [...preguntaLabels];

    // Asegura que "Falta de Usabilidad" solo se agregue si aún no está presente.
    const faltaUsabilidadIndex = finalLabels.indexOf('Falta de Usabilidad');
    if (faltaUsabilidadIndex === -1) {  // Solo agregar si no está presente.
        finalScores.push(missingUsability);
        finalLabels.push('Falta de Usabilidad');
    }

    // Crea la gráfica de pastel.
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: finalLabels,
            datasets: [{
                data: finalScores,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'],
            }]
        },
        options: {
            responsive: false,
            plugins: {
                legend: { position: 'top' }, // Posiciona la leyenda arriba.
                title: { display: true, text: `Gráfica de Usabilidad - ${evaluatorName}` }, // Título de la gráfica.
            }
        }
    });

    // Retorna la imagen de la gráfica en formato base64.
    return new Promise((resolve) => {
        setTimeout(() => resolve(canvas.toDataURL('image/png', 0.9)), 1000);
    });
};

/* Función para crear gráfico de Risk Meter (sin heurísticas)
 Crea un gráfico de medidor de riesgo basado en el porcentaje de usabilidad.
 @param {number} usabilityPercentage - Porcentaje de usabilidad calculado.
 @returns {string} - Imagen del gráfico en formato base64. */
const createRiskMeterImage = (usabilityPercentage) => {
    usabilityPercentage = usabilityPercentage || 0;

    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    canvas.width = 400;
    canvas.height = 200;
    const meterWidth = 360;
    const meterHeight = 40;

    // Gradiente de color para el medidor de riesgo.
    const gradient = ctx.createLinearGradient(20, 0, meterWidth + 20, 0);
    gradient.addColorStop(0, '#F44336');  // Rojo para baja usabilidad.
    gradient.addColorStop(0.5, '#FFC107'); // Amarillo para media usabilidad.
    gradient.addColorStop(1, '#4CAF50');  // Verde para alta usabilidad.

    ctx.fillStyle = gradient;
    ctx.fillRect(20, 100, meterWidth, meterHeight);

    let riskLevel;
    if (usabilityPercentage <= 33) {
        riskLevel = (usabilityPercentage / 33) * (meterWidth * 0.33);
    } else if (usabilityPercentage <= 66) {
        riskLevel = (usabilityPercentage - 33) / 33 * (meterWidth * 0.33) + (meterWidth * 0.33);
    } else {
        riskLevel = (usabilityPercentage - 66) / 34 * (meterWidth * 0.34) + (meterWidth * 0.66);
    }

    // Dibuja el marcador de riesgo.
    ctx.beginPath();
    ctx.moveTo(20 + riskLevel, 100);
    ctx.lineTo(20 + riskLevel - 5, 70);
    ctx.lineTo(20 + riskLevel + 5, 70);
    ctx.closePath();
    ctx.fillStyle = '#000000';
    ctx.fill();

    // Dibuja el círculo en el nivel de riesgo.
    ctx.beginPath();
    ctx.arc(20 + riskLevel, 100, 5, 0, Math.PI * 2);
    ctx.fillStyle = '#000000';
    ctx.fill();

    // Añade el texto del porcentaje de usabilidad.
    const usabilityText = `Usabilidad: ${usabilityPercentage.toFixed(2)}%`;
    ctx.font = '16px Arial';
    ctx.fillText(usabilityText, (400 - ctx.measureText(usabilityText).width) / 2, 40);

    return canvas.toDataURL('image/png', 1.0); // Retorna la imagen en formato base64.
};

/* Función para exportar gráficos en el PDF
 Exporta los gráficos de evaluación (gráfica de pastel y medidor de riesgo) al PDF.
 @param {Object} doc - El documento PDF en el que se añaden los gráficos.
 @param {Array} preguntaScores - Puntajes obtenidos por pregunta.
 @param {Array} labels - Etiquetas para las preguntas.
 @param {string} evaluatorName - Nombre del evaluador.
 @param {number} totalPercentage - Porcentaje total de usabilidad calculado. */
const exportEvaluatorGraphsPDF = async (doc, preguntaScores, labels, evaluatorName, totalPercentage) => {
    doc.setFontSize(18); // Tamaño de fuente para el título.
    doc.text(`Gráficas de Evaluación - ${evaluatorName}`, 10, 20); // Añade el título.

    // Crear la gráfica de pastel.
    const pieChartImage = await createPieChartImage(preguntaScores, labels, evaluatorName);
    if (pieChartImage) {
        doc.addImage(pieChartImage, 'PNG', 15, doc.autoTable.previous.finalY, 180, 100); // Añade la gráfica al PDF.
    }

    // Crear el gráfico de Risk Meter.
    const riskMeterImage = createRiskMeterImage(totalPercentage);
    if (riskMeterImage) {
        doc.addImage(riskMeterImage, 'PNG', 15, 180, 180, 70); // Añade el gráfico de Risk Meter al PDF.
    }
};

/* Función para capturar una captura de pantalla del iframe
 Captura una imagen de la URL de un prototipo Figma y la convierte en formato base64.
 @param {string} url - URL del prototipo a capturar.
 @param {boolean} hasHeuristics - Indica si el prototipo tiene heurísticas.
 @returns {Promise<string|null>} - Imagen capturada en formato base64, o null si falla. */
const captureIframeScreenshot = async (url, hasHeuristics) => {
    try {
        // Limpia la URL antes de la captura, pasando el valor de hasHeuristics.
        const cleanedUrl = cleanFigmaUrl(url, hasHeuristics);

        const response = await axios.post('http://localhost:8000/api/capture/', { url: cleanedUrl }, { responseType: 'blob' });
        if (response.status === 200) {
            const blob = response.data;
            const reader = new FileReader();
            return new Promise((resolve) => {
                reader.onloadend = () => resolve(reader.result); // Retorna la imagen en base64.
                reader.readAsDataURL(blob);
            });
        }
    } catch (error) {
        console.error('Error capturando la pantalla:', error); // Muestra error si falla la captura.
    }
    return null;
};