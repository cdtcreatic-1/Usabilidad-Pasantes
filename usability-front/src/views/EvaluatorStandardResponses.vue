<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import axios from 'axios';
import { useRoute, useRouter } from 'vue-router';
import { useAuthStore } from '../stores/useAuthStore';

// Rutas y store
const route = useRoute();  // Obtiene la ruta actual
const router = useRouter();  // Instancia para redirigir entre rutas
const testId = route.params.testId;  // ID de la prueba desde la ruta
const authStore = useAuthStore();  // Usamos el authStore para obtener el evaluador
const evaluatorId = ref(authStore.userId);  // Guardamos el ID del evaluador

// Variables reactivas
const questionnaires = ref([]);  // Lista de cuestionarios cargados
const responses = ref({});  // Respuestas del evaluador a los cuestionarios
const allResponsesCompleted = ref(false);  // Bandera para verificar si todas las respuestas están completas
const responsesSubmitted = ref(false);  // Indica si el evaluador ya ha enviado todas las respuestas
const testType = ref('');  // Tipo de prueba (web, móvil, tablet)
const iframeStyle = ref({});  // Estilos dinámicos para el iframe
const containerStyle = ref({});  // Estilos dinámicos para el contenedor del iframe
let saveResponsesInterval = null;  // Temporizador para guardar respuestas automáticamente cada 15 segundos

// Función que se ejecuta al montar el componente
onMounted(async () => {
  await checkSubmissionStatus();  // Verifica si las respuestas ya fueron enviadas
  if (!responsesSubmitted.value) {  // Si las respuestas no fueron enviadas
    await loadTestDetails();  // Cargar detalles del test
    await loadQuestionnaires();  // Cargar los cuestionarios disponibles
    await loadSavedResponses();  // Cargar respuestas guardadas del evaluador, si existen
    checkAllResponsesCompleted();  // Verifica si todas las respuestas están completas
    setIframeStyles();  // Establece los estilos del iframe según el tipo de prueba
    
    // Iniciar temporizador de guardado automático cada 15 segundos
    startAutoSaveResponses();
  }
});

// Limpiar el temporizador de guardado automático al salir del componente
onBeforeUnmount(() => {
  clearInterval(saveResponsesInterval);
});

// Función para verificar si el evaluador ya envió las respuestas
const checkSubmissionStatus = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/designtests/${testId}/check_submission`, {
      params: { evaluator_id: evaluatorId.value }
    });
    responsesSubmitted.value = response.data.submitted;  // Marcar como enviadas si corresponde
    if (responsesSubmitted.value) {
      router.push('/designtests/access');  // Redirigir si ya se enviaron
    }
  } catch (error) {
    console.error('Error al verificar el estado de envío:', error);
  }
};

// Función para cargar los detalles de la prueba
const loadTestDetails = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/designtest/test_id/${testId}/`);
    if (response.status === 200) {
      testType.value = response.data.test_type;  // Asignar el tipo de prueba
    }
  } catch (error) {
    console.error('Error al cargar detalles del test:', error);
  }
};

// Función para establecer los estilos del iframe según el tipo de prueba
const setIframeStyles = () => {
  if (testType.value === 'Web') {
    // Estilos para pruebas web
    iframeStyle.value = { width: '100%', height: '600px', display: 'block', margin: '0 auto' };
    containerStyle.value = { width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'center' };
  } else if (testType.value === 'Movil') {
    // Estilos para pruebas móviles
    iframeStyle.value = { width: '340px', height: '600px' };
    containerStyle.value = { width: '340px', margin: 'auto' };
  }
};

