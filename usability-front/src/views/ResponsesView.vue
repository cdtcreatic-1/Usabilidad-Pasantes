<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRoute } from 'vue-router';
import { exportFullReportPDF } from './exportPDF';
const route = useRoute();
const testId = route.params.testId;

const testDetails = ref(null);
const groupedEvaluators = ref([]);
const hasHeuristics = ref(false);
const currentQuestionIndex = ref({});
const isLoadingPDF = ref(false);

// Función para construir la URL del iframe con todos los parámetros
const buildFigmaEmbedUrl = (baseUrl, hasHeuristics) => {
  const scalingParam = hasHeuristics ? '&content-scaling=fixed' : '&scaling=scale-down-width';
  const commonParams = '&hide=footer,viewport-controls&hotspot-hints=0&disable-default-keyboard-nav=true&hide-ui=1';
  return `${baseUrl}?embed_host=your-site${commonParams}${scalingParam}`;
};


const handleExportFullReportPDF = async () => {
  await exportFullReportPDF(
    { design_test: testDetails.value, evaluators: groupedEvaluators.value },
    () => { isLoadingPDF.value = true; },  // onStart: Iniciar carga
    () => { isLoadingPDF.value = false; }  // onEnd: Terminar carga
  );
};

/* const handleExportUsabilityMeasurementPDF = async () => {
  await exportUsabilityMeasurementPDF(
    { design_test: testDetails.value, evaluators: groupedEvaluators.value },
    () => { isLoadingPDF.value = true; },  // onStart: Iniciar carga
    () => { isLoadingPDF.value = false; }  // onEnd: Terminar carga
  );
};

const handleExportSummaryPDF = async () => {
  await exportSummaryPDF(
    { design_test: testDetails.value, evaluators: groupedEvaluators.value },
    () => { isLoadingPDF.value = true; },  // onStart: Iniciar carga
    () => { isLoadingPDF.value = false; }  // onEnd: Terminar carga
  );
}; */

// Función para cargar los detalles de la prueba y las respuestas
const loadResponsesAndDetails = async () => {
  try {
    // Cargar los detalles de la prueba de diseño
    const testResponse = await axios.get(`http://localhost:8000/api/designtest/test_id/${testId}/`);
    testDetails.value = testResponse.data;
    hasHeuristics.value = testDetails.value.has_heuristics;

    // Definir la URL para cargar las respuestas basadas en si tiene heurísticas o no
    const url = hasHeuristics.value
      ? `http://localhost:8000/api/designtests/${testId}/evaluatorheuristicresponsesfinalize/`
      : `http://localhost:8000/api/designtests/${testId}/evaluatorstandardresponsesfinalize/`;

    const response = await axios.get(url);
    if (response.status === 200) {
      const evaluators = response.data.evaluators;

      // Agrupar respuestas según si tiene heurísticas o no
      groupedEvaluators.value = evaluators.map(evaluator => ({
        ...evaluator,
        responsesByQuestion: groupResponsesByQuestion(evaluator.responses),
      }));

      initializeQuestionIndex(evaluators);
    } else {
      console.error('Error al cargar los datos:', response.status);
    }
  } catch (error) {
    console.error('Error en la solicitud:', error);
  }
};

// Agrupar respuestas por question_id (aplica tanto para heurísticas como estándar)
const groupResponsesByQuestion = (responses) => {
  return responses.reduce((grouped, response) => {
    const questionId = response.question?.question_id || response.question_id;
    if (!grouped[questionId]) {
      grouped[questionId] = [];
    }
    grouped[questionId].push(response);
    return grouped;
  }, {});
};

// Inicializar el índice de la pregunta actual para cada evaluador
const initializeQuestionIndex = (evaluators) => {
  evaluators.forEach(evaluator => {
    currentQuestionIndex.value[evaluator.evaluator_id] = 0;
  });
};

// Navegar a la siguiente pregunta
const nextQuestion = (evaluatorId) => {
  const evaluator = groupedEvaluators.value.find(evaluator => evaluator.evaluator_id === evaluatorId);
  const questions = Object.keys(evaluator.responsesByQuestion);
  if (currentQuestionIndex.value[evaluatorId] < questions.length - 1) {
    currentQuestionIndex.value[evaluatorId]++;
  }
};

// Navegar a la pregunta anterior
const previousQuestion = (evaluatorId) => {
  if (currentQuestionIndex.value[evaluatorId] > 0) {
    currentQuestionIndex.value[evaluatorId]--;
  }
};

// Obtener las respuestas actuales según el índice
const currentResponsesByEvaluator = (evaluator) => {
  const questionIds = Object.keys(evaluator.responsesByQuestion);
  const currentQuestionId = questionIds[currentQuestionIndex.value[evaluator.evaluator_id]];
  return evaluator.responsesByQuestion[currentQuestionId];
};

// Cargar datos al montar el componente
onMounted(() => {
  loadResponsesAndDetails();
});
</script>

