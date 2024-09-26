<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

// Obtiene el ID de la prueba desde la ruta
const route = useRoute();
const testId = route.params.testId;

// Variables reactivas
const questions = ref([]);  // Almacena las preguntas del cuestionario
const heuristics = ref([]);  // Lista de heurísticas para las preguntas
const responses = ref({});  // Almacena las respuestas del evaluador
const allResponsesCompleted = ref(false);  // Verifica si todas las respuestas han sido completadas
const responsesSubmitted = ref(false);  // Indica si las respuestas fueron enviadas
const evaluatorId = ref(localStorage.getItem('userId'));  // Obtenemos el ID del evaluador desde el localStorage

// Al montar el componente, cargamos las preguntas y las respuestas guardadas
onMounted(async () => {
  await loadQuestions();  // Cargar las preguntas del cuestionario
  await loadSavedResponses();  // Cargar respuestas previamente guardadas (si existen)
  checkAllResponsesCompleted();  // Verifica si todas las respuestas están completas
});

// Cargar las preguntas y las heurísticas relacionadas
const loadQuestions = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/designtest/${testId}/designquestions/`);
    questions.value = response.data;  // Asigna las preguntas cargadas
    await loadHeuristics();  // Cargar las heurísticas para las preguntas
  } catch (error) {
    console.error('Error al cargar las preguntas:', error);
  }
};

// Cargar las heurísticas asociadas a la prueba
const loadHeuristics = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/heuristics');
    heuristics.value = response.data;  // Asigna las heurísticas

    // Asigna heurísticas a cada pregunta y prepara las respuestas
    questions.value.forEach(question => {
      // Inicializar el objeto de respuestas para cada pregunta
      responses.value[question.question_id] = {
        heuristics: {}
      };
      
      // Vincula cada heurística con sus subprincipios
      question.heuristics.forEach((heuristicCode, index) => {
        const matchedHeuristic = heuristics.value.find(h => h.code === heuristicCode);
        if (matchedHeuristic) {
          question.heuristics[index] = {
            ...matchedHeuristic,
            isOpen: false  // Controla si la heurística está desplegada
          };

          // Inicializar las respuestas para cada heurística y sus subprincipios
          responses.value[question.question_id].heuristics[matchedHeuristic.code] = {
            comment: '',  // Comentario sobre la heurística
            subprinciples: {}
          };

          // Inicializa las respuestas para los subprincipios de la heurística
          matchedHeuristic.subprinciples.forEach(subprinciple => {
            responses.value[question.question_id].heuristics[matchedHeuristic.code].subprinciples[subprinciple.code] = {
              score: null  // Calificación del subprincipio
            };
          });
        }
      });
    });
  } catch (error) {
    console.error('Error al cargar las heurísticas:', error);
  }
};

// Cargar las respuestas guardadas del evaluador (si existen)
const loadSavedResponses = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/designtests/${testId}/evaluatorheuristicresponses/${evaluatorId.value}/`);
    response.data.forEach(r => {
      const heuristicResponses = responses.value[r.question_id].heuristics[r.heuristic_code];
      if (heuristicResponses) {
        heuristicResponses.subprinciples[r.subprinciple_code].score = r.response_value;  // Calificación
        heuristicResponses.comment = r.comment;  // Comentario a nivel de heurística
      }
    });
    checkAllResponsesCompleted();  // Verifica si todas las respuestas están completas
  } catch (error) {
    console.error('Error al cargar las respuestas guardadas:', error);
  }
};

