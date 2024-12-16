<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/useAuthStore';

// Inicializa el enrutador para la navegación y la tienda de autenticación para manejar el estado del usuario
const router = useRouter();
const authStore = useAuthStore();

// Estado para controlar si estamos editando una prueba existente
const isEditing = ref(false);

// ID de la prueba que se está editando
const editingTestId = ref(null);

// Guarda el código original cuando se está en modo edición
const originalCode = ref('');

// Lista de pruebas de diseño y estados adicionales como el rol del usuario
const tests = ref([]);
const showCodes = ref({});
const rol = ref('');

// Datos del formulario para crear o editar pruebas de diseño
const form = ref({
  name: '',       
  url: '',        
  description: '',
  testType: '',   
  heuristics: '', 
  code: '',       
});

// Errores de validación del formulario
const errors = ref({
  name: '',
  url: '',
  description: '',
  testType: '',
  heuristics: '',
  code: '',
});

// Genera un código único de 10 caracteres para cada prueba de diseño
const generateCode = () => {
  const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let code = '';
  for (let i = 0; i < 10; i++) {
    code += chars.charAt(Math.floor(Math.random() * chars.length));
  }
  return code;
};

// Al montar el componente, genera un código único y obtiene las pruebas existentes
onMounted(async () => {
  rol.value = authStore.role;  // Establece el rol del usuario desde la tienda de autenticación
  form.value.code = generateCode(); // Genera el código de la prueba al cargar el componente
  await refreshOwnersList();  // Carga la lista de pruebas del usuario
});

// Valida el formulario antes de crear o actualizar una prueba
const validateCreateForm = async () => {
  // Reinicia los errores de validación
  errors.value = {
    name: '',
    url: '',
    description: '',
    testType: '',
    heuristics: '',
    code: '',
  };

  // Validaciones básicas de los campos obligatorios
  if (!form.value.name) {
    errors.value.name = 'El Nombre de la Prueba es obligatorio.';
  }
  if (!form.value.url) {
    errors.value.url = 'La URL es obligatoria.';
  }
  if (!form.value.description) {
    errors.value.description = 'La Descripción es obligatoria.';
  }
  if (!form.value.testType) {
    errors.value.testType = 'El Tipo de Prueba es obligatorio.';
  }
  if (!form.value.heuristics) {
    errors.value.heuristics = 'El tipo de heurísticas es obligatorio.';
  }

  // Si el código es nuevo o ha sido modificado, verificar si ya está en uso
  if (!isEditing.value || (isEditing.value && form.value.code !== originalCode.value)) {
    if (!form.value.code) {
      errors.value.code = 'El Código es obligatorio.';
    } else {
      const codeExists = await checkCodeAvailability(form.value.code);
      if (codeExists) {
        errors.value.code = 'Este código ya está en uso. Intenta nuevamente con un código diferente.';
      }
    }
  }

  // Retorna true si el formulario es válido, de lo contrario false
  return !Object.values(errors.value).some(error => error !== '');
};

// Verifica si el código de prueba ya está en uso en el backend
const checkCodeAvailability = async (code) => {
  try {
    const response = await axios.get(`http://localhost:8000/api/designtest/checkcode/${code}`);
    return response.data.exists;
  } catch (error) {
    console.error("Error verificando disponibilidad del código", error);
    return false;
  }
};

// Maneja la creación de una nueva prueba de diseño
const handleSaveDesignTest = async () => {
  if (!await validateCreateForm()) {
    return;
  }

  // Formatea la URL según si se usan heurísticas o no
  const formattedUrl = formatFigmaUrl(form.value.url, form.value.heuristics === 'Con heuristicas');

  try {
    // Datos que se enviarán al backend
    const requestData = {
      name: form.value.name,
      url: formattedUrl,
      description: form.value.description,
      user: authStore.userId,
      user_name: authStore.username,
      test_type: form.value.testType,
      has_heuristics: form.value.heuristics === 'Con heuristicas',
      code: form.value.code,
    };

    // Enviar la solicitud POST al backend para crear la prueba
    const response = await axios.post('http://localhost:8000/api/designtest/', requestData);
    console.log(response);

    // Actualiza la lista de pruebas y limpia el formulario
    await refreshOwnersList();
    form.value.name = '';
    form.value.url = '';
    form.value.description = '';
    form.value.testType = '';
    form.value.heuristics = ''; 
    form.value.code = generateCode(); 

  } catch (error) {
    console.error(error);
    if (error.response && error.response.data.error) {
      alert(error.response.data.error);
    }
  }
};

