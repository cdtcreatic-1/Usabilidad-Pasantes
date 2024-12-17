<script setup>
import pdfMake from 'pdfmake/build/pdfmake';
import pdfFonts from 'pdfmake/build/vfs_fonts';

pdfMake.vfs = pdfFonts.pdfMake.vfs;


import { ref, onMounted, toRaw } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const route = useRoute();
const evaluationResults = ref([]);
const ownerId = ref();
const evaluationDescription = ref(
  "A continuación se presentan los resultados de la evaluación de usabilidad, utilizando el método de prueba denominado análisis heurístico. Se muestra la tabla de resultados con sus respectivos niveles de criterios de usabilidad."
);

onMounted(() => {
  ownerId.value = route.params.ownerId;
  getEvaluationResults();
});

const getEvaluationResults = async () => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/evaluations/${ownerId.value}`);
    evaluationResults.value = response.data;
    console.log("Datos obtenidos:", evaluationResults.value);
  } catch (error) {
    console.error("Error al obtener los resultados de la evaluación:", error);
  }
};

const generatePDFContent = () => {
  const valuesArray = toRaw(evaluationResults.value).map(obj => Object.values(obj));
  const tableHeader = [
    'Código',
    'Descripción',
    'Heurística Incumplida',
    'Criticismo',
    'Frecuencia',
    'Severidad',
    'Incidentes'
  ];
  
  const tableBody = valuesArray.map(value => [
    value[5], value[1], value[3], value[0], value[2], value[6], value[4]
  ]);

  return {
    content: [
      { text: 'Resultados de la Evaluación', style: 'header' },
      evaluationDescription.value,
      { text: 'Tabla de Resultados', style: 'subheader' },
      {
        style: 'tableExample',
        table: {
          body: [tableHeader, ...tableBody]
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

const exportPDF = () => {
  const pdfContent = generatePDFContent();
  pdfMake.createPdf(pdfContent).open();
};
</script>

<template>
  <div class="container-fluid">
    <button class="btn btn-success" @click="exportPDF">Descargar PDF</button>
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
                <tr v-for="evaluation in evaluationResults" :key="evaluation.name">
                  <td>{{ evaluation.name }}</td>
                  <td>{{ evaluation.description }}</td>
                  <td>{{ evaluation.hi }}</td>
                  <td>{{ evaluation.criticism }}</td>
                  <td>{{ evaluation.frequency }}</td>
                  <td>{{ evaluation.severity }}</td>
                  <td>{{ evaluation.incidents }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
