<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">
        <i class="bi bi-people"></i>
        Участники
      </h1>
      <div class="header-buttons">
        <button class="btn btn-success me-2" @click="openImportModal()">
          <i class="bi bi-file-earmark-excel"></i>
          Импорт Excel
        </button>
        <button class="btn btn-primary" @click="openModal()">
          <i class="bi bi-plus-lg"></i>
          Добавить
        </button>
      </div>
    </div>

    <div class="filters-bar">
      <div class="search-box">
        <i class="bi bi-search"></i>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Поиск по фамилии, имени, email..."
          @input="fetchData"
        >
      </div>
      <select v-model="statusFilter" @change="fetchData" class="form-select">
        <option value="">Все статусы</option>
        <option value="зарегистрирован">Зарегистрирован</option>
        <option value="подтвердил участие">Подтвердил участие</option>
        <option value="оплатил">Оплатил</option>
        <option value="не оплатил">Не оплатил</option>
        <option value="отказался">Отказался</option>
      </select>
      <select v-model="konferentsiyaFilter" @change="fetchData" class="form-select">
        <option value="">Все конференции</option>
        <option v-for="konf in konferentsiyas" :key="konf.id" :value="konf.id">
          {{ konf.nazvanie }}
        </option>
      </select>
    </div>

    <div class="table-container">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>ФИО</th>
            <th>Email</th>
            <th>Организация</th>
            <th>Город</th>
            <th>Номер телефона</th>
            <th>Статус</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.familiya }} {{ item.name }} {{ item.otchestvo }}</td>
            <td>{{ item.email }}</td>
            <td>{{ item.organizatsiya }}</td>
            <td>{{ item.gorod }}</td>
            <td>{{ item.telefon }}</td>
            <td>
              <span :class="['status-badge', 'status-' + item.status_uchastnika]">
                {{ getStatusLabel(item.status_uchastnika) }}
              </span>
            </td>
            <td>{{ item.konferentsiya_nazvanie }}</td>
            <td class="text-end">
              <button class="btn btn-sm btn-outline-primary me-1" @click="editItem(item)">
                <i class="bi bi-pencil"></i>
              </button>
              <button class="btn btn-sm btn-outline-danger" @click="deleteItem(item.id)">
                <i class="bi bi-trash"></i>
              </button>
            </td>
          </tr>
          <tr v-if="items.length === 0">
            <td colspan="7" class="text-center text-muted py-4">
              Нет данных
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Модальное окно добавления/редактирования участника -->
    <div class="modal fade" ref="modalRef" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEdit ? 'Редактировать' : 'Добавить' }} участника</h5>
            <button type="button" class="btn-close" @click="closeModal()"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveItem()">
              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label">Фамилия *</label>
                  <input type="text" class="form-control" v-model="form.familiya" required>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Имя *</label>
                  <input type="text" class="form-control" v-model="form.name" required>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Отчество</label>
                  <input type="text" class="form-control" v-model="form.otchestvo">
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Email *</label>
                  <input type="email" class="form-control" v-model="form.email" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Телефон</label>
                  <input type="text" class="form-control" v-model="form.telefon">
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Организация</label>
                  <input type="text" class="form-control" v-model="form.organizatsiya">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Город</label>
                  <input type="text" class="form-control" v-model="form.gorod">
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Должность</label>
                  <input type="text" class="form-control" v-model="form.doljnost">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Ученая степень</label>
                  <input type="text" class="form-control" v-model="form.uchenaya_stepen">
                </div>
              </div>
              <div class="row">
                <div class="col-md-4 mb-3">
                  <label class="form-label">Конференция *</label>
                  <select class="form-select" v-model="form.konferentsiya" required>
                    <option v-for="konf in konferentsiyas" :key="konf.id" :value="konf.id">
                      {{ konf.nazvanie }}
                    </option>
                  </select>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Секция</label>
                  <select class="form-select" v-model="form.sektsiya">
                    <option v-for="sek in sekciyas" :key="sek.id" :value="sek.id">
                      {{ sek.nazvanie }}
                    </option>
                  </select>
                </div>
                <div class="col-md-4 mb-3">
                  <label class="form-label">Статус *</label>
                  <select class="form-select" v-model="form.status_uchastnika" required>
                    <option value="зарегистрирован">Зарегистрирован</option>
                    <option value="подтвердил участие">Подтвердил участие</option>
                    <option value="оплатил">Оплатил</option>
                    <option value="не оплатил">Не оплатил</option>
                    <option value="отказался">Отказался</option>
                  </select>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Нужен трансфер</label>
                  <select class="form-select" v-model="form.nuzhen_transfer">
                    <option :value="false">Нет</option>
                    <option :value="true">Да</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Комментарии</label>
                  <input type="text" class="form-control" v-model="form.kommentarii">
                </div>
              </div>
              <div class="modal-footer px-0 pb-0">
                <button type="button" class="btn btn-secondary" @click="closeModal()">Отмена</button>
                <button type="submit" class="btn btn-primary">Сохранить</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно импорта Excel -->
    <div class="modal fade" ref="importModalRef" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="bi bi-file-earmark-excel"></i>
              Импорт участников из Excel
            </h5>
            <button type="button" class="btn-close" @click="closeImportModal()"></button>
          </div>
          <div class="modal-body">
            <div class="alert alert-info">
              <i class="bi bi-info-circle"></i>
              <strong>Требования к файлу:</strong>
              <ul class="mb-0 mt-2">
                <li>Формат: .xlsx</li>
                <li>Обязательные колонки: Фамилия, E-mail</li>
                <li>Порядок: №, Дата подачи, Конференция, Статус, Комментарий, Фамилия, Имя, Отчество, Организация, Город, Учёная степень, Должность, Телефон, E-mail, Секция</li>
                <li>Статус "Одобрена" → подтвердил участие</li>
                <li>Секции и конференции создаются автоматически</li>
              </ul>
            </div>
            
            <div class="mb-3">
              <label class="form-label">Выберите файл *</label>
              <input type="file" class="form-control" accept=".xlsx" @change="onFileSelect" ref="fileInput">
            </div>
            
            <div v-if="importStatus" :class="['alert', importStatus.success ? 'alert-success' : 'alert-danger']">
              <div v-if="importStatus.success">
                <i class="bi bi-check-circle"></i>
                <strong>Успешно!</strong> Импортировано: {{ importStatus.imported }} участников, 
                создано секций: {{ importStatus.sections_created }}, 
                создано конференций: {{ importStatus.conferences_created }}
              </div>
              <div v-else>
                <i class="bi bi-x-circle"></i>
                <strong>Ошибка:</strong> {{ importStatus.error }}
              </div>
            </div>
            
            <div v-if="importStatus && importStatus.errors && importStatus.errors.length > 0" class="alert alert-warning">
              <i class="bi bi-exclamation-triangle"></i>
              <strong>Ошибки:</strong>
              <ul class="mb-0 mt-2">
                <li v-for="(error, idx) in importStatus.errors" :key="idx">{{ error }}</li>
              </ul>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" @click="closeImportModal()">Отмена</button>
            <button type="button" class="btn btn-success" @click="uploadFile()" :disabled="!selectedFile || isUploading">
              <i class="bi bi-upload"></i>
              {{ isUploading ? 'Загрузка...' : 'Импортировать' }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { uchastnikAPI, konferentsiyaAPI, sekciyaAPI, importAPI } from '../services/api'
import { Modal } from 'bootstrap'

export default {
  name: 'UchastnikList',
  data() {
    return {
      items: [],
      konferentsiyas: [],
      sekciyas: [],
      searchQuery: '',
      statusFilter: '',
      konferentsiyaFilter: '',
      form: {
        id: null,
        familiya: '',
        name: '',
        otchestvo: '',
        email: '',
        telefon: '',
        organizatsiya: '',
        gorod: '',
        doljnost: '',
        uchenaya_stepen: '',
        konferentsiya: null,
        sektsiya: null,
        status_uchastnika: 'зарегистрирован',
        nuzhen_transfer: false,
        kommentarii: ''
      },
      isEdit: false,
      modal: null,
      importModal: null,
      selectedFile: null,
      importStatus: null,
      isUploading: false
    }
  },
  mounted() {
    this.modal = new Modal(this.$refs.modalRef)
    this.importModal = new Modal(this.$refs.importModalRef)
    this.fetchData()
    this.loadKonferentsiyas()
    this.loadSekciyas()
  },
  methods: {
    async fetchData() {
      try {
        const response = await uchastnikAPI.getAll()
        let data = response.data.results || response.data
        if (this.searchQuery) {
          data = data.filter(item => 
            item.familiya.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            item.name.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            item.email.toLowerCase().includes(this.searchQuery.toLowerCase())
          )
        }
        if (this.statusFilter) {
          data = data.filter(item => item.status_uchastnika === this.statusFilter)
        }
        if (this.konferentsiyaFilter) {
          data = data.filter(item => item.konferentsiya === this.konferentsiyaFilter)
        }
        this.items = data
      } catch (error) {
        console.error('Ошибка загрузки:', error)
        alert('Не удалось загрузить данные')
      }
    },
    async loadKonferentsiyas() {
      try {
        const response = await konferentsiyaAPI.getAll()
        this.konferentsiyas = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки конференций:', error)
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
    getStatusLabel(status) {
      const labels = {
        'зарегистрирован': 'Зарегистрирован',
        'подтвердил участие': 'Подтвердил участие',
        'оплатил': 'Оплатил',
        'не оплатил': 'Не оплатил',
        'отказался': 'Отказался'
      }
      return labels[status] || status
    },
    openModal(item = null) {
      this.isEdit = !!item
      if (item) {
        this.form = { ...item }
      } else {
        this.form = {
          id: null,
          familiya: '',
          name: '',
          otchestvo: '',
          email: '',
          telefon: '',
          organizatsiya: '',
          gorod: '',
          doljnost: '',
          uchenaya_stepen: '',
          konferentsiya: null,
          sektsiya: null,
          status_uchastnika: 'зарегистрирован',
          nuzhen_transfer: false,
          kommentarii: ''
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
          await uchastnikAPI.update(this.form.id, this.form)
        } else {
          await uchastnikAPI.create(this.form)
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
      if (!confirm('Удалить участника?')) return
      try {
        await uchastnikAPI.delete(id)
        this.fetchData()
        alert('Удалено')
      } catch (error) {
        console.error('Ошибка удаления:', error)
        alert('Ошибка при удалении')
      }
    },
    openImportModal() {
      this.selectedFile = null
      this.importStatus = null
      this.isUploading = false
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
      this.importModal.show()
    },
    closeImportModal() {
      this.importModal.hide()
    },
    onFileSelect(event) {
      this.selectedFile = event.target.files[0]
      this.importStatus = null
    },
    async uploadFile() {
      if (!this.selectedFile) {
        alert('Выберите файл')
        return
      }
      
      this.isUploading = true
      this.importStatus = null
      
      try {
        const response = await importAPI.participants(this.selectedFile)
        this.importStatus = response.data
        
        if (response.data.success) {
          setTimeout(() => {
            this.closeImportModal()
            this.fetchData()
          }, 2000)
        }
      } catch (error) {
        console.error('Ошибка импорта:', error)
        this.importStatus = {
          success: false,
          error: error.response?.data?.error || 'Ошибка при импорте'
        }
      } finally {
        this.isUploading = false
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

.header-buttons {
  display: flex;
  gap: 10px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.page-title {
  font-size: 24px;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
}

.page-title i {
  font-size: 26px;
  color: #3498db;
}

.filters-bar {
  display: flex;
  gap: 16px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 250px;
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
  width: 100%;
}

.table-container {
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  overflow: hidden;
}

.table {
  margin: 0;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 500;
}

.status-зарегистрирован {
  background: #e3f2fd;
  color: #1976d2;
}

.status-подтвердил участие {
  background: #e8f5e9;
  color: #388e3c;
}

.status-оплатил {
  background: #fff3e0;
  color: #f57c00;
}

.status-не оплатил {
  background: #ffebee;
  color: #c62828;
}

.status-отказался {
  background: #f5f5f5;
  color: #616161;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>