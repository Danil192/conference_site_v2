<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">
        <i class="bi bi-calendar-week"></i>
        Расписание конференции
      </h1>
      <div class="header-actions d-flex gap-2">
        <button 
          v-if="programFilter" 
          class="btn btn-outline-danger" 
          @click="downloadProgramPDF()"
        >
          <i class="bi bi-file-earmark-pdf"></i>
          Скачать PDF
        </button>

        <button class="btn btn-primary" @click="openModal()">
          <i class="bi bi-plus-lg"></i>
          Добавить мероприятие
        </button>
      </div>
    </div>

    <!-- Фильтры -->
    <div class="filters-bar shadow-sm p-4 bg-white rounded-3 mb-4">
      <div class="row g-4 align-items-end">
        
        <!-- 1. Поиск: Уменьшаем до 3 (был 5) -->
        <div class="col-md-3">
          <label class="form-label small fw-bold text-muted mb-2">
            <i class="bi bi-search me-1"></i> Поиск
          </label>
          <div class="search-box">
            <i class="bi bi-search"></i>
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Доклад..."
              @input="fetchData"
              class="form-control form-control-custom"
            >
          </div>
        </div>

        <!-- 2. Программа: Увеличиваем до 6 (был 3). Теперь это поле самое широкое -->
        <div class="col-md-6">
          <label class="form-label small fw-bold text-muted mb-2">Программа (Мероприятие)</label>
          <select v-model="programFilter" @change="fetchData" class="form-select form-select-custom">
            <option value="">Все программы</option>
            <option v-for="prog in programs" :key="prog.id" :value="prog.id">
              {{ prog.nazvanie }}
            </option>
          </select>
        </div>

        <!-- 3. Секция: Оставляем 3 (был 4) -->
        <div class="col-md-3">
          <label class="form-label small fw-bold text-muted mb-2">Секция</label>
          <select v-model="sekciyaFilter" @change="fetchData" class="form-select form-select-custom">
            <option value="">Все секции</option>
            <option v-for="sek in sekciyas" :key="sek.id" :value="sek.id">
              {{ sek.nazvanie }}
            </option>
          </select>
        </div>
        
      </div>
    </div>

    <!-- Группированное расписание -->
    <div class="schedule-body">
      <div v-if="Object.keys(groupedSchedule).length > 0">
        <div v-for="(sections, date) in groupedSchedule" :key="date" class="day-block mb-5">
          <div class="day-header d-flex align-items-center mb-3">
            <div class="day-badge me-3">
              <i class="bi bi-calendar-check"></i>
            </div>
            <h2 class="h4 mb-0 text-primary fw-bold">{{ date }}</h2>
          </div>

          <div v-for="(events, sectionName) in sections" :key="sectionName" class="section-block ms-4 mb-4">
            <h3 class="h6 text-uppercase fw-bold text-muted mb-3 border-start border-3 border-primary ps-2">
              {{ sectionName }}
            </h3>

            <div class="table-container shadow-sm bg-white rounded-3">
              <table class="table table-hover align-middle mb-0">
                <thead class="table-light">
                  <tr>
                    <th style="width: 15%">Время</th>
                    <th style="width: 40%">Тема доклада / Мероприятие</th>
                    <th style="width: 25%">Докладчик</th>
                    <th style="width: 10%">Зал</th>
                    <th style="width: 10%" class="text-end">Действия</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in events" :key="item.id" :class="{'table-info': item.ne_vystupaet}">
                    <td>
                      <div class="fw-bold text-dark">{{ formatTime(item.vremya_nachala) }}</div>
                      <div class="small text-muted">{{ formatTime(item.vremya_okonchaniya) }}</div>
                    </td>
                    <td>
                      <div class="fw-semibold">{{ item.doklad_nazvanie || 'Технический перерыв' }}</div>
                      <span v-if="item.ne_vystupaet" class="badge bg-warning text-dark small">Без выступления</span>
                    </td>
                    <td>
                      <div v-if="item.uchastnik_fio">
                        <i class="bi bi-person-circle text-secondary me-1"></i>
                        {{ item.uchastnik_fio }}
                      </div>
                      <span v-else class="text-muted">—</span>
                    </td>
                    <td>
                      <span v-if="item.pomeshchenie" class="badge bg-light text-dark border">
                        <i class="bi bi-geo-alt me-1"></i>{{ item.pomeshchenie }}
                      </span>
                      <span v-else class="text-muted">—</span>
                    </td>
                    <td class="text-end">
                      <div class="btn-group">
                        <button class="btn btn-sm btn-outline-primary" @click="editItem(item)">
                          <i class="bi bi-pencil"></i>
                        </button>
                        <button class="btn btn-sm btn-outline-danger" @click="deleteItem(item.id)">
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Пустое состояние -->
      <div v-else class="empty-state text-center py-5 bg-white rounded-3 shadow-sm">
        <i class="bi bi-calendar-x display-1 text-muted opacity-25"></i>
        <h3 class="mt-3 text-muted">Расписание не найдено</h3>
        <p>Попробуйте сбросить фильтры или добавьте новое мероприятие</p>
      </div>
    </div>

    <!-- Модальное окно (без изменений) -->
    <div class="modal fade" ref="modalRef" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content border-0 shadow">
          <div class="modal-header bg-primary text-white">
            <h5 class="modal-title"><i class="bi bi-clock-history me-2"></i> Редактирование</h5>
            <button type="button" class="btn-close btn-close-white" @click="closeModal()"></button>
          </div>
          <div class="modal-body p-4">
            <form @submit.prevent="saveItem()">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold">Программа *</label>
                  <select class="form-select" v-model="form.program" required>
                    <option v-for="prog in programs" :key="prog.id" :value="prog.id">{{ prog.nazvanie }}</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold">Секция</label>
                  <select class="form-select" v-model="form.sekciya">
                    <option :value="null">Общая (без секции)</option>
                    <option v-for="sek in sekciyas" :key="sek.id" :value="sek.id">{{ sek.nazvanie }}</option>
                  </select>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold">Доклад</label>
                  <select class="form-select" v-model="form.doklad">
                    <option :value="null">Без доклада</option>
                    <option v-for="dok in doklads" :key="dok.id" :value="dok.id">{{ dok.nazvanie }}</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold">Участник</label>
                  <select class="form-select" v-model="form.uchastnik">
                    <option :value="null">Не указан</option>
                    <option v-for="uch in uchastniks" :key="uch.id" :value="uch.id">{{ uch.familiya }} {{ uch.name }}</option>
                  </select>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold">Время начала *</label>
                  <input type="datetime-local" class="form-control" v-model="form.vremya_nachala" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold">Время окончания *</label>
                  <input type="datetime-local" class="form-control" v-model="form.vremya_okonchaniya" required>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold">Помещение</label>
                  <input type="text" class="form-control" v-model="form.pomeshchenie">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label fw-bold">Порядок (№)</label>
                  <input type="number" class="form-control" v-model="form.nomer_v_programme">
                </div>
              </div>
              <div class="modal-footer px-0 pb-0 pt-3">
                <button type="button" class="btn btn-light" @click="closeModal()">Отмена</button>
                <button type="submit" class="btn btn-primary">Сохранить</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { programmaAPI, programAPI, sekciyaAPI, dokladAPI, uchastnikAPI } from '../services/api'
