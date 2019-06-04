<template>
  <div id="received-container">
    <el-card>
      <template v-slot:header>
        <el-tabs v-model="activeTab" v-on:tab-click="handleClick">
          <el-tab-pane label="进行中" name="processing"></el-tab-pane>
          <el-tab-pane label="已结束" name="over"></el-tab-pane>
          <div>
            <el-pagination
                id="pagination-container" background layout="prev, pager, next, sizes, total, jumper"
                v-bind:page-sizes="[5, 10, 20, 30]"
                v-bind:page-size="pageSize"
                v-bind:current-page.sync="currentPage"
                v-bind:total="tableMission.length"
                v-on:current-change="handleCurrentChange"
                v-on:size-change="handleSizeChange">
            </el-pagination>
          </div>
        </el-tabs>
      </template>
      <el-table id="mission-table"
                stripe
                v-bind:data="tableMission.slice((currentPage-1) * pageSize, currentPage * pageSize)">
        <el-table-column label="任务类型"
                         prop="missionType"
                         v-bind:filters="[{text:'问卷调查', value: ''}, {text: '其他任务', value: '✔'}]"
                         v-bind:filter-method="filtersHandler"></el-table-column>
        <el-table-column prop="status" label="任务摘要"></el-table-column>
        <el-table-column align="right" v-if="activeTab === 'processing'">
          <template v-slot:default="scope">
            <el-button
                size="mini"
                type="danger"
                v-on:click="handleDelete(scope.$index, scope.row)">放弃任务</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ReceivedPage',
  data () {
    return {
      activeTab: 'processing',
      allMission: [
        {
          id: '1',
          missionType: '问卷调查',
          status: '已结束'
        },
        {
          id: '2',
          missionType: '其他任务',
          status: '已结束'
        },
        {
          id: '3',
          missionType: '其他任务',
          status: '已结束'
        },
        {
          id: '4',
          missionType: '问卷调查',
          status: '进行中'
        },
        {
          id: '5',
          missionType: '其他任务',
          status: '已结束'
        },
        {
          id: '6',
          missionType: '问卷调查',
          status: '已结束'
        },
        {
          id: '7',
          missionType: '其他任务',
          status: '已结束'
        }
      ],
      pageSize: 5,
      currentPage: 1,
      tableMission: []
    }
  },

  created: function () {
    if (this.tableMission.length !== 0) {
      this.tableMission = []
    }

    for (let i = 0; i < this.allMission.length; ++i) {
      if (this.allMission[i].status === '进行中') {
        this.tableMission.push(this.allMission[i])
      }
    }
  },

  methods: {
    handleClick (tab, event) {
      if (this.tableMission.length !== 0) {
        this.tableMission = []
      }

      for (let i = 0; i < this.allMission.length; ++i) {
        if (tab.name === 'processing' && this.allMission[i].status === '进行中') {
          this.tableMission.push(this.allMission[i])
        } else if (tab.name === 'over' && this.allMission[i].status === '已结束') {
          this.tableMission.push(this.allMission[i])
        }
      }
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

    handleDelete (index, row) {
      this.$confirm('确认放弃该任务？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.onConfirmDelete(index)
        this.$message({
          type: 'success',
          message: '任务放弃成功！'
        })
      })
    },

    onConfirmDelete (i) {
      // to-do: refresh data in db
      let index = this.allMission.indexOf(this.tableMission[i])
      this.allMission.splice(index, 1)
      this.tableMission.splice(i, 1)
    }
  }
}
</script>

<style scoped>
  #received-container {
    margin: 0 10px 0 10px;
  }

  #pagination-container {
    float: right;
  }

  #mission-table {
    cursor: pointer;
  }
</style>
