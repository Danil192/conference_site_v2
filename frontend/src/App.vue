<template>
  <div id="app">
    <nav class="sidebar">
      <div class="sidebar-header">
        <h3>СОК ИСЭМ СО РАН</h3>
        <p class="subtitle">Система организации конференций</p>
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
            <span>Контейнеры</span>
          </router-link>
        </li>
        <li>
          <router-link to="/programmas" class="nav-link">
            <i class="bi bi-calendar-week"></i>
            <span>Расписание</span>
          </router-link>
        </li>
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
export default {
  name: 'App'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  display: flex;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.sidebar {
  width: 260px;
  background: linear-gradient(180deg, #2c3e50 0%, #1a252f 100%);
  color: white;
  padding: 20px 0;
  position: fixed;
  height: 100vh;
  overflow-y: auto;
  box-shadow: 2px 0 10px rgba(0,0,0,0.1);
}

.sidebar-header {
  padding: 0 20px 20px;
  border-bottom: 1px solid rgba(255,255,255,0.1);
  margin-bottom: 20px;
}

.sidebar-header h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 5px;
}

.subtitle {
  font-size: 12px;
  color: rgba(255,255,255,0.6);
}

.nav-list {
  list-style: none;
  padding: 0;
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
}

.nav-link:hover {
  background: rgba(255,255,255,0.1);
  color: white;
}

.nav-link.router-link-active {
  background: #3498db;
  color: white;
}

.nav-link i {
  margin-right: 12px;
  font-size: 16px;
}

.sidebar-footer {
  position: absolute;
  bottom: 20px;
  width: 100%;
  padding: 0 20px;
}

.admin-link {
  display: block;
  padding: 12px 20px;
  background: rgba(255,255,255,0.1);
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  border-radius: 5px;
  font-size: 13px;
  transition: all 0.3s ease;
}

.admin-link:hover {
  background: rgba(255,255,255,0.2);
  color: white;
}

.main-content {
  margin-left: 260px;
  flex: 1;
  padding: 30px;
  background: #f5f6fa;
  min-height: 100vh;
}

@media (max-width: 768px) {
  .sidebar {
    width: 200px;
  }
  
  .main-content {
    margin-left: 200px;
  }
}
</style>