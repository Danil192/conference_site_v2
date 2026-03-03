<template>
  <div class="auth-page">
    <div class="card auth-card shadow-lg border-0">
      <div class="card-body p-5">
        <div class="text-center mb-4">
          <i class="bi bi-person-badge text-success" style="font-size: 3rem;"></i>
          <h2 class="mt-2 fw-bold text-dark">Регистрация</h2>
          <p class="text-muted">Новый член организационного комитета</p>
        </div>

        <div v-if="error" class="alert alert-danger small py-2">{{ error }}</div>

        <form @submit.prevent="handleRegister">
          <div class="mb-3">
            <label class="form-label text-muted small fw-bold">Имя пользователя (Логин)</label>
            <input type="text" class="form-control" v-model="form.username" required>
          </div>
          
          <div class="mb-3">
            <label class="form-label text-muted small fw-bold">Email</label>
            <input type="email" class="form-control" v-model="form.email" required>
          </div>

          <div class="mb-4">
            <label class="form-label text-muted small fw-bold">Пароль</label>
            <input type="password" class="form-control" v-model="form.password" required minlength="6">
          </div>

          <button type="submit" class="btn btn-success w-100 py-2 mb-3 fw-bold" :disabled="isLoading">
            <span v-if="isLoading" class="spinner-border spinner-border-sm me-2"></span>
            Зарегистрироваться
          </button>
          
          <div class="text-center mt-3">
            <span class="text-muted small">Уже есть аккаунт? </span>
            <router-link to="/login" class="text-success text-decoration-none small fw-bold">Войти</router-link>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
// Пока сделаем простую заглушку для фронтенда
export default {
  name: 'Register',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: ''
      },
      error: null,
      isLoading: false
    }
  },
  methods: {
    async handleRegister() {
      this.isLoading = true;
      // В будущем здесь будет запрос к API: axios.post('/api/users/register/', this.form)
      setTimeout(() => {
        alert('Регистрация прошла успешно! Теперь вы можете войти.');
        this.$router.push('/login');
        this.isLoading = false;
      }, 1000);
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
</style>