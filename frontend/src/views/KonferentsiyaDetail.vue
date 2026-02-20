<template>
  <div class="conference-detail">
    <!-- Заголовок с навигацией -->
    <div class="detail-header">
      <button class="btn btn-outline-secondary back-btn" @click="goBack()">
        <i class="bi bi-arrow-left"></i> Назад
      </button>
      <div class="header-actions">
        <button class="btn btn-outline-primary" @click="editConference()">
          <i class="bi bi-pencil"></i> Редактировать
        </button>
        <button class="btn btn-outline-danger" @click="deleteConference()">
          <i class="bi bi-trash"></i> Удалить
        </button>
      </div>
    </div>

    <!-- Основная информация -->
    <div class="conference-info-card">
      <div class="info-header">
        <div class="info-icon">
          <i class="bi bi-calendar-event"></i>
        </div>
        <div class="info-title">
          <h1>{{ conference.nazvanie }}</h1>
          <div class="info-meta">
            <span class="status-badge" :class="'status-' + conference.status">
              {{ getStatusLabel(conference.status) }}
            </span>
            <span class="date-range">
              <i class="bi bi-calendar-range"></i>
              {{ formatDate(conference.data_nachala) }} — {{ formatDate(conference.data_okonchaniya) }}
            </span>
          </div>
        </div>
      </div>
      
      <div v-if="conference.opisanie" class="info-description">
        <p>{{ conference.opisanie }}</p>
      </div>
    </div>

    <!-- Карточки статистики -->
    <div class="stats-grid">
      <div class="stat-card stat-primary">
        <div class="stat-icon">
          <i class="bi bi-people"></i>
        </div>
        <div class="stat-info">
          <h3>{{ stats.participants }}</h3>
          <p>Участников</p>
        </div>
      </div>
      
      <div class="stat-card stat-success">
        <div class="stat-icon">
          <i class="bi bi-layers"></i>
        </div>
        <div class="stat-info">
          <h3>{{ stats.sections }}</h3>
          <p>Секций</p>
        </div>
      </div>
      
      <div class="stat-card stat-warning">
        <div class="stat-icon">
          <i class="bi bi-file-earmark-text"></i>
        </div>
        <div class="stat-info">
          <h3>{{ stats.reports }}</h3>
          <p>Докладов</p>
        </div>
      </div>
      
      <div class="stat-card stat-info">
        <div class="stat-icon">
          <i class="bi bi-hotel"></i>
        </div>
        <div class="stat-info">
          <h3>{{ stats.accommodation }}</h3>
          <p>Проживаний</p>
        </div>
      </div>
      
      <div class="stat-card stat-danger">
        <div class="stat-icon">
          <i class="bi bi-bus-front"></i>
        </div>
        <div class="stat-info">
          <h3>{{ stats.transfers }}</h3>
          <p>Трансферов</p>
        </div>
      </div>
      
      <div class="stat-card stat-secondary">
        <div class="stat-icon">
          <i class="bi bi-calendar-week"></i>
        </div>
        <div class="stat-info">
          <h3>{{ stats.programItems }}</h3>
          <p>Мероприятий</p>
        </div>
      </div>
    </div>

    <!-- Вкладки с детальной информацией -->
    <div class="detail-tabs">
      <ul class="nav nav-tabs" role="tablist">
        <li class="nav-item" role="presentation">
          <button class="nav-link active" data-bs-toggle="tab" data-bs-target="#participants-tab" type="button">
            <i class="bi bi-people"></i> Участники ({{ stats.participants }})
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" data-bs-toggle="tab" data-bs-target="#sections-tab" type="button">
            <i class="bi bi-layers"></i> Секции ({{ stats.sections }})
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" data-bs-toggle="tab" data-bs-target="#reports-tab" type="button">
            <i class="bi bi-file-earmark-text"></i> Доклады ({{ stats.reports }})
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" data-bs-toggle="tab" data-bs-target="#program-tab" type="button">
            <i class="bi bi-calendar-week"></i> Программа
          </button>
        </li>
        <li class="nav-item" role="presentation">
          <button class="nav-link" data-bs-toggle="tab" data-bs-target="#logistics-tab" type="button">
            <i class="bi bi-truck"></i> Логистика
          </button>
        </li>
      </ul>
      
      <div class="tab-content">
        <!-- Вкладка: Участники -->
        <div class="tab-pane fade show active" id="participants-tab">
          <div class="tab-header">
            <h5><i class="bi bi-people"></i> Участники конференции</h5>
            <router-link :to="`/uchastniks?konferentsiya=${conferenceId}`" class="btn btn-sm btn-primary">
              <i class="bi bi-plus"></i> Добавить
            </router-link>
          </div>
          
          <div v-if="participants.length > 0" class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>ФИО</th>
                  <th>Email</th>
                  <th>Организация</th>
                  <th>Город</th>
                  <th>Статус</th>
                  <th>Секция</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="p in participants" :key="p.id">
                  <td><strong>{{ p.familiya }} {{ p.name }} {{ p.otchestvo }}</strong></td>
                  <td>{{ p.email }}</td>
                  <td>{{ p.organizatsiya }}</td>
                  <td>{{ p.gorod }}</td>
                  <td>
                    <span class="status-badge" :class="'status-' + p.status_uchastnika">
                      {{ getStatusLabel(p.status_uchastnika) }}
                    </span>
                  </td>
                  <td>{{ p.sektsiya_nazvanie || '—' }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="empty-state">
            <i class="bi bi-inbox"></i>
            <p>Участников пока нет</p>
          </div>
        </div>
        
        <!-- Вкладка: Секции -->
        <div class="tab-pane fade" id="sections-tab">
          <div class="tab-header">
            <h5><i class="bi bi-layers"></i> Секции конференции</h5>
            <router-link to="/sekciyas" class="btn btn-sm btn-primary">
              <i class="bi bi-plus"></i> Добавить
            </router-link>
          </div>
          
          <div v-if="sections.length > 0" class="sections-grid">
            <div v-for="sekciya in sections" :key="sekciya.id" class="section-card">
              <div class="section-header">
                <i class="bi bi-layers"></i>
                <h6>{{ sekciya.nazvanie }}</h6>
              </div>
              <p v-if="sekciya.opisanie" class="section-description">{{ sekciya.opisanie }}</p>
              <div class="section-stats">
                <span class="badge bg-primary">Докладов: {{ getSectionReportsCount(sekciya.id) }}</span>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <i class="bi bi-inbox"></i>
            <p>Секции не созданы</p>
          </div>
        </div>
        
        <!-- Вкладка: Доклады -->
        <div class="tab-pane fade" id="reports-tab">
          <div class="tab-header">
            <h5><i class="bi bi-file-earmark-text"></i> Доклады</h5>
            <router-link to="/doklads" class="btn btn-sm btn-primary">
              <i class="bi bi-plus"></i> Добавить
            </router-link>
          </div>
          
          <div v-if="reports.length > 0" class="table-responsive">
            <table class="table table-hover">
              <thead>
                <tr>
                  <th>Название</th>
                  <th>Автор</th>
                  <th>Секция</th>
                  <th>Статус</th>
                  <th>Дата подачи</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="report in reports" :key="report.id">
                  <td>{{ report.nazvanie }}</td>
                  <td>{{ report.uchastnik_fio }}</td>
                  <td>{{ report.sekciya_nazvanie || '—' }}</td>
                  <td>
                    <span class="status-badge" :class="'status-' + report.status_doklada">
                      {{ getReportStatusLabel(report.status_doklada) }}
                    </span>
                  </td>
                  <td>{{ formatDate(report.data_podachi) }}</td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="empty-state">
            <i class="bi bi-inbox"></i>
            <p>Докладов пока нет</p>
          </div>
        </div>
        
        <!-- Вкладка: Программа -->
        <div class="tab-pane fade" id="program-tab">
          <div class="tab-header">
            <h5><i class="bi bi-calendar-week"></i> Программа конференции</h5>
            <router-link to="/programmas" class="btn btn-sm btn-primary">
              <i class="bi bi-plus"></i> Добавить мероприятие
            </router-link>
          </div>
          
          <div v-if="programItems.length > 0" class="program-timeline">
            <div v-for="item in sortedProgramItems" :key="item.id" class="program-item">
              <div class="program-time">
                {{ formatTime(item.vremya_nachala) }}
                <br>
                <small>{{ formatTime(item.vremya_okonchaniya) }}</small>
              </div>
              <div class="program-content">
                <h6>{{ item.doklad_nazvanie || item.uchastnik_fio || 'Мероприятие' }}</h6>
                <p v-if="item.pomeshchenie">
                  <i class="bi bi-geo-alt"></i> {{ item.pomeshchenie }}
                </p>
                <p v-if="item.sekciya_nazvanie">
                  <i class="bi bi-layers"></i> {{ item.sekciya_nazvanie }}
                </p>
              </div>
            </div>
          </div>
          <div v-else class="empty-state">
            <i class="bi bi-inbox"></i>
            <p>Программа ещё не составлена</p>
          </div>
        </div>
        
        <!-- Вкладка: Логистика -->
        <div class="tab-pane fade" id="logistics-tab">
          <div class="logistics-grid">
            <!-- Проживание -->
            <div class="logistics-card">
              <div class="logistics-header">
                <i class="bi bi-hotel"></i>
                <h5>Проживание</h5>
              </div>
              <div class="logistics-stats">
                <div class="logistic-stat">
                  <span class="stat-value">{{ stats.accommodation }}</span>
                  <span class="stat-label">Забронировано</span>
                </div>
              </div>
              <router-link to="/prozhivanies" class="btn btn-sm btn-outline-primary mt-3">
                Управление
              </router-link>
            </div>
            
            <!-- Трансфер -->
            <div class="logistics-card">
              <div class="logistics-header">
                <i class="bi bi-bus-front"></i>
                <h5>Трансфер</h5>
              </div>
              <div class="logistics-stats">
                <div class="logistic-stat">
                  <span class="stat-value">{{ stats.transfers }}</span>
                  <span class="stat-label">Запланировано</span>
                </div>
              </div>
              <router-link to="/transfers" class="btn btn-sm btn-outline-primary mt-3">
                Управление
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { konferentsiyaAPI, uchastnikAPI, sekciyaAPI, dokladAPI, programmaAPI, prozhivanieAPI, transferAPI } from '../services/api'
import { Tab } from 'bootstrap'

export default {
  name: 'KonferentsiyaDetail',
  data() {
    return {
      conferenceId: null,
      conference: {
        nazvanie: '',
        data_nachala: '',
        data_okonchaniya: '',
        status: 'планируется',
        opisanie: ''
      },
      participants: [],
      sections: [],
      reports: [],
      programItems: [],
      stats: {
        participants: 0,
        sections: 0,
        reports: 0,
        accommodation: 0,
        transfers: 0,
        programItems: 0
      }
    }
  },
  computed: {
    sortedProgramItems() {
      return [...this.programItems].sort((a, b) => 
        new Date(a.vremya_nachala) - new Date(b.vremya_nachala)
      )
    }
  },
  mounted() {
    this.conferenceId = this.$route.params.id
    this.loadData()
  },
  methods: {
    async loadData() {
      await this.loadConference()
      await Promise.all([
        this.loadParticipants(),
        this.loadSections(),
        this.loadReports(),
        this.loadProgramItems(),
        this.loadLogistics()
      ])
      this.calculateStats()
    },
    
    async loadConference() {
      try {
        const response = await konferentsiyaAPI.getById(this.conferenceId)
        this.conference = response.data
      } catch (error) {
        console.error('Ошибка загрузки конференции:', error)
        alert('Не удалось загрузить информацию о конференции')
      }
    },
    
    async loadParticipants() {
      try {
        const response = await uchastnikAPI.getAll()
        const all = response.data.results || response.data
        this.participants = all.filter(p => p.konferentsiya == this.conferenceId)
      } catch (error) {
        console.error('Ошибка загрузки участников:', error)
      }
    },
    
    async loadSections() {
    try {
        const response = await sekciyaAPI.getAll(this.conferenceId)
        this.sections = response.data.results || response.data
        this.stats.sections = this.sections.length
    } catch (error) {
        console.error('Ошибка загрузки секций:', error)
    }
    },
    
    async loadReports() {
      try {
        const response = await dokladAPI.getAll()
        const all = response.data.results || response.data
        this.reports = all.filter(r => r.konferentsiya == this.conferenceId)
      } catch (error) {
        console.error('Ошибка загрузки докладов:', error)
      }
    },
    
    async loadProgramItems() {
      try {
        const response = await programmaAPI.getAll()
        const all = response.data.results || response.data
        this.programItems = all.filter(p => p.program_konferentsiya == this.conferenceId || true)
      } catch (error) {
        console.error('Ошибка загрузки программы:', error)
      }
    },
    
    async loadLogistics() {
      try {
        const [prozh, trans] = await Promise.all([
          prozhivanieAPI.getAll(),
          transferAPI.getAll()
        ])
        this.stats.accommodation = (prozh.data.results || prozh.data).length
        this.stats.transfers = (trans.data.results || trans.data).length
      } catch (error) {
        console.error('Ошибка загрузки логистики:', error)
      }
    },
    
    calculateStats() {
      this.stats.participants = this.participants.length
      this.stats.sections = this.sections.length
      this.stats.reports = this.reports.length
      this.stats.programItems = this.programItems.length
    },
    
    getSectionReportsCount(sectionId) {
      return this.reports.filter(r => r.sekciya == sectionId).length
    },
    
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU')
    },
    
    formatTime(datetime) {
      if (!datetime) return ''
      return new Date(datetime).toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
    },
    
    getStatusLabel(status) {
      const labels = {
        'планируется': 'Планируется',
        'идет': 'Идет',
        'завершена': 'Завершена',
        'отменена': 'Отменена',
        'зарегистрирован': 'Зарегистрирован',
        'подтвердил участие': 'Подтвердил участие',
        'оплатил': 'Оплатил',
        'не оплатил': 'Не оплатил',
        'отказался': 'Отказался'
      }
      return labels[status] || status
    },
    
    getReportStatusLabel(status) {
      const labels = {
        'на рассмотрении': 'На рассмотрении',
        'принят': 'Принят',
        'отклонен': 'Отклонен',
        'отложен': 'Отложен'
      }
      return labels[status] || status
    },
    
    goBack() {
      this.$router.push('/konferentsiyas')
    },
    
    editConference() {
      // Можно открыть модальное окно или перейти на страницу редактирования
      alert('Функция редактирования будет добавлена')
    },
    
    async deleteConference() {
      if (!confirm('Вы уверены, что хотите удалить эту конференцию? Это действие нельзя отменить.')) {
        return
      }
      try {
        await konferentsiyaAPI.delete(this.conferenceId)
        this.$router.push('/konferentsiyas')
        alert('Конференция удалена')
      } catch (error) {
        console.error('Ошибка удаления:', error)
        alert('Ошибка при удалении конференции')
      }
    }
  }
}
</script>