// Maneja la actualización de una prueba existente
const handleUpdateDesignTest = async () => {
  if (!await validateCreateForm()) {
    return;
  }
  try {
    // Datos actualizados de la prueba a enviar al backend
    const requestData = {
      name: form.value.name,
      url: form.value.url,
      description: form.value.description,
      user: authStore.userId,
      test_type: form.value.testType,
      has_heuristics: form.value.heuristics === 'Con heuristicas',
      code: form.value.code,
    };

    // Enviar la solicitud PUT al backend para actualizar la prueba
    await axios.put(`http://localhost:8000/api/designtest/test_id/${editingTestId.value}/`, requestData);
    await refreshOwnersList();

    // Restablecer el formulario y el estado de edición
    form.value.name = '';
    form.value.url = '';
    form.value.description = '';
    form.value.testType = '';
    form.value.heuristics = ''; 
    form.value.code = '';
    isEditing.value = false;
    editingTestId.value = null;

  } catch (error) {
    console.error(error);
    if (error.response && error.response.data.error) {
      alert(error.response.data.error);
    }
  }
};

// Formatea las URLs de Figma para que sean correctas según el tipo de prueba
const formatFigmaUrl = (url, hasHeuristics) => {
  const isEmbedded = url.includes("embed");

  // Elimina parámetros no deseados de la URL
  const removeScalingParams = url => {
    return url.replace(/&scaling=[^&]+/g, '').replace(/&content-scaling=[^&]+/g, '');
  };

  // Asegura que la URL tenga "embed"
  const ensureEmbed = url => {
    if (!isEmbedded) {
      url = url.replace('www.figma.com', 'embed.figma.com');
      url += '&embed-host=share';
    }
    return url;
  };

  // Ajustes dependiendo de si se usan heurísticas o no
  if (hasHeuristics) {
    url = url.replace(/&content-scaling=[^&]+/g, '');  // Eliminar "content-scaling" si es móvil
  } else {
    url = removeScalingParams(url);  // Eliminar "scaling" y "content-scaling" si es web
  }

  return ensureEmbed(url);
};

// Navega a la página para crear un cuestionario asociado a una prueba
const createQuestionary = (test) => {
  router.push({ name: 'Design_Questions', params: { testId: test.test_id } });
};

// Navega a la página para ver las respuestas de una prueba de diseño
const viewResponses = (test) => {
  router.push({ name: 'responses', params: { testId: test.test_id } });
};

// Activa el modo de edición para una prueba existente
const editDesignTest = (test) => {
  isEditing.value = true;
  editingTestId.value = test.test_id;

  // Carga los datos de la prueba en el formulario
  form.value.name = test.name;
  form.value.url = test.url;
  form.value.description = test.description;
  form.value.testType = test.test_type;
  form.value.heuristics = test.has_heuristics ? 'Con heuristicas' : 'Sin heuristicas';
  form.value.code = test.code;

  originalCode.value = test.code;  // Guarda el código original para verificar cambios
};

// Elimina una prueba de diseño después de confirmar con el usuario
const deleteDesignTest = async (test) => {
  if (!confirm('¿Estás seguro de que deseas eliminar esta prueba?')) {
    return;
  }
  try {
    await axios.delete(`http://localhost:8000/api/designtest/test_id/${test.test_id}/`);
    await refreshOwnersList();
  } catch (error) {
    console.error("Error eliminando la prueba de diseño", error);
    alert(`Error eliminando la prueba de diseño: ${error.response ? error.response.data.error : error.message}`);
  }
};

// Alterna la visibilidad del código asociado a una prueba
const toggleShowCode = (testId) => {
  showCodes.value[testId] = !showCodes.value[testId];
};

