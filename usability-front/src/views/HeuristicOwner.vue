<template>
  <h3>Crea tu prueba de análisis heurístico</h3>
  <div class="container">
    <div class="row">
      <!-- Formulario para el administrador -->
      <div class="col-sm-6" v-if="rol === 'administrator'">
        <form @submit.prevent="handleSaveHTest">
          <div class="mb-3">
            <label for="name" class="form-label">Nombre de la prueba</label>
            <input type="text" class="form-control" v-model="form.name" id="name" aria-describedby="nameHelp" />
            <div id="nameHelp" class="form-text">Ingrese el nombre de la prueba.</div>
            <div class="text-danger">{{ errors.name }}</div>
          </div>
          <div class="mb-3">
            <label for="url" class="form-label">URL</label>
            <input type="text" class="form-control" v-model="form.url" id="url" aria-describedby="urlHelp" />
            <div id="urlHelp" class="form-text">Ingrese la URL de la prueba.</div>
            <div class="text-danger">{{ errors.url }}</div>
          </div>
          <div class="mb-3">
            <label for="description" class="form-label">Descripción</label>
            <textarea
              class="form-control"
              v-model="form.description"
              id="description"
              aria-describedby="descriptionHelp"
            ></textarea>
            <div id="descriptionHelp" class="form-text">Ingrese una descripción para la prueba.</div>
            <div class="text-danger">{{ errors.description }}</div>
          </div>
          <button type="submit" class="btn btn-primary">Añadir Prueba</button>
        </form>
      </div>

      <!-- Formulario para el evaluador -->
      <div class="col-sm-6" v-if="rol === 'evaluator'">
        <form @submit.prevent="handleSaveEvaluadorTest">
          <h1>Información del usuario Evaluador</h1>
          <div class="mb-3">
            <label for="age" class="form-label">Edad</label>
            <input type="number" class="form-control" v-model="evaluadorForm.age" id="age" />
          </div>
          <div class="mb-3">
            <label for="profession" class="form-label">Profesión</label>
            <input type="text" class="form-control" v-model="evaluadorForm.profession" id="profession" />
          </div>
          <div class="mb-3">
            <label for="status" class="form-label">Estatus</label>
            <input type="text" class="form-control" v-model="evaluadorForm.status" id="status" />
          </div>
          <div class="mb-3">
            <label for="technologyExperience" class="form-label">Experiencia tecnológica</label>
            <input
              type="text"
              class="form-control"
              v-model="evaluadorForm.technological_experience"
              id="technologyExperience"
            />
          </div>
          <div class="mb-3">
            <label for="description">Descripción/personalidad</label>
            <textarea class="form-control" v-model="evaluadorForm.personality_description" id="description"></textarea>
          </div>
          <div class="mb-3">
            <label for="objectives">Objetivos</label>
            <textarea class="form-control" v-model="evaluadorForm.goals" id="objectives"></textarea>
          </div>
          <div class="mb-3">
            <label for="habits">Hábitos, habilidades y frustraciones</label>
            <textarea class="form-control" v-model="evaluadorForm.habits" id="habits"></textarea>
          </div>
          <button type="submit" class="btn btn-primary">Guardar</button>
        </form>
      </div>

      <!-- Tabla de pruebas -->
      <div class="col-sm-12">
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
                <button
                  @click="copylink(owner)"
                  class="btn btn-primary"
                  v-if="rol === 'evaluator' || rol === 'administrator'"
                >
                  Ir a Encuesta
                </button>
                <button @click="goToEvaluate(owner.id)" class="btn btn-success" v-if="rol === 'owner' || rol === 'administrator'">
                  Evaluar
                </button>
                <button @click="goToEvaluationResults(owner.id)" class="btn btn-warning" v-if="rol === 'owner' || rol === 'administrator'">
                  Resultados
                </button>
                <button
                  @click="handleDeleteHTest(owner.id)"
                  class="btn btn-danger"
                  v-if="rol === 'administrator'"
                >
                  Eliminar
                </button>
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
const authStore = useAuthStore();
const router = useRouter();
const username = ref(localStorage.getItem('username'));
const rol = ref(authStore.role);

// Formulario del administrador
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

// Formulario del evaluador
const evaluadorForm = ref({
  username: username.value,
  age: '',
  profession: '',
  status: '',
  technological_experience: '',
  personality_description: '',
  goals: '',
  habits: '',
});

// Lista de propietarios
const owners = ref([]);

// Métodos
const handleSaveHTest = async () => {
  errors.value = {}; // Reinicia errores

  if (!form.value.name) errors.value.name = 'El nombre de la prueba es obligatorio.';
  if (!form.value.url) errors.value.url = 'La URL es obligatoria.';
  if (!form.value.description) errors.value.description = 'La descripción es obligatoria.';

  if (Object.values(errors.value).some(error => error)) return;

  try {
    await axios.post('http://127.0.0.1:8000/api/owners', form.value);
    await refreshOwnersList();
  } catch (error) {
    console.error('Error al guardar:', error);
  }
};

const handleSaveEvaluadorTest = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/api/evaluator_info', evaluadorForm.value);
  } catch (error) {
    console.error('Error al guardar información del evaluador:', error);
  }
};

const handleDeleteHTest = async id => {
  try {
    await axios.delete(`http://127.0.0.1:8000/api/owners/${id}`);
    await refreshOwnersList();
  } catch (error) {
    console.error('Error al eliminar:', error);
  }
};

const copylink = owner => {
  router.push(`/o/${owner.id}/checklist`);
};

const goToEvaluate = ownerId => {
  router.push(`/o/${ownerId}/evaluacion`);
};

const goToEvaluationResults = ownerId => {
  router.push(`/o/${ownerId}/resultadoevaluacion`);
};

const refreshOwnersList = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/owners');
    owners.value = response.data;
  } catch (error) {
    console.error('Error al obtener la lista de propietarios:', error);
  }
};

// Inicialización
onMounted(() => {
  refreshOwnersList();
});
</script>

<style>
.container {
  margin-top: 20px;
}
</style>
