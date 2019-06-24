<template>
  <div class="received-container">
    <el-card>
      <template v-slot:header>
        <el-tabs v-model="activeTab" v-on:tab-click="handleClick">
          <el-tab-pane label="进行中" name="processing"></el-tab-pane>
          <el-tab-pane label="已完成" name="complete"></el-tab-pane>
          <el-tab-pane label="已结束" name="over"></el-tab-pane>
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
        row-key="mission_id"
        v-bind:data="tableMission.slice((currentPage-1) * pageSize, currentPage * pageSize)"
        v-on:row-click="rowClick">
        <el-table-column
          label="任务类型"
          prop="missionType"
          v-bind:filters="[{text:'问卷调查', value: '问卷调查'}, {text: '其他任务', value: '其他任务'}]"
          v-bind:filter-method="filtersHandler">
        </el-table-column>
        <el-table-column prop="title" label="title"></el-table-column>
        <el-table-column align="right">{{ '>' }}</el-table-column>
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
                <span>{{ username }}</span>
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
            <el-row style="margin: 1rem 0">
              <el-col v-bind:span="3" v-bind:offset="1"><i class="el-icon-document"></i> 任务描述：</el-col>
              <el-col v-bind:span="20">{{ description }}</el-col>
            </el-row>
            <el-row style="margin: 1rem 0">
              <el-col v-bind:span="3" v-bind:offset="1"><i class="el-icon-coin"></i>&nbsp;任务报酬：</el-col>
              <el-col v-bind:span="20">{{ bounty }}</el-col>
            </el-row>
          </el-col>
        </el-row>
        <el-divider></el-divider>
        <el-row>
          <time-slider
            v-bind:start-time="startTime"
            v-bind:end-time="endTime"
            v-bind:order-state="finishState"
            v-bind:finish-time="finishTime">
          </time-slider>
        </el-row>
      </div>
      <span slot="footer" class="dialog-footer">
        <el-button
            v-bind:disabled="cancelButtonDisable"
            type="danger"
            v-on:click="handleMissionCancel()">
          放弃任务
        </el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import backend from '../backend'
import TimeSlider from '../components/TimeSlider'

