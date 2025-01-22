<template>
  <h3>Crea tu prueba de análisis heurístico</h3>
  <div class="container">
    <div class="row">
      <div class="col-sm-6">
        <form @submit.prevent="handleSaveHTest">
          <div class="mb-3">
            <label for="name" class="form-label">Nombre de la prueba</label>
            <input type="text" class="form-control" v-model="form.name" id="name" aria-describedby="nameHelp">
            <div id="nameHelp" class="form-text">Ingrese el nombre de la prueba.</div>
            <div class="text-danger">{{ errors.name }}</div>
          </div>
          <div class="mb-3">
            <label for="url" class="form-label">URL</label>
            <input type="text" class="form-control" v-model="form.url" id="url" aria-describedby="urlHelp">
            <div id="urlHelp" class="form-text">Ingrese la URL de la prueba.</div>
            <div class="text-danger">{{ errors.url }}</div>
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Descripción</label>
            <input type="text" class="form-control" v-model="form.description" id="description"
              aria-describedby="descriptionHelp">
            <div id="descriptionHelp" class="form-text">Ingrese una descripción para la prueba.</div>
            <div class="text-danger">{{ errors.description }}</div>
          </div>

          <button type="submit" class="btn btn-primary">Añadir Prueba</button>
        </form>
      </div>
      <div class="col-sm-6">
        <table class="table table-primary table-striped-columns">
          <thead>
            <tr>
              <th scope="col">Nombre</th>
              <th scope="col">URL</th>
              <th scope="col">Descripción</th>
              <th scope="col">Opciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="owner in owners" :key="owner.id">
              <td>{{ owner.name }}</td>
              <td>{{ owner.url }}</td>
              <td>{{ owner.description }}</td>
              <td>
                <!-- Botones visibles para depuración -->
                <button @click="copylink(owner)" class="btn btn-primary">Ir a Encuesta</button>
                <button @click="goToEvaluate(owner.id)" class="btn btn-success">Evaluar</button>
                <button @click="goToEvaluationResults(owner.id)" class="btn btn-warning">Resultados</button>
                <button @click="handleDeleteHTest(owner.id)" class="btn btn-danger">Eliminar</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/useAuthStore';

// Variables y referencias
const rol = ref('');
const authStore = useAuthStore();
const router = useRouter();
const form = ref({
  name: '',
  url: '',
  description: '',
});
const errors = ref({
  name: '',
  url: '',
  description: '',
});
const owners = ref([]);

// Métodos
const handleSaveHTest = async () => {
  errors.value = {}; // Reinicia errores

  // Validación del formulario
  if (!form.value.name) errors.value.name = 'El nombre de la prueba es obligatorio.';
  if (!form.value.url) errors.value.url = 'La URL es obligatoria.';
  if (!form.value.description) errors.value.description = 'La descripción es obligatoria.';

  // Si hay errores, no enviamos la solicitud
  if (Object.values(errors.value).some(error => error)) return;

  try {
    // Solicitud POST a la API para agregar la prueba
    const response = await axios.post('http://127.0.0.1:8000/api/owners', form.value);
    await refreshOwnersList();
    // Limpiar formulario después de agregar
    form.value = { name: '', url: '', description: '' };
    console.log('Prueba añadida:', response.data);
  } catch (error) {
    console.error('Error al guardar:', error.response?.data || error);
  }
};

const handleDeleteHTest = async (id) => {
  try {
    // Solicitud DELETE para eliminar la prueba
    await axios.delete(`http://127.0.0.1:8000/api/owners/${id}`);
    await refreshOwnersList();
  } catch (error) {
    console.error('Error al eliminar:', error.response?.data || error);
  }
};

const copylink = (owner) => {
  const url = `/o/${owner.id}/checklist`;
  router.push(url);
};

const goToEvaluate = (ownerId) => {
  router.push(`/o/${ownerId}/evaluacion`);
};

const goToEvaluationResults = (ownerId) => {
  router.push(`/o/${ownerId}/resultadoevaluacion`);
};

const refreshOwnersList = async () => {
  try {
    // Solicitud GET para obtener la lista de pruebas
    const response = await axios.get('http://127.0.0.1:8000/api/owners');
    owners.value = Array.isArray(response.data) ? response.data : [];
  } catch (error) {
    console.error('Error al obtener la lista de propietarios:', error.response?.data || error);
  }
};

// Montaje inicial
onMounted(async () => {
  rol.value = authStore.role;
  console.log('Rol del usuario:', rol.value);
  await refreshOwnersList();
});
</script>