<style scoped>
.conference-detail {
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

/* Header */
.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  flex-wrap: wrap;
  gap: 15px;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

/* Conference Info Card */
.conference-info-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.info-header {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.info-icon {
  font-size: 48px;
  opacity: 0.9;
}

.info-title h1 {
  font-size: 28px;
  margin: 0 0 15px 0;
  font-weight: 700;
}

.info-meta {
  display: flex;
  gap: 15px;
  align-items: center;
  flex-wrap: wrap;
}

.date-range {
  display: flex;
  align-items: center;
  gap: 8px;
  opacity: 0.9;
}

.info-description {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid rgba(255,255,255,0.2);
  opacity: 0.9;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 20px rgba(0,0,0,0.12);
}

.stat-icon {
  font-size: 36px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.stat-primary .stat-icon { background: #e3f2fd; color: #1976d2; }
.stat-success .stat-icon { background: #e8f5e9; color: #388e3c; }
.stat-warning .stat-icon { background: #fff3e0; color: #f57c00; }
.stat-info .stat-icon { background: #e0f7fa; color: #0097a7; }
.stat-danger .stat-icon { background: #ffebee; color: #c62828; }
.stat-secondary .stat-icon { background: #f5f5f5; color: #616161; }

.stat-info h3 {
  font-size: 32px;
  color: #2c3e50;
  margin: 0;
  font-weight: 700;
}

.stat-info p {
  color: #7f8c8d;
  font-size: 14px;
  margin: 0;
}

/* Tabs */
.detail-tabs {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  overflow: hidden;
}

.nav-tabs {
  background: #f8f9fa;
  border-bottom: 2px solid #dee2e6;
  padding: 0 20px;
}

.nav-tabs .nav-link {
  border: none;
  color: #6c757d;
  padding: 15px 20px;
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s ease;
}

.nav-tabs .nav-link:hover {
  color: #3498db;
  background: rgba(52, 152, 219, 0.1);
}

.nav-tabs .nav-link.active {
  color: #3498db;
  background: white;
  border-bottom: 3px solid #3498db;
}

.tab-content {
  padding: 25px;
}

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.tab-header h5 {
  margin: 0;
  display: flex;
  align-items: center;
  gap: 10px;
  color: #2c3e50;
}

/* Tables */
.table-responsive {
  border: 1px solid #dee2e6;
  border-radius: 8px;
  overflow: hidden;
}

.table {
  margin: 0;
}

.table thead {
  background: #f8f9fa;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #7f8c8d;
}

.empty-state i {
  font-size: 64px;
  margin-bottom: 15px;
  opacity: 0.5;
}

.empty-state p {
  font-size: 16px;
}

/* Sections Grid */
.sections-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.section-card {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 20px;
  border-left: 4px solid #3498db;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 10px;
}

.section-header i {
  font-size: 24px;
  color: #3498db;
}

.section-header h6 {
  margin: 0;
  color: #2c3e50;
}

.section-description {
  color: #7f8c8d;
  font-size: 14px;
  margin-bottom: 15px;
}

/* Program Timeline */
.program-timeline {
  position: relative;
  padding-left: 30px;
}

.program-timeline::before {
  content: '';
  position: absolute;
  left: 10px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: #dee2e6;
}

.program-item {
  position: relative;
  padding: 15px 20px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 15px;
  display: flex;
  gap: 20px;
}

.program-item::before {
  content: '';
  position: absolute;
  left: -24px;
  top: 20px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #3498db;
}

.program-time {
  min-width: 100px;
  font-weight: 600;
  color: #3498db;
}

.program-time small {
  font-weight: 400;
  color: #7f8c8d;
}

.program-content h6 {
  margin: 0 0 10px 0;
  color: #2c3e50;
}

.program-content p {
  margin: 5px 0;
  color: #7f8c8d;
  font-size: 14px;
  display: flex;
  align-items: center;
  gap: 8px;
}

/* Logistics */
.logistics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.logistics-card {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 25px;
  text-align: center;
}

.logistics-header {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-bottom: 20px;
}

.logistics-header i {
  font-size: 32px;
  color: #3498db;
}

.logistics-header h5 {
  margin: 0;
  color: #2c3e50;
}

.logistic-stat {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 36px;
  font-weight: 700;
  color: #3498db;
}

.stat-label {
  color: #7f8c8d;
  font-size: 14px;
}

/* Status Badges */
.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
  display: inline-block;
}

.status-планируется { background: #e3f2fd; color: #1976d2; }
.status-идет { background: #e8f5e9; color: #388e3c; }
.status-завершена { background: #f5f5f5; color: #616161; }
.status-отменена { background: #ffebee; color: #c62828; }
.status-зарегистрирован { background: #e3f2fd; color: #1976d2; }
.status-подтвердил участие { background: #e8f5e9; color: #388e3c; }
.status-оплатил { background: #fff3e0; color: #f57c00; }
.status-не оплатил { background: #ffebee; color: #c62828; }
.status-отказался { background: #f5f5f5; color: #616161; }
.status-на рассмотрении { background: #fff3e0; color: #f57c00; }
.status-принят { background: #e8f5e9; color: #388e3c; }
.status-отклонен { background: #ffebee; color: #c62828; }
.status-отложен { background: #f5f5f5; color: #616161; }
</style>