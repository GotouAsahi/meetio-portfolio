<template>
  <div class="article-post mx-auto my-10 w-10/12 text-gray-700">
    <div
      class="border-b-4 border-blue-900 flex px-12 pb-3 justify-between items-center text-2xl font-semibold"
    >
      <div v-if="contestflag">[[this.contestname||""]]</div>
      <div v-else>難易度[[this.$route.query.q||""]]</div>
    </div>
    <!-- リスト中身 -->
    <div v-if="testList != null">
      <div v-for="test in testList" :key="test.id">
        <div class="border-[3px] text-gray-700 border-blue-300 bg-slate-50 rounded-3xl my-8 mx-20 px-10 py-3">
          <div class="grid grid-flow-row-dense grid-cols-4 grid-rows-5">
            <div
              class="col-span-3 row-span-3 flex justify-start items-center text-3xl"
            >[[test.title||""]]</div>
            <div class="col-span-1 row-span-3 flex justify-start items-center text-xl">
              正解率：
              <div class="flex pl-1 text-2xl">[[test.accuracy||""]]%</div>
            </div>
            <div class="col-span-1 row-span-2 flex justify-start items-center text-xl pt-1">
              難易度：
              <star-rating
                :increment="0.01"
                :rating="test.difficulty"
                :read-only="true"
                v-bind:star-size="18"
                :show-rating="false"
                :inline="true"
              ></star-rating>
            </div>
            <div class="col-span-1 row-span-2 flex justify-start items-center text-xl pt-1">
              目標解答時間：
              <div class="flex pl-1 text-xl">[[test.target_time||""]]分</div>
            </div>
            <div class="col-span-1 row-span-2 flex justify-start items-center text-xl pt-1">
              解答人数：
              <div class="flex pl-1 text-xl">[[test.user_answer_count||""]]人</div>
            </div>
            <div class="col-span-1 row-span-2 flex justify-start items-center text-xl">
              <div v-if="contestflag">
                <router-link
                  :to="{name: 'JudgeForm',params: {group_id: this.$route.query.q ,id: test.id }}"
                >
                  <div
                    class="text-center py-2.5 px-8 text-lg font-medium bg-teal-500 text-gray-50 rounded-xl cursor-pointer hover:bg-teal-400"
                  >チャレンジする</div>
                </router-link>
              </div>
              <div v-else>
                <router-link :to="{name: 'JudgeForm',params: {group_id: 1 ,id: test.id }}">
                  <div
                    class="text-center py-2.5 px-8 text-lg font-medium bg-teal-500 text-gray-50 rounded-xl cursor-pointer hover:bg-teal-400"
                  >チャレンジする</div>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import commonMethods from "@/mixins/commonMethods";
import StarRating from "vue-star-rating";

export default {
  name: "JudgeIndex",
  mixins: [commonMethods],
  props: {
    msg: String
  },
  data() {
    return {
      testList: [],
      contestname: "",
      contestflag: true
    };
  },
  components: {
    StarRating
  },
  created() {
    this.checkCookieExpiration();
    setInterval(this.checkCookieExpiration, 60000);
    this.getTestList();
  },
  methods: {
    getTestList() {
      if (this.$route.params.key == "contest") {
        axios
          .get(`/api/v1/judge/grouplist/${this.$route.query.q}`)
          .then(response => {
            this.testList = response.data.problems;
            this.contestname = response.data.name;
            this.contestflag = true;
            console.log("status:", response.status);
            console.log("axiosGetData:", response.data);
          })
          .catch(err => {
            console.log("axiosGetErr", err);
          });
      } else if (this.$route.params.key == "difficulty") {
        axios
          .get("/api/v1/judge/search", {
            params: {
              diff: this.$route.query.q
            }
          })
          .then(response => {
            this.testList = response.data;
            this.contestflag = false;
            console.log("status:", response.status);
            console.log("axiosGetData:", response.data);
          })
          .catch(err => {
            console.log("axiosGetErr", err);
          });
      }
    }
  }
};
</script>
<style scoped>
</style>