// Función para cargar los cuestionarios disponibles
const loadQuestionnaires = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/designtest/${testId}/designquestions/`);
    if (response.status === 200) {
      questionnaires.value = response.data;  // Asigna los cuestionarios cargados
      // Inicializa el objeto de respuestas para cada pregunta
      response.data.forEach(q => {
        responses.value[q.question_id] = {
          response_value: null,  // Valor de la respuesta
          comment: '',  // Comentario opcional del evaluador
          url_frame: q.url_frame,  // URL del diseño relacionado
          evaluator_id: evaluatorId.value,  // ID del evaluador
          test_id: testId,  // ID de la prueba
          response_type: q.response_type  // Tipo de respuesta
        };
      });
    }
  } catch (error) {
    console.error('Error al cargar los cuestionarios:', error);
  }
};

// Función para cargar las respuestas previamente guardadas del evaluador
const loadSavedResponses = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/designtests/${testId}/evaluatorstandardresponses/${evaluatorId.value}/`);
    response.data.forEach(r => {
      if (responses.value[r.question.question_id]) {
        responses.value[r.question.question_id].response_value = r.response_value;  // Asignar la respuesta guardada
        responses.value[r.question.question_id].comment = r.comment;  // Asignar el comentario guardado
      }
    });
    checkAllResponsesCompleted();  // Verifica si las respuestas están completas
  } catch (error) {
    console.error('Error al cargar las respuestas guardadas:', error);
  }
};

// Inicia el guardado automático de respuestas cada 15 segundos
const startAutoSaveResponses = () => {
  saveResponsesInterval = setInterval(saveAllResponses, 15000);  // Guardado automático cada 15s
};

// Función para guardar todas las respuestas automáticamente
const saveAllResponses = async () => {
  try {
    // Prepara el payload para enviar las respuestas
    await axios.post(`http://localhost:8000/api/designtests/${testId}/evaluatorstandardresponses/${evaluatorId.value}/`, {
      responses: Object.keys(responses.value).map(qId => ({
        question: qId,
        response_value: responses.value[qId].response_value,  // Respuesta del evaluador
        comment: responses.value[qId].comment  // Comentario del evaluador
      }))
    });
    console.log('Respuestas guardadas automáticamente.');
  } catch (error) {
    console.error('Error al guardar las respuestas:', error);
  }
};

// Función para verificar si todas las respuestas están completas
const checkAllResponsesCompleted = () => {
  allResponsesCompleted.value = questionnaires.value.every(q => {
    const response = responses.value[q.question_id];
    // Verifica que la respuesta y el comentario no estén vacíos
    return response.response_value !== null && response.comment.trim() !== '';
  });
};

// Escucha cambios en las respuestas y verifica si están completas
watch(responses, checkAllResponsesCompleted, { deep: true });

// Función para enviar todas las respuestas
const submitAllResponses = async () => {
  try {
    // Enviar las respuestas al servidor
    await axios.post(`http://localhost:8000/api/designtests/${testId}/evaluatorstandardresponsesfinalize/`, {
      evaluator_id: evaluatorId.value,
      responses: Object.keys(responses.value).map(qId => ({
        question: qId,
        response_value: responses.value[qId].response_value,  // Respuesta final
        comment: responses.value[qId].comment  // Comentario final
      }))
    });
    alert('Todas las respuestas han sido enviadas.');
    responsesSubmitted.value = true;  // Marca como enviadas
    clearInterval(saveResponsesInterval);  // Detener el guardado automático
    router.push('/designtests/access');  // Redirigir al acceso de pruebas
  } catch (error) {
    console.error('Error al enviar las respuestas:', error);
    alert('Ocurrió un error al enviar las respuestas.');
  }
};
</script>