import { Modal } from 'bootstrap'

export default {
  name: 'ProgrammaList',
  data() {
    return {
      items: [],
      programs: [],
      sekciyas: [],
      doklads: [],
      uchastniks: [],
      searchQuery: '',
      programFilter: '',
      sekciyaFilter: '',
      form: {
        id: null,
        program: null,
        doklad: null,
        uchastnik: null,
        sekciya: null,
        vremya_nachala: '',
        vremya_okonchaniya: '',
        nomer_v_programme: 1,
        ne_vystupaet: false,
        pomeshchenie: ''
      },
      isEdit: false,
      modal: null
    }
  },

  // ВЫЧИСЛЯЕМЫЕ СВОЙСТВА ДОЛЖНЫ БЫТЬ ОТДЕЛЬНО ОТ METHODS
  computed: {
    groupedSchedule() {
      if (!this.items || !this.items.length) return {};

      const groups = {};

      // 1. Сортируем все элементы по времени начала
      const sorted = [...this.items].sort((a, b) => new Date(a.vremya_nachala) - new Date(b.vremya_nachala));

      sorted.forEach(item => {
        // Создаем ключ даты (например: "12 октября 2024")
        // Используем UTC, чтобы время не съезжало
        const dateObj = new Date(item.vremya_nachala);
        const dateKey = dateObj.toLocaleDateString('ru-RU', {
          day: 'numeric',
          month: 'long',
          year: 'numeric',
          timeZone: 'UTC'
        });

        const sectionKey = item.sekciya_nazvanie || 'Общая программа';

        if (!groups[dateKey]) groups[dateKey] = {};
        if (!groups[dateKey][sectionKey]) groups[dateKey][sectionKey] = [];

        groups[dateKey][sectionKey].push(item);
      });

      return groups;
    }
  },

  mounted() {
    this.modal = new Modal(this.$refs.modalRef)
    this.fetchData()
    this.loadPrograms()
    this.loadSekciyas()
    this.loadDoklads()
    this.loadUchastniks()
  },

  methods: {
    async fetchData() {
      try {
        const response = await programmaAPI.getAll()
        let data = response.data.results || response.data
        if (this.searchQuery) {
          const q = this.searchQuery.toLowerCase()
          data = data.filter(item => 
            (item.doklad_nazvanie && item.doklad_nazvanie.toLowerCase().includes(q)) ||
            (item.uchastnik_fio && item.uchastnik_fio.toLowerCase().includes(q))
          )
        }
        if (this.programFilter) {
          data = data.filter(item => item.program === this.programFilter)
        }
        if (this.sekciyaFilter) {
          data = data.filter(item => item.sekciya === this.sekciyaFilter)
        }
        this.items = data
      } catch (error) {
        console.error('Ошибка загрузки:', error)
      }
    },

    async downloadProgramPDF() {
      if (!this.programFilter) return;

      // Находим выбранную программу в массиве, чтобы узнать ID её конференции
      const selectedProgram = this.programs.find(p => p.id === this.programFilter);
      
      if (!selectedProgram || !selectedProgram.konferentsiya) {
        alert('Не удалось определить конференцию для этой программы');
        return;
      }

      const confId = selectedProgram.konferentsiya;

      try {
        // Формируем прямую ссылку на API генерации PDF
        const url = `http://localhost:8000/api/konferentsiyas/${confId}/program-pdf/`;
        
        // Открываем в новой вкладке для скачивания
        window.open(url, '_blank');
      } catch (error) {
        console.error('Ошибка скачивания PDF:', error);
        alert('Ошибка при генерации PDF');
      }
    },

    async loadPrograms() {
      try {
        const response = await programAPI.getAll()
        this.programs = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки программ:', error)
      }
    },

    async loadSekciyas() {
      try {
        const response = await sekciyaAPI.getAll()
        this.sekciyas = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки секций:', error)
      }
    },

    async loadDoklads() {
      try {
        const response = await dokladAPI.getAll()
        this.doklads = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки докладов:', error)
      }
    },

    async loadUchastniks() {
      try {
        const response = await uchastnikAPI.getAll()
        this.uchastniks = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки участников:', error)
      }
    },

    formatTime(datetime) {
      if (!datetime) return '';
      const date = new Date(datetime);
      // Используем UTC методы, чтобы 16:35 не превращалось в 00:35
      const hours = String(date.getUTCHours()).padStart(2, '0');
      const minutes = String(date.getUTCMinutes()).padStart(2, '0');
      return `${hours}:${minutes}`;
    },

    openModal(item = null) {
      this.isEdit = !!item
      if (item) {
        this.form = { ...item }
        if (item.vremya_nachala) {
          this.form.vremya_nachala = item.vremya_nachala.slice(0, 16)
        }
        if (item.vremya_okonchaniya) {
          this.form.vremya_okonchaniya = item.vremya_okonchaniya.slice(0, 16)
        }
      } else {
        this.form = {
          id: null,
          program: null,
          doklad: null,
          uchastnik: null,
          sekciya: null,
          vremya_nachala: '',
          vremya_okonchaniya: '',
          nomer_v_programme: 1,
          ne_vystupaet: false,
          pomeshchenie: ''
        }
      }
      this.modal.show()
    },

    closeModal() {
      this.modal.hide()
    },

    editItem(item) {
      this.openModal(item)
    },

    async saveItem() {
      try {
        if (this.isEdit) {
          await programmaAPI.update(this.form.id, this.form)
        } else {
          await programmaAPI.create(this.form)
        }
        this.closeModal()
        this.fetchData()
        alert('Сохранено успешно')
      } catch (error) {
        console.error('Ошибка сохранения:', error)
        alert('Ошибка при сохранении')
      }
    },

    async deleteItem(id) {
      if (!confirm('Удалить из расписания?')) return
      try {
        await programmaAPI.delete(id)
        this.fetchData()
        alert('Удалено')
      } catch (error) {
        console.error('Ошибка удаления:', error)
        alert('Ошибка при удалении')
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
}

/* ГЛАВНЫЙ ФИКС: Убрали flex, используем только shadow и отступы */
.filters-section {
  border: 1px solid rgba(0,0,0,0.05);
}

.search-box {
  position: relative;
  width: 100%;
}

.search-box i {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #adb5bd;
}

.search-box input {
  padding-left: 38px;
  width: 100%; /* Теперь инпут не вылезет за границы своей col-md-3 */
}

.form-control-custom, .form-select-custom {
  border: 1px solid #dee2e6;
  height: 42px;
}

.form-select-custom {
  cursor: pointer;
}

.day-badge {
  width: 40px;
  height: 40px;
  background: #0d6efd;
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.table-container {
  background: white;
  border-radius: 10px;
  overflow: hidden;
}

.section-block {
  border-left: 1px dashed #dee2e6;
  padding-left: 20px;
}
</style>