<template>
  <div class="statistic-container">
    <el-button
      plain
      circle
      class="back-button"
      icon="el-icon-back"
      v-on:click="backToPrev">
    </el-button>

    <el-card v-loading="loadData">

      <template v-slot:header>
        <h2 style="text-align: center">问卷标题 统计详情</h2>
        <p style="text-align: center">ID: {{ missionId }}</p>
      </template>

      <div v-for="(problem, index) of statistic" v-bind:key="index">
        <h3>{{ index + 1 }}. {{ problem.question }}</h3>

        <el-tabs v-if="problem.type !== 2" tab-position="left">

          <el-tab-pane label="柱状图" lazy>
            <el-row type="flex" justify="center">
              <v-chart
                theme="light"
                v-bind:options="parseBarData(problem)"
              ></v-chart>
            </el-row>
          </el-tab-pane>

          <el-tab-pane label="饼图" lazy>
            <el-row type="flex" justify="center">
              <v-chart
                theme="light"
                v-bind:options="parsePieData(problem)"
              ></v-chart>
            </el-row>
          </el-tab-pane>

        </el-tabs>

        <div v-else>
          <el-row v-bind:gutter="20">
            <el-col
              v-bind:span="4"
              v-for="(ans, idx) of problem.answer.slice((textPageRecorder[index] - 1) * 6, textPageRecorder[index] * 6)"
              v-bind:key="textPageRecorder[index] * 6 + idx">
              <el-card shadow="hover">
                <p>{{ ans }}</p>
              </el-card>
            </el-col>
          </el-row>
          <el-row style="margin-top: 1rem">
            <el-pagination
              small
              hide-on-single-page
              v-bind:total="problem.answer.length"
              v-bind:page-size="6"
              v-bind:current-page="textPageRecorder[index]"
              v-on:current-change="changeRecorder(index, $event)">
            </el-pagination>
          </el-row>
        </div>

        <el-divider v-if="index < statistic.length - 1"></el-divider>
      </div>

    </el-card>
  </div>
</template>

<script>
import $backend from '../backend'
import 'echarts/lib/chart/bar'
import 'echarts/lib/chart/pie'
import 'echarts/lib/component/tooltip'
import 'echarts/lib/component/polar'
import 'echarts/lib/component/legend'
export default {
  name: 'StatisticPage',

  data () {
    return {
      loadData: true,
      missionId: -1,
      statistic: [],
      textPageRecorder: {}
    }
  },

  methods: {
    parseBarData (problem) {
      return {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: [
          {
            type: 'category',
            data: problem.choices,
            axisTick: {
              alignWithLabel: true
            }
          }
        ],
        yAxis: [
          {
            type: 'value'
          }
        ],
        series: [
          {
            type: 'bar',
            name: '选择人数',
            barWidth: '60%',
            data: problem.answer
          }
        ]
      }
    },

    parsePieData (problem) {
      let option = {
        tooltip: {
          trigger: 'item',
          formatter: '{b} <br/>{a}: {c} ( {d}% )'
        },
        legend: {
          orient: 'vertical',
          x: 'left'
        },
        label: {
          show: true
        },
        series: [
          {
            type: 'pie',
            name: '选择人数',
            data: []
          }
        ]
      }

      for (let [index, choice] of problem.choices.entries()) {
        option.series[0].data.push({ value: problem.answer[index], name: choice })
      }

      return option
    },

    changeRecorder (recorderIdx, payload) {
      this.$set(this.textPageRecorder, recorderIdx, payload)
    },

    backToPrev () {
      this.$router.go(-1)
    }
  },

  created () {
    this.missionId = this.$route.params.id
    $backend.getRequest('mission/', {
      params: {
        return_problems: 1,
        return_statistics: 1,
        personal: 1,
        mission_id: this.$route.params.id
      }
    }).then(response => {
      this.statistic = this.statistic.concat(response.data.data.missions[0].problems)

      // initialize the current pages of areas of text problems
      for (const [index, problem] of this.statistic.entries()) {
        if (problem.type === 2) {
          this.$set(this.textPageRecorder, index, 1)
        }
      }

      this.loadData = false
    }).catch(error => {
      this.$alert('发生了错误！请稍后重试', '错误', {
        confirmButtonText: '返回',
        type: 'error',
        callback: action => {
          this.$router.go(-1)
        }
      })
    })
  }

  // beforeRouteEnter (to, from, next) {
  //   if (from.name.localeCompare('published') === 0) {
  //     next()
  //   } else {
  //     next(false)
  //   }
  // }
}
</script>

<style scoped>
  .statistic-container {
    padding: 1rem 3rem;
  }

  .back-button {
    position: fixed;
    margin-top: 2rem;
    margin-left: 2rem;
  }
</style>

<style>
  .echarts {
    width: 100%;
    height: 100%;
  }
</style>
