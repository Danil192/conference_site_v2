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
        <button class="action-btn primary" @click="openWizard()">
          <i class="bi bi-plus-circle"></i> Создать конференцию
        </button>
        <router-link to="/uchastniks" class="action-btn secondary">
          <i class="bi bi-people"></i> Участники
        </router-link>
      </div>
    </div>

    <!-- Мастер создания конференции -->
    <div class="modal fade wizard-modal" ref="wizardModalRef" tabindex="-1" data-bs-backdrop="static">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-calendar-plus"></i>
              Создание конференции
            </h5>
            <button type="button" class="btn-close" @click="closeWizard()" :disabled="isCreating"></button>
          </div>
          
          <!-- Индикатор прогресса -->
          <div class="wizard-progress">
            <div class="progress-steps">
              <div class="progress-step" :class="{ active: currentStep >= 1, completed: currentStep > 1 }">
                <div class="step-number">1</div>
                <div class="step-label">Основная информация</div>
              </div>
              <div class="progress-line" :class="{ active: currentStep > 1 }"></div>
              <div class="progress-step" :class="{ active: currentStep >= 2, completed: currentStep > 2 }">
                <div class="step-number">2</div>
                <div class="step-label">Участники</div>
              </div>
              <div class="progress-line" :class="{ active: currentStep > 2 }"></div>
              <div class="progress-step" :class="{ active: currentStep >= 3, completed: currentStep > 3 }">
                <div class="step-number">3</div>
                <div class="step-label">Настройки</div>
              </div>
            </div>
          </div>
          
          <div class="modal-body">
            <form @submit.prevent="nextStep()">
              
              <!-- ШАГ 1: Основная информация -->
              <div v-if="currentStep === 1" class="wizard-step">
                <h6 class="step-title">
                  <i class="bi bi-info-circle"></i> Основная информация о конференции
                </h6>
                
                <div class="row">
                  <div class="col-12 mb-3">
                    <label class="form-label">Название конференции *</label>
                    <input type="text" class="form-control form-control-lg" v-model="wizardData.nazvanie" required placeholder="Например: XXX Байкальская Всероссийская конференция">
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Дата начала *</label>
                    <input type="date" class="form-control" v-model="wizardData.data_nachala" required>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Дата окончания *</label>
                    <input type="date" class="form-control" v-model="wizardData.data_okonchaniya" required>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Статус *</label>
                    <select class="form-select" v-model="wizardData.status" required>
                      <option value="планируется">Планируется</option>
                      <option value="идет">Идет</option>
                      <option value="завершена">Завершена</option>
                      <option value="отменена">Отменена</option>
                    </select>
                  </div>
                </div>
                
                <hr class="my-4">
                
                <h6 class="step-title">
                  <i class="bi bi-layers"></i> Секции конференции
                </h6>
                
                <div class="mb-3">
                  <label class="form-label">Добавить секцию</label>
                  <div class="input-group">
                    <input type="text" class="form-control" v-model="newSectionName" placeholder="Например: Секция 1. Информационные технологии" @keyup.enter="addSection()">
                    <button type="button" class="btn btn-outline-primary" @click="addSection()">
                      <i class="bi bi-plus"></i> Добавить
                    </button>
                  </div>
                </div>
                
                <div v-if="wizardData.sekciyas.length > 0" class="sections-list">
                  <div class="list-group">
                    <div v-for="(sekciya, index) in wizardData.sekciyas" :key="index" class="list-group-item d-flex justify-content-between align-items-center">
                      <span>
                        <i class="bi bi-layers me-2 text-primary"></i>
                        {{ sekciya.nazvanie }}
                      </span>
                      <button type="button" class="btn btn-sm btn-outline-danger" @click="removeSection(index)">
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- ШАГ 2: Участники -->
              <div v-if="currentStep === 2" class="wizard-step">
                <h6 class="step-title">
                  <i class="bi bi-people"></i> Выбор участников конференции
                </h6>
                
                <div class="alert alert-info">
                  <i class="bi bi-info-circle"></i>
                  Выберите существующих участников или добавьте новых
                </div>
                
                <!-- Поиск и фильтры -->
                <div class="filters-bar mb-3">
                  <div class="search-box">
                    <i class="bi bi-search"></i>
                    <input type="text" v-model="participantSearch" placeholder="Поиск участников..." class="form-control">
                  </div>
                </div>
                
                <!-- Таблица участников -->
                <div class="participants-table-container">
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th style="width: 50px;">
                          <input type="checkbox" class="form-check-input" @change="toggleSelectAll()" :checked="isAllSelected">
                        </th>
                        <th>ФИО</th>
                        <th>Email</th>
                        <th>Организация</th>
                        <th>Город</th>
                        <th style="width: 100px;">Действия</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="participant in filteredParticipants" :key="participant.id">
                        <td>
                          <input type="checkbox" class="form-check-input" 
                                 :checked="isSelected(participant.id)" 
                                 @change="toggleParticipant(participant)">
                        </td>
                        <td>{{ participant.familiya }} {{ participant.name }} {{ participant.otchestvo }}</td>
                        <td>{{ participant.email }}</td>
                        <td>{{ participant.organizatsiya }}</td>
                        <td>{{ participant.gorod }}</td>
                        <td>
                          <button type="button" class="btn btn-sm btn-outline-primary" @click="addParticipant(participant)">
                            <i class="bi bi-plus"></i>
                          </button>
                        </td>
                      </tr>
                      <tr v-if="filteredParticipants.length === 0">
                        <td colspan="6" class="text-center text-muted py-4">
                          Нет участников
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
                
                <!-- Выбранные участники -->
                <div v-if="wizardData.selectedParticipants.length > 0" class="selected-participants mt-3">
                  <h6>Выбрано участников: {{ wizardData.selectedParticipants.length }}</h6>
                  <div class="badges-list">
                    <span v-for="p in wizardData.selectedParticipants" :key="p.id" class="badge bg-primary me-1 mb-1">
                      {{ p.familiya }} {{ p.name[0] }}.
                      <button type="button" class="btn-close btn-close-white ms-1" @click="removeParticipant(p.id)"></button>
                    </span>
                  </div>
                </div>
                
                <div class="mt-3">
                  <button type="button" class="btn btn-outline-success" @click="openAddParticipantModal()">
                    <i class="bi bi-person-plus"></i> Добавить нового участника
                  </button>
                </div>
              </div>
              
              <!-- ШАГ 3: Настройки -->
              <div v-if="currentStep === 3" class="wizard-step">
                <h6 class="step-title">
                  <i class="bi bi-gear"></i> Дополнительные настройки
                </h6>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Тип регистрации</label>
                    <select class="form-select" v-model="wizardData.registrationType">
                      <option value="free">Свободная</option>
                      <option value="moderated">С модерацией</option>
                      <option value="invite">По приглашениям</option>
                    </select>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Лимит участников</label>
                    <input type="number" class="form-control" v-model="wizardData.participantLimit" placeholder="Без ограничений">
                  </div>
                  
                  <div class="col-12 mb-3">
                    <label class="form-label">Описание конференции</label>
                    <textarea class="form-control" v-model="wizardData.opisanie" rows="3" placeholder="Краткое описание конференции..."></textarea>
                  </div>
                  
                  <div class="col-12 mb-3">
                    <div class="form-check">
                      <input class="form-check-input" type="checkbox" v-model="wizardData.enableEmails" id="enableEmails">
                      <label class="form-check-label" for="enableEmails">
                        Включить email-уведомления для участников
                      </label>
                    </div>
                  </div>
                  
                  <div class="col-12 mb-3">
                    <div class="form-check">
                      <input class="form-check-input" type="checkbox" v-model="wizardData.enableReports" id="enableReports">
                      <label class="form-check-label" for="enableReports">
                        Разрешить подачу докладов
                      </label>
                    </div>
                  </div>
                </div>
                
                <hr class="my-4">
                
                <h6 class="step-title">
                  <i class="bi bi-check-circle"></i> Итоговая информация
                </h6>
                
                <div class="summary-card">
                  <div class="summary-row">
                    <strong>Конференция:</strong>
                    <span>{{ wizardData.nazvanie }}</span>
                  </div>
                  <div class="summary-row">
                    <strong>Даты:</strong>
                    <span>{{ formatDate(wizardData.data_nachala) }} — {{ formatDate(wizardData.data_okonchaniya) }}</span>
                  </div>
                  <div class="summary-row">
                    <strong>Секции:</strong>
                    <span>{{ wizardData.sekciyas.length }}</span>
                  </div>
                  <div class="summary-row">
                    <strong>Участников:</strong>
                    <span>{{ wizardData.selectedParticipants.length }}</span>
                  </div>
                </div>
              </div>
              
            </form>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeWizard()" :disabled="isCreating">Отмена</button>
            <button type="button" class="btn btn-outline-primary" @click="prevStep()" v-if="currentStep > 1" :disabled="isCreating">
              <i class="bi bi-arrow-left"></i> Назад
            </button>
            <button type="button" class="btn btn-primary" @click="nextStep()" v-if="currentStep < 3" :disabled="!canProceed">
              Далее <i class="bi bi-arrow-right"></i>
            </button>
            <button type="button" class="btn btn-success" @click="createConference()" v-if="currentStep === 3" :disabled="isCreating">
              <i class="bi" :class="isCreating ? 'bi-hourglass-split' : 'bi-check-circle'"></i>
              {{ isCreating ? 'Создание...' : 'Создать конференцию' }}
            </button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- Модальное окно добавления участника -->
    <div class="modal fade" ref="addParticipantModalRef" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Добавить участника</h5>
            <button type="button" class="btn-close" @click="closeAddParticipantModal()"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveNewParticipant()">
              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label">Фамилия *</label>
                  <input type="text" class="form-control" v-model="newParticipant.familiya" required>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Имя *</label>
                  <input type="text" class="form-control" v-model="newParticipant.name" required>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Отчество</label>
                  <input type="text" class="form-control" v-model="newParticipant.otchestvo">
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Email *</label>
                <input type="email" class="form-control" v-model="newParticipant.email" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Организация</label>
                <input type="text" class="form-control" v-model="newParticipant.organizatsiya">
              </div>
              <div class="mb-3">
                <label class="form-label">Город</label>
                <input type="text" class="form-control" v-model="newParticipant.gorod">
              </div>
              <div class="modal-footer px-0 pb-0">
                <button type="button" class="btn btn-secondary" @click="closeAddParticipantModal()">Отмена</button>
                <button type="submit" class="btn btn-primary">Добавить</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { konferentsiyaAPI, sekciyaAPI, uchastnikAPI } from '../services/api'
