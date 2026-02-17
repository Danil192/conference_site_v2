<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">
        <i class="bi bi-x-circle"></i>
        Отказы
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
          placeholder="Поиск по участнику..."
          @input="fetchData"
        >
      </div>
      <select v-model="statusFilter" @change="fetchData" class="form-select">
        <option value="">Все статусы</option>
        <option value="запланирован">Запланирован</option>
        <option value="подтвержден">Подтвержден</option>
      </select>
    </div>

    <div class="table-container">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>Участник</th>
            <th>Конференция</th>
            <th>Доклад</th>
            <th>Причина</th>
            <th>Статус</th>
            <th>Дата</th>
            <th class="text-end">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.uchastnik_fio }}</td>
            <td>{{ item.konferentsiya_nazvanie }}</td>
            <td>{{ item.doklad_nazvanie || '—' }}</td>
            <td>{{ item.prichina || '—' }}</td>
            <td>
              <span :class="['status-badge', 'status-' + item.status_otkaza]">
                {{ getStatusLabel(item.status_otkaza) }}
              </span>
            </td>
            <td>{{ formatDate(item.created_at) }}</td>
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
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ isEdit ? 'Редактировать' : 'Добавить' }} отказ</h5>
            <button type="button" class="btn-close" @click="closeModal()"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveItem()">
              <div class="mb-3">
                <label class="form-label">Участник *</label>
                <select class="form-select" v-model="form.uchastnik" required>
                  <option v-for="uch in uchastniks" :key="uch.id" :value="uch.id">
                    {{ uch.familiya }} {{ uch.name }} {{ uch.otchestvo }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Конференция *</label>
                <select class="form-select" v-model="form.konferentsiya" required>
                  <option v-for="konf in konferentsiyas" :key="konf.id" :value="konf.id">
                    {{ konf.nazvanie }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Доклад</label>
                <select class="form-select" v-model="form.doklad">
                  <option v-for="dok in doklads" :key="dok.id" :value="dok.id">
                    {{ dok.nazvanie }}
                  </option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label">Причина</label>
                <textarea class="form-control" v-model="form.prichina" rows="3"></textarea>
              </div>
              <div class="mb-3">
                <label class="form-label">Статус *</label>
                <select class="form-select" v-model="form.status_otkaza" required>
                  <option value="запланирован">Запланирован</option>
                  <option value="подтвержден">Подтвержден</option>
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
import { otkazAPI, uchastnikAPI, konferentsiyaAPI, dokladAPI } from '../services/api'
import { Modal } from 'bootstrap'

export default {
  name: 'OtkazList',
  data() {
    return {
      items: [],
      uchastniks: [],
      konferentsiyas: [],
      doklads: [],
      searchQuery: '',
      statusFilter: '',
      form: {
        id: null,
        uchastnik: null,
        konferentsiya: null,
        doklad: null,
        prichina: '',
        status_otkaza: 'запланирован'
      },
      isEdit: false,
      modal: null
    }
  },
  mounted() {
    this.modal = new Modal(this.$refs.modalRef)
    this.fetchData()
    this.loadUchastniks()
    this.loadKonferentsiyas()
    this.loadDoklads()
  },
  methods: {
    async fetchData() {
      try {
        const response = await otkazAPI.getAll()
        let data = response.data.results || response.data
        if (this.searchQuery) {
          data = data.filter(item => 
            (item.uchastnik_fio && item.uchastnik_fio.toLowerCase().includes(this.searchQuery.toLowerCase()))
          )
        }
        if (this.statusFilter) {
          data = data.filter(item => item.status_otkaza === this.statusFilter)
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
        this.konferentsiyas = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки конференций:', error)
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
    formatDate(date) {
      if (!date) return ''
      return new Date(date).toLocaleDateString('ru-RU')
    },
    getStatusLabel(status) {
      const labels = {
        'запланирован': 'Запланирован',
        'подтвержден': 'Подтвержден'
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
          uchastnik: null,
          konferentsiya: null,
          doklad: null,
          prichina: '',
          status_otkaza: 'запланирован'
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
          await otkazAPI.update(this.form.id, this.form)
        } else {
          await otkazAPI.create(this.form)
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
      if (!confirm('Удалить отказ?')) return
      try {
        await otkazAPI.delete(id)
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

.status-запланирован {
  background: #fff3e0;
  color: #f57c00;
}

.status-подтвержден {
  background: #ffebee;
  color: #c62828;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>