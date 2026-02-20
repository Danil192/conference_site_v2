<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">
        <i class="bi bi-calendar-event"></i>
        Конференции
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
          placeholder="Поиск по названию..."
          @input="fetchData"
        >
      </div>
      <select v-model="statusFilter" @change="fetchData" class="form-select">
        <option value="">Все статусы</option>
        <option value="планируется">Планируется</option>
        <option value="идет">Идет</option>
        <option value="завершена">Завершена</option>
        <option value="отменена">Отменена</option>
      </select>
    </div>

    <div class="table-container">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>Название</th>
            <th>Дата начала</th>
            <th>Дата окончания</th>
            <th>Статус</th>
            <th class="text-end">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>
            <router-link :to="`/konferentsiyas/${item.id}`" class="conference-link">
                {{ item.nazvanie }}
            </router-link>
            </td>
            <td>{{ formatDate(item.data_nachala) }}</td>
            <td>{{ formatDate(item.data_okonchaniya) }}</td>
            <td>
              <span :class="['status-badge', 'status-' + item.status]">
                {{ getStatusLabel(item.status) }}
              </span>
            </td>
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
            <td colspan="5" class="text-center text-muted py-4">
              Нет данных
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="modal fade" ref="modalRef" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEdit ? 'Редактировать' : 'Добавить' }} конференцию</h5>
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
                  <label class="form-label">Дата начала *</label>
                  <input type="date" class="form-control" v-model="form.data_nachala" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Дата окончания *</label>
                  <input type="date" class="form-control" v-model="form.data_okonchaniya" required>
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Статус *</label>
                <select class="form-select" v-model="form.status" required>
                  <option value="планируется">Планируется</option>
                  <option value="идет">Идет</option>
                  <option value="завершена">Завершена</option>
                  <option value="отменена">Отменена</option>
                </select>
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
import { konferentsiyaAPI } from '../services/api'
import { Modal } from 'bootstrap'

export default {
  name: 'KonferentsiyaList',
  data() {
    return {
      items: [],
      searchQuery: '',
      statusFilter: '',
      form: {
        id: null,
        nazvanie: '',
        data_nachala: '',
        data_okonchaniya: '',
        status: 'планируется'
      },
      isEdit: false,
      modal: null
    }
  },
  mounted() {
    this.modal = new Modal(this.$refs.modalRef)
    this.fetchData()
  },
  methods: {
    async fetchData() {
      try {
        const response = await konferentsiyaAPI.getAll()
        let data = response.data.results || response.data
        if (this.searchQuery) {
          data = data.filter(item => 
            item.nazvanie.toLowerCase().includes(this.searchQuery.toLowerCase())
          )
        }
        if (this.statusFilter) {
          data = data.filter(item => item.status === this.statusFilter)
        }
        this.items = data
      } catch (error) {
        console.error('Ошибка загрузки:', error)
        alert('Не удалось загрузить данные')
      }
    },
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU')
    },
    getStatusLabel(status) {
      const labels = {
        'планируется': 'Планируется',
        'идет': 'Идет',
        'завершена': 'Завершена',
        'отменена': 'Отменена'
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
          nazvanie: '',
          data_nachala: '',
          data_okonchaniya: '',
          status: 'планируется'
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
          await konferentsiyaAPI.update(this.form.id, this.form)
        } else {
          await konferentsiyaAPI.create(this.form)
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
      if (!confirm('Удалить конференцию?')) return
      try {
        await konferentsiyaAPI.delete(id)
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
.conference-link {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s ease;
}

.conference-link:hover {
  color: #2980b9;
  text-decoration: underline;
}

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

.status-планируется {
  background: #e3f2fd;
  color: #1976d2;
}

.status-идет {
  background: #e8f5e9;
  color: #388e3c;
}

.status-завершена {
  background: #f5f5f5;
  color: #616161;
}

.status-отменена {
  background: #ffebee;
  color: #c62828;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>