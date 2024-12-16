<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/useAuthStore';

// Formulario de inicio de sesión
const form = ref({
  username: '',
  password: ''
});

// Objeto para almacenar los errores de validación
const errors = ref({
  username: '',
  password: ''
});

// Inicializa el authStore y el router
const useAuth = useAuthStore();
const router = useRouter();

const handleLogin = async () => {
  // Reiniciar los errores antes de validar
  errors.value = {};

  if (!form.value.username) {
    errors.value.username = 'El nombre de usuario es obligatorio.';
  }

  if (!form.value.password) {
    errors.value.password = 'La contraseña es obligatoria.';
  }

  // Si hay errores, detener el inicio de sesión
  if (Object.values(errors.value).some(error => error !== '')) {
    return;
  }

  try {
    // Enviar la solicitud de inicio de sesión al backend
    const response = await axios.post('http://localhost:8000/api/login/', {
      username: form.value.username,
      password: form.value.password
    });

    // Verifica si la respuesta tiene datos del usuario
    if (response.data && response.data.rol) {
      const { id, username, email, rol, experience } = response.data;

      // Iniciar sesión en el authStore con userId, username, email, rol y experience
      useAuth.login(id, username, email, rol, experience);

      // Redirigir según el rol
      if (rol === 'Propietario') {
        router.push('/designtest');
      } else if (rol === 'Evaluador') {
        router.push('/designtests/access');
      } else {
        router.push('/'); // Redirigir a la página de inicio para cualquier otro rol
      }
    } else {
      throw new Error('Datos de usuario no encontrados en la respuesta');
    }
  } catch (error) {
    // Manejo de errores del backend
    if (error.response && error.response.data) {
      errors.value = error.response.data.errors || {};
    } else {
      console.error(error.message || 'Error desconocido');
    }
  }
};
</script>

<template>
  <div class="container-fluid min-vh-100 d-flex align-items-center justify-content-center position-relative bg-light">
    <!-- Blobs Difuminados -->
    <div class="blob1 position-absolute"></div>
    <div class="blob2 position-absolute"></div>

    <!-- Contenedor del contenido -->
    <div class="row bg-white shadow-lg rounded p-5 position-relative" style="max-width: 1200px; width: 100%; z-index: 10;">
      <!-- Imagen -->
      <div class="col-md-6 d-flex justify-content-center align-items-center">
        <img src="/src/assets/images/imagen1.svg" alt="Illustration" class="img-fluid" style="max-width: 400px;" />
      </div>

      <!-- Formulario -->
      <div class="col-md-6 d-flex flex-column justify-content-center">
        <h2 class="text-center mb-4" style="font-size: 2rem;">Inicio de sesión</h2>
        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label for="username" class="form-label">Nombre de usuario</label>
            <input type="text" class="form-control form-control-lg" v-model="form.username" id="username" />
            <div class="text-danger">{{ errors.username }}</div>
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Contraseña</label>
            <input type="password" class="form-control form-control-lg" v-model="form.password" id="password" />
            <div class="text-danger">{{ errors.password }}</div>
          </div>
          <button type="submit" class="btn btn-primary btn-lg w-100">Iniciar sesión</button>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
body {
  font-family: 'Roboto', sans-serif;
}
.container-fluid {
  background-color: #f8f9fa;
}
.shadow-lg {
  box-shadow: 0 1rem 3rem rgba(0, 0, 0, 0.175);
}
.img-fluid {
  max-width: 100%;
  height: auto;
}

/* Estilos para los blobs */
.blob1 {
  top: -100px;
  left: -150px;
  width: 500px;
  height: 500px;
  background: rgba(0, 170, 255, 0.4);
  border-radius: 50%;
  filter: blur(100px);
}

.blob2 {
  bottom: -100px;
  right: -150px;
  width: 400px;
  height: 400px;
  background: rgba(100, 100, 255, 0.5);
  border-radius: 50%;
  filter: blur(100px);
}

.blob1, .blob2 {
  position: absolute;
  z-index: 0;
}

</style>
