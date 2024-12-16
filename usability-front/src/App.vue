<script setup>
// import { RouterLink, RouterView } from 'vue-router'
import NavbarComponent from './components/NavbarComponent.vue';

</script>

<template>

  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">

  <NavbarComponent />
  
  <!-- Fondo con blobs -->
  <main class="main-container">
    <RouterView />
  </main>
</template>