<template>
  <div class="container mt-4">
    <h2 class="mb-4">Responder Cuestionarios</h2>

    <!-- Mostrar mensaje si ya se enviaron todas las respuestas -->
    <div v-if="responsesSubmitted">
      <p class="text-danger text-center fs-1">Ya has enviado todas las respuestas para esta prueba de diseño.</p>
    </div>

    <!-- Mostrar el formulario si hay cuestionarios y aún no se han enviado las respuestas -->
    <div v-else-if="questionnaires.length > 0">
      <!-- Iterar sobre las preguntas del cuestionario -->
      <div v-for="questionnaire in questionnaires" :key="questionnaire.question_id" class="card mb-3">
        <div class="card-body d-flex">
          
          <!-- Información de la pregunta -->
          <div class="questionnaire-info" style="flex: 1;">
            <h5 class="card-title">{{ questionnaire.title }}</h5>
            <p class="card-text">{{ questionnaire.description }}</p>

            <!-- Mostrar el tipo de respuesta basado en "response_type" -->
            <div v-if="questionnaire.response_type === 'Calificacion'">
              <label>Calificación:</label>
              <div class="radio-group">
                <!-- Opciones de calificación del 1 al 10 -->
                <div v-for="n in 10" :key="n" class="radio-item">
                  <input type="radio" :id="'calificacion' + questionnaire.question_id + n" :value="n" v-model="responses[questionnaire.question_id].response_value">
                  <label :for="'calificacion' + questionnaire.question_id + n">{{ n }}</label>
                </div>
              </div>
            </div>

            <!-- Opciones de legibilidad (1-5) -->
            <div v-else-if="questionnaire.response_type === 'Legibilidad'">
              <label>Legibilidad:</label>
              <div class="radio-group">
                <div v-for="n in 5" :key="n" class="radio-item">
                  <input type="radio" :id="'legibilidad' + questionnaire.question_id + n" :value="n" v-model="responses[questionnaire.question_id].response_value">
                  <label :for="'legibilidad' + questionnaire.question_id + n">{{ n }}</label>
                </div>
              </div>
            </div>

            <!-- Opciones de coherencia (1-10) -->
            <div v-else-if="questionnaire.response_type === 'Coherencia'">
              <label>Coherencia:</label>
              <div class="radio-group">
                <div v-for="n in 10" :key="n" class="radio-item">
                  <input type="radio" :id="'coherencia' + questionnaire.question_id + n" :value="n" v-model="responses[questionnaire.question_id].response_value">
                  <label :for="'coherencia' + questionnaire.question_id + n">{{ n }}</label>
                </div>
              </div>
            </div>

            <!-- Campo de comentario opcional -->
            <div>
              <label>Comentario:</label>
              <textarea v-model="responses[questionnaire.question_id].comment" class="form-control"></textarea>
            </div>
          </div>

          <!-- Iframe con la URL relacionada con la pregunta -->
          <div class="iframe-container ms-3" :style="containerStyle">
            <iframe :src="responses[questionnaire.question_id].url_frame" :style="iframeStyle" frameborder="0"></iframe>
          </div>

        </div>
      </div>
      
      <!-- Botón para enviar todas las respuestas -->
      <button @click="submitAllResponses" class="btn btn-success mt-3" :disabled="!allResponsesCompleted">
        Enviar Todas las Respuestas
      </button>
    </div>

    <!-- Mostrar mensaje si no hay cuestionarios disponibles -->
    <div v-else>
      <p>No se encontraron cuestionarios para esta prueba de diseño.</p>
    </div>
  </div>
</template>

<style scoped>
/* Estilo para las tarjetas del cuestionario */
.card {
  margin-top: 20px;
}

/* Grupo de radio buttons (calificación, legibilidad, coherencia) */
.radio-group {
  display: flex;
  justify-content: left;
  align-items: center;
  margin-top: 10px;
}

/* Estilo para cada opción de radio (1-10 para calificación y coherencia, 1-5 para legibilidad) */
.radio-item {
  margin: 0 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Contenedor del iframe, con ancho máximo para limitar el tamaño */
.iframe-container {
  border: 1px solid #ccc;
  width: 100%;
  max-width: 900px;  /* Limitar el tamaño máximo del iframe */
  overflow: hidden;
}

/* Estilo para distribuir el contenido de la pregunta y el iframe */
.d-flex {
  display: flex;
  justify-content: space-between;  /* Espacio entre la info de la pregunta y el iframe */
}

/* Margen izquierdo para el iframe */
.ms-3 {
  margin-left: 1rem;
}

/* Estilo para la información de la pregunta */
.questionnaire-info {
  flex: 1;
  padding-right: 15px;  /* Espacio entre la información y el iframe */
}
</style>