// Guardar las respuestas parciales de una pregunta específica
const saveResponse = async (questionId) => {
  try {
    const question = questions.value.find(q => q.question_id === questionId);
    if (!question) {
      console.error("No se encontró la pregunta con ese ID");
      return;
    }

    // Mapeamos cada heurística de la pregunta con sus subprincipios
    const heuristicsData = question.heuristics.map(heuristic => {
      return {
        heuristic_code: heuristic.code,  // Código de la heurística
        comment: responses.value[questionId].heuristics[heuristic.code].comment,  // Comentario sobre la heurística
        subprinciples: Object.keys(responses.value[questionId].heuristics[heuristic.code].subprinciples).map(subprinciple_id => ({
          subprinciple_code: subprinciple_id,
          response_value: responses.value[questionId].heuristics[heuristic.code].subprinciples[subprinciple_id].score
        }))
      };
    });

    // Estructura del payload que se envía al servidor
    const payload = {
      evaluator_id: evaluatorId.value,
      test_id: testId,
      question_id: questionId,  // ID de la pregunta
      heuristics: heuristicsData  // Respuestas de las heurísticas y subprincipios
    };

    console.log('Payload:', JSON.stringify(payload, null, 2));

    // Validación de los datos antes de enviar
    if (!payload.evaluator_id || !payload.test_id || !payload.question_id || !payload.heuristics.length) {
      console.error("Faltan datos para el guardado");
      return;
    }

    // Enviar las respuestas parciales al servidor
    await axios.post(`http://localhost:8000/api/designtests/${testId}/evaluatorheuristicresponses/${evaluatorId.value}/`, payload);
    console.log('Respuestas guardadas parcialmente.');
  } catch (error) {
    console.error('Error al guardar la respuesta:', error.response?.data || error.message);
  }
};

// Verificar si todas las respuestas están completas
const checkAllResponsesCompleted = () => {
  allResponsesCompleted.value = questions.value.every(q => {
    return Object.values(responses.value[q.question_id].heuristics).every(heuristic => {
      return Object.values(heuristic.subprinciples).every(subprinciple => subprinciple.score !== null) &&
             heuristic.comment.trim() !== '';  // Asegura que todos los subprincipios tengan calificación y comentario
    });
  });
};

// Guardar todas las respuestas como completadas y enviarlas
const submitAllResponses = async () => {
  try {
    const payload = {
      evaluator_id: evaluatorId.value,
      test_id: testId,
      responses: Object.keys(responses.value).map(question_id => {
        const question = questions.value.find(q => q.question_id == question_id);
        if (!question || !question.heuristics || !question.heuristics.length) {
          console.error(`No se encontraron heurísticas para la pregunta ${question_id}`);
          return null;
        }

        const heuristics = question.heuristics.map(heuristic => {
          const subprinciples = Object.keys(responses.value[question_id].heuristics[heuristic.code].subprinciples).map(subprinciple_id => {
            const subprinciple = responses.value[question_id].heuristics[heuristic.code].subprinciples[subprinciple_id];
            if (!subprinciple) {
              console.error(`No se encontró subprincipio para el id ${subprinciple_id}`);
              return null;
            }
            return {
              subprinciple_code: subprinciple_id,
              response_value: subprinciple.score
            };
          }).filter(sp => sp !== null);

          return {
            heuristic_code: heuristic.code,  // Código de la heurística
            comment: responses.value[question_id].heuristics[heuristic.code].comment,  // Comentario sobre la heurística
            subprinciples: subprinciples
          };
        }).filter(h => h !== null);

        return {
          question_id: question_id,
          heuristics: heuristics
        };
      }).filter(q => q !== null)
    };

    if (!payload.responses.length) {
      console.error("No hay respuestas completas para enviar");
      return;
    }

    // Enviar todas las respuestas al servidor
    await axios.post(`http://localhost:8000/api/designtests/${testId}/evaluatorheuristicresponsesfinalize/`, payload);
    alert('Todas las respuestas han sido enviadas.');
    responsesSubmitted.value = true;  // Marcar respuestas como enviadas
    window.location.href = '/designtests/access';  // Redirigir al acceso de pruebas
  } catch (error) {
    console.error('Error al enviar las respuestas:', error.response?.data || error.message);
  }
};

// Alternar el despliegue de los subprincipios de una heurística
const toggleSubprinciples = (questionId, heuristicCode) => {
  const question = questions.value.find(q => q.question_id === questionId);
  const heuristic = question.heuristics.find(h => h.code === heuristicCode);
  heuristic.isOpen = !heuristic.isOpen;  // Cambia el estado de despliegue
};
</script>

