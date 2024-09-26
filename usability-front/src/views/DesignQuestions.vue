<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

// Obtenemos el ID de la prueba desde los parámetros de la ruta
const route = useRoute();
const testId = route.params.testId;

// Determina si la prueba tiene heurísticas
const hasHeuristics = ref(false);

// Datos del formulario para crear y editar preguntas
const form = ref({
  title: '',        
  url_frame: '',    
  description: '',  
  heuristics: [],   
  response_type: '',
});

const editForm = ref({
  title: '',        
  url_frame: '',    
  description: '',  
  heuristics: [],   
  response_type: '',
});

// Maneja los errores de validación del formulario
const errors = ref({
  title: '',
  url_frame: '',
  description: '',
  response_type: '',
});

// Datos sobre la prueba actual (URL, tipo de prueba)
const testUrl = ref('');
const testType = ref('');
const iframeStyle = ref({});
const containerStyle = ref({});
const heuristics = ref([]);
const questions = ref([]);

// Al montar el componente, cargamos los datos de la prueba y configuramos los estilos del iframe
onMounted(async () => {
  await fetchTestDetails();  // Obtener detalles de la prueba (tipo, URL)
  setIframeStyles();         // Establecer los estilos según el tipo de prueba (móvil o web)
  await checkHasHeuristics(testId);  // Verificar si la prueba tiene heurísticas
  await fetchHeuristics();   // Cargar la lista de heurísticas desde el backend
  await fetchQuestions();    // Cargar la lista de preguntas asociadas a la prueba
});

// Construye la URL del embed de Figma, ajustando los parámetros según si tiene heurísticas o no
const buildFigmaEmbedUrl = (baseUrl, hasHeuristics) => {
  const scalingParam = hasHeuristics ? '&content-scaling=fixed' : '&scaling=scale-down-width';
  const commonParams = '&disable-default-keyboard-nav=true';
  return `${baseUrl}?embed_host=your-site${commonParams}${scalingParam}`;
};

// Verifica si la prueba tiene heurísticas
const checkHasHeuristics = async (testId) => {
  try {
    const response = await axios.get(`http://localhost:8000/api/designtest/${testId}/heuristics/`);
    hasHeuristics.value = response.data.hasHeuristics;
  } catch (error) {
    console.error("Error al verificar si la prueba tiene heurísticas:", error);
  }
};

// Obtiene los detalles de la prueba de diseño
const fetchTestDetails = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/designtest/test_id/${testId}/`);
    testUrl.value = response.data.url;
    testType.value = response.data.test_type;
  } catch (error) {
    console.error('Error al obtener los detalles de la prueba:', error);
  }
};

// Carga las heurísticas disponibles desde el backend
const fetchHeuristics = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/heuristics');
    heuristics.value = response.data.map(h => ({
      ...h,
      isOpen: false,  // Controla si la heurística se despliega para mostrar sus subprincipios
    }));
  } catch (error) {
    console.error('Error al obtener las heurísticas:', error);
  }
};

// Carga las preguntas relacionadas con la prueba desde el backend
const fetchQuestions = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/designtest/${testId}/designquestions/`);
    questions.value = response.data;
  } catch (error) {
    console.error('Error al obtener las preguntas:', error);
  }
};

// Establece los estilos del iframe según el tipo de prueba (móvil o web)
const setIframeStyles = () => {
  if (testType.value === 'Movil') {
    iframeStyle.value = { width: '540px', height: '840px' };
    containerStyle.value = { width: '580px', height: '870px' };
  } else if (testType.value === 'Web') {
    iframeStyle.value = { width: '1046px', height: '942px' };
    containerStyle.value = { width: '1086px', height: '812px' };
  }
};

// Valida el formulario antes de crear una nueva pregunta
const validateForm = () => {
  errors.value = {
    title: '',
    url_frame: '',
    description: '',
    response_type: '',
  };

  // Verifica que los campos necesarios estén completos
  if (!form.value.title) {
    errors.value.title = 'El Título es obligatorio.';
  }
  if (!form.value.url_frame) {
    errors.value.url_frame = 'La URL es obligatoria.';
  }
  if (!form.value.description) {
    errors.value.description = 'La descripción es obligatoria.';
  }

  // Si no hay heurísticas, el tipo de respuesta es obligatorio
  if (!hasHeuristics.value && !form.value.response_type) {
    errors.value.response_type = 'El tipo de respuesta es obligatorio.';
  }

  return !Object.values(errors.value).some(error => error !== '');
};

