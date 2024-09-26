<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/useAuthStore';

const router = useRouter();
const code = ref('');  // El código de la prueba de diseño
const designTests = ref([]);  // Lista de pruebas de diseño disponibles para el evaluador
const authStore = useAuthStore();  // Usamos el authStore para el rol y la autenticación
const rol = ref('');  // Guardamos el rol del usuario
const evaluatorId = ref(authStore.userId);  // Obtenemos el ID del evaluador desde el authStore

// Verificar si el rol es "Evaluador"
onMounted(() => {
  rol.value = authStore.role;

  // Si es Evaluador, cargar las pruebas de diseño
  if (rol.value === 'Evaluador') {
    loadDesignTests();
  } else {
    console.log('No autorizado: Solo los evaluadores pueden acceder a esta página.');
  }
});

// Verifica el código de acceso y carga la prueba correspondiente
const checkDesignTestCode = async () => {
  try {
    const response = await axios.post(`http://localhost:8000/api/designtests/access/${evaluatorId.value}/`, {
      code: code.value
    });

    if (response.status === 200 || response.status === 201) {
      const newTest = response.data;

      // Verifica si la prueba está marcada como oculta
      if (newTest.is_hidden) {
        await axios.post(`http://localhost:8000/api/designtests/access/${newTest.test_id}/show/`, {
          evaluator_id: evaluatorId.value
        });
        newTest.is_hidden = false;
      }

      // Pausa antes de agregar la prueba a la lista
      setTimeout(() => {
        const exists = designTests.value.some(test => test.test_id === newTest.test_id);

        if (!exists) {
          console.log('Nuevo test:', newTest); // Asegúrate de que has_heuristics sea correcto aquí
          newTest.heuristicsText = newTest.has_heuristics ? 'Con heurísticas' : 'Sin heurísticas';
          designTests.value.push(newTest);

          // Recargar las pruebas de diseño para asegurarnos de que están sincronizadas
          loadDesignTests();
        } else {
          alert('Esta prueba de diseño ya está en la lista.');
        }
      }, 500);  // Pausa de medio segundo para una carga correcta
    } else {
      alert('Código no válido o prueba de diseño no encontrada.');
    }
  } catch (error) {
    console.error('Error:', error);
    alert('Ocurrió un error al verificar el código.');
  }
};


// Cargar todas las pruebas de diseño accesibles para el evaluador
const loadDesignTests = async () => {
  try {
    const response = await axios.get(`http://localhost:8000/api/designtests/access/${evaluatorId.value}/`);
    if (response.status === 200) {
      console.log('API response:', response.data);
      designTests.value = response.data.filter(test => !test.is_hidden);
    }
  } catch (error) {
    console.error('Error al cargar las pruebas de diseño:', error);
  }
};


// Oculta el acceso a la prueba de diseño para el evaluador
const hideDesignTestAccess = async (testId) => {
  try {
    await axios.post(`http://localhost:8000/api/designtests/access/${testId}/hide/`, {
      evaluator_id: evaluatorId.value
    });
    alert('Acceso a la prueba de diseño ocultado exitosamente');
    setTimeout(() => {
      loadDesignTests(); // Recargar las pruebas disponibles después de ocultar
    }, 500);
  } catch (error) {
    console.error('Error al ocultar el acceso a la prueba de diseño:', error);
    alert('Ocurrió un error al ocultar el acceso a la prueba de diseño.');
  }
}

// Redirige a los cuestionarios de la prueba de diseño
const goToQuestionnaires = (testId, hasHeuristics) => {
  if (hasHeuristics) {
    // Redirigir a la ruta de respuestas con heurísticas
    router.push(`/questionnaires/${testId}/heuristicresponses`);
  } else {
    // Redirigir a la ruta de respuestas estándar
    router.push(`/questionnaires/${testId}/standardresponses`);
  }
};
</script>

<template>
  <div>
    <div class="card m-3">
      <!-- Sección visible solo si el usuario tiene el rol de "Evaluador" -->
      <div v-if="rol === 'Evaluador'">
        <h1 class="text-center mt-3">Pruebas de Diseño</h1>
        
        <!-- Formulario para ingresar y verificar el código de una prueba de diseño -->
        <div class="card-body">
          <form @submit.prevent="checkDesignTestCode" class="mb-4">
            <div class="input-group mb-3">
              <input v-model="code" type="text" class="form-control" placeholder="Ingrese el código de la prueba de diseño" />
              <button class="btn btn-primary" type="submit">Verificar Código</button>
            </div>
          </form>
        </div>

        <!-- Tabla que lista las pruebas de diseño accesibles para el evaluador -->
        <div class="card mt-3">
          <div class="card-body">
            <!-- Tabla de pruebas de diseño, solo se muestra si hay pruebas disponibles -->
            <table class="table table-primary table-striped-columns" v-if="designTests.length > 0">
              <thead>
                <tr style="text-align: center;">
                  <th scope="col">Nombre</th>
                  <th scope="col">Descripción</th>
                  <th scope="col">URL</th>
                  <th scope="col">Tipo</th>
                  <th scope="col">Heurísticas</th>
                  <th scope="col">Fecha de acceso</th>
                  <th scope="col">Acciones</th>
                </tr>
              </thead>
              <tbody>
                <!-- Iteración sobre la lista de pruebas de diseño -->
                <tr v-for="test in designTests" :key="test.test_id" style="text-align: center;">
                  <td>{{ test.name }}</td>
                  <td style="max-width: 200px; min-width: 100px;">{{ test.description }}</td>
                  <td style="max-width: 300px; min-width: 300px;">{{ test.url }}</td>
                  <td>{{ test.test_type }}</td>
                  <td>{{ test.has_heuristics ? 'Con heurísticas' : 'Sin heurísticas' }}</td>
                  <td>{{ test.created_at }}</td>
                  <td>
                    <!-- Botón para responder cuestionarios, deshabilitado si la prueba ya está completa -->
                    <button @click="goToQuestionnaires(test.test_id, test.has_heuristics)" class="btn btn-secondary" :disabled="test.is_complete">
                      Responder Cuestionarios
                    </button>
                    <!-- Botón para ocultar el acceso a la prueba de diseño -->
                    <button @click="hideDesignTestAccess(test.test_id)" class="btn btn-danger ms-2">Ocultar</button>
                  </td>
                </tr>
              </tbody>
            </table>
            <!-- Mensaje si no hay pruebas de diseño disponibles -->
            <div v-else>No hay pruebas de diseño para mostrar</div>
          </div>
        </div>
      </div>

      <!-- Mensaje de acceso denegado si el usuario no es "Evaluador" -->
      <div v-else>
        <p class="text-danger text-center fs-1">Acceso denegado. Esta página es solo para evaluadores.</p>
      </div>
    </div>
  </div>
</template>


<style scoped>
.table-responsive {
  margin-top: 20px;
}
</style>
