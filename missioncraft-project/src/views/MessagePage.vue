<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div class="message-container">
    <el-card class="message-card">
      <template v-slot:header>
        <el-button class="el-icon-delete-solid" type="danger" size="mini" v-on:click="deleteRow" v-bind:disabled="multipleSelection.length === 0"></el-button>
        <el-button size="mini" v-on:click="markRead" v-bind:disabled="multipleSelection.length === 0">标为已读</el-button>
        <el-button size="mini" v-on:click="unMarkRead" v-bind:disabled="multipleSelection.length === 0">标为未读</el-button>
        <el-button size="mini" v-on:click="cancelSelection" v-bind:disabled="multipleSelection.length === 0">取消选择</el-button>
        <el-pagination
          class="pagination-container" layout="prev, pager, next, sizes, total, jumper"
          v-bind:page-sizes="[20, 50, 100]"
          v-bind:page-size="pageSize"
          v-bind:current-page.sync="currentPage"
          v-bind:total="messageData.length"
          v-on:current-change="handleCurrentChange"
          v-on:size-change="handleSizeChange">
        </el-pagination>
      </template>
      <div class="table-container">
        <el-table
          class="message-table"
          ref="multipleTable"
          stripe
          v-bind:data="messageData.slice((currentPage-1) * pageSize, currentPage * pageSize)"
          v-bind:default-sort="{prop: 'date', order: 'descending'}"
          v-on:selection-change="handleSelectionChange"
          v-on:expand-change="handleExpendChange"
          v-on:row-click="rowClick"
          row-key="n_id"
          v-bind:expand-row-keys="expandRows">
          <el-table-column type="selection" width="50"></el-table-column>
          <el-table-column type="expand" v-on:click="markRead">
            <template v-slot:default="props">
              <el-form label-position="left" inline class="table-expand">
                <el-row>
                  <el-form-item label="消息日期：">
                    <span class="expend-format">{{ props.row.create_time }}</span>
                  </el-form-item>
                </el-row>
                <el-row>
                  <el-form-item label="消息内容：">
                    <span class="expend-format">{{ props.row.message }}</span>
                  </el-form-item>
                </el-row>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column
            prop="has_read" label="已读"
            v-bind:filters="[{text:'未读', value: ''}, {text: '已读', value: '✔'}]"
            v-bind:filter-method="filtersHandler"
            width="70"></el-table-column>
          <el-table-column prop="create_time" label="日期" sortable width="170"></el-table-column>
          <el-table-column prop="message" label="内容" show-overflow-tooltip></el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
import backend from '../backend'

export default {
  name: 'MessagePage',
  data () {
    return {
      messageData: [],
      multipleSelection: [],
      pageSize: 20,
      currentPage: 1,
      expandRows: []
    }
  },
  methods: {
    handleSelectionChange (val) {
      this.multipleSelection = val
    },

    handleExpendChange (row, expandedRows) {
      if (row.has_read === '') {
        let notification = []

        notification.push({ 'n_id': row.n_id, 'has_read': 1 })
        backend.putRequest('notification/', {
          notification: notification,
          type: 0
        }).then((response) => {
          row.has_read = '✔'
          // this.$emit('markMessage', 1)
          this.$store.commit('updateMessage', {
            message: this.messageData
          })
        }).catch(() => {

        })
      }
    },

    markRead () {
      let notification = []
      for (let i = 0; i < this.multipleSelection.length; ++i) {
        if (this.multipleSelection[i].has_read === '') {
          notification.push({ 'n_id': this.multipleSelection[i].n_id, 'has_read': 1 })
        }
      }

      backend.putRequest('notification/', {
        notification: notification,
        type: 0
      }).then((response) => {
        for (let i = 0; i < this.multipleSelection.length; ++i) {
          if (this.multipleSelection[i].has_read === '') {
            this.multipleSelection[i].has_read = '✔'
          }
        }

        this.$store.commit('updateMessage', {
          message: this.messageData
        })
        // this.$emit('markMessage', count)
        // clear selection after operations
        this.$refs.multipleTable.clearSelection()
      }).catch(() => {

      })
    },

    unMarkRead () {
      let notification = []
      for (let i = 0; i < this.multipleSelection.length; ++i) {
        if (this.multipleSelection[i].has_read === '✔') {
          notification.push({ 'n_id': this.multipleSelection[i].n_id, 'has_read': 0 })
        }
      }

      backend.putRequest('notification/', {
        notification: notification,
        type: 0
      }).then((response) => {
        for (let i = 0; i < this.multipleSelection.length; ++i) {
          if (this.multipleSelection[i].has_read === '✔') {
            this.multipleSelection[i].has_read = ''
          }
        }

        this.$store.commit('updateMessage', {
          message: this.messageData
        })
        // this.$emit('markMessage', -count)
        // clear selection after operations
        this.$refs.multipleTable.clearSelection()
      }).catch(() => {

      })
    },

    deleteRow () {
      // confirm if continue the delete operation
      this.$confirm('确认永久删除所选消息？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.onConfirmDelete()
      })
    },

    onConfirmDelete () {
      let notification = []
      for (let i = 0; i < this.multipleSelection.length; ++i) {
        notification.push(this.multipleSelection[i].n_id)
      }

      backend.putRequest('notification/', {
        notification: notification,
        type: 1
      }).then((response) => {
        this.$message({
          type: 'success',
          message: '删除成功！'
        })
        for (let i = 0; i < this.multipleSelection.length; ++i) {
          let index = this.messageData.indexOf(this.multipleSelection[i])
          this.messageData.splice(index, 1)
        }

        this.$store.commit('updateMessage', {
          message: this.messageData
        })
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '删除失败！'
        })
      })
    },

    cancelSelection () {
      // clear selection after operations
      this.$refs.multipleTable.clearSelection()
    },

    handleCurrentChange (cPage) {
      this.currentPage = cPage
    },

    handleSizeChange (pSize) {
      this.pageSize = pSize
    },

    filtersHandler (value, row, column) {
      const property = column['property']
      return row[property] === value
    },

    rowClick (row) {
      // 在<table>里，我们已经设置row的key值设置为每行数据id：row-key="id"
      let index = this.expandRows.indexOf(row.n_id)
      if (index < 0) {
        let notification = []
        this.expandRows.push(row.n_id)
        if (row.has_read === '') {
          // to-do: refresh data in db
          notification.push({ 'n_id': row.n_id, 'has_read': 1 })
          backend.putRequest('notification/', {
            notification: notification,
            type: 0
          }).then((response) => {
            row.has_read = '✔'
            this.$store.commit('updateMessage', {
              message: this.messageData
            })
            // this.$emit('markMessage', 1)
          }).catch(() => {

          })
        }
      } else {
        this.expandRows.splice(index, 1)
      }
    }
  },

  created () {
    this.messageData = []
    backend.getRequest('notification/').then((response) => {
      if (response.data.data['notifications'].length !== 0) {
        this.messageData = response.data.data['notifications']

        for (let i = 0; i < this.messageData.length; ++i) {
          if (this.messageData[i].has_read !== 0) {
            this.messageData[i].has_read = '✔'
          } else {
            this.messageData[i].has_read = ''
          }
        }
      }
    }).catch(() => {

    })
  }
}
</script>

<style scoped>
  .message-container {
    margin: 0 2rem;
  }

  .message-card {
    width: 100%;
  }

  .table-container {
    width: 100%;
  }

  .message-table {
    width: 100%;
    cursor: pointer;
  }

  .pagination-container {
    float: right;
  }

  .expend-format {
    font-weight: bold;
  }
</style>
