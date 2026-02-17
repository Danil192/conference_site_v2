<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">
        <i class="bi bi-bus-front"></i>
        Трансфер
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
          placeholder="Поиск по месту встречи..."
          @input="fetchData"
        >
      </div>
      <select v-model="tipFilter" @change="fetchData" class="form-select">
        <option value="">Все типы</option>
        <option value="автобус">Автобус</option>
        <option value="маршрутка">Маршрутка</option>
        <option value="такси">Такси</option>
        <option value="индивидуально">Индивидуально</option>
      </select>
    </div>

    <div class="table-container">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>Место встречи</th>
            <th>Тип трансфера</th>
            <th>Вместимость</th>
            <th>Занято/Свободно</th>
            <th class="text-end">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.mesto_vstrechi }}</td>
            <td>
              <span class="badge" :class="getTipBadgeClass(item.tip_transfera)">
                {{ getTipLabel(item.tip_transfera) }}
              </span>
            </td>
            <td>{{ item.vmestimost }}</td>
            <td>
              <span class="badge" :class="item.mesta_svobodnye > 0 ? 'bg-success' : 'bg-danger'">
                {{ item.mesta_zanyaty }} / {{ item.mesta_svobodnye }}
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
            <h5 class="modal-title">{{ isEdit ? 'Редактировать' : 'Добавить' }} трансфер</h5>
            <button type="button" class="btn-close" @click="closeModal()"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveItem()">
              <div class="mb-3">
                <label class="form-label">Место встречи *</label>
                <input type="text" class="form-control" v-model="form.mesto_vstrechi" required>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Тип трансфера *</label>
                  <select class="form-select" v-model="form.tip_transfera" required>
                    <option value="автобус">Автобус</option>
                    <option value="маршрутка">Маршрутка</option>
                    <option value="такси">Такси</option>
                    <option value="индивидуально">Индивидуально</option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Вместимость *</label>
                  <input type="number" class="form-control" v-model="form.vmestimost" required>
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
import { transferAPI } from '../services/api'
import { Modal } from 'bootstrap'

export default {
  name: 'TransferList',
  data() {
    return {
      items: [],
      searchQuery: '',
      tipFilter: '',
      form: {
        id: null,
        mesto_vstrechi: '',
        tip_transfera: 'автобус',
        vmestimost: 20
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
        const response = await transferAPI.getAll()
        let data = response.data.results || response.data
        if (this.searchQuery) {
          data = data.filter(item => 
            item.mesto_vstrechi.toLowerCase().includes(this.searchQuery.toLowerCase())
          )
        }
        if (this.tipFilter) {
          data = data.filter(item => item.tip_transfera === this.tipFilter)
        }
        this.items = data
      } catch (error) {
        console.error('Ошибка загрузки:', error)
        alert('Не удалось загрузить данные')
      }
    },
    getTipLabel(tip) {
      const labels = {
        'автобус': 'Автобус',
        'маршрутка': 'Маршрутка',
        'такси': 'Такси',
        'индивидуально': 'Индивидуально'
      }
      return labels[tip] || tip
    },
    getTipBadgeClass(tip) {
      const classes = {
        'автобус': 'bg-primary',
        'маршрутка': 'bg-info',
        'такси': 'bg-warning text-dark',
        'индивидуально': 'bg-secondary'
      }
      return classes[tip] || 'bg-secondary'
    },
    openModal(item = null) {
      this.isEdit = !!item
      if (item) {
        this.form = { ...item }
      } else {
        this.form = {
          id: null,
          mesto_vstrechi: '',
          tip_transfera: 'автобус',
          vmestimost: 20
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
          await transferAPI.update(this.form.id, this.form)
        } else {
          await transferAPI.create(this.form)
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
      if (!confirm('Удалить трансфер?')) return
      try {
        await transferAPI.delete(id)
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

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>