<template>
  <div class="container mt-4">
    <h2 class="mb-4">Responder Cuestionarios con Heurísticas</h2>

    <!-- Mensaje que indica si las respuestas ya han sido enviadas -->
    <div v-if="responsesSubmitted">
      <p class="text-danger text-center fs-1">Ya has enviado todas las respuestas para esta prueba de diseño.</p>
    </div>

    <!-- Mostrar el cuestionario si hay preguntas disponibles -->
    <div v-else-if="questions.length > 0">
      <!-- Iterar sobre todas las preguntas del cuestionario -->
      <div v-for="question in questions" :key="question.question_id" class="card mb-3">
        <div class="card-body d-flex">
          <!-- Información sobre la pregunta -->
          <div class="questionnaire-info">
            <h5 class="card-title">{{ question.title }}</h5>
            <p class="card-text">{{ question.description }}</p>
            <p><strong>URL:</strong> <a :href="question.url_frame" target="_blank">{{ question.url_frame }}</a></p>

            <!-- Iterar sobre las heurísticas asociadas a la pregunta -->
            <div v-for="heuristic in question.heuristics" :key="heuristic.code">
              <h6>
                {{ heuristic.title }}
                <!-- Botón para alternar el despliegue de los subprincipios de la heurística -->
                <button @click="toggleSubprinciples(question.question_id, heuristic.code)" class="btn btn-link">
                  <i :class="{'fas fa-chevron-down': !heuristic.isOpen, 'fas fa-chevron-up': heuristic.isOpen}"></i>
                </button>
              </h6>

              <!-- Descripción y subprincipios de la heurística, si está desplegada -->
              <div v-if="heuristic.isOpen">
                <p>{{ heuristic.description }}</p>

                <!-- Iterar sobre los subprincipios de la heurística -->
                <div v-for="subprinciple in heuristic.subprinciples" :key="subprinciple.code">
                  <p><strong>{{ subprinciple.title }}</strong></p>
                  <p>{{ subprinciple.description }}</p>

                  <!-- Selección de calificación para el subprincipio -->
                  <label>Calificación:</label>
                  <div class="radio-group">
                    <div v-for="n in 10" :key="n" class="radio-item">
                      <input type="radio" :id="'calificacion' + subprinciple.code + n" :value="n"
                            v-model="responses[question.question_id].heuristics[heuristic.code].subprinciples[subprinciple.code].score"
                            @change="saveResponse(question.question_id)">
                      <label :for="'calificacion' + subprinciple.code + n">{{ n }}</label>
                    </div>
                  </div>
                </div>

                <!-- Campo de comentario para la heurística -->
                <label>Comentario para la heurística:</label>
                <textarea v-model="responses[question.question_id].heuristics[heuristic.code].comment" 
                          class="form-control" @blur="saveResponse(question.question_id)"></textarea>
              </div>
            </div>
          </div>

          <!-- Contenedor para mostrar el iframe con el diseño -->
          <div class="iframe-container ms-3">
            <iframe :src="question.url_frame" width="100%" height="800" frameborder="0"></iframe>
          </div>
        </div>
      </div>

      <!-- Botón para enviar todas las respuestas, deshabilitado si no están completas -->
      <button @click="submitAllResponses" class="btn btn-success mt-3" :disabled="!allResponsesCompleted">
        Enviar Todas las Respuestas
      </button>
    </div>

    <!-- Mensaje si no se encontraron cuestionarios -->
    <div v-else>
      <p>No se encontraron cuestionarios para esta prueba de diseño.</p>
    </div>
  </div>
</template>

<style scoped>
/* Estilo para las tarjetas (preguntas) */
.card {
  margin-top: 20px;
}

/* Grupo de radio buttons para la calificación */
.radio-group {
  display: flex;
  justify-content: left;
  align-items: center;
  margin-top: 10px;
}

/* Estilo para cada opción de calificación */
.radio-item {
  margin: 0 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Contenedor del iframe, con un borde para mejor visibilidad */
.iframe-container {
  border: 1px solid #ccc;
  width: 100%;
  max-width: 900px;
  overflow: hidden;
}

/* Clase para alinear los elementos en el cuestionario */
.d-flex {
  display: flex;
}

/* Clase para dar un margen izquierdo */
.ms-3 {
  margin-left: 1rem;
}

/* Estilo para la sección de información del cuestionario */
.questionnaire-info {
  flex: 1;
  padding-right: 15px;
}
</style>

