<script setup>
import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';

// Verificar si `pdfFonts.pdfMake.vfs` está disponible antes de asignarlo
if (pdfFonts && pdfFonts.pdfMake && pdfFonts.pdfMake.vfs) {
  pdfMake.vfs = pdfFonts.pdfMake.vfs;
} else {
  console.error("vfs no encontrado en pdfFonts.");
}

import { ref, onMounted, toRaw } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

// Variables reactivas
const route = useRoute();
const evaluationResults = ref([]);
const ownerId = ref();
const evaluationDescription = ref(
  "A continuación se presentan los resultados de la evaluación de usabilidad, utilizando el método de prueba denominado análisis heurístico. Se muestra la tabla de resultados con sus respectivos niveles de criterios de usabilidad."
);

// Obtener resultados al montar el componente
onMounted(() => {
  ownerId.value = route.params.ownerId;
  getEvaluationResults();
});

// Función para obtener resultados de evaluación
const getEvaluationResults = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:8000/api/evaluations/${ownerId.value}`);
    evaluationResults.value = response.data;
    console.log("Datos obtenidos:", evaluationResults.value);
  } catch (error) {
    console.error("Error al obtener los resultados de la evaluación:", error.response || error.message);
  }
};

// Función para mostrar PDF desde el caché
const mostrarPDFDesdeCache = () => {
  const cachedPDF = localStorage.getItem('cachedPDF');
  if (cachedPDF) {
    window.open(cachedPDF, '_blank');
  } else {
    console.log('No hay PDF en caché');
  }
};

// Función abrir el PDF tabla de problemas guardado en caché
const openCachedPDF = () => {
  const cachedPDFUrl = localStorage.getItem('cachedPDF');
  if (cachedPDFUrl) {
    window.open(cachedPDFUrl, '_blank');
  } else {
    console.error('No hay PDF guardado en caché.');
  }
};

// Generar contenido para el PDF
const generatePDFContent = () => {
  const valuesArray = toRaw(evaluationResults.value).map(obj => [
    obj.name || "N/A",
    obj.description || "N/A",
    obj.hi || "N/A",
    obj.criticism || "N/A",
    obj.frequency || "N/A",
    obj.severity || "N/A",
    obj.incidents || "N/A"
  ]);

  return {
    content: [
      { text: 'Resultados de la Evaluación', style: 'header' },
      evaluationDescription.value,
      { text: 'Tabla de Resultados', style: 'subheader' },
      {
        style: 'tableExample',
        table: {
          body: [
            ['Código', 'Descripción', 'Heurística Incumplida', 'Criticismo', 'Frecuencia', 'Severidad', 'Incidentes'],
            ...valuesArray
          ]
        }
      }
    ],
    styles: {
      header: {
        fontSize: 18,
        bold: true,
        margin: [0, 0, 0, 10]
      },
      subheader: {
        fontSize: 16,
        bold: true,
        margin: [0, 10, 0, 5]
      },
      tableExample: {
        margin: [0, 5, 0, 15]
      }
    }
  };
};

// Exportar a PDF
const exportPDF = () => {
  const pdfContent = generatePDFContent();
  pdfMake.createPdf(pdfContent).open();
};

// Función para mostrar la lista de chequeo
const infode = () => {
  const valuesArray = toRaw(evaluationResults.value).map(obj => Object.values(obj));
  let arreglofinal = [['Código', 'Descripción', 'Heuristica Incumplida', 'Criticismo', 'Frecuencia', "Severidad", 'Incidentes']];
  valuesArray.forEach(value => {
    arreglofinal.push([value[5], value[1], value[3], value[0], value[2], value[6], value[4]]);
  });
  var dd = {
    content: [
      { text: 'Tables', style: 'header' },
      evaluationDescription.value,
      { text: 'Resultados Evaluacioon', style: 'subheader' },
      'Resultado de la evaluacion',
      {
        style: 'tableExample',
        table: {
          body: arreglofinal
        }
      }
    ],
    styles: {
      header: {
        fontSize: 18,
        bold: true,
        margin: [0, 0, 0, 10]
      },
      subheader: {
        fontSize: 16,
        bold: true,
        margin: [0, 10, 0, 5]
      },
      tableExample: {
        margin: [0, 5, 0, 15]
      }
    }
  };
  pdfMake.createPdf(dd).open();
};

// Exportar PDF para tabla de problemas
const exportProblemsPDF = () => {
  infode();
};
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col">
        <button class="btn btn-success" @click="openCachedPDF()">Descargar PDF Gráfica/cálculos tabla problemas</button>
        <button class="btn btn-success" @click="exportPDF">Descargar PDF</button>
        <button class="btn btn-success" @click="mostrarPDFDesdeCache()">Descargar PDF lista de chequeo</button>
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <div class="card">
          <div class="card-header">
            <h5 class="card-title">Resultados</h5>
          </div>
          <div class="card-body">
            <p class="card-text">{{ evaluationDescription }}</p>
          </div>
        </div>
        <div class="card mt-3">
          <div class="card-header">
            <h6 class="card-title">Evaluaciones</h6>
          </div>
          <div class="card-body">
            <div class="table-responsive">
              <table class="table table-striped table-warning">
                <thead>
                  <tr>
                    <th>Código</th>
                    <th>Descripción</th>
                    <th>Heurística Incumplida</th>
                    <th>Criticismo</th>
                    <th>Frecuencia</th>
                    <th>Severidad</th>
                    <th>Incidentes</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(evaluation, index) in evaluationResults" :key="index">
                    <td>{{ evaluation.name || "N/A" }}</td>
                    <td>{{ evaluation.description || "N/A" }}</td>
                    <td>{{ evaluation.hi || "N/A" }}</td>
                    <td>{{ evaluation.criticism || "N/A" }}</td>
                    <td>{{ evaluation.frequency || "N/A" }}</td>
                    <td>{{ evaluation.severity || "N/A" }}</td>
                    <td>{{ evaluation.incidents || "N/A" }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