import { Modal } from 'bootstrap'

export default {
  name: 'Dashboard',
  data() {
    return {
      stats: {
        konferentsiyas: 0,
        uchastniks: 0,
        doklads: 0
      },
      wizardModal: null,
      addParticipantModal: null,
      currentStep: 1,
      isCreating: false,
      wizardData: {
        nazvanie: '',
        data_nachala: '',
        data_okonchaniya: '',
        status: 'планируется',
        sekciyas: [],
        selectedParticipants: [],
        registrationType: 'free',
        participantLimit: null,
        opisanie: '',
        enableEmails: true,
        enableReports: true
      },
      newSectionName: '',
      allParticipants: [],
      participantSearch: '',
      newParticipant: {
        familiya: '',
        name: '',
        otchestvo: '',
        email: '',
        organizatsiya: '',
        gorod: ''
      }
    }
  },
  computed: {
    canProceed() {
      if (this.currentStep === 1) {
        return this.wizardData.nazvanie && this.wizardData.data_nachala && this.wizardData.data_okonchaniya
      }
      if (this.currentStep === 2) {
        return true // Участники опциональны
      }
      return true
    },
    filteredParticipants() {
      if (!this.participantSearch) {
        return this.allParticipants
      }
      const search = this.participantSearch.toLowerCase()
      return this.allParticipants.filter(p => 
        p.familiya.toLowerCase().includes(search) ||
        p.name.toLowerCase().includes(search) ||
        p.email.toLowerCase().includes(search) ||
        p.organizatsiya.toLowerCase().includes(search)
      )
    },
    isAllSelected() {
      return this.filteredParticipants.length > 0 && 
             this.filteredParticipants.every(p => this.isSelected(p.id))
    }
  },
  mounted() {
    this.wizardModal = new Modal(this.$refs.wizardModalRef)
    this.addParticipantModal = new Modal(this.$refs.addParticipantModalRef)
    this.loadStats()
  },
  methods: {
    async loadStats() {
      try {
        const [konf, uch, dok] = await Promise.all([
          konferentsiyaAPI.getAll(),
          uchastnikAPI.getAll(),
        ])
        this.stats.konferentsiyas = konf.data.count || konf.data.length || 0
        this.stats.uchastniks = uch.data.count || uch.data.length || 0
        this.stats.doklads = dok.data.count || dok.data.length || 0
      } catch (error) {
        console.error('Ошибка загрузки статистики:', error)
      }
    },
    
    async loadParticipants() {
      try {
        const response = await uchastnikAPI.getAll()
        this.allParticipants = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки участников:', error)
      }
    },
    
    // Методы wizard
    openWizard() {
      this.currentStep = 1
      this.wizardData = {
        nazvanie: '',
        data_nachala: '',
        data_okonchaniya: '',
        status: 'планируется',
        sekciyas: [],
        selectedParticipants: [],
        registrationType: 'free',
        participantLimit: null,
        opisanie: '',
        enableEmails: true,
        enableReports: true
      }
      this.newSectionName = ''
      this.participantSearch = ''
      this.isCreating = false
      this.loadParticipants()
      this.wizardModal.show()
    },
    
    closeWizard() {
      this.wizardModal.hide()
    },
    
    nextStep() {
      if (this.currentStep === 1 && !this.canProceed) {
        alert('Заполните обязательные поля')
        return
      }
      if (this.currentStep < 3) {
        this.currentStep++
      }
    },
    
    prevStep() {
      if (this.currentStep > 1) {
        this.currentStep--
      }
    },
    
    // Методы секций
    addSection() {
      const name = this.newSectionName.trim()
      if (name) {
        if (!this.wizardData.sekciyas.some(s => s.nazvanie.toLowerCase() === name.toLowerCase())) {
          this.wizardData.sekciyas.push({ nazvanie: name })
          this.newSectionName = ''
        } else {
          alert('Такая секция уже добавлена')
        }
      }
    },
    
    removeSection(index) {
      this.wizardData.sekciyas.splice(index, 1)
    },
    
    // Методы участников
    isSelected(id) {
      return this.wizardData.selectedParticipants.some(p => p.id === id)
    },
    
    toggleParticipant(participant) {
      const index = this.wizardData.selectedParticipants.findIndex(p => p.id === participant.id)
      if (index > -1) {
        this.wizardData.selectedParticipants.splice(index, 1)
      } else {
        this.wizardData.selectedParticipants.push(participant)
      }
    },
    
    toggleSelectAll() {
      if (this.isAllSelected) {
        this.wizardData.selectedParticipants = this.wizardData.selectedParticipants.filter(
          p => !this.filteredParticipants.some(fp => fp.id === p.id)
        )
      } else {
        this.filteredParticipants.forEach(p => {
          if (!this.isSelected(p.id)) {
            this.wizardData.selectedParticipants.push(p)
          }
        })
      }
    },
    
    addParticipant(participant) {
      if (!this.isSelected(participant.id)) {
        this.wizardData.selectedParticipants.push(participant)
      }
    },
    
    removeParticipant(id) {
      const index = this.wizardData.selectedParticipants.findIndex(p => p.id === id)
      if (index > -1) {
        this.wizardData.selectedParticipants.splice(index, 1)
      }
    },
    
    // Модальное окно добавления участника
    openAddParticipantModal() {
      this.newParticipant = {
        familiya: '',
        name: '',
        otchestvo: '',
        email: '',
        organizatsiya: '',
        gorod: ''
      }
      this.addParticipantModal.show()
    },
    
    closeAddParticipantModal() {
      this.addParticipantModal.hide()
    },
    
    async saveNewParticipant() {
      try {
        const response = await uchastnikAPI.create(this.newParticipant)
        this.allParticipants.push(response.data)
        this.wizardData.selectedParticipants.push(response.data)
        this.closeAddParticipantModal()
        alert('Участник добавлен')
      } catch (error) {
        console.error('Ошибка добавления участника:', error)
        alert('Ошибка: ' + (error.response?.data?.error || error.message))
      }
    },
    
    // Создание конференции
    async createConference() {
      if (!this.wizardData.nazvanie || !this.wizardData.data_nachala || !this.wizardData.data_okonchaniya) {
        alert('Заполните обязательные поля')
        return
      }
      
      if (new Date(this.wizardData.data_nachala) > new Date(this.wizardData.data_okonchaniya)) {
        alert('Дата начала должна быть раньше даты окончания')
        return
      }
      
      this.isCreating = true
      
      try {
        // 1. Создаём конференцию
        const conferenceResponse = await konferentsiyaAPI.create({
          nazvanie: this.wizardData.nazvanie,
          data_nachala: this.wizardData.data_nachala,
          data_okonchaniya: this.wizardData.data_okonchaniya,
          status: this.wizardData.status
        })
        
        const conferenceId = conferenceResponse.data.id
        
        // 2. Создаём секции
        for (const sekciya of this.wizardData.sekciyas) {
        try {
            await sekciyaAPI.create({ 
            nazvanie: sekciya.nazvanie,
            konferentsiya: conferenceId
            })
        } catch (e) {
            console.warn(`Не удалось создать секцию "${sekciya.nazvanie}":`, e)
        }
        }
        
        // 3. Обновляем участников (привязываем к конференции)
        for (const participant of this.wizardData.selectedParticipants) {
          try {
            await uchastnikAPI.update(participant.id, {
              ...participant,
              konferentsiya: conferenceId
            })
          } catch (e) {
            console.warn(`Не удалось обновить участника "${participant.familiya}":`, e)
          }
        }
        
        this.closeWizard()
        this.loadStats()
        
        alert(`Конференция "${this.wizardData.nazvanie}" успешно создана!\n` +
              `Секций: ${this.wizardData.sekciyas.length}\n` +
              `Участников: ${this.wizardData.selectedParticipants.length}`)
        
        this.$router.push('/konferentsiyas')
        
      } catch (error) {
        console.error('Ошибка создания конференции:', error)
        alert('Ошибка при создании конференции: ' + (error.response?.data?.error || error.message))
      } finally {
        this.isCreating = false
      }
    },
    
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU')
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
  transition: transform 0.2s ease;
}

.stat-card:hover {
  transform: translateY(-3px);
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
  border: none;
  cursor: pointer;
  transition: background 0.2s ease;
}

.action-btn i {
  font-size: 18px;
}

.action-btn.primary {
  background: #27ae60;
}

.action-btn.primary:hover {
  background: #219a52;
}

.action-btn.secondary {
  background: #95a5a6;
}

.action-btn.secondary:hover {
  background: #7f8c8d;
}

/* Wizard Modal Styles */
.wizard-modal .modal-dialog {
  max-width: 900px;
}

.wizard-progress {
  padding: 20px 30px;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
}

.progress-steps {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.progress-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.step-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #dee2e6;
  color: #6c757d;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  margin-bottom: 8px;
  transition: all 0.3s ease;
}

.progress-step.active .step-number {
  background: #3498db;
  color: white;
}

.progress-step.completed .step-number {
  background: #27ae60;
  color: white;
}

.step-label {
  font-size: 12px;
  color: #6c757d;
  text-align: center;
}

.progress-step.active .step-label {
  color: #3498db;
  font-weight: 600;
}

.progress-line {
  flex: 1;
  height: 2px;
  background: #dee2e6;
  margin: 0 10px;
  transition: background 0.3s ease;
}

.progress-line.active {
  background: #27ae60;
}

/* Wizard Step */
.wizard-step {
  padding: 20px 0;
}

.step-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
}

.step-title i {
  color: #3498db;
}

/* Sections List */
.sections-list .list-group-item {
  background: #f8f9fa;
  border: 1px solid #dee2e6;
}

/* Participants Table */
.participants-table-container {
  max-height: 400px;
  overflow-y: auto;
  border: 1px solid #dee2e6;
  border-radius: 8px;
}

.participants-table-container table {
  margin: 0;
}

.filters-bar {
  display: flex;
  gap: 10px;
}

.search-box {
  flex: 1;
  position: relative;
}

.search-box i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #7f8c8d;
}

.search-box input {
  padding-left: 36px;
}

/* Selected Participants */
.selected-participants .badges-list {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.badges-list .badge {
  padding: 8px 12px;
  font-size: 13px;
}

/* Summary Card */
.summary-card {
  background: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  border-bottom: 1px solid #dee2e6;
}

.summary-row:last-child {
  border-bottom: none;
}

.summary-row strong {
  color: #2c3e50;
}

.summary-row span {
  color: #7f8c8d;
}

/* Modal Footer */
.modal-footer {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  padding: 15px 20px;
  border-top: 1px solid #dee2e6;
}
</style>