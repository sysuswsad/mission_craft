<template>
  <div>
    <el-card class="message-card">
      <template v-slot:header>
        <el-button class="el-icon-arrow-left" v-on:click="toLastPage" size="mini"></el-button>
        <el-button class="el-icon-delete-solid" type="danger" size="mini" v-on:click="deleteRow" v-bind:disabled="multipleSelection.length === 0"></el-button>
        <el-button size="mini" v-on:click="markRead" v-bind:disabled="multipleSelection.length === 0">标为已读</el-button>
        <el-button size="mini" v-on:click="unMarkRead" v-bind:disabled="multipleSelection.length === 0">标为未读</el-button>
        <el-button size="mini" v-on:click="cancelSelection" v-bind:disabled="multipleSelection.length === 0">取消选择</el-button>
        <el-pagination
          id="pagination-container" background layout="prev, pager, next, sizes, total, jumper"
          v-bind:page-sizes="[5, 10, 20, 30]"
          v-bind:page-size="pageSize"
          v-bind:total="tableData.length"
          v-on:current-change="handleCurrentChange"
          v-on:size-change="handleSizeChange">
        </el-pagination>
      </template>
      <div id="table-container">
        <el-table
          id="message-table"
          ref="multipleTable"
          stripe
          v-bind:data="tableData.slice((currentPage-1) * pageSize, currentPage * pageSize)"
          v-bind:default-sort="{prop: 'date', order: 'descending'}"
          v-on:selection-change="handleSelectionChange">
          <el-table-column type="selection" width="50"></el-table-column>
          <el-table-column type="expand" v-on:click="markRead">
            <template v-slot:default="props">
              <el-form label-position="left" inline class="demo-table-expand">
                <el-form-item label="消息日期：">
                  <span class="expend-format">{{ props.row.date }}</span>
                </el-form-item>
                <el-form-item label="消息内容：">
                  <span class="expend-format">{{ props.row.content }}</span>
                </el-form-item>
              </el-form>
            </template>
          </el-table-column>
          <el-table-column prop="hasRead" label="已读" sortable width="80"></el-table-column>
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
      tableData: [
        {
          hasRead: '✔',
          date: '2016-05-02',
          content: '您有新的任务。'
        },
        {
          hasRead: '',
          date: '2016-05-04',
          content: 'xxx任务发布成功。'
        },
        {
          hasRead: '✔',
          date: '2016-05-01',
          content: '你发布的xxx任务已完成，请确认。'
        },
        {
          hasRead: '',
          date: '2016-05-03',
          content: '您接收的xxx任务已完成，闲钱已到账。'
        },
        {
          hasRead: '',
          date: '2016-05-04',
          content: '您接收的xxx任务已完成，闲钱已到账。'
        },
        {
          hasRead: '',
          date: '2016-05-06',
          content: '您接收的xxx任务已完成，闲钱已到账。'
        },
        {
          hasRead: '',
          date: '2016-05-05',
          content: '您接收的xxx任务已完成，闲钱已到账。'
        },
        {
          hasRead: '',
          date: '2016-05-07',
          content: '您接收的xxx任务已完成，闲钱已到账。'
        },
        {
          hasRead: '',
          date: '2016-05-08',
          content: '您接收的xxx任务已完成，闲钱已到账。'
        }
      ],
      multipleSelection: [],
      pageSize: 5,
      currentPage: 1
    }
  },
  methods: {
    toLastPage () {
      this.$router.back()
    },

    handleSelectionChange (val) {
      this.multipleSelection = val
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
        let index = this.tableData.indexOf(this.multipleSelection[i])
        this.tableData.splice(index, 1)
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
    }
  }
}
</script>

<style scoped>
  .message-card {
    width: 100%;
  }

  #table-container {
    width: 100%;
  }

  #message-table {
    width: 100%;
  }

  #pagination-container {
    float: right;
  }

  .demo-table-expand {
    font-size: 0;
  }

  .demo-table-expand label {
    width: 90px;
    color: #99a9bf;
  }

  .demo-table-expand {
    margin-right: 0;
    margin-bottom: 0;
    width: 50%;
  }

  .expend-format {
    font-weight: bold;
  }
</style>
