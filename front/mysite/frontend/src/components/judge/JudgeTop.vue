<template>
  <div class="article-post mx-auto my-10 w-10/12 text-gray-700">
    <div
      class="border-b-4 border-blue-900 flex px-12 pb-2 justify-between items-center text-2xl font-semibold"
    >開催中の大会</div>
    <div v-if="contestList != null">
      <div v-for="contest in contestList" :key="contest.id">
        <div
          class="border-[3px] text-gray-700 border-blue-300 bg-slate-50 rounded-3xl mt-8 mx-20 px-10 py-6"
        >
          <div class>
            <div class="flex justify-start items-center text-3xl">[[contest.name || ""]]</div>
            <div class="flex items-center justify-between">
              <div class="flex gap-8">
                <div class="text-xl flex items-center">
                  開催者：
                  <div class="px-1 flex text-2xl">[[contest.admins[0].username || ""]]</div>
                </div>
                <div class="text-xl flex items-center">
                  問題数：
                  <div class="px-1 flex text-2xl">[[contest.problems.length || ""]]</div>問
                </div>
                <div class="text-xl flex items-center">
                  参加者数：
                  <div class="px-1 flex text-2xl">[[contest.member.length || "0"]]</div>人
                </div>
                <!-- <div class="text-xl flex items-center">
                  終了日時：
                  <div class="px-1 flex text-2xl">
                  [[ endTime(contest.endtime) || ""]]
                  </div>
                </div>-->
              </div>
              <div>
                <router-link :to="{ name: 'JudgeContest',params: { id: contest.id }}">
                  <div
                    class="text-center py-2.5 px-8 text-lg font-medium bg-teal-500 text-gray-50 rounded-xl cursor-pointer hover:bg-teal-400"
                  >詳細を確認する</div>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div
      class="border-b-4 border-blue-900 flex mt-8 px-12 pb-2 justify-between items-center text-2xl font-semibold"
    >難易度一覧</div>
    <div class="border-[3px] text-gray-700 border-blue-300 bg-slate-50 rounded-3xl my-8 mx-20 p-10">
      <div class="flex justify-between items-center">
        <div class="flex items-center gap-8">
          <div class="flex justify-start items-center text-3xl">チュートリアル</div>
        </div>
        <div v-if="this.tutorialId != null">
          <router-link :to="{name: 'JudgeForm',params: {group_id: 2 ,id: this.tutorialId  }}">
            <div
              class="text-center py-2.5 px-8 text-lg font-medium bg-teal-500 text-gray-50 rounded-xl cursor-pointer hover:bg-teal-400"
            >チャレンジする</div>
          </router-link>
        </div>
      </div>
    </div>
    <div v-if="diffList != null">
      <div v-for="(diff, index) in diffList.diff" :key="diff.id" :value="index.id">
        <div
          class="border-[3px] text-gray-700 border-blue-300 bg-slate-50 rounded-3xl my-8 mx-20 p-10"
        >
          <div class="flex justify-between items-center">
            <div class="flex items-center gap-8">
              <div class="flex justify-start items-center text-3xl">難易度[[index + 1||""]]</div>
              <div class="text-xl flex items-center">
                問題数：
                <div class="px-1 flex text-2xl">[[diff||""]]</div>問
              </div>
            </div>
            <router-link
              :to="{ name: 'JudgeIndex', params: { key: 'difficulty' }, query: { q: index+  1 }}"
            >
              <div
                class="text-center py-2.5 px-8 text-lg font-medium bg-teal-500 text-gray-50 rounded-xl cursor-pointer hover:bg-teal-400"
              >チャレンジする</div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import commonMethods from "@/mixins/commonMethods";
// import moment from "moment";
// import StarRating from "vue-star-rating";

export default {
  name: "JudgeTop",
  mixins: [commonMethods],
  props: {
    msg: String
  },
  data() {
    return {
      contestList: [],
      diffList: [],
      currentuser: {
        id: ""
      },
      date: "",
      tutorialId: null
    };
  },
  // computed: {
  //   endTime: function(){
  //     return function(endtime){
  //       let date = ""
  //       if(endtime != null){
  //         date = moment(endtime).format('MM月DD日HH時MM分')
  //       }
  //       return date
  //     }
  //   }
  // },
  created() {
    this.checkCookieExpiration();
    setInterval(this.checkCookieExpiration, 60000);
    this.getContests();
    this.getDiff();
    this.getTutorial();
  },
  methods: {
    getContests() {
      axios
        .get(`/api/v1/judge/grouplist/`)
        .then(response => {
          this.contestList = response.data;
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErriiii", err);
        });
    },
    getDiff() {
      axios
        .get(`/api/v1/judge/diff/`)
        .then(response => {
          this.diffList = response.data;
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    getTutorial() {
      axios
        .get("/api/v1/judge/search", {
          params: {
            diff: 0
          }
        })
        .then(response => {
          this.tutorialId = response.data[0].id;
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    }
  }
};
</script>
<style scoped>
</style>