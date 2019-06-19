<template>
  <div class="publication-container">
    <el-card>
      <template v-slot:header>
        <el-tabs v-model="activeTab" v-on:tab-click="handleClick">
          <el-tab-pane label="进行中" name="processing"></el-tab-pane>
          <el-tab-pane label="已完成" name="complete"></el-tab-pane>
          <div>
            <el-pagination
              class="pagination-container" background layout="prev, pager, next, sizes, total, jumper"
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
      <el-table
        class="mission-table"
        stripe
        v-bind:data="tableMission.slice((currentPage-1) * pageSize, currentPage * pageSize)"
        v-on:row-click="rowClick">
        <el-table-column
          label="任务类型"
          prop="missionType"
          v-bind:filters="[{text:'问卷调查', value: '问卷调查'}, {text: '其他任务', value: '其他任务'}]"
          v-bind:filter-method="filtersHandler"></el-table-column>
        <el-table-column prop="status" label="任务摘要"></el-table-column>
        <el-table-column align="right" v-if="activeTab === 'processing'">
          <template v-slot:default="scope">
            <el-button
              size="mini"
              type="danger"
              v-on:click="handleDelete(scope.$index, scope.row)">
              取消任务
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    <el-dialog
      width="70%"
      center
      v-bind:visible.sync="dialogVisible">
      <template v-slot:title>
        <h2>{{ missionTitle }}</h2>
      </template>
      <el-divider></el-divider>
      <div class="detail-container">
        <el-row type="flex">
          <el-col v-bind:span="8">
            <el-row>
              <h1>发布者</h1>
            </el-row>
            <el-row>
              <el-col v-bind:span="8" v-bind:offset="1" class="img-wrapper">
                <div>
                  <img class="img-container" v-bind:src=url alt="加载失败"/>
                </div>
              </el-col>
              <el-col class="username-container" v-bind:span="8">
                <span>caixukun</span>
                <div style="margin-top: 10px">
                  <span style="font-weight: bold">{{ '信誉积分：' + integral }}</span>
                </div>
              </el-col>
            </el-row>
            <div v-for="(index, value) in contactWay" v-bind:key="value">
              <el-row v-if="contactWay[value] !== emptyStr" class="contact-row-wrapper">
                <el-col v-bind:span="20" v-bind:offset="2" v-if="value === 'phone'">
                  <span>{{ '手机号码：' + contactWay[value] }}</span>
                </el-col>
                <el-col v-bind:span="20" v-bind:offset="2" v-if="value === 'weChat'">
                  <span>{{ '微信：' + contactWay[value] }}</span>
                </el-col>
                <el-col v-bind:span="20" v-bind:offset="2" v-if="value === 'qq'">
                  <span>{{ 'qq：' + contactWay[value] }}</span>
                </el-col>
                <el-col v-bind:span="20" v-bind:offset="2" v-if="value === 'other'">
                  <span>{{ '其他联系方式：' + contactWay[value] }}</span>
                </el-col>
              </el-row>
            </div>
          </el-col>
          <el-col v-bind:span="2" style="display: flex; justify-content: center">
            <div class="vertical-divider"></div>
          </el-col>
          <el-col v-bind:span="14">
            <h1>任务详情</h1>
            <el-col v-bind:span="20" v-bind:offset="2">caixukunhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh...</el-col>
          </el-col>
        </el-row>
        <el-divider></el-divider>
        <el-row v-bind:gutter="15" style="margin-top: 30px">
          <el-col v-bind:span="5" style="padding: 8px 0 0 40px">{{ startTime }}</el-col>
          <el-col v-bind:span="14">
            <el-slider
              v-bind:step="Math.floor(100 / timeDiff(startTime, endTime))"
              v-bind:value="passTime(startTime)"
              v-bind:format-tooltip="formatTooltip"
              disabled></el-slider>
          </el-col>
          <el-col v-bind:span="5" style="padding: 8px 0 0 0">{{ endTime }}</el-col>
        </el-row>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button v-on:click="dialogVisible = false">关 闭</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: 'PublicationPage',
  data () {
    return {
      activeTab: 'processing',
      allMission: [
        {
          id: '1',
          missionType: '问卷调查',
          missionTitle: '大学生就业调查',
          status: '已完成'
        },
        {
          id: '2',
          missionType: '其他任务',
          missionTitle: '快递代取',
          status: '已完成'
        },
        {
          id: '3',
          missionType: '其他任务',
          missionTitle: '大学英语线下辅导',
          status: '已完成'
        },
        {
          id: '4',
          missionType: '问卷调查',
          missionTitle: '第三饭堂饭菜调查',
          status: '进行中'
        },
        {
          id: '5',
          missionType: '其他任务',
          missionTitle: '篮球租赁请求',
          status: '已完成'
        },
        {
          id: '6',
          missionType: '问卷调查',
          missionTitle: '大学生就业调查',
          status: '已完成'
        },
        {
          id: '7',
          missionType: '其他任务',
          missionTitle: '网上求夸找自信',
          status: '已完成'
        }
      ],
      pageSize: 5,
      currentPage: 1,
      tableMission: [],
      dialogVisible: false,
      missionTitle: '',
      url: 'https://oj.vmatrix.org.cn/img/default-avatar.b6541da3.png',
      integral: 8,
      contactWay: {
        phone: '17878787878',
        weChat: 'we-chat',
        qq: '',
        other: ''
      },
      emptyStr: '',
      startTime: '2019-06-09 00:00:00',
      endTime: '2019-06-10 23:59:59'
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
        } else if (tab.name === 'complete' && this.allMission[i].status === '已完成') {
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
      this.$confirm('确认取消该任务？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.onConfirmDelete(index)
        this.$message({
          type: 'success',
          message: '任务取消成功！'
        })
      })
    },

    onConfirmDelete (i) {
      // to-do: refresh data in db
      let index = this.allMission.indexOf(this.tableMission[i])
      this.allMission.splice(index, 1)
      this.tableMission.splice(i, 1)
    },

    rowClick (row) {
      // judge and jump to the detail page
      if (row.missionType === '问卷调查') {
        // to-do: route to detail page and pass some parameters to sign if the mission is over/finished or
        // if the mission is published by the one clicking the row

      } else {
        // dialog for other missions
        this.missionTitle = row.missionTitle
        this.dialogVisible = true
      }
    },

    showInfo () {
      console.log('show info')
    },

    formatTooltip () {
      let startTime = Date.now()
      let endTime = new Date(this.endTime)
      let left = '剩余0天0时0分0秒'
      if (endTime.getTime() > startTime) {
        let msDiff = endTime.getTime() - startTime
        // compute day left
        let leftDay = Math.floor(msDiff / (1000 * 24 * 60 * 60))
        // hours left after computing day left
        let leaveForHour = msDiff % (1000 * 24 * 60 * 60)
        // compute hour left
        let leftHour = Math.floor(leaveForHour / (1000 * 60 * 60))
        let leaveForMinute = leaveForHour % (1000 * 3600)
        let leftMinute = Math.floor(leaveForMinute / (1000 * 60))
        let leaveForSecond = leaveForMinute % (1000 * 60)
        let leftSecond = Math.round(leaveForSecond / 1000)
        left = '剩余' + leftDay + '天' + leftHour + '时' + leftMinute + '分' + leftSecond + '秒'
      }
      return left
    },

    timeDiff (sTime, eTime) {
      let startTime = new Date(sTime)
      let endTime = new Date(eTime)
      let leftHour = 0
      if (endTime.getTime() > startTime.getTime()) {
        let msDiff = endTime.getTime() - startTime.getTime()
        leftHour = Math.floor(msDiff / (1000 * 3600))
      }
      return leftHour
    },

    passTime (startTime) {
      let nowTime = Date.now()
      let sTime = new Date(startTime)
      let passHour = 0
      if (nowTime > sTime.getTime()) {
        let msDiff = nowTime - sTime.getTime()
        passHour = Math.ceil(msDiff / (1000 * 3600))
      }
      return passHour * Math.floor(100 / this.$options.methods.timeDiff(startTime, this.endTime))
    }
  }
}
</script>

<style scoped>
  .publication-container {
    margin: 0 2rem;
  }

  .pagination-container {
    float: right;
  }

  .mission-table {
    cursor: pointer;
  }

  .detail-container {
    display: block;
  }

  .vertical-divider {
    width: 1px;
    display: inline-block;
    background-color: #DCDFE6;
  }

  .img-wrapper {
    cursor: pointer;
  }

  .img-container {
    width: 80px;
    height: 80px;
    border-radius: 50%;
  }

  .username-container {
    margin: 20px 0 0 0;
    font-weight: bold;
  }

  .contact-row-wrapper {
    margin-bottom: 10px;
  }
</style>
