<script setup>
import { RouterView, useRoute } from 'vue-router'
import { onMounted, ref, watch } from 'vue'
import { isLoggedIn, currentUsername, authReady, transitionName } from './auth.js'
import { API } from './config.js'
const route = useRoute()

function getDepth(path) {
  if (path.match(/^\/recipes\/[^/]+\/edit$/)) return 3
  if (path === '/recipes/new') return 2
  if (path.match(/^\/recipes\/[^/]+$/)) return 2
  if (path === '/login' || path === '/register') return 0
  return 1
}

watch(() => route.path, (to, from) => {
  const toDepth = getDepth(to)
  const fromDepth = getDepth(from)
  if (toDepth > fromDepth) transitionName.value = 'page-forward'
  else if (toDepth < fromDepth) transitionName.value = 'page-back'
  else transitionName.value = 'fade'
})

onMounted(async () => {
  try {
    const response = await fetch(`${API}/auth/me`, {
      credentials: "include"
    })
    if (response.ok) {
      const data = await response.json()
      isLoggedIn.value = true
      currentUsername.value = data.username
    } else {
      isLoggedIn.value = false
    }
  } catch (err) {
    isLoggedIn.value = false
  } finally {
    authReady.value = true
  }
})
</script>

<template>
  <div v-if="!authReady" class="auth-loading"></div>
  <div v-else class="router-wrapper">
    <RouterView v-slot=" {Component}">
      <Transition :name="transitionName">
        <component :is="Component" :key="$route.path"/>
      </Transition>
    </RouterView>
  </div>
</template>

<style>
.router-wrapper {
    position: relative;
    min-height: 100vh;
    overflow: hidden;
}
.auth-loading {
    min-height: 100vh;
    background-color: var(--bg-primary);
}

.page-forward-enter-from { opacity: 0; transform: translateY(20px) scale(0.985); }
.page-forward-enter-active { transition: opacity 0.35s ease, transform 0.35s ease; }
.page-forward-leave-to { opacity: 0; transform: translateY(-10px) scale(1.01); }
.page-forward-leave-active { transition: opacity 0.22s ease, transform 0.22s ease; }


.page-back-enter-from { opacity: 0; transform: translateY(-10px) scale(1.01); }
.page-back-enter-active { transition: opacity 0.35s ease, transform 0.35s ease; }
.page-back-leave-to { opacity: 0; transform: translateY(20px) scale(0.985); }
.page-back-leave-active { transition: opacity 0.22s ease, transform 0.22s ease; }

.fade-enter-from, .fade-leave-to { opacity: 0; }
.fade-enter-active, .fade-leave-active { transition: opacity 0.28s ease; }
</style>