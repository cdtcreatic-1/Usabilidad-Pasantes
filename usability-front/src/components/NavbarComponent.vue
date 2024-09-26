<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary" style="background-color: transparent;">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      
      <!-- Logo Section -->
      <a class="navbar-brand d-flex align-items-center" href="/">
        <img src="/src/assets/lading/imagen2.png" alt="Logo Creatic" class="me-2" style="height: 60px;" />
      </a>

      <!-- Center Links Section -->
      <div class="collapse navbar-collapse justify-content-center" id="navbarNav">
        <ul class="navbar-nav rounded-pill" style="background-color: white; padding: 0.5rem 1rem;">
          <li class="nav-item me-3">
            <RouterLink class="nav-link text-dark" to="/">
              <i class="bi bi-house-fill" style="font-size: 1.5rem;"></i>
            </RouterLink>
          </li>
          <li class="nav-item me-3">
            <RouterLink class="nav-link text-dark" to="/pruebasheuristicas">Pruebas heurísticas</RouterLink>
          </li>
          <li class="nav-item me-3">
            <a @click="handleDesignTestNavigation" class="nav-link">Pruebas de Diseño</a>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link text-dark" to="/contacto">Contacto</RouterLink>
          </li>
        </ul>
      </div>

      <!-- Condicional para mostrar los botones -->
      <div class="d-flex">
        <!-- Si el usuario NO está logueado, mostrar botones de Registrarse e Iniciar Sesión -->
        <template v-if="!isUserLoggedIn">
          <RouterLink class="btn btn-outline-secondary me-2 rounded-pill" to="/register">
            Registrarse
          </RouterLink>
          <RouterLink class="btn btn-primary rounded-pill" to="/login" style="background: linear-gradient(90deg, rgba(96, 95, 255, 1) 0%, rgba(34, 193, 195, 1) 100%);">
            Iniciar sesión
          </RouterLink>
        </template>
        <!-- Si el usuario está logueado, mostrar botón de Cerrar Sesión -->
        <template v-else>
          <button class="btn btn-danger rounded-pill" @click="handleLogout">
            Cerrar sesión
          </button>
        </template>
      </div>

    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'; // Para crear una propiedad computada
import { useAuthStore } from '../stores/useAuthStore';
import { useRouter } from 'vue-router';

const router = useRouter();
const useAuth = useAuthStore();

// Computamos el valor de isLoggedIn para asegurar que sea reactivo
const isUserLoggedIn = computed(() => useAuth.isLoggedIn);

// Función para manejar la navegación según el rol
const handleDesignTestNavigation = () => {
  if (useAuth.role === 'Propietario') {
    router.push('/designtest');
  } else if (useAuth.role === 'Evaluador') {
    router.push('/designtests/access');
  } else {
    alert('No tienes acceso a esta sección');
  }
};

// Función para cerrar sesión
const handleLogout = () => {
  useAuth.logout();
  router.push('/');
};
</script>

<style scoped>
.navbar {
  background-color: transparent; /* Fondo transparente para el navbar */
}

.nav-link {
  font-size: 1rem;
  font-weight: 500;
  color: #111111; /* Color del texto */
}

.nav-link:hover {
  color: #277959; /* Color del texto al pasar el mouse */
}

.btn-outline-secondary {
  color: #555;
  border-color: #ddd;
}

.btn-outline-secondary:hover {
  color: white;
  background-color: #ddd;
}

.btn-primary {
  border: none;
}

.btn-primary:hover {
  background-color: #2575fc; /* On hover, keep one color */
}

.btn-danger {
  background-color: #dc3545;
  border: none;
}

.btn-danger:hover {
  background-color: #c82333;
}
</style>
