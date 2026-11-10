<!-- frontend/app/pages/register.vue -->
<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>Create an Account</h2>
      <p class="subtitle">Join KyroKart to place orders and track delivery.</p>

      <div v-if="errorMsg" class="error-banner">
        {{ errorMsg }}
      </div>

      <form @submit.prevent="handleRegister" class="auth-form">
        <div class="form-group">
          <label for="reg-username">Username</label>
          <input
            id="reg-username"
            v-model="form.username"
            type="text"
            required
            placeholder="Choose a username"
          />
        </div>

        <div class="form-group">
          <label for="reg-email">Email Address</label>
          <input
            id="reg-email"
            v-model="form.email"
            type="email"
            required
            placeholder="you@example.com"
          />
        </div>

        <div class="form-group">
          <label for="reg-password">Password (min 8 chars)</label>
          <input
            id="reg-password"
            v-model="form.password"
            type="password"
            required
            minlength="8"
            placeholder="••••••••"
          />
        </div>

        <div class="form-group">
          <label for="reg-confirm">Confirm Password</label>
          <input
            id="reg-confirm"
            v-model="form.confirm_password"
            type="password"
            required
            minlength="8"
            placeholder="••••••••"
          />
        </div>

        <button type="submit" class="submit-btn" :disabled="isSubmitting">
          {{ isSubmitting ? 'Creating account...' : 'Create Account' }}
        </button>
      </form>

      <p class="switch-link">
        Already have an account? <NuxtLink to="/login">Sign In</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: 'guest'
})

const { register, user } = useAuthState()

if (user.value) {
  navigateTo('/')
}

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirm_password: ''
})

const errorMsg = ref('')
const isSubmitting = ref(false)

async function handleRegister() {
  errorMsg.value = ''

  if (form.password !== form.confirm_password) {
    errorMsg.value = 'Passwords do not match.'
    return
  }

  isSubmitting.value = true

  try {
    await register(form)
    await navigateTo('/')
  } catch (err) {
    if (err.data && typeof err.data === 'object') {
      const messages = Object.values(err.data).flat()
      errorMsg.value = messages.join(' ')
    } else {
      errorMsg.value = err.message || 'Registration failed.'
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
  gap: 1.15rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
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
