<template>
  <div class="page-container">
    <div class="page-header">
      <h1 class="page-title">
        <i class="bi bi-calendar-week"></i>
        Расписание программы
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
          placeholder="Поиск по докладу или участнику..."
          @input="fetchData"
        >
      </div>
      <select v-model="programFilter" @change="fetchData" class="form-select">
        <option value="">Все программы</option>
        <option v-for="prog in programs" :key="prog.id" :value="prog.id">
          {{ prog.nazvanie }}
        </option>
      </select>
      <select v-model="sekciyaFilter" @change="fetchData" class="form-select">
        <option value="">Все секции</option>
        <option v-for="sek in sekciyas" :key="sek.id" :value="sek.id">
          {{ sek.nazvanie }}
        </option>
      </select>
    </div>

    <div class="table-container">
      <table class="table table-hover">
        <thead>
          <tr>
            <th>Время</th>
            <th>Доклад</th>
            <th>Докладчик</th>
            <th>Секция</th>
            <th>Помещение</th>
            <th>Программа</th>
            <th class="text-end">Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in items" :key="item.id">
            <td>
              <strong>{{ formatTime(item.vremya_nachala) }}</strong>
              <br>
              <small class="text-muted">{{ formatTime(item.vremya_okonchaniya) }}</small>
            </td>
            <td>{{ item.doklad_nazvanie || '—' }}</td>
            <td>{{ item.uchastnik_fio || '—' }}</td>
            <td>{{ item.sekciya_nazvanie || '—' }}</td>
            <td>{{ item.pomeshchenie || '—' }}</td>
            <td>{{ item.program_nazvanie }}</td>
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
            <h5 class="modal-title">{{ isEdit ? 'Редактировать' : 'Добавить' }} в расписание</h5>
            <button type="button" class="btn-close" @click="closeModal()"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="saveItem()">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Программа *</label>
                  <select class="form-select" v-model="form.program" required>
                    <option v-for="prog in programs" :key="prog.id" :value="prog.id">
                      {{ prog.nazvanie }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Секция</label>
                  <select class="form-select" v-model="form.sekciya">
                    <option v-for="sek in sekciyas" :key="sek.id" :value="sek.id">
                      {{ sek.nazvanie }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Доклад</label>
                  <select class="form-select" v-model="form.doklad">
                    <option v-for="dok in doklads" :key="dok.id" :value="dok.id">
                      {{ dok.nazvanie }}
                    </option>
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Участник</label>
                  <select class="form-select" v-model="form.uchastnik">
                    <option v-for="uch in uchastniks" :key="uch.id" :value="uch.id">
                      {{ uch.familiya }} {{ uch.name }} {{ uch.otchestvo }}
                    </option>
                  </select>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Время начала *</label>
                  <input type="datetime-local" class="form-control" v-model="form.vremya_nachala" required>
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Время окончания *</label>
                  <input type="datetime-local" class="form-control" v-model="form.vremya_okonchaniya" required>
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label class="form-label">Помещение</label>
                  <input type="text" class="form-control" v-model="form.pomeshchenie">
                </div>
                <div class="col-md-6 mb-3">
                  <label class="form-label">Номер в программе</label>
                  <input type="number" class="form-control" v-model="form.nomer_v_programme">
                </div>
              </div>
              <div class="mb-3">
                <label class="form-label">Не выступает</label>
                <select class="form-select" v-model="form.ne_vystupaet">
                  <option :value="false">Нет</option>
                  <option :value="true">Да</option>
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
          data = data.filter(item => 
            (item.doklad_nazvanie && item.doklad_nazvanie.toLowerCase().includes(this.searchQuery.toLowerCase())) ||
            (item.uchastnik_fio && item.uchastnik_fio.toLowerCase().includes(this.searchQuery.toLowerCase()))
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
        alert('Не удалось загрузить данные')
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
      if (!datetime) return ''
      const date = new Date(datetime)
      return date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })
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