// Guarda una nueva pregunta de diseño
const handleSaveQuestion = async () => {
  if (!validateForm()) return;

  try {
    const data = {
      title: form.value.title,
      url_frame: form.value.url_frame,
      description: form.value.description,
      heuristics: form.value.heuristics,  // Lista de heurísticas seleccionadas
      response_type: hasHeuristics.value ? null : form.value.response_type,  // Tipo de respuesta solo si no tiene heurísticas
    };

    await axios.post(`http://localhost:8000/api/designtest/${testId}/designquestions/`, data);
    alert('Pregunta creada exitosamente');
    
    // Reiniciar el formulario tras crear la pregunta
    form.value = { title: '', url_frame: '', description: '', heuristics: [], response_type: '' };
    await fetchQuestions();  // Recargar las preguntas
  } catch (error) {
    console.error('Error al crear la pregunta:', error);
    alert('Error al crear la pregunta');
  }
};

// Inicia la edición de una pregunta existente
const startEditQuestion = (question) => {
  // Cargar los datos de la pregunta en el formulario de edición
  editForm.value.title = question.title;
  editForm.value.description = question.description;
  editForm.value.url_frame = question.url_frame;
  editForm.value.response_type = question.response_type || '';  // Solo si no tiene heurísticas
  if (hasHeuristics.value) {
    editForm.value.heuristics = [...question.heuristics];  // Solo si tiene heurísticas
  }
  question.isEditing = true;  // Marca la pregunta como en edición
};

// Cancela la edición de una pregunta
const cancelEditQuestion = (question) => {
  question.isEditing = false;
};

// Guarda los cambios en una pregunta editada
const saveEditQuestion = async (question) => {
  try {
    const data = {
      title: editForm.value.title,
      description: editForm.value.description,
      url_frame: editForm.value.url_frame,
      response_type: editForm.value.response_type,
      heuristics: hasHeuristics.value ? editForm.value.heuristics : [],  // Solo si tiene heurísticas
    };

    await axios.put(`http://localhost:8000/api/designtest/${testId}/designquestions/${question.question_id}/`, data);
    alert('Pregunta actualizada exitosamente');
    question.isEditing = false;
    await fetchQuestions();  // Recargar las preguntas tras la actualización
  } catch (error) {
    console.error('Error al actualizar la pregunta:', error);
    alert('Error al actualizar la pregunta');
  }
};

// Elimina una pregunta tras confirmación del usuario
const handleDeleteQuestion = async (questionId) => {
  if (!confirm('¿Estás seguro de que deseas eliminar esta pregunta?')) return;

  try {
    await axios.delete(`http://localhost:8000/api/designtest/${testId}/designquestions/${questionId}/`);
    alert('Pregunta eliminada exitosamente');
    await fetchQuestions();  // Recargar las preguntas tras eliminar
  } catch (error) {
    console.error('Error al eliminar la pregunta:', error);
    alert('Error al eliminar la pregunta');
  }
};

// Alterna la visibilidad de los subprincipios de una heurística
const toggleSubprinciples = (heuristic) => {
  heuristic.isOpen = !heuristic.isOpen;
};

// Obtiene el título de una heurística por su código
const getHeuristicTitle = (code) => {
  const heuristic = heuristics.value.find(h => h.code === code);
  return heuristic ? heuristic.title : 'Heurística no encontrada';
};
</script>

