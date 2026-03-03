<template>
  <div class="auth-page">
    <div class="card auth-card shadow-lg border-0">
      <div class="card-body p-5">
        <div class="text-center mb-4">
          <i class="bi bi-shield-lock text-primary" style="font-size: 3rem;"></i>
          <h2 class="mt-2 fw-bold text-dark">Вход в систему</h2>
          <p class="text-muted">Для членов оргкомитета ИСЭМ СО РАН</p>
        </div>

        <div v-if="error" class="alert alert-danger small py-2">
          <i class="bi bi-exclamation-triangle-fill me-2"></i>{{ error }}
        </div>

        <form @submit.prevent="handleLogin">
          <div class="mb-3">
            <label class="form-label text-muted small fw-bold">Имя пользователя (Логин)</label>
            <div class="input-group">
              <span class="input-group-text bg-light"><i class="bi bi-person"></i></span>
              <input type="text" class="form-control" v-model="username" required placeholder="Введите логин">
            </div>
          </div>

          <div class="mb-4">
            <label class="form-label text-muted small fw-bold">Пароль</label>
            <div class="input-group">
              <span class="input-group-text bg-light"><i class="bi bi-key"></i></span>
              <input type="password" class="form-control" v-model="password" required placeholder="••••••••">
            </div>
          </div>

          <button type="submit" class="btn btn-primary w-100 py-2 mb-3 fw-bold" :disabled="isLoading">
            <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
            {{ isLoading ? 'Проверка...' : 'Войти' }}
          </button>
          
          <div class="text-center mt-3">
            <span class="text-muted small">Нет аккаунта? </span>
            <router-link to="/register" class="text-primary text-decoration-none small fw-bold">Регистрация</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      error: null,
      isLoading: false
    }
  },
  methods: {
    async handleLogin() {
      this.error = null;
      this.isLoading = true;
      
      const authStore = useAuthStore();
      
      try {
        // Вызываем метод из auth.js
        await authStore.login(this.username, this.password);
        
        // Если успешно - кидаем на главную страницу
        this.$router.push('/');
      } catch (err) {
        this.error = 'Неверный логин или пароль. Попробуйте еще раз.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    }
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 60px);
}

.auth-card {
  width: 100%;
  max-width: 450px;
  border-radius: 15px;
}

.input-group-text {
  border-right: none;
  color: #adb5bd;
}

.form-control {
  border-left: none;
}

.form-control:focus {
  box-shadow: none;
  border-color: #dee2e6;
}

.input-group:focus-within .input-group-text,
.input-group:focus-within .form-control {
  border-color: #3498db;
}
</style>