export default {
  name: 'ReceivedPage',

  components: { TimeSlider },

  data () {
    return {
      activeTab: 'processing',
      allMission: [
        {
          order_id: '1',
          mission_id: '1',
          missionType: '问卷调查',
          title: '大学生就业调查',
          status: '已完成',
          finish_time: ''
        },
        {
          order_id: '2',
          mission_id: '2',
          missionType: '其他任务',
          title: '快递代取',
          status: '已完成',
          finish_time: ''
        },
        {
          order_id: '3',
          mission_id: '3',
          missionType: '其他任务',
          title: '大学英语线下辅导',
          status: '已结束'
        },
        {
          order_id: '4',
          mission_id: '4',
          missionType: '问卷调查',
          title: '第三饭堂饭菜调查',
          status: '进行中',
          finish_time: ''
        },
        {
          order_id: '5',
          mission_id: '5',
          missionType: '其他任务',
          title: '篮球租赁请求',
          status: '进行中',
          finish_time: ''
        },
        {
          order_id: '6',
          mission_id: '6',
          missionType: '问卷调查',
          title: '大学生就业调查',
          status: '已结束',
          finish_time: ''
        },
        {
          order_id: '7',
          mission_id: '7',
          missionType: '其他任务',
          title: '网上求夸找自信',
          status: '进行中',
          finish_time: ''
        }
      ],
      pageSize: 5,
      currentPage: 1,
      tableMission: [],
      dialogVisible: false,
      missionTitle: '',
      url: 'https://oj.vmatrix.org.cn/img/default-avatar.b6541da3.png',
      username: '',
      description: '',
      integral: 8,
      contactWay: {
        phone: '17878787878',
        weChat: 'we-chat',
        qq: '',
        other: ''
      },
      emptyStr: '',
      startTime: '2019-06-09 00:00:00',
      endTime: '2019-06-22 23:59:59',
      finishTime: '2019-06-19 00:00:00',
      finishState: 0,
      cancelMissionId: -1,
      cancelButtonDisable: false,
      bounty: 0
    }
  },

  created () {
    if (this.tableMission.length !== 0) {
      this.tableMission = []
    }

    // read all missions from db
    backend.getRequest('order/').then((response) => {
      let orders = response.data.data['orders']
      if (orders.length !== 0) {
        this.allMission = []
        for (let i = 0; i < orders.length; ++i) {
          let mission = {
            order_id: '',
            mission_id: '',
            missionType: '',
            title: '',
            status: ''
          }
          mission.order_id = orders[i].order_id
          mission.mission_id = orders[i].mission_id
          mission.title = orders[i].title
          mission.finish_time = orders[i].finish_time
          if (orders[i].type === 0) {
            mission.missionType = '问卷调查'
          } else {
            mission.missionType = '其他任务'
          }
          if (orders[i].order_state === 1) {
            mission.status = '已完成'
          } else if (orders[i].order_state === 0) {
            mission.status = '进行中'
          } else {
            mission.status = '已结束'
          }
          this.allMission.push(mission)
        }
      }
      for (let i = 0; i < this.allMission.length; ++i) {
        if (this.allMission[i].status === '进行中') {
          this.tableMission.push(this.allMission[i])
        }
      }
    }).catch(() => {

    })
  },

  methods: {
    handleClick (tab, event) {
      if (this.tableMission.length !== 0) {
        this.tableMission = []
      }

      for (let i = 0; i < this.allMission.length; ++i) {
        if (tab.name === 'processing' && this.allMission[i].status === '进行中') {
          this.tableMission.push(this.allMission[i])
          this.cancelButtonDisable = false
        } else if (tab.name === 'complete' && this.allMission[i].status === '已完成') {
          this.tableMission.push(this.allMission[i])
          this.cancelButtonDisable = true
        } else if (tab.name === 'over' && this.allMission[i].status === '已结束') {
          this.tableMission.push(this.allMission[i])
          this.cancelButtonDisable = true
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

    handleMissionCancel () {
      this.$confirm('确认放弃该任务？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let index = -1
        for (let i = 0; i < this.tableMission.length; ++i) {
          if (this.cancelMissionId === this.tableMission[i].mission_id) {
            index = i
          }
        }
        this.onConfirmCancel(index)
      })
    },

    onConfirmCancel (i) {
      // to-do: refresh data in db
      console.log(`cancelMissionId: ${this.cancelMissionId}`)
      backend.putRequest('mission/', {
        mission_id: this.cancelMissionId
      }).then((response) => {
        this.$message({
          type: 'success',
          message: '任务放弃成功！'
        })
        let index = this.allMission.indexOf(this.tableMission[i])
        this.allMission[index].status = '已结束'
        this.tableMission.splice(i, 1)
        this.dialogVisible = false
      }).catch(() => {
        this.$message({
          type: 'error',
          message: '任务放弃失败！'
        })
      })
    },

    rowClick (row) {
      // this.finishTime = row.finish_time
      this.cancelMissionId = row.mission_id
      if (row.status === '进行中') {
        this.finishState = 0
      } else if (row.status === '已完成') {
        this.finishState = 1
      } else {
        this.finishState = 2
      }
      // judge and jump to the detail page
      if (row.missionType === '问卷调查') {
        // dialog for other missions
        if (this.finishState === 0) {
          this.$router.push({
            name: 'answerQuestionnaire',
            params: {
              missionId: row.mission_id,
              orderId: row.order_id
            }
          })
        } else if (this.finishState === 1) {
          // this.$message('您已完成该问卷，报酬为' + this.bounty)
          backend.getRequest('mission/', {
            params: {
              mission_id: row.mission_id
            }
          }).then((response) => {
            let mission = response.data.data['missions']
            this.bounty = mission[0].bounty

            this.$message('您已完成该问卷，报酬为' + this.bounty)
          }).catch(() => {

          })
        } else {
          this.$message('无效问卷')
        }
      } else {
        // dialog for other missions
        this.missionTitle = row.title
        backend.getRequest('mission/', {
          params: {
            mission_id: row.mission_id
          }
        }).then((response) => {
          let mission = response.data.data['missions']
          if (mission[0].avatar !== '') {
            this.url = mission[0].receviver_avatar
          }
          this.username = mission[0].publisher_name
          this.description = mission[0].description
          this.startTime = mission[0].create_time
          this.endTime = mission[0].deadline
          this.bounty = mission[0].bounty
          this.dialogVisible = true
          // contact way
        }).catch(() => {

        })
      }
    }
  }
}
</script>

<style scoped>
  .received-container {
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