// Actualiza la lista de pruebas de diseño desde el backend
const refreshOwnersList = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/designtest/user/${authStore.userId}`);
    if (response.status === 200) {
      tests.value = response.data.length > 0 ? response.data : [];
    } else {
      console.error(`Error al obtener pruebas de diseño: ${response.status} ${response.statusText}`);
    }
  } catch (error) {
    console.error("Error obteniendo las pruebas de diseño", error);
    tests.value = [];
  }
};
</script>

<template>
  <div class="container-fluid min-vh-100 position-relative">
    <!-- Sección del formulario para añadir o editar pruebas de diseño -->
    <div class="card p-4 shadow-lg mb-5 w-100" style="max-width: none;">
      <h2 class="text-center mb-4">Gestión de prueba de diseño</h2>

      <!-- Formulario que cambia su comportamiento según si se está editando o creando una prueba -->
      <form @submit.prevent="isEditing ? handleUpdateDesignTest() : handleSaveDesignTest()">
        <div class="row">
          <!-- Campo para el nombre de la prueba -->
          <div class="col-md-6 mb-3">
            <label for="name" class="form-label">Nombre de la prueba de diseño</label>
            <input type="text" class="form-control" v-model="form.name" id="name" />
            <div class="text-danger">{{ errors.name }}</div>
          </div>

          <!-- Selector del tipo de prueba: Web o Móvil -->
          <div class="col-md-6 mb-3">
            <label for="testType" class="form-label">Tipo de Prueba</label>
            <select class="form-control" v-model="form.testType" id="testType">
              <option value="">Seleccionar tipo de prueba</option>
              <option value="Web">Web</option>
              <option value="Movil">Móvil</option>
            </select>
            <div class="text-danger">{{ errors.testType }}</div>
          </div>
        </div>

        <div class="row">
          <!-- Campo para ingresar el enlace embed de Figma -->
          <div class="col-md-6 mb-3">
            <label for="url" class="form-label">Enlace de Figma embed</label>
            <input type="text" class="form-control" v-model="form.url" id="url" />
            <div class="text-danger">{{ errors.url }}</div>
          </div>

          <!-- Selector de heurísticas: con o sin -->
          <div class="col-md-6 mb-3">
            <label for="heuristics" class="form-label">Tipo de heurísticas</label>
            <select class="form-control" v-model="form.heuristics" id="heuristics">
              <option value="">Seleccionar tipo de heurísticas</option>
              <option value="Con heuristicas">Con heurísticas</option>
              <option value="Sin heuristicas">Sin heurísticas</option>
            </select>
            <div class="text-danger">{{ errors.heuristics }}</div>
          </div>
        </div>

        <div class="row">
          <!-- Campo para la descripción de la prueba -->
          <div class="col-md-6 mb-3">
            <label for="description" class="form-label">Descripción de la prueba de diseño</label>
            <textarea class="form-control" v-model="form.description" id="description"></textarea>
            <div class="text-danger">{{ errors.description }}</div>
          </div>

          <!-- Campo para el código único de la prueba -->
          <div class="col-md-6 mb-3">
            <label for="code" class="form-label">Código</label>
            <input type="text" class="form-control" v-model="form.code" id="code" />
            <div class="text-danger">{{ errors.code }}</div>
          </div>
        </div>

        <!-- Botón que cambia su texto según si se está creando o actualizando una prueba -->
        <button type="submit" class="btn btn-primary w-100">
          {{ isEditing ? 'Actualizar prueba de diseño' : 'Añadir prueba de diseño' }}
        </button>
      </form>
    </div>

    <!-- Sección de la tabla para listar las pruebas de diseño -->
    <div class="card p-4 shadow-lg w-100">
      <h2 class="text-center mb-4">Lista de pruebas de diseño</h2>
      <table class="table table-striped text-center">
        <thead>
          <tr>
            <th scope="col" style="width: 10%;">Nombre</th>
            <th scope="col" style="width: 25%;">Descripción</th>
            <th scope="col" style="width: 15%;">Url</th>
            <th scope="col" style="width: 10%;">Tipo</th>
            <th scope="col" style="width: 10%;">Heurísticas</th>
            <th scope="col" style="width: 10%;">Código</th>
            <th scope="col" style="width: 10%;">Fecha de creación</th>
            <th scope="col" style="width: 20%;">Opciones</th>
          </tr>
        </thead>
        <tbody>
          <!-- Iteración sobre la lista de pruebas de diseño -->
          <tr v-for="test in tests" :key="test.test_id">
            <td>{{ test.name }}</td>
            <td>{{ test.description }}</td>
            <td>{{ test.url }}</td>
            <td>{{ test.test_type }}</td>
            <td>{{ test.has_heuristics ? 'Si' : 'No' }}</td>
            <td>
              <!-- Botón para mostrar u ocultar el código -->
              <button @click="toggleShowCode(test.test_id)" class="btn btn-secondary mb-2">
                {{ showCodes[test.test_id] ? 'Ocultar' : 'Mostrar' }}
              </button>
              <!-- Código de la prueba si está visible -->
              <div v-if="showCodes[test.test_id]">{{ test.code }}</div>
            </td>
            <td>{{ test.created_at }}</td>
            <td>
              <!-- Botones para crear cuestionario, ver respuestas, editar o eliminar la prueba -->
              <button @click="createQuestionary(test)" class="btn btn-primary btn-sm me-2">Cuestionario</button>
              <button @click="viewResponses(test)" class="btn btn-info btn-sm me-2">Ver Respuestas</button>
              <button @click="editDesignTest(test)" class="btn btn-warning btn-sm me-2">Editar</button>
              <button @click="deleteDesignTest(test)" class="btn btn-danger btn-sm">Eliminar</button>
            </td>
          </tr>
        </tbody>
      </table>
      <!-- Mensaje cuando no hay pruebas de diseño disponibles -->
      <div v-if="tests.length === 0" class="text-center">No hay pruebas de diseño disponibles</div>
    </div>
  </div>
</template>

<style scoped>
/* Estilo de la tarjeta que contiene el formulario y la tabla */
.card {
  border-radius: 12px;
  background: linear-gradient(145deg, rgba(240, 248, 255, 1), rgba(230, 240, 255, 1));  /* Degradado sutil */
}
h2 {
  font-size: 1.5rem;
  font-weight: bold;
}

button {
  border-radius: 12px;
}

/* El textarea no se puede redimensionar */
textarea {
  resize: none;
}
</style>