<template>
  <div>
    <h2 class="mb-4 text-center">Respuestas del Cuestionario</h2>

    <!-- Mostrar respuestas si las hay -->
    <div v-if="groupedEvaluators.length > 0" class="container mt-4">
      <div
        v-for="(evaluator) in groupedEvaluators"
        :key="evaluator.evaluator_id"
        class="m-4 question-group"
      >
        <h3>Evaluador: {{ evaluator.username }}</h3>

        <!-- Navegación entre preguntas -->
        <button @click="previousQuestion(evaluator.evaluator_id)" :disabled="currentQuestionIndex[evaluator.evaluator_id] === 0">
          Anterior
        </button>
        <button @click="nextQuestion(evaluator.evaluator_id)" :disabled="currentQuestionIndex[evaluator.evaluator_id] >= Object.keys(evaluator.responsesByQuestion).length - 1">
          Siguiente
        </button>

        <!-- Contenedor para respuestas y iframe -->
        <div class="response-layout">
          <!-- Contenedor con scroll para respuestas -->
          <div class="heuristics-container">
            <div v-for="response in currentResponsesByEvaluator(evaluator)" :key="response.question?.question_id || response.question_id" class="card mb-3">
              <div class="card-body">
                <p><strong>Título:</strong> {{ response.title || response.question?.title || 'Sin título' }}</p>
                <p><strong>Descripción:</strong> {{ response.description || response.question?.description || 'Sin descripción' }}</p>

                <!-- Renderizar heurísticas y subprincipios si existen -->
                <div v-if="hasHeuristics">
                  <div v-for="(heuristic, heuristicIndex) in response.heuristics" :key="`heuristic-${heuristicIndex}`" class="mt-3">
                    <h5>{{ heuristic.heuristic_title }}</h5>
                    <ul>
                      <li v-for="(subprinciple, subprincipleIndex) in heuristic.subprinciples" :key="`subprinciple-${subprincipleIndex}`">
                        <p><strong>Subprincipio:</strong> {{ subprinciple.subprinciple_subtitle }}</p>
                        <p><strong>Descripción:</strong> {{ subprinciple.subprinciple_description }}</p>
                        <p><strong>Valor de respuesta:</strong> {{ subprinciple.response_value }}</p>
                      </li>
                    </ul>
                    <p><strong>Comentario:</strong> {{ heuristic.comment || 'Sin comentario' }}</p> <!-- Comentario a nivel de heurística -->
                  </div>
                </div>

                <!-- Renderizar respuestas estándar si no tiene heurísticas -->
                <div v-else>
                  <p><strong>Tipo de respuesta:</strong> {{ response.response.response_type || 'Desconocido' }}</p>
                  <p><strong>Valor de respuesta:</strong> {{ response.response.response_value || 'N/A' }}</p>
                  <p><strong>Comentario:</strong> {{ response.response.comment || 'Sin comentario' }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Mostrar iframe a la derecha con los parámetros deseados -->
          <iframe 
            v-if="currentResponsesByEvaluator(evaluator)[0].url_frame || currentResponsesByEvaluator(evaluator)[0].question?.url_frame" 
            :src="buildFigmaEmbedUrl(currentResponsesByEvaluator(evaluator)[0].url_frame || currentResponsesByEvaluator(evaluator)[0].question?.url_frame, hasHeuristics)" 
            :class="hasHeuristics ? 'iframe-mobile' : 'iframe-web'" 
            frameborder="0" allowfullscreen
          ></iframe>
        </div>
      </div>
      <div class="export-buttons">
        <button @click="handleExportFullReportPDF">Exportar Informe Completo</button> 
      </div>
    </div>
    <div v-else>
      <p>No se encontraron respuestas para esta prueba de diseño.</p>
    </div>
    <div v-if="isLoadingPDF" class="spinner-overlay">
      <div class="spinner"></div>
    </div>    
  </div>
  
</template>

<style scoped>

/* Estilos del spinner de carga */
.spinner-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.spinner {
  border: 8px solid rgba(255, 255, 255, 0.3);
  border-top: 8px solid #fff;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Flexbox para alinear las respuestas a la izquierda y el iframe a la derecha */
.response-layout {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

/* Contenedor con scroll solo para las respuestas */
.heuristics-container {
  flex: 1;
  max-height: 900px;
  overflow-y: auto;
  margin-right: 20px;
}

/* Estilo del iframe para móvil */
.iframe-mobile {
  width: 500px;
  height: 900px;
  border-radius: 8px;
  overflow: hidden;
  border: 0;
}

/* Estilo del iframe para web */
.iframe-web {
  width: 900px;
  height: 600px;
  border-radius: 8px;
  overflow: hidden;
  border: 0;
}

/* Estilos generales para el grupo de preguntas */
.question-group {
  margin-bottom: 20px;
}

/* Estilos para los botones de navegación */
button {
  margin: 10px;
  padding: 5px 10px;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Estilos para las tarjetas de las respuestas */
.card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 15px;
  margin-bottom: 10px;
}

.card-body {
  display: flex;
  flex-direction: column;
}

.card-body p {
  margin: 5px 0;
}

.card-body ul {
  list-style-type: none;
  padding-left: 0;
}

/* Estilos para los títulos dentro de las tarjetas */
h5 {
  margin-top: 0;
  font-size: 1.2em;
  font-weight: bold;
}

/* Estilo del iframe para mantener bordes suaves */
iframe {
  border-radius: 8px;
  border: 0;
  overflow: hidden;
}

/* Scrollbar para los contenedores con scroll */
.heuristics-container::-webkit-scrollbar {
  width: 8px;
}

.heuristics-container::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 4px;
}

.heuristics-container::-webkit-scrollbar-thumb:hover {
  background-color: #555;
}

/* Contenedor principal */
.container {
  padding: 20px;
  background-color: #f9f9f9;
}

h2 {
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}

/* Adaptar el iframe y el layout para pantallas pequeñas */
@media (max-width: 768px) {
  .response-layout {
    flex-direction: column;
  }

  .iframe-mobile, .iframe-web {
    width: 100%;
    height: 700px;
  }

  .heuristics-container {
    margin-right: 0;
  }
}
</style>
