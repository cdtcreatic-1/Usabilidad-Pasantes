<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

// Objeto que almacena los datos del formulario de registro
const form = ref({
  username: '',
  email: '',
  password: '',
  rol: '',
  experience: ''
});

// Objeto que contiene los posibles errores de validación
const errors = ref({
  username: '',
  email: '',     
  password: '',  
  rol: '',       
  experience: '' 
});

const router = useRouter(); // Para redirigir al usuario tras un registro exitoso

/**
 * Maneja el registro del usuario.
 * - Valida los campos del formulario.
 * - Envía la solicitud de registro al backend.
 * - Redirige al usuario a la pantalla de inicio de sesión tras un registro exitoso.
 */
const handleRegister = async () => {
  // Reinicia los errores antes de validar
  errors.value = {};

  // Validación de los campos del formulario
  if (!form.value.username) errors.value.username = 'El nombre de usuario es obligatorio.';
  if (!form.value.email) errors.value.email = 'El correo electrónico es obligatorio.';
  if (!form.value.password) errors.value.password = 'La contraseña es obligatoria.';
  if (!form.value.rol) errors.value.rol = 'El rol es obligatorio.';

  // Validación específica para evaluadores: se requiere experiencia
  if (form.value.rol === 'Evaluador' && !form.value.experience) {
    errors.value.experience = 'Debe seleccionar una experiencia.';
  }

  // Si hay errores, detener el proceso de registro
  if (Object.values(errors.value).some(error => error !== '')) return;

  try {
    // Enviar la solicitud de registro al backend con los datos del formulario
    const response = await axios.post('http://localhost:8000/api/users/', {
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      rol: form.value.rol,
      experience: form.value.experience // Este campo solo se envía si el rol es "Evaluador"
    });

    console.log('Usuario registrado:', response.data);
    router.push('/login'); // Redirige al usuario a la pantalla de inicio de sesión tras el registro
  } catch (error) {
    // Manejo de errores de la solicitud al backend
    if (error.response && error.response.data) {
      errors.value = error.response.data.errors || {}; // Asigna los errores enviados por el backend
    } else {
      console.error(error); // Error general de red u otro tipo
    }
  }
};
</script>

<template>
  <div class="register-container container mt-5">
    <div class="form-wrapper">
      <h1 class="text-center mb-4 text-primary">Registro de Usuario</h1>
      <!-- Formulario de registro -->
      <form @submit.prevent="handleRegister">
        
        <!-- Campo para el nombre de usuario -->
        <div class="mb-3">
          <label for="username" class="form-label">Nombre de Usuario</label>
          <input type="text" v-model="form.username" id="username" class="form-control" />
          <span class="text-danger">{{ errors.username }}</span>
        </div>
        
        <!-- Campo para el correo electrónico -->
        <div class="mb-3">
          <label for="email" class="form-label">Correo Electrónico</label>
          <input type="email" v-model="form.email" id="email" class="form-control" />
          <span class="text-danger">{{ errors.email }}</span>
        </div>
        
        <!-- Campo para la contraseña -->
        <div class="mb-3">
          <label for="password" class="form-label">Contraseña</label>
          <input type="password" v-model="form.password" id="password" class="form-control" />
          <span class="text-danger">{{ errors.password }}</span>
        </div>
        
        <!-- Campo para seleccionar el rol del usuario -->
        <div class="mb-3">
          <label for="rol" class="form-label">Rol</label>
          <select v-model="form.rol" class="form-select">
            <option value="" disabled>Selecciona un rol</option>
            <option value="Administrador">Administrador</option>
            <option value="Propietario">Propietario</option>
            <option value="Evaluador">Evaluador</option>
          </select>
          <span class="text-danger">{{ errors.rol }}</span>
        </div>
        
        <!-- Campo para seleccionar la experiencia (solo para el rol de Evaluador) -->
        <div v-if="form.rol === 'Evaluador'" class="mb-3">
          <label for="experience" class="form-label">Experiencia</label>
          <select v-model="form.experience" class="form-select">
            <option value="" disabled>Selecciona tu experiencia</option>
            <option value="Novato">Novato</option>
            <option value="Experto">Experto</option>
          </select>
          <span class="text-danger">{{ errors.experience }}</span>
        </div>
        
        <!-- Botón para enviar el formulario de registro -->
        <div class="d-grid">
          <button type="submit" class="btn btn-primary btn-lg">Registrar</button>
        </div>
      </form>
    </div>
    
    <!-- Sección de imagen decorativa -->
    <div class="image-wrapper">
      <img src="/src/assets/rocket.svg" alt="Cohete" class="rocket-image" />
    </div>
  </div>
</template>

<style scoped>
/* Estilos del contenedor de registro */
.register-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 900px;
  margin: auto;
  position: relative;
}

.register-container::before {
  width: 300px;
  height: 300px;
  background: rgba(47, 0, 132, 0.2);
  top: -50px;
  left: -150px;
}

.register-container::after {
  width: 400px;
  height: 400px;
  background: rgba(0, 222, 151, 0.2);
  bottom: -100px;
  right: -200px;
}

/* Estilos de la tarjeta de registro */
.card {
  width: 50%;
  border-radius: 15px;
  background-color: #f8f9fa;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  position: relative;
  z-index: 1;
  padding: 40px;
}

/* Estilos de la imagen */
.rocket-container {
  width: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.rocket-container img {
  width: 100%;
  height: auto;
  max-width: 100px;
}

/* Estilos de los encabezados */
h1 {
  color: #2F0084; /* Persian Indigo */
  font-family: 'Roboto', sans-serif;
}

/* Estilos del botón de registro */
.btn-primary {
  background-color: #00DE97;
  border-color: #00DE97;
}

.btn-primary:hover {
  background-color: #00c085;
}

/* Estilos de las etiquetas del formulario */
.form-label {
  font-family: 'Lato', sans-serif;
}

/* Estilos de los inputs y selects */
input, select {
  font-family: 'Lato', sans-serif;
}
</style>
