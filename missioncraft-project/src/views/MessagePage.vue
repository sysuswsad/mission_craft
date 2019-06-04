<template xmlns:v-slot="http://www.w3.org/1999/XSL/Transform">
  <div id="message-container">
    <el-card class="message-card">
      <template v-slot:header>
        <el-button class="el-icon-delete-solid" type="danger" size="mini" v-on:click="deleteRow" v-bind:disabled="multipleSelection.length === 0"></el-button>
        <el-button size="mini" v-on:click="markRead" v-bind:disabled="multipleSelection.length === 0">标为已读</el-button>
        <el-button size="mini" v-on:click="unMarkRead" v-bind:disabled="multipleSelection.length === 0">标为未读</el-button>
        <el-button size="mini" v-on:click="cancelSelection" v-bind:disabled="multipleSelection.length === 0">取消选择</el-button>
        <el-pagination
          id="pagination-container" background layout="prev, pager, next, sizes, total, jumper"
          v-bind:page-sizes="[5, 10, 20, 30]"
          v-bind:page-size="pageSize"
          v-bind:current-page.sync="currentPage"
          v-bind:total="messageData.length"
          v-on:current-change="handleCurrentChange"
          v-on:size-change="handleSizeChange">
        </el-pagination>
      </template>
      <div id="table-container">
        <el-table
          id="message-table"
          ref="multipleTable"
          stripe
          v-bind:data="messageData.slice((currentPage-1) * pageSize, currentPage * pageSize)"
          v-bind:default-sort="{prop: 'date', order: 'descending'}"
          v-on:selection-change="handleSelectionChange"
          v-on:expand-change="handleExpendChange"
          v-on:row-click="rowClick"
          row-key="id"
          v-bind:expand-row-keys="expandRows">
          <el-table-column type="selection" width="50"></el-table-column>
          <el-table-column type="expand" v-on:click="markRead">
            <template v-slot:default="props">
              <el-form label-position="left" inline class="table-expand">
                <el-row>
                  <el-form-item label="消息日期：">
                    <span class="expend-format">{{ props.row.date }}</span>
                  </el-form-item>
                </el-row>
                <el-row>
                  <el-form-item label="消息内容：">
                    <span class="expend-format">{{ props.row.content }}</span>
                  </el-form-item>
                </el-row>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column
            prop="hasRead" label="已读"
            v-bind:filters="[{text:'未读', value: ''}, {text: '已读', value: '✔'}]"
            v-bind:filter-method="filtersHandler"
            width="80"></el-table-column>
          <el-table-column prop="date" label="日期" sortable width="150"></el-table-column>
          <el-table-column prop="content" label="内容" show-overflow-tooltip></el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'MessagePage',
  data () {
    return {
      messageData: [
        {
          id: '1',
          hasRead: '✔',
          date: '2016-05-02',
          content: '您有新的任务。'
        },
        {
          id: '2',
          hasRead: '',
          date: '2016-05-04',
          content: 'xxx任务发布成功。'
        },
        {
          id: '3',
          hasRead: '✔',
          date: '2016-05-01',
          content: '你发布的xxx任务已完成，请确认。'
        },
        {
          id: '4',
          hasRead: '',
          date: '2016-05-03',
          content: '您接收的xxx任务已完成，闲钱已到账。'
        },
        {
          id: '5',
          hasRead: '',
          date: '2016-05-04',
          content: '您接收的xxx任务已完成，闲钱已到账。'
        },
        {
          id: '6',
          hasRead: '',
          date: '2016-05-06',
          content: '您接收的xxx任务已完成，闲钱已到账。'
        },
        {
          id: '7',
          hasRead: '',
          date: '2016-05-05',
          content: '您接收的xxx任务已完成，闲钱已到账。'
        },
        {
          id: '8',
          hasRead: '',
          date: '2016-05-07',
          content: '您接收的xxx任务已完成，闲钱已到账。'
        },
        {
          id: '9',
          hasRead: '',
          date: '2016-05-08',
          content: '您接收的xxx任务已完成，闲钱已到账。'
        }
      ],
      multipleSelection: [],
      pageSize: 5,
      currentPage: 1,
      expandRows: []
    }
  },
  methods: {
    handleSelectionChange (val) {
      this.multipleSelection = val
    },

    handleExpendChange (row, expandedRows) {
      row.hasRead = '✔'
      // to-do: refresh data in db
    },

    markRead () {
      // to-do: refresh data in db

      for (let i = 0; i < this.multipleSelection.length; ++i) {
        this.multipleSelection[i].hasRead = '✔'
      }
      // clear selection after operations
      this.$refs.multipleTable.clearSelection()
    },

    unMarkRead () {
      // to-do: refresh data in db

      for (let i = 0; i < this.multipleSelection.length; ++i) {
        this.multipleSelection[i].hasRead = ''
      }
      // clear selection after operations
      this.$refs.multipleTable.clearSelection()
    },

    deleteRow () {
      // confirm if continue the delete operation
      this.$confirm('确认永久删除所选消息？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.onConfirmDelete()
        this.$message({
          type: 'success',
          message: '删除成功！'
        })
      })
    },

    onConfirmDelete () {
      // to-do: refresh data in db

      for (let i = 0; i < this.multipleSelection.length; ++i) {
        let index = this.messageData.indexOf(this.multipleSelection[i])
        this.messageData.splice(index, 1)
      }
      console.log('delete')
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
      let index = this.expandRows.indexOf(row.id)
      if (index < 0) {
        this.expandRows.push(row.id)
        row.hasRead = '✔'
        // to-do: refresh data in db
      } else {
        this.expandRows.splice(index, 1)
      }
    }
  }
}
</script>

<style scoped>
  #message-container {
    margin: 0 2rem;
  }

  .message-card {
    width: 100%;
  }

  #table-container {
    width: 100%;
  }

  #message-table {
    width: 100%;
    cursor: pointer;
  }

  #pagination-container {
    float: right;
  }

  .expend-format {
    font-weight: bold;
  }
</style>
