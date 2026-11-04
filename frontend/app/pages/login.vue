<!-- frontend/app/pages/login.vue -->
<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>Welcome Back</h2>
      <p class="subtitle">Log in to manage your orders and account.</p>

      <div v-if="errorMsg" class="error-banner">
        {{ errorMsg }}
      </div>

      <form @submit.prevent="handleLogin" class="auth-form">
        <div class="form-group">
          <label for="username">Username or Email</label>
          <input id="username" v-model="form.username_or_email" type="text" required
            placeholder="e.g. customer or user@example.com" />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input id="password" v-model="form.password" type="password" required placeholder="••••••••" />
        </div>

        <button type="submit" class="submit-btn" :disabled="isSubmitting">
          {{ isSubmitting ? 'Signing in...' : 'Sign In' }}
        </button>
      </form>

      <p class="switch-link">
        Don't have an account? <NuxtLink to="/register">Create one</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'guest'
})

const { login, user, isAdmin } = useAuthState()

if (user.value) {
  navigateTo(user.value.is_staff ? '/admin' : '/')
}

const form = reactive({
  username_or_email: '',
  password: ''
})

const errorMsg = ref('')
const isSubmitting = ref(false)

async function handleLogin() {
  errorMsg.value = ''
  isSubmitting.value = true

  try {
    await login(form)
    const destination = user.value?.is_staff ? '/admin' : '/'
    await navigateTo(destination)
  } catch (err) {
    if (err.data && typeof err.data === 'object') {
      const messages = Object.values(err.data).flat()
      errorMsg.value = messages.join(' ')
    } else {
      errorMsg.value = err.message || 'Login failed. Please check your credentials.'
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
}

.auth-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 2.5rem;
  max-width: 440px;
  width: 100%;
  box-shadow: var(--shadow-md);
}

h2 {
  font-size: 1.5rem;
  font-weight: 700;
  margin-bottom: 0.25rem;
}

.subtitle {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-bottom: 1.5rem;
}

.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
  padding: 0.75rem;
  border-radius: var(--radius-md);
  font-size: 0.85rem;
  margin-bottom: 1.25rem;
}

.auth-form {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  text-align: left;
}

label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-main);
}

input {
  border: 1px solid var(--border-color);
  padding: 0.75rem 0.85rem;
  border-radius: var(--radius-sm);
  font-size: 0.9rem;
  outline: none;
  transition: border-color 0.15s;
}

input:focus {
  border-color: var(--primary);
}

.submit-btn {
  background: var(--primary);
  color: #fff;
  font-weight: 600;
  padding: 0.8rem;
  border-radius: var(--radius-md);
  margin-top: 0.5rem;
  transition: background 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: var(--primary-hover);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.switch-link {
  margin-top: 1.5rem;
  font-size: 0.85rem;
  color: var(--text-muted);
  text-align: center;
}

.switch-link a {
  color: var(--primary);
  font-weight: 600;
}
</style>
