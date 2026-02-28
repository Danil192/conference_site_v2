<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">
        <i class="bi bi-file-earmark-text"></i>
        Доклады
      </h1>
      <button class="btn btn-primary" @click="openModal()">
        <i class="bi bi-plus-lg"></i>
        Добавить
      </button>
    </div>

    <div class="filters-bar">
      <div class="search-box">
        <i class="bi bi-search"></i>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Поиск по названию доклада..."
          @input="fetchData"
        >
      </div>
      <select v-model="statusFilter" @change="fetchData" class="form-select">
        <option value="">Все статусы</option>
        <option value="на рассмотрении">На рассмотрении</option>
        <option value="принят">Принят</option>
        <option value="отклонен">Отклонен</option>
        <option value="отложен">Отложен</option>
      </select>

      <select v-model="konferentsiyaFilter" @change="fetchData" class="form-select">
        <option value="">Все конференции</option>
        <option v-for="konf in allKonferentsiyas" :key="konf.id" :value="konf.id">
          {{ konf.nazvanie }}
        </option>
      </select>
    </div>

    <div class="table-container">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>Название</th>
            <th>Автор</th>
            <th>Конференция</th>
            <th>Секция</th>
            <th>Статус</th>
            <th>Дата подачи</th>
            <th class="text-end">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.nazvanie }}</td>
            <td>{{ item.uchastnik_fio }}</td>
            <td>{{ item.konferentsiya_nazvanie }}</td>
            <td>
              <span v-if="item.sektsiya_nazvanie" class="badge bg-info">
                {{ item.sektsiya_nazvanie }}
              </span>
              <span v-else class="text-muted">—</span>
            </td>
            <td>
              <span :class="['status-badge', 'status-' + item.status_doklada]">
                {{ getStatusLabel(item.status_doklada) }}
              </span>
            </td>
            <td>{{ formatDate(item.data_podachi) }}</td>
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

    <div class="modal fade" ref="modalRef" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEdit ? 'Редактировать' : 'Добавить' }} доклад</h5>
            <button type="button" class="btn-close" @click="closeModal()"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveItem()">
              <div class="mb-3">
                <label class="form-label">Название *</label>
                <input type="text" class="form-control" v-model="form.nazvanie" required>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Участник *</label>
                  <select class="form-select" v-model="form.uchastnik" required>
                    <option v-for="uch in uchastniks" :key="uch.id" :value="uch.id">
                      {{ uch.familiya }} {{ uch.name }} {{ uch.otchestvo }}
                    </option>
                  </select>
                </div>
                
                <div class="col-md-6 mb-3">
                  <label class="form-label">Конференция *</label>
                  <select 
                    class="form-select" 
                    v-model="form.konferentsiya" 
                    required
                    @change="onConferenceChange"
                  >
                    <option value="" disabled>Выберите конференцию</option>
                    <option v-for="konf in allKonferentsiyas" :key="konf.id" :value="konf.id">
                      {{ konf.nazvanie }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="row">
             
                <div class="col-md-6 mb-3">
                  <label class="form-label">Секция</label>
                  <select class="form-select" v-model="form.sektsiya">
                    <option value="">Не выбрана</option>
                    <option 
                      v-for="sek in filteredSekciyas" 
                      :key="sek.id" 
                      :value="sek.id"
                    >
                      {{ sek.nazvanie }}
                    </option>
                  </select>
                  <div class="form-text">
                    Секции отображаются только для выбранной конференции
                  </div>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Статус *</label>
                  <select class="form-select" v-model="form.status_doklada" required>
                    <option value="на рассмотрении">На рассмотрении</option>
                    <option value="принят">Принят</option>
                    <option value="отклонен">Отклонен</option>
                    <option value="отложен">Отложен</option>
                  </select>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Выступает</label>
                <select class="form-select" v-model="form.vystupaet">
                  <option :value="true">Да</option>
                  <option :value="false">Нет</option>
                </select>
              </div>
              
              <!-- Загрузка файла -->
              <div class="mb-3">
                <label class="form-label">Файл доклада</label>
                <div class="alert alert-info" v-if="isEdit && currentFileUrl">
                  <i class="bi bi-info-circle"></i>
                  Текущий файл: 
                  <a :href="currentFileUrl" target="_blank" class="ms-1">
                    <i class="bi bi-download"></i> Скачать текущий файл
                  </a>
                </div>
                <input 
                  type="file" 
                  class="form-control" 
                  @change="onFileSelect"
                  accept=".pdf,.doc,.docx,.ppt,.pptx,.odt,.ods,.odp"
                  ref="fileInput"
                >
                <div class="form-text">
                  Допустимые форматы: PDF, DOC, DOCX, PPT, PPTX (макс. 10MB)
                </div>
                <div v-if="selectedFile" class="alert alert-success mt-2">
                  <i class="bi bi-check-circle"></i>
                  Выбран файл: {{ selectedFile.name }} ({{ formatFileSize(selectedFile.size) }})
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
  </div>
</template>

<script>
import { dokladAPI, uchastnikAPI, konferentsiyaAPI, sekciyaAPI } from '../services/api'
import { Modal } from 'bootstrap'

export default {
  name: 'DokladList',
  data() {
    return {
      items: [],
      uchastniks: [],
      allKonferentsiyas: [],  
      allSekciyas: [],         
      searchQuery: '',
      statusFilter: '',
      konferentsiyaFilter: '', 
      form: {
        id: null,
        nazvanie: '',
        uchastnik: null,
        konferentsiya: null,   
        sektsiya: null,        
        status_doklada: 'на рассмотрении',
        vystupaet: true
      },
      selectedFile: null,
      currentFileUrl: null,
      isEdit: false,
      modal: null
    }
  },
  computed: {
 
    filteredSekciyas() {
      if (!this.form.konferentsiya) {
        return []
      }
      return this.allSekciyas.filter(sek => sek.konferentsiya == this.form.konferentsiya)
    }
  },
  mounted() {
    this.modal = new Modal(this.$refs.modalRef)
    this.fetchData()
    this.loadUchastniks()
    this.loadKonferentsiyas()
    this.loadSekciyas()  
  },
  methods: {
    async fetchData() {
      try {
        const response = await dokladAPI.getAll()
        let data = response.data.results || response.data
        
        // Фильтрация по поиску
        if (this.searchQuery) {
          data = data.filter(item => 
            item.nazvanie.toLowerCase().includes(this.searchQuery.toLowerCase())
          )
        }
        // Фильтрация по статусу
        if (this.statusFilter) {
          data = data.filter(item => item.status_doklada === this.statusFilter)
        }
     
        if (this.konferentsiyaFilter) {
          data = data.filter(item => item.konferentsiya == this.konferentsiyaFilter)
        }
        this.items = data
      } catch (error) {
        console.error('Ошибка загрузки:', error)
        alert('Не удалось загрузить данные')
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
    async loadKonferentsiyas() {
      try {
        const response = await konferentsiyaAPI.getAll()
        this.allKonferentsiyas = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки конференций:', error)
      }
    },
    async loadSekciyas() {
      try {
        const response = await sekciyaAPI.getAll()
        this.allSekciyas = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки секций:', error)
      }
    },
   
    onConferenceChange() {
   
      this.form.sektsiya = null
    },
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU')
    },
    formatFileSize(bytes) {
      if (!bytes) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
    },
    getStatusLabel(status) {
      const labels = {
        'на рассмотрении': 'На рассмотрении',
        'принят': 'Принят',
        'отклонен': 'Отклонен',
        'отложен': 'Отложен'
      }
      return labels[status] || status
    },
    onFileSelect(event) {
      const file = event.target.files[0]
      if (file) {
        if (file.size > 10 * 1024 * 1024) {
          alert('Файл слишком большой. Максимальный размер: 10MB')
          this.selectedFile = null
          if (this.$refs.fileInput) {
            this.$refs.fileInput.value = ''
          }
          return
        }
        const allowedExtensions = ['pdf', 'doc', 'docx', 'ppt', 'pptx', 'odt', 'ods', 'odp']
        const fileExtension = file.name.split('.').pop().toLowerCase()
        if (!allowedExtensions.includes(fileExtension)) {
          alert('Недопустимый формат файла')
          this.selectedFile = null
          if (this.$refs.fileInput) {
            this.$refs.fileInput.value = ''
          }
          return
        }
        this.selectedFile = file
      }
    },
    openModal(item = null) {
      this.isEdit = !!item
      this.selectedFile = null
      this.currentFileUrl = null
      if (this.$refs.fileInput) {
        this.$refs.fileInput.value = ''
      }
      if (item) {
       
        this.form = { 
          id: item.id,
          nazvanie: item.nazvanie,
          uchastnik: item.uchastnik,
          konferentsiya: item.konferentsiya,
          sektsiya: item.sektsiya || null,
          status_doklada: item.status_doklada,
          vystupaet: item.vystupaet
        }
        this.currentFileUrl = item.file_url
      } else {
       
        this.form = {
          id: null,
          nazvanie: '',
          uchastnik: null,
          konferentsiya: null,  
          sektsiya: null,
          status_doklada: 'на рассмотрении',
          vystupaet: true
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
          await dokladAPI.update(this.form.id, this.form, this.selectedFile)
        } else {
          await dokladAPI.create(this.form, this.selectedFile)
        }
        this.closeModal()
        this.fetchData()
        alert('Сохранено успешно')
      } catch (error) {
        console.error('Ошибка сохранения:', error)
        alert('Ошибка при сохранении: ' + (error.response?.data?.error || error.message))
      }
    },
    async deleteItem(id) {
      if (!confirm('Удалить доклад?')) return
      try {
        await dokladAPI.delete(id)
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

.status-на рассмотрении {
  background: #fff3e0;
  color: #f57c00;
}

.status-принят {
  background: #e8f5e9;
  color: #388e3c;
}

.status-отклонен {
  background: #ffebee;
  color: #c62828;
}

.status-отложен {
  background: #f5f5f5;
  color: #616161;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.file-link {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
}

.file-link:hover {
  text-decoration: underline;
}

.badge.bg-info {
  background-color: #0dcaf0 !important;
  color: #000;
}
</style>