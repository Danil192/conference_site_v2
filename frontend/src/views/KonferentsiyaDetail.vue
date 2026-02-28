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
            <div class="header-actions">
              <button class="btn btn-sm btn-success me-2" @click="addParticipantToConference()">
                <i class="bi bi-person-plus"></i> Добавить участника
              </button>
              <router-link :to="`/uchastniks?konferentsiya=${conferenceId}`" class="btn btn-sm btn-primary">
                <i class="bi bi-people"></i> Все участники
              </router-link>
            </div>
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
                  <th class="text-end">Действия</th>
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
                  <td class="text-end">
                    <button class="btn btn-sm btn-outline-primary" @click="editParticipant(p)">
                      <i class="bi bi-pencil"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div v-else class="empty-state">
            <i class="bi bi-inbox"></i>
            <p>Участников пока нет</p>
            <button class="btn btn-primary mt-3" @click="addParticipantToConference()">
              <i class="bi bi-person-plus"></i> Добавить первого участника
            </button>
          </div>
        </div>
        
        <!-- Модальное окно добавления участника -->
        <div class="modal fade" ref="addParticipantModalRef" tabindex="-1">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">
                  <i class="bi bi-person-plus"></i>
                  Добавить участника к конференции "{{ conference.nazvanie }}"
                </h5>
                <button type="button" class="btn-close" @click="closeAddParticipantModal()"></button>
              </div>
              <div class="modal-body">
                <form @submit.prevent="saveParticipantToConference()">
                  <div class="alert alert-info">
                    <i class="bi bi-info-circle"></i>
                    Участник будет автоматически привязан к конференции "{{ conference.nazvanie }}"
                  </div>
                  
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
                  
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Email *</label>
                      <input type="email" class="form-control" v-model="newParticipant.email" required>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Телефон</label>
                      <input type="text" class="form-control" v-model="newParticipant.telefon">
                    </div>
                  </div>
                  
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Организация</label>
                      <input type="text" class="form-control" v-model="newParticipant.organizatsiya">
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Город</label>
                      <input type="text" class="form-control" v-model="newParticipant.gorod">
                    </div>
                  </div>
                  
                  <div class="row">
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Секция</label>
                      <select class="form-select" v-model="newParticipant.sektsiya">
                        <option value="">Не выбрана</option>
                        <option v-for="sek in conferenceSections" :key="sek.id" :value="sek.id">
                          {{ sek.nazvanie }}
                        </option>
                      </select>
                    </div>
                    <div class="col-md-6 mb-3">
                      <label class="form-label">Статус *</label>
                      <select class="form-select" v-model="newParticipant.status_uchastnika" required>
                        <option value="зарегистрирован">Зарегистрирован</option>
                        <option value="подтвердил участие">Подтвердил участие</option>
                        <option value="оплатил">Оплатил</option>
                      </select>
                    </div>
                  </div>
                  
                  <div class="modal-footer px-0 pb-0">
                    <button type="button" class="btn btn-secondary" @click="closeAddParticipantModal()">Отмена</button>
                    <button type="submit" class="btn btn-success">
                      <i class="bi bi-check-circle"></i> Добавить участника
                    </button>
                  </div>
                </form>
              </div>
            </div>
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
                  <td>{{ report.sektsiya_nazvanie || '—' }}</td>
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
            <div class="header-actions">
              <button class="btn btn-sm btn-danger me-2" @click="downloadProgramPDF()">
                <i class="bi bi-file-earmark-pdf"></i> Скачать PDF
              </button>
              <router-link to="/programmas" class="btn btn-sm btn-primary">
                <i class="bi bi-plus"></i> Добавить мероприятие
              </router-link>
            </div>
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
              <div class="d-flex gap-2 mt-3">
                <router-link to="/prozhivanies" class="btn btn-sm btn-outline-primary flex-grow-1">
                  Управление
                </router-link>
                <button class="btn btn-sm btn-success flex-grow-1" @click="openSettlementModal()">
                  <i class="bi bi-person-fill-up"></i> Расселение
                </button>
              </div>
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
    
    <!-- Модальное окно расселения -->
    <div class="modal fade modal-xl" ref="settlementModalRef" tabindex="-1">
      <div class="modal-dialog modal-fullscreen-lg-down">
        <div class="modal-content">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title">
              <i class="bi bi-person-fill-up"></i> Расселение участников
            </h5>
            <button type="button" class="btn-close btn-close-white" @click="closeSettlementModal()"></button>
          </div>
          
          <div class="modal-body p-0">
            <div class="row g-0 h-100">
              <!-- ЛЕВАЯ КОЛОНКА: Участники -->
              <div class="col-lg-5 border-end">
                <div class="p-3 border-bottom bg-light">
                  <h6 class="mb-2"><i class="bi bi-people"></i> Участники без проживания</h6>
                  <div class="input-group input-group-sm">
                    <span class="input-group-text"><i class="bi bi-search"></i></span>
                    <input 
                      type="text" 
                      class="form-control" 
                      v-model="settlementSearch"
                      placeholder="Поиск по ФИО, email..."
                      @input="filterAvailableParticipants"
                    >
                  </div>
                  <div class="mt-2 text-muted small">
                    Найдено: {{ filteredAvailableParticipants.length }} из {{ availableParticipants.length }}
                  </div>
                </div>
                
                <div class="participants-list p-2" style="max-height: calc(100vh - 250px); overflow-y: auto;">
                  <div 
                    v-for="participant in filteredAvailableParticipants" 
                    :key="participant.id"
                    class="participant-card mb-2"
                    draggable="true"
                    @dragstart="onDragStart($event, participant)"
                    @dragend="onDragEnd"
                  >
                    <div class="d-flex align-items-center gap-2">
                      <i class="bi bi-grip-vertical text-muted"></i>
                      <div class="flex-grow-1">
                        <div class="fw-semibold">{{ participant.familiya }} {{ participant.name }}</div>
                        <div class="small text-muted">{{ participant.email }}</div>
                        <div v-if="participant.sektsiya_nazvanie" class="small">
                          <span class="badge bg-info text-dark">{{ participant.sektsiya_nazvanie }}</span>
                        </div>
                      </div>
                      <i class="bi bi-arrows-move text-primary"></i>
                    </div>
                  </div>
                  
                  <div v-if="filteredAvailableParticipants.length === 0" class="text-center text-muted py-4">
                    <i class="bi bi-inbox fs-1"></i>
                    <p class="mt-2">Нет доступных участников</p>
                  </div>
                </div>
              </div>
              
              <!-- ПРАВАЯ КОЛОНКА: Проживания -->
              <div class="col-lg-7">
                <div class="p-3 border-bottom bg-light">
                  <h6 class="mb-2"><i class="bi bi-hotel"></i> Варианты проживания</h6>
                  <div class="d-flex gap-2">
                    <select v-model="turbazaFilter" class="form-select form-select-sm" @change="filterAccommodations">
                      <option value="">Все турбазы</option>
                      <option v-for="turbaza in Object.keys(groupedAccommodations)" :key="turbaza" :value="turbaza">
                        {{ turbaza }}
                      </option>
                    </select>
                    <select v-model="categoryFilter" class="form-select form-select-sm" @change="filterAccommodations">
                      <option value="">Все категории</option>
                      <option value="одноместный">Одноместный</option>
                      <option value="двухместный">Двухместный</option>
                      <option value="трёхместный">Трёхместный</option>
                      <option value="люкс">Люкс</option>
                    </select>
                  </div>
                </div>
                
                <div class="accommodations-list p-3" style="max-height: calc(100vh - 250px); overflow-y: auto;">
                  <div 
                    v-for="(turbazaData, turbazaName) in filteredAccommodations" 
                    :key="turbazaName"
                    class="turbaza-section mb-4"
                  >
                    <h6 class="text-primary mb-2">
                      <i class="bi bi-building"></i> {{ turbazaName }}
                    </h6>
                    
                    <div 
                      v-for="(prozhivaniya, category) in turbazaData.categories" 
                      :key="category"
                      class="category-section mb-3"
                    >
                      <div class="d-flex justify-content-between align-items-center mb-2">
                        <span class="badge bg-secondary">{{ category }}</span>
                        <span class="small text-muted">
                          Свободно: {{ getTotalFreePlaces(prozhivaniya) }}
                        </span>
                      </div>
                      
                      <div class="row g-2">
                        <div v-for="proj in prozhivaniya" :key="proj.id" class="col-md-6">
                          <div 
                            class="accommodation-card p-3 border rounded"
                            :class="{
                              'border-success bg-success-subtle': proj.mesta_svobodnye > 0,
                              'border-danger bg-danger-subtle': proj.mesta_svobodnye === 0
                            }"
                            @dragover.prevent="onDragOver($event)"
                            @drop="onDrop($event, proj)"
                          >
                            <div class="d-flex justify-content-between align-items-start mb-2">
                              <div>
                                <div class="fw-semibold">{{ proj.nazvanie }}</div>
                                <div class="small text-muted">{{ proj.stoimost }} ₽/ночь</div>
                              </div>
                              <span 
                                class="badge" 
                                :class="proj.mesta_svobodnye > 0 ? 'bg-success' : 'bg-danger'"
                              >
                                {{ proj.mesta_zanyaty }}/{{ proj.vmestimost }}
                              </span>
                            </div>
                            
                            <!-- Прогресс-бар заполненности -->
                            <div class="progress mb-2" style="height: 6px;">
                              <div 
                                class="progress-bar" 
                                :class="getProgressClass(proj.mesta_zanyaty / proj.vmestimost)"
                                :style="{ width: `${(proj.mesta_zanyaty / proj.vmestimost) * 100}%` }"
                              ></div>
                            </div>
                            
                            <!-- Статус -->
                            <div v-if="proj.mesta_svobodnye === 0" class="text-danger small">
                              <i class="bi bi-x-circle"></i> Нет мест
                            </div>
                            <div v-else class="text-success small">
                              <i class="bi bi-check-circle"></i> {{ proj.mesta_svobodnye }} мест свободно
                            </div>
                            
                            <!-- Подсказка для drag-and-drop -->
                            <div v-if="draggedParticipant && proj.mesta_svobodnye > 0" 
                                 class="mt-2 small text-primary">
                              <i class="bi bi-plus-circle"></i> Перетащите участника сюда
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div v-if="Object.keys(filteredAccommodations).length === 0" 
                       class="text-center text-muted py-4">
                    <i class="bi bi-building-exclamation fs-1"></i>
                    <p class="mt-2">Нет вариантов проживания</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeSettlementModal()">Закрыть</button>
            <button type="button" class="btn btn-outline-primary" @click="refreshSettlementData()">
              <i class="bi bi-arrow-clockwise"></i> Обновить
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { konferentsiyaAPI, uchastnikAPI, sekciyaAPI, dokladAPI, programmaAPI, prozhivanieAPI, transferAPI } from '../services/api'
import axios from 'axios'  // ✅ Добавлен импорт axios
import { Modal } from 'bootstrap'

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
      },
      // Для модального окна участника
      addParticipantModal: null,
      conferenceSections: [],
      newParticipant: {
        familiya: '',
        name: '',
        otchestvo: '',
        email: '',
        telefon: '',
        organizatsiya: '',
        gorod: '',
        sektsiya: null,
        status_uchastnika: 'зарегистрирован',
        konferentsiya: null
      },
      // Для модального окна расселения
      settlementModal: null,
      availableParticipants: [],
      filteredAvailableParticipants: [],
      groupedAccommodations: {},
      filteredAccommodations: {},
      settlementSearch: '',
      turbazaFilter: '',
      categoryFilter: '',
      draggedParticipant: null
    }
  },
  
  computed: {
    sortedProgramItems() {
      return [...this.programItems].sort((a, b) =>
        new Date(a.vremya_nachala) - new Date(b.vremya_nachala)
      )
    },
    
    // Группировка докладов по секциям
    reportsBySection() {
      const groups = {}
      this.reports.forEach(report => {
        const sectionId = report.sektsiya || 'no-section'
        const sectionName = report.sektsiya_nazvanie || 'Без секции'
        if (!groups[sectionId]) {
          groups[sectionId] = {
            sectionId: sectionId,
            sectionName: sectionName,
            reports: []
          }
        }
        groups[sectionId].reports.push(report)
      })
      return Object.values(groups)
    }
  },
  
  mounted() {
    // Инициализация модальных окон
    this.addParticipantModal = new Modal(this.$refs.addParticipantModalRef)
    this.settlementModal = new Modal(this.$refs.settlementModalRef)
    
    this.conferenceId = this.$route.params.id
    this.loadData()
  },
  
  methods: {

    // ========== PDF ПРОГРАММА ==========
  
  async downloadProgramPDF() {
     try {
      const url = `/api/konferentsiyas/${this.conferenceId}/program-pdf/`
      
      // Создаём ссылку для скачивания
      const link = document.createElement('a')
      link.href = url
      link.download = `program_${this.conference.nazvanie}.pdf`
      link.target = '_blank'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      
    } catch (error) {
      console.error('Ошибка скачивания PDF:', error)
      alert('Ошибка при скачивании программы: ' + error.message)
    }
  },
    // ========== ЗАГРУЗКА ДАННЫХ ==========
    
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
    
    async loadConferenceSections() {
      try {
        const response = await sekciyaAPI.getAll(this.conferenceId)
        this.conferenceSections = response.data.results || response.data
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
        this.programItems = all.filter(p => p.program_konferentsiya == this.conferenceId)
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
    
    // ========== ДОБАВЛЕНИЕ УЧАСТНИКА ==========
    
    addParticipantToConference() {
      this.newParticipant = {
        familiya: '',
        name: '',
        otchestvo: '',
        email: '',
        telefon: '',
        organizatsiya: '',
        gorod: '',
        sektsiya: null,
        status_uchastnika: 'зарегистрирован',
        konferentsiya: this.conferenceId
      }
      this.loadConferenceSections()
      this.addParticipantModal.show()
    },
    
    closeAddParticipantModal() {
      this.addParticipantModal.hide()
    },
    
    async saveParticipantToConference() {
      if (!this.newParticipant.familiya || !this.newParticipant.name || !this.newParticipant.email) {
        alert('Заполните обязательные поля: Фамилия, Имя, Email')
        return
      }
      
      try {
        const response = await uchastnikAPI.create({
          ...this.newParticipant,
          konferentsiya: this.conferenceId
        })
        
        this.participants.push(response.data)
        this.stats.participants = this.participants.length
        this.closeAddParticipantModal()
        alert(`Участник "${this.newParticipant.familiya} ${this.newParticipant.name}" добавлен`)
      } catch (error) {
        console.error('Ошибка добавления участника:', error)
        alert('Ошибка: ' + (error.response?.data?.error || error.message))
      }
    },
    
    editParticipant(participant) {
      this.$router.push(`/uchastniks?id=${participant.id}`)
    },
    
    // ========== РАССЕЛЕНИЕ ==========
    
    async openSettlementModal() {
      await this.loadSettlementData()
      this.settlementModal.show()
    },
    
    closeSettlementModal() {
      this.settlementModal.hide()
      this.resetSettlementFilters()
    },
    
    async loadSettlementData() {
  try {
    console.log('Загрузка данных расселения для конференции:', this.conferenceId)
    
    // Загрузка доступных участников
    const participantsResponse = await uchastnikAPI.getAll()
    const allParticipants = participantsResponse.data.results || participantsResponse.data
    
    // Загружаем заселённых участников
    const settledResponse = await axios.get(
      `settlement/available/`,
      { params: { konferentsiya: this.conferenceId } }
    )
    const settledData = settledResponse.data.results || settledResponse.data
    const settledIds = Array.isArray(settledData) ? settledData.map(p => p.id) : []
    
    console.log('Заселённые участники IDs:', settledIds)
    
    // Фильтруем: только участники этой конференции и не заселённые
    this.availableParticipants = allParticipants.filter(p => 
      p.konferentsiya == this.conferenceId && !settledIds.includes(p.id)
    )
    this.filteredAvailableParticipants = [...this.availableParticipants]
    
    console.log('Доступно участников:', this.availableParticipants.length)
    
    // Загрузка вариантов проживания
    const accommodationsResponse = await axios.get(
      `settlement/accommodations/`,
      { params: { konferentsiya: this.conferenceId } }
    )
    
    console.log('Ответ API проживания:', accommodationsResponse.data)
    console.log('Ключи объекта:', Object.keys(accommodationsResponse.data))
    
    this.groupedAccommodations = accommodationsResponse.data
    this.filteredAccommodations = { ...this.groupedAccommodations }
    
    console.log('Вариантов проживания (турбаз):', Object.keys(this.groupedAccommodations).length)
    
  } catch (error) {
    console.error('Ошибка загрузки данных расселения:', error)
    console.error('Ответ сервера:', error.response?.data)
    alert('Не удалось загрузить данные для расселения: ' + error.message)
  }
},
    
    async refreshSettlementData() {
      await this.loadSettlementData()
      alert('Данные обновлены')
    },
    
    resetSettlementFilters() {
      this.settlementSearch = ''
      this.turbazaFilter = ''
      this.categoryFilter = ''
      this.filteredAvailableParticipants = [...this.availableParticipants]
      this.filteredAccommodations = { ...this.groupedAccommodations }
    },
    
    filterAvailableParticipants() {
      const search = this.settlementSearch.toLowerCase()
      this.filteredAvailableParticipants = this.availableParticipants.filter(p =>
        p.familiya.toLowerCase().includes(search) ||
        p.name.toLowerCase().includes(search) ||
        p.email.toLowerCase().includes(search)
      )
    },
    
    filterAccommodations() {
      const filtered = {}
      for (const [turbaza, data] of Object.entries(this.groupedAccommodations)) {
        if (this.turbazaFilter && turbaza !== this.turbazaFilter) continue
        
        const categories = {}
        for (const [category, prozhivaniya] of Object.entries(data.categories)) {
          if (this.categoryFilter && category !== this.categoryFilter) continue
          categories[category] = prozhivaniya
        }
        
        if (Object.keys(categories).length > 0) {
          filtered[turbaza] = { ...data, categories }
        }
      }
      this.filteredAccommodations = filtered
    },
    
    getTotalFreePlaces(prozhivaniya) {
      return prozhivaniya.reduce((sum, p) => sum + p.mesta_svobodnye, 0)
    },
    
    getProgressClass(ratio) {
      if (ratio < 0.5) return 'bg-low'
      if (ratio < 0.9) return 'bg-medium'
      return 'bg-high'
    },
    
    // ========== DRAG AND DROP ==========
    
    onDragStart(event, participant) {
      this.draggedParticipant = participant
      event.dataTransfer.setData('text/plain', participant.id)
      event.dataTransfer.effectAllowed = 'move'
      
      const el = event.target.closest('.participant-card')
      if (el) el.classList.add('dragging')
    },
    
    onDragEnd(event) {
      const el = event.target.closest('.participant-card')
      if (el) el.classList.remove('dragging')
      this.draggedParticipant = null
    },
    
    onDragOver(event) {
      event.preventDefault()
      event.dataTransfer.dropEffect = 'move'
      
      const el = event.target.closest('.accommodation-card')
      if (el && !el.classList.contains('drag-over')) {
        el.classList.add('drag-over')
      }
    },
    
    async onDrop(event, prozhivanie) {
      event.preventDefault()
      
      const cards = document.querySelectorAll('.accommodation-card')
      cards.forEach(card => card.classList.remove('drag-over'))
      
      if (!this.draggedParticipant) return
      
      // Проверка: есть ли места?
      if (prozhivanie.mesta_svobodnye <= 0) {
        alert('В этом варианте проживания нет свободных мест!')
        return
      }
      
      // Подтверждение
      const confirmMsg = `Заселить ${this.draggedParticipant.familiya} ${this.draggedParticipant.name} в "${prozhivanie.nazvanie}"?`
      if (!confirm(confirmMsg)) return
      
      try {
        console.log('Заселение участника:', this.draggedParticipant.id, 'в проживание:', prozhivanie.id)
        
        const response = await axios.post(
          `settlement/settle/`,
          {
            uchastnik_id: this.draggedParticipant.id,
            prozhivanie_id: prozhivanie.id
          }
        )
        
        const result = response.data
        
        if (result.success) {
          alert(result.message)
          
          // Обновляем счётчик в карточке проживания
          prozhivanie.mesta_zanyaty = result.prozhivanie.mesta_zanyaty
          prozhivanie.mesta_svobodnye = result.prozhivanie.mesta_svobodnye
          
          // Удаляем участника из списка доступных
          this.availableParticipants = this.availableParticipants.filter(
            p => p.id !== this.draggedParticipant.id
          )
          this.filteredAvailableParticipants = this.filteredAvailableParticipants.filter(
            p => p.id !== this.draggedParticipant.id
          )
          
          // Обновляем статистику
          this.stats.accommodation++
          
          console.log('Участник успешно заселён')
        } else {
          alert('Ошибка: ' + (result.error || 'Неизвестная ошибка'))
        }
        
      } catch (error) {
        console.error('Ошибка заселения:', error)
        console.error('Ответ сервера:', error.response?.data)
        alert('Ошибка при заселении участника: ' + (error.response?.data?.error || error.message))
      }
      
      this.draggedParticipant = null
    },
    
    // ========== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ==========
    
    getSectionReportsCount(sectionId) {
      return this.reports.filter(r => r.sektsiya == sectionId).length
    },
    
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU')
    },
    
    formatTime(datetime) {
      if (!datetime) return ''
      return new Date(datetime).toLocaleTimeString('ru-RU', {
        hour: '2-digit',
        minute: '2-digit'
      })
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

.section-group {
  background: #f8f9fa;
  border-radius: 10px;
  padding: 15px;
  margin-bottom: 20px;
}

.section-group-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 1px solid #dee2e6;
}

.section-group-header i {
  font-size: 20px;
  color: #3498db;
}

.section-group-header h6 {
  margin: 0;
  color: #2c3e50;
  font-weight: 600;
}

.section-group .table {
  margin: 0;
  font-size: 14px;
}

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

/* Стили для drag-and-drop расселения */
.participant-card {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 8px;
  padding: 12px;
  cursor: grab;
  transition: all 0.2s ease;
}

.participant-card:hover {
  border-color: #3498db;
  box-shadow: 0 2px 8px rgba(52, 152, 219, 0.15);
}

.participant-card:active {
  cursor: grabbing;
}

.participant-card.dragging {
  opacity: 0.6;
  transform: scale(0.98);
}

.accommodation-card {
  background: white;
  transition: all 0.2s ease;
  cursor: pointer;
}

.accommodation-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.accommodation-card.drag-over {
  border-color: #27ae60 !important;
  background: #d4edda !important;
  transform: scale(1.02);
}

.progress-bar.bg-low { background: #27ae60 !important; }
.progress-bar.bg-medium { background: #f39c12 !important; }
.progress-bar.bg-high { background: #e74c3c !important; }

.participants-list {
  background: #f8f9fa;
}

.accommodations-list {
  background: #fff;
}

@media (max-width: 992px) {
  .modal-fullscreen-lg-down .modal-dialog {
    max-width: 100%;
    margin: 0;
  }
  
  .modal-fullscreen-lg-down .modal-content {
    border-radius: 0;
    height: 100vh;
  }
}
</style>