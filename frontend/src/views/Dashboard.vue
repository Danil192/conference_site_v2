<template>
  <div class="dashboard">
    <h1 class="page-title">
      <i class="bi bi-speedometer2"></i>
      Панель управления
    </h1>
    
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">
          <i class="bi bi-calendar-event"></i>
        </div>
        <div class="stat-info">
          <h3>{{ stats.konferentsiyas }}</h3>
          <p>Конференций</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="bi bi-people"></i>
        </div>
        <div class="stat-info">
          <h3>{{ stats.uchastniks }}</h3>
          <p>Участников</p>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon">
          <i class="bi bi-file-earmark-text"></i>
        </div>
        <div class="stat-info">
          <h3>{{ stats.doklads }}</h3>
          <p>Докладов</p>
        </div>
      </div>
    </div>

    <div class="quick-actions">
      <h2>
        <i class="bi bi-lightning-charge"></i>
        Быстрые действия
      </h2>
      <div class="action-buttons">
        <router-link to="/konferentsiyas" class="action-btn primary">
          <i class="bi bi-plus-circle"></i> Конференции
        </router-link>
        <router-link to="/uchastniks" class="action-btn secondary">
          <i class="bi bi-plus-circle"></i> Участники
        </router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {
        konferentsiyas: 0,
        uchastniks: 0,
        doklads: 0
      }
    }
  }
}
</script>

<style scoped>
.dashboard {
  max-width: 1200px;
}

.page-title {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-title i {
  font-size: 32px;
  color: #3498db;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 20px;
  margin-bottom: 40px;
}

.stat-card {
  background: white;
  border-radius: 10px;
  padding: 25px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

.stat-icon {
  font-size: 40px;
  margin-right: 20px;
  color: #3498db;
}

.stat-icon i {
  font-size: 40px;
}

.stat-info h3 {
  font-size: 32px;
  color: #2c3e50;
  margin-bottom: 5px;
}

.stat-info p {
  color: #7f8c8d;
  font-size: 14px;
}

.quick-actions {
  background: white;
  border-radius: 10px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

.quick-actions h2 {
  font-size: 20px;
  color: #2c3e50;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.quick-actions h2 i {
  color: #f39c12;
}

.action-buttons {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.action-btn {
  padding: 12px 24px;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 500;
  color: white;
  background: #3498db;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.action-btn i {
  font-size: 18px;
}

.action-btn.primary {
  background: #3498db;
}

.action-btn.primary:hover {
  background: #2980b9;
}

.action-btn.secondary {
  background: #95a5a6;
}

.action-btn.secondary:hover {
  background: #7f8c8d;
}
</style>