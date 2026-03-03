<template>
  <div id="app">
    <nav class="sidebar">
      <div class="sidebar-header">
        <h3>СОК ИСЭМ СО РАН</h3>
        <p class="subtitle">Система организации конференций</p>

        <!-- БЛОК АВТОРИЗАЦИИ -->
        <div class="auth-wrapper mt-3">
          <!-- Если пользователь НЕ вошел -->
          <template v-if="!authStore.isAuthenticated">
            <div class="d-grid gap-2">
              <router-link to="/login" class="admin-link text-center">
                <i class="bi bi-box-arrow-in-right"></i> Войти
              </router-link>
              <router-link to="/register" class="register-link">
                Регистрация оргкомитета
              </router-link>
            </div>
          </template>

          <!-- Если пользователь ВОШЕЛ -->
          <template v-else>
            <div class="user-profile-box">
              <div class="d-flex align-items-center mb-2">
                <div class="avatar-circle me-2">
                  <i class="bi bi-person-badge"></i>
                </div>
                <div class="user-info">
                  <div class="user-name text-truncate">{{ authStore.user?.username }}</div>
                  <div class="user-status">
                    {{ authStore.user?.role === 'admin' ? 'Администратор' : 'Оргкомитет' }}
                  </div>
                </div>
              </div>
              <button @click="handleLogout" class="btn-logout">
                <i class="bi bi-power"></i> Выйти
              </button>
            </div>
          </template>
        </div>
      </div>
      
      <ul class="nav-list">
        <li>
          <router-link to="/" class="nav-link">
            <i class="bi bi-speedometer2"></i>
            <span>Главная</span>
          </router-link>
        </li>
        <li class="nav-section">Конференции</li>
        <li>
          <router-link to="/konferentsiyas" class="nav-link">
            <i class="bi bi-calendar-event"></i>
            <span>Конференции</span>
          </router-link>
        </li>
        <li>
          <router-link to="/sekciyas" class="nav-link">
            <i class="bi bi-layers"></i>
            <span>Секции</span>
          </router-link>
        </li>
        
        <li class="nav-section">Участники</li>
        <li>
          <router-link to="/uchastniks" class="nav-link">
            <i class="bi bi-people"></i>
            <span>Участники</span>
          </router-link>
        </li>
        <li>
          <router-link to="/doklads" class="nav-link">
            <i class="bi bi-file-earmark-text"></i>
            <span>Доклады</span>
          </router-link>
        </li>
        <li>
          <router-link to="/otkazs" class="nav-link">
            <i class="bi bi-x-circle"></i>
            <span>Отказы</span>
          </router-link>
        </li>
        
        <li class="nav-section">Логистика</li>
        <li>
          <router-link to="/prozhivanies" class="nav-link">
            <i class="bi bi-hotel"></i>
            <span>Проживание</span>
          </router-link>
        </li>
        <li>
          <router-link to="/transfers" class="nav-link">
            <i class="bi bi-bus-front"></i>
            <span>Трансфер</span>
          </router-link>
        </li>
        
        <li class="nav-section">Программа</li>
        <li>
          <router-link to="/programs" class="nav-link">
            <i class="bi bi-kanban"></i>
            <span>Программа</span>
          </router-link>
        </li>
        <li>
          <router-link to="/programmas" class="nav-link">
            <i class="bi bi-calendar-week"></i>
            <span>Расписание</span>
          </router-link>
        </li>
         <template v-if="authStore.user?.role === 'admin'">
          <li class="nav-section">Администрирование</li>
          <li>
            <router-link to="/system-users" class="nav-link">
              <i class="bi bi-person-lines-fill"></i>
              <span>Пользователи системы</span>
            </router-link>
          </li>
          <li>
            <!-- Прямая ссылка на админку Django -->
            <a href="http://localhost:8000/admin/" target="_blank" class="nav-link text-warning">
              <i class="bi bi-gear-fill"></i>
              <span>Django Админка</span>
            </a>
          </li>
        </template>
      </ul>
      
      <div class="sidebar-footer">
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script>
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()

    const handleLogout = () => {
      if (confirm('Выйти из системы?')) {
        authStore.logout()
        router.push('/login')
      }
    }

    return {
      authStore,
      handleLogout
    }
  }
}
</script>

<style scoped>
/* ==========================================
   ОСНОВНАЯ СТРУКТУРА
========================================== */
#app {
  display: flex;
  min-height: 100vh;
}

.main-content {
  margin-left: 260px;
  flex: 1;
  padding: 30px;
  min-height: 100vh;
}

/* ==========================================
   САЙДБАР (SIDEBAR)
========================================== */
.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #2c3e50 0%, #1a252f 100%);
  color: white;
  padding: 20px 0;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
  box-shadow: 2px 0 10px rgba(0,0,0,0.1);
  z-index: 1000;
}

.sidebar-header {
  padding: 0 20px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.05);
  margin-bottom: 10px;
}

.sidebar-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 5px;
  color: white;
}

.subtitle {
  font-size: 12px;
  color: rgba(255,255,255,0.5);
  margin-bottom: 0;
}

/* ==========================================
   БЛОК АВТОРИЗАЦИИ
========================================== */
.auth-wrapper {
  background: rgba(255, 255, 255, 0.03);
  border-radius: 8px;
  padding: 15px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.admin-link {
  display: block;
  padding: 10px 15px;
  background: rgba(255,255,255,0.05);
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  border-radius: 6px;
  font-size: 13px;
  transition: all 0.3s ease;
  border: 1px solid rgba(255,255,255,0.1);
}

.admin-link:hover {
  background: rgba(255,255,255,0.15);
  color: white;
}

.register-link {
  display: block;
  text-align: center;
  font-size: 11px;
  color: rgba(255,255,255,0.4);
  text-decoration: none;
  margin-top: 10px;
  transition: color 0.3s ease;
}

.register-link:hover {
  color: #3498db;
}

.user-profile-box {
  color: white;
}

.avatar-circle {
  width: 36px;
  height: 36px;
  background: rgba(52, 152, 219, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3498db;
  font-size: 18px;
}

.user-name {
  font-size: 14px;
  font-weight: 600;
}

.user-status {
  font-size: 10px;
  color: #2ecc71;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.btn-logout {
  width: 100%;
  background: rgba(231, 76, 60, 0.1);
  border: 1px solid rgba(231, 76, 60, 0.2);
  color: #e74c3c;
  font-size: 12px;
  padding: 8px;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 15px;
}

.btn-logout:hover {
  background: #e74c3c;
  color: white;
}

/* ==========================================
   НАВИГАЦИЯ (ОРИГИНАЛ)
========================================== */
.nav-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.nav-section {
  padding: 15px 20px 5px;
  font-size: 11px;
  text-transform: uppercase;
  color: rgba(255,255,255,0.4);
  font-weight: 600;
  letter-spacing: 1px;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 12px 20px;
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
  font-size: 14px;
}

.nav-link i {
  margin-right: 12px;
  font-size: 16px;
  width: 20px;
  text-align: center;
}

.nav-link:hover {
  background: rgba(255,255,255,0.05);
  color: white;
}

.nav-link.router-link-active {
  background-color: #3498db !important;
  color: white !important;
  border-left: 3px solid transparent; /* Убирает дергание, если рамка была */
}

/* Адаптивность */
@media (max-width: 768px) {
  .sidebar { width: 200px; }
  .main-content { margin-left: 200px; }
}
</style>