<template>
  <div class="container mt-2 d-flex justify-content-center">

    <!-- Contenedor para pruebas Web (cuando no hay heurísticas) -->
    <div v-if="!hasHeuristics" class="d-flex justify-content-between align-items-start">
      
      <!-- Sección del formulario de creación de preguntas para pruebas web -->
      <div class="card mt-3" style="width: 400px;">
        <div class="card-header">
          <h2>Crear Pregunta de Diseño - Web</h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleSaveQuestion">
            <!-- Campo para el título de la pregunta -->
            <div class="mb-3">
              <label for="title" class="form-label">Título</label>
              <input v-model="form.title" type="text" class="form-control" id="title" :class="{ 'is-invalid': errors.title }" />
              <div class="invalid-feedback">{{ errors.title }}</div>
            </div>

            <!-- Campo para la URL del frame -->
            <div class="mb-3">
              <label for="url_frame" class="form-label">URL del Frame</label>
              <input v-model="form.url_frame" type="text" class="form-control" id="url_frame" :class="{ 'is-invalid': errors.url_frame }" />
              <div class="invalid-feedback">{{ errors.url_frame }}</div>
            </div>

            <!-- Campo para la descripción de la pregunta -->
            <div class="mb-3">
              <label for="description" class="form-label">Descripción</label>
              <input v-model="form.description" type="text" class="form-control" id="description" :class="{ 'is-invalid': errors.description }" />
              <div class="invalid-feedback">{{ errors.description }}</div>
            </div>

            <!-- Selección del tipo de respuesta (aplica solo cuando no hay heurísticas) -->
            <div class="mb-3">
              <label for="response_type" class="form-label">Tipo de Respuesta</label>
              <select v-model="form.response_type" class="form-select" id="response_type" :class="{ 'is-invalid': errors.response_type }">
                <option value="Calificacion">Calificación</option>
                <option value="Legibilidad">Legibilidad</option>
                <option value="Coherencia">Coherencia</option>
              </select>
              <div class="invalid-feedback">{{ errors.response_type }}</div>
            </div>

            <!-- Botón para enviar el formulario de creación -->
            <button type="submit" class="btn btn-primary">Crear Pregunta</button>
          </form>
        </div>
      </div>

      <!-- Contenedor del iframe que visualiza el diseño web -->
      <div class="container mt-3">
        <div class="card p-3" ref="iframeContainer" :style="containerStyle">
          <iframe 
            :src="buildFigmaEmbedUrl(testUrl, hasHeuristics)"
            :style="iframeStyle" 
            frameborder="0" 
            allowfullscreen
          ></iframe>
        </div>
      </div>
    </div>

    <!-- Contenedor para pruebas móviles (con heurísticas) -->
    <div v-if="hasHeuristics" class="d-flex justify-content-between align-items-start">
      
      <!-- Sección del formulario de creación de preguntas para pruebas móviles -->
      <div class="card mt-3" style="width: 800px;">
        <div class="card-header">
          <h2>Crear Pregunta de Diseño - Móvil</h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="handleSaveQuestion">
            <!-- Campo para el título de la pregunta -->
            <div class="mb-3">
              <label for="title" class="form-label">Título</label>
              <input v-model="form.title" type="text" class="form-control" id="title" :class="{ 'is-invalid': errors.title }" />
              <div class="invalid-feedback">{{ errors.title }}</div>
            </div>

            <!-- Campo para la URL -->
            <div class="mb-3">
              <label for="url_frame" class="form-label">URL del Frame</label>
              <input v-model="form.url_frame" type="text" class="form-control" id="url_frame" :class="{ 'is-invalid': errors.url_frame }" />
              <div class="invalid-feedback">{{ errors.url_frame }}</div>
            </div>

            <!-- Campo para la descripción de la pregunta -->
            <div class="mb-3">
              <label for="description" class="form-label">Descripción</label>
              <input v-model="form.description" type="text" class="form-control" id="description" :class="{ 'is-invalid': errors.description }" />
              <div class="invalid-feedback">{{ errors.description }}</div>
            </div>

            <!-- Selección de principios heurísticos (solo para móviles) -->
            <div v-if="hasHeuristics">
              <h2>Principios Heurísticos</h2>
              <!-- Listado de heurísticas con opción de seleccionar cada una -->
              <div v-for="heuristic in heuristics" :key="heuristic.code" class="form-check">
                <input type="checkbox" :id="heuristic.code" :value="heuristic.code" v-model="form.heuristics" class="form-check-input"/>
                <label :for="heuristic.code" class="form-check-label">{{ heuristic.title }}</label>

                <!-- Botón para desplegar los subprincipios de la heurística -->
                <button type="button" @click="toggleSubprinciples(heuristic)" class="btn btn-link">
                  <i :class="{'fas fa-chevron-down': !heuristic.isOpen, 'fas fa-chevron-up': heuristic.isOpen}"></i>
                </button>

                <!-- Subprincipios, solo se muestran si la heurística está desplegada -->
                <div v-if="heuristic.isOpen" style="margin-left: 20px;">
                  <ul>
                    <li v-for="subprinciple in heuristic.subprinciples" :key="subprinciple.code">
                      <p><strong>{{ subprinciple.subtitle }}</strong></p>
                      <p><strong>Descripción:</strong> {{ subprinciple.description }}</p>
                    </li>
                  </ul>
                </div>
              </div>
            </div>

            <!-- Botón para enviar el formulario de creación -->
            <button type="submit" class="btn btn-primary">Crear Pregunta</button>
          </form>
        </div>
      </div>

      <!-- Contenedor del iframe que visualiza el diseño móvil -->
      <div class="container mt-3">
        <div class="card p-3" ref="iframeContainer" :style="containerStyle">
          <iframe 
            :src="buildFigmaEmbedUrl(testUrl, hasHeuristics)"
            :style="iframeStyle" 
            frameborder="0" 
            allowfullscreen
          ></iframe>
        </div>
      </div>
    </div>

  </div>

  <!-- Sección de lista de preguntas creadas -->
  <div class="m-5">
    <div class="card-body" v-if="questions.length > 0">
      <p class="card-title m-3" style="text-align:center;"><strong>Preguntas de Diseño</strong></p>
      <!-- Iteración sobre la lista de preguntas existentes -->
      <div v-for="question in questions" :key="question.question_id" class="mb-3 d-flex">
        <!-- Tarjeta que muestra la información de la pregunta -->
        <div class="card me-3" style="width: 25%;">
          <div class="card-body">
            <!-- Sección de visualización de la pregunta -->
            <div v-if="!question.isEditing">
              <p class="card-title"><strong>Título: </strong>{{ question.title }}</p>
              <p class="card-description"><strong>Descripción: </strong>{{ question.description }}</p>
              <p class="card-url"><strong>URL: </strong><a :href="question.url_frame" target="_blank">{{ question.url_frame }}</a></p>

              <!-- Mostrar heurísticas si la pregunta tiene -->
              <div v-if="hasHeuristics">
                <strong>Heurísticas:</strong>
                <ul>
                  <li v-for="heuristicCode in question.heuristics" :key="heuristicCode">
                    {{ getHeuristicTitle(heuristicCode) }}
                  </li>
                </ul>
              </div>

              <!-- Mostrar el tipo de respuesta si no tiene heurísticas -->
              <p v-else><strong>Tipo de Respuesta: </strong>{{ question.response_type }}</p>

              <!-- Botones para editar o eliminar la pregunta -->
              <button @click="startEditQuestion(question)" class="btn btn-warning me-2">Editar</button>
              <button @click="handleDeleteQuestion(question.question_id)" class="btn btn-danger">Eliminar</button>
            </div>

            <!-- Sección de edición de la pregunta -->
            <div v-else>
              <div class="mb-3">
                <label for="editTitle" class="form-label">Título</label>
                <input v-model="editForm.title" type="text" class="form-control" id="editTitle" />
              </div>
              <div class="mb-3">
                <label for="editDescription" class="form-label">Descripción</label>
                <textarea v-model="editForm.description" class="form-control" id="editDescription"></textarea>
              </div>
              <div class="mb-3">
                <label for="editUrlFrame" class="form-label">URL del Frame</label>
                <input v-model="editForm.url_frame" type="text" class="form-control" id="editUrlFrame" />
              </div>

              <!-- Edición de heurísticas (solo si la pregunta tiene heurísticas) -->
              <div v-if="hasHeuristics">
                <h2>Principios Heurísticos</h2>
                <div v-for="heuristic in heuristics" :key="heuristic.code" class="form-check">
                  <input type="checkbox" :id="heuristic.code" :value="heuristic.code" v-model="editForm.heuristics" class="form-check-input"/>
                  <label :for="heuristic.code" class="form-check-label">{{ heuristic.title }}</label>

                  <!-- Botón para alternar subprincipios en edición -->
                  <button type="button" @click="toggleSubprinciples(heuristic)" class="btn btn-link">
                    <i :class="{'fas fa-chevron-down': !heuristic.isOpen, 'fas fa-chevron-up': heuristic.isOpen}"></i>
                  </button>

                  <!-- Subprincipios si está desplegado -->
                  <div v-if="heuristic.isOpen" style="margin-left: 20px;">
                    <ul>
                      <li v-for="subprinciple in heuristic.subprinciples" :key="subprinciple.code">
                        <p><strong>{{ subprinciple.subtitle }}</strong></p>
                        <p><strong>Descripción:</strong> {{ subprinciple.description }}</p>
                      </li>
                    </ul>
                  </div>
                </div>
              </div>

              <!-- Edición del tipo de respuesta (solo si no tiene heurísticas) -->
              <div v-else>
                <div class="mb-3">
                  <label for="editResponseType" class="form-label">Tipo de Respuesta</label>
                  <select v-model="editForm.response_type" class="form-select" id="editResponseType">
                    <option value="Calificacion">Calificación</option>
                    <option value="Legibilidad">Legibilidad</option>
                    <option value="Coherencia">Coherencia</option>
                  </select>
                </div>
              </div>

              <!-- Botones para guardar o cancelar la edición -->
              <button @click="saveEditQuestion(question)" class="btn btn-success me-2">Guardar</button>
              <button @click="cancelEditQuestion(question)" class="btn btn-secondary">Cancelar</button>
            </div>
          </div>
        </div>

        <!-- Contenedor del iframe para cada pregunta -->
        <div class="card" style="width: 75%;">
          <div class="card-body">
            <iframe 
              :src="buildFigmaEmbedUrl(question.url_frame, hasHeuristics)"
              width="100%" height="700"
              frameborder="0" 
              allowfullscreen
            ></iframe>
          </div>
        </div>
      </div>
    </div>

    <!-- Mensaje cuando no hay preguntas de diseño -->
    <div v-else>
      <p>No hay preguntas de diseño disponibles.</p>
    </div>
  </div>
</template>
