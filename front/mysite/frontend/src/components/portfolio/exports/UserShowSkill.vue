<template>
  <div class="carousel">
    <div @click="carouselPrev" class="carousel_prev" :class="{ no_carousel_prev: (carouselIndex === 0) }">
      <font-awesome-icon class="text-gray-900" icon="circle-chevron-left" />
    </div>
    <div class="nodata_text" v-if="user.likelanguage == null">
          <p>データがありません</p>
    </div>
    <div class="carousel_list_outer">
      <div class="carousel_listu" :style="{ transform: 'translate(-' + carouselIndex + '00%, 0)' }">
        <Bar class="mx-2" v-if="chartflag" id="my-chart-id" :options="barChartOptions" :data="barChartData" 
        :class="{'nodata': user.likelanguage == null}"/>
        <Pie class="mx-2" v-if="chartflag" id="my-chart-id" :options="pieChartOptions" :data="pieChartData" />
      </div>
    </div>
    <div @click="carouselNext" class="carousel_next" :class="{ no_carousel_next: (carouselIndex === carouselIndexMax) }">
      <font-awesome-icon class="text-gray-900" icon="circle-chevron-right" />
    </div>
  </div>
</template>

<script>
import settingMethods from "@/mixins/settingMethods";
import commonMethods from "@/mixins/commonMethods";
import searchMethods from "@/mixins/searchMethods";
import { Bar, Pie } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale
} from "chart.js";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  ArcElement,
  CategoryScale,
  LinearScale
);
export default {
  name: "UserShowSkill",
  mixins: [settingMethods, commonMethods, searchMethods],
  props: ['user'],
  components: {
    Bar,
    Pie
  },
  data() {
    return{
      barChartData: {
        labels: [5, 4, 3, 2, 1],
        datasets: [
          {
            label: "難易度別回答数",
            backgroundColor: [
              "#652CB3",
              "#414BB2",
              "#2D9BF0",
              "#12CDD4",
              "#B1E6E8"
            ],
            data: []
          }
        ]
      },
      barChartOptions: {
        indexAxis: "y",
        responsive: true,
        //グラフのサイズを変更させない
        maintainAspectRatio: false,
        scales: {
          x: {
            title: {
              display: true,
              text: "問題の正解数"
            }
          },
          y: {
            title: {
              display: true,
              text: "問題の難易度"
            },
            beginAtZero: true
          }
        },
        plugins: {
          legend: {
            display: false, //グラフラベルのオンオフ
            position: "top"
          },
          tooltip: {
            titleFont: {
              size: 16 // ホバー時のタイトルフォントサイズ
            },
            bodyFont: {
              size: 14 // ホバー時の本文フォントサイズ
            }
          }
        }
      },
      pieChartData: {
        labels: [],
        datasets: [
          {
            label: "回答言語数",
            backgroundColor: []
          }
        ]
      },
      pieChartOptions: {
        responsive: true,
        //グラフのサイズを変更させない
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: true, //グラフラベルのオンオフ
            position: "top"
          },
          tooltip: {
            titleFont: {
              size: 16 // ホバー時のタイトルフォントサイズ
            },
            bodyFont: {
              size: 14 // ホバー時の本文フォントサイズ
            }
          }
        }
      },
      chartflags: false,
      carouselIndex: 0,
      carouselIndexMax: 1,
    };
  },
  created() {
    console.log('user = ',this.user)
    this.reRenderChart();
  },
  methods: {
    reRenderChart() {
      this.barChartData.datasets[0].data = this.user.difficulty_level_count;
      this.pieChartData.labels = Object.keys(this.user.language_answer_count);
      this.pieChartData.datasets[0].data = Object.values(
        this.user.language_answer_count
      );
      this.assignColors();
    },
    assignColors() {
      console.log("qa", Object.keys(this.user.language_answer_count));
      this.pieChartData.datasets[0].backgroundColor = this.pieChartData.labels.map(
        label => this.getColorForLabel(label)
      );
      this.chartflag = true;
    },
    getColorForLabel(label) {
      console.log("qa", label);
      switch (label) {
        case "C":
          return "#555555";
        case "Cpp":
          return "#f34b7d";
        case "Dart":
          return "#00B4AB";
        case "Go":
          return "#375eab";
        case "Java":
          return "#b07219";
        case "Javascript":
          return "#f1e05a";
        case "Perl":
          return "#0298c3";
        case "Php":
          return "#4F5D95";
        case "Python3":
          return "#3572A5";
        case "R":
          return "#198ce7";
        case "Ruby":
          return "#701516";
        case "Swift":
          return "#ffac45";
        case "TypeScript":
          return "#2b7489";
        default:
          return "#000000";
      }
    },
    carouselPrev() {
      this.carouselIndex--;
    },
    carouselNext() {
      this.carouselIndex++;
    },
  }
}
</script>

<style>
.carousel {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.carousel_prev,
.carousel_next {
  padding: 4px;
  cursor: pointer;
  font-size: 30px;
}

.no_carousel_prev,
.no_carousel_next {
  padding: 4px;
  cursor: pointer;
  font-size: 30px;
  pointer-events: none;
  opacity: 0.3;
}

.carousel_list_outer {
  flex: 1;
  flex-shrink: 0;
  overflow: hidden;
  justify-content: center;
}

.carousel_listu {
  display: flex;
  align-items: center;
  transition: 0.3s;
  flex-shrink: 0;
  width: 100%;
  height: 100%;
}

.carousel_item {
  padding: 10px;
  flex: 0 0 20%;
  align-items: center;
  justify-content: center;
}
.nodata{
  -ms-filter: blur(6px);
  filter: blur(6px);
}
.nodata_text{
  position: absolute;
}
</style>