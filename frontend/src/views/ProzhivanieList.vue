<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">
        <i class="bi bi-hotel"></i>
        Проживание
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
          placeholder="Поиск по названию гостиницы..."
          @input="fetchData"
        >
      </div>
      <select v-model="kategoriyaFilter" @change="fetchData" class="form-select">
        <option value="">Все категории</option>
        <option value="одноместный">Одноместный</option>
        <option value="двухместный">Двухместный</option>
        <option value="трёхместный">Трёхместный</option>
        <option value="люкс">Люкс</option>
      </select>
    </div>

    <div class="table-container">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>Название</th>
            <th>Турбаза</th>
            <th>Категория</th>
            <th>Вместимость</th>
            <th>Стоимость</th>
            <th>Занято/Свободно</th>
            <th class="text-end">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>{{ item.nazvanie }}</td>
            <td>{{ item.turbaza_nazvanie || '—' }}</td>
            <td>{{ item.kategoriya_nomerov || '—' }}</td>
            <td>{{ item.vmestimost }}</td>
            <td>{{ item.stoimost }} ₽</td>
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
            <h5 class="modal-title">{{ isEdit ? 'Редактировать' : 'Добавить' }} проживание</h5>
            <button type="button" class="btn-close" @click="closeModal()"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveItem()">
              <div class="mb-3">
                <label class="form-label">Название *</label>
                <input type="text" class="form-control" v-model="form.nazvanie" required>
              </div>
              <div class="mb-3">
                <label class="form-label">Турбаза</label>
                <input type="text" class="form-control" v-model="form.turbaza_nazvanie">
              </div>
              
              <div class="mb-3">
                <label class="form-label">Конференция *</label>
                <select class="form-select" v-model="form.konferentsiya" required>
                  <option value="" disabled>Выберите конференцию</option>
                  <option v-for="konf in konferentsiyas" :key="konf.id" :value="konf.id">
                    {{ konf.nazvanie }}
                  </option>
                </select>
                <div class="form-text">
                  К какой конференции относится этот номерной фонд
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Категория номеров</label>
                  <input type="text" class="form-control" v-model="form.kategoriya_nomerov">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Вместимость *</label>
                  <input type="number" class="form-control" v-model="form.vmestimost" required>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Стоимость (₽) *</label>
                  <input type="number" class="form-control" v-model="form.stoimost" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Кол-во домиков</label>
                  <input type="number" class="form-control" v-model="form.kolvo_domikov">
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
import { prozhivanieAPI, konferentsiyaAPI } from '../services/api'
import { Modal } from 'bootstrap'

export default {
  name: 'ProzhivanieList',
  data() {
    return {
      items: [],
      konferentsiyas: [], 
      searchQuery: '',
      kategoriyaFilter: '',
      form: {
        id: null,
        nazvanie: '',
        turbaza_nazvanie: '',
        konferentsiya: null, 
        kategoriya_nomerov: '',
        stoimost: 0,
        vmestimost: 1,
        kolvo_domikov: 0
      },
      isEdit: false,
      modal: null
    }
  },
  mounted() {
    this.modal = new Modal(this.$refs.modalRef)
    this.fetchData()
    this.loadKonferentsiyas() 
  },
  methods: {
    async loadKonferentsiyas() {
      try {
        const response = await konferentsiyaAPI.getAll()
        this.konferentsiyas = response.data.results || response.data
      } catch (error) {
        console.error('Ошибка загрузки конференций:', error)
      }
    },

    async fetchData() {
      try {
        const response = await prozhivanieAPI.getAll()
        let data = response.data.results || response.data
        if (this.searchQuery) {
          data = data.filter(item => 
            item.nazvanie.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
            (item.turbaza_nazvanie && item.turbaza_nazvanie.toLowerCase().includes(this.searchQuery.toLowerCase()))
          )
        }
        if (this.kategoriyaFilter) {
          data = data.filter(item => item.kategoriya_nomerov === this.kategoriyaFilter)
        }
        this.items = data
      } catch (error) {
        console.error('Ошибка загрузки:', error)
        alert('Не удалось загрузить данные')
      }
    },

openModal(item = null) {
      this.isEdit = !!item
      if (item) {
        this.form = { ...item }
      } else {
        this.form = {
          id: null,
          nazvanie: '',
          turbaza_nazvanie: '',
          konferentsiya: null, 
          kategoriya_nomerov: '',
          stoimost: 0,
          vmestimost: 1,
          kolvo_domikov: 0
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
          await prozhivanieAPI.update(this.form.id, this.form)
        } else {
          await prozhivanieAPI.create(this.form)
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
      if (!confirm('Удалить запись о проживании?')) return
      try {
        await prozhivanieAPI.delete(id)
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