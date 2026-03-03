<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">
        <i class="bi bi-person-lines-fill"></i>
        Пользователи системы
      </h1>
    </div>

    <div class="alert alert-warning shadow-sm" role="alert">
      <i class="bi bi-shield-lock-fill me-2"></i>
      Этот раздел доступен только администраторам системы.
    </div>

    <div class="table-container shadow-sm bg-white rounded-3">
      <table class="table table-hover align-middle mb-0">
        <thead class="table-light">
          <tr>
            <th>Логин</th>
            <th>Email</th>
            <th>Роль</th>
            <th>Дата регистрации</th>
            <th class="text-end">Действия</th>
          </tr>
        </thead>
        <tbody>
          <!-- Временно используем заглушки, пока не подключим API -->
          <tr v-for="user in mockUsers" :key="user.id">
            <td><strong>{{ user.username }}</strong></td>
            <td>{{ user.email }}</td>
            <td>
              <span class="badge" :class="user.role === 'admin' ? 'bg-danger' : 'bg-primary'">
                {{ user.role === 'admin' ? 'Администратор' : 'Оргкомитет' }}
              </span>
            </td>
            <td>{{ user.date_joined }}</td>
            <td class="text-end">
              <button class="btn btn-sm btn-outline-danger" @click="deleteUser(user.id)" :disabled="user.role === 'admin'">
                <i class="bi bi-trash"></i>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SystemUsersList',
  data() {
    return {
      // Фейковые данные для демонстрации
      mockUsers:[
        { id: 1, username: 'admin', email: 'admin@isem.ru', role: 'admin', date_joined: '01.03.2026' },
        { id: 2, username: 'ivanov', email: 'ivanov@isem.ru', role: 'organizer', date_joined: '02.03.2026' },
        { id: 3, username: 'petrov', email: 'petrov@mail.ru', role: 'organizer', date_joined: '03.03.2026' },
      ]
    }
  },
  methods: {
    deleteUser(id) {
      if(confirm('Заблокировать доступ этому пользователю?')) {
        this.mockUsers = this.mockUsers.filter(u => u.id !== id);
      }
    }
  }
}
</script>

<style scoped>
.page-container {
  max-width: 1400px;
  margin: 0 auto;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}
.page-title {
  font-size: 24px;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}
.table-container {
  overflow: hidden;
}
</style>