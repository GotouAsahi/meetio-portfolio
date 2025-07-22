<template>
  <div class="article-post mx-auto my-10 w-10/12 text-gray-700">
    <div class="z-0">
      <div class="text-base">
        <div
          class="border-b-4 border-blue-900 pb-2 flex px-8 justify-between items-center text-2xl font-bold"
        >[[this.contest.name || ""]]</div>

        <!-- タブ -->
        <!-- contest-detail,rankingは変更 -->
        <div class="flex flex-row tabs mt-5 text-xl">
          <button
            class="border-2 border-gray-200 rounded-tl-lg"
            @click="changeTab('contest-detail')"
            :class="{
            'tab basis-1/2 px-10 py-3 hover:text-teal-600 bg-white border-gray-200 border-b-4 border-b-teal-600 text-teal-600 font-semibold': selectedTab === 'contest-detail',
            'tab basis-1/2 px-10 py-3 text-gray-700 hover:text-teal-600 bg-white border-t-2 border-b-2 border-gray-200': selectedTab !== 'contest-detail'
          }"
          >コンテスト詳細</button>
          <button
            @click="changeTab('ranking')"
            :class="{
            'tab basis-1/2 px-10 py-3 hover:text-teal-600 bg-white border-2 rounded-tr-lg border-gray-200 border-b-4 border-b-teal-600 text-teal-600 font-semibold': selectedTab === 'ranking',
            'tab basis-1/2 px-10 py-3 text-gray-700 hover:text-teal-600 bg-white border-2 rounded-tr-lg border-b-2 border-gray-200': selectedTab !== 'ranking'
          }"
          >ランキング</button>
        </div>

        <!-- タブ内 -->
        <div class="border-x-2 border-b-2 border-t bg-white border-gray-200 rounded-b-lg">
          <div class="bg-white rounded-lg">
            <div
              class="flex flex-wrap bg-white w-full rounded-b"
              v-if="selectedTab === 'contest-detail'"
            >
              <!-- コンテスト詳細 -->
              <div class="w-full mx-8 my-5">
                <!-- v-if="selectedTab === 'contest-detail'" -->
                <div class="w-full bg-gray-200 px-6 py-2">
                  <div class="grid grid-cols-3 gap-4 items-center">
                    <div v-if="this.contest != null">
                      <div v-for="admin in this.contest.admins" :key="admin.id">
                        <div class="col-span-2 w-full flex text-xl justify-start items-center">
                          開催者 :
                          <div class="flex flex-row items-center text-gray-700 ml-5">
                            <!--ユーザーアイコン-->
                            <div class="flex h-[2.5rem] w-[2.5rem]">
                              <img
                                class="object-cover aspect-square rounded-full"
                                :src="admin.icon"
                                alt="Image Description"
                              />
                            </div>
                            <p class="ml-4 text-xl">[[ admin.username || ""]]</p>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div class="col-span-1 w-full flex text-xl justify-start items-center">
                      問題数 :
                      <div class="ml-4 text-2xl font-semibold">
                        [[this.contest.problems ? this.contest.problems.length ||
                        "-" : "-"]]問
                      </div>
                    </div>
                    <div class="col-span-1 w-full flex text-xl justify-start items-center">
                      参加人数 :
                      <div class="ml-2 text-2xl font-semibold">
                        [[this.contest.member ? this.contest.member.length || "-" :
                        "-"]]人
                      </div>
                    </div>
                    <div class="col-span-1 w-full flex text-xl justify-start items-center">
                      終了日時 :
                      <div
                        class="ml-2 text-2xl font-semibold"
                      >[[this.endTime(contest.endtime) || ""]]</div>
                    </div>
                  </div>
                </div>
                <div
                  class="border-b-2 border-blue-900 pb-2 flex px-8 justify-between items-center text-2xl font-bold mt-5"
                >コンテスト内容</div>
                <div
                  class="flex justify-start text-left text-xl mt-6 mx-8"
                >[[this.contest.introduction || ""]]</div>
                <div v-if="currentuser.id" class="flex justify-center items-center mt-16 mb-8">
                  <div v-if="this.checkJoin()">
                    <button
                      class="text-center py-[12px] px-12 text-xl font-medium bg-teal-500 text-gray-50 rounded-xl cursor-pointer hover:bg-teal-400"
                      @click="contestJoin(this.contest.id)"
                    >参加する</button>
                  </div>
                  <div v-else>
                    <router-link
                      class="text-center py-[12px] px-12 text-xl font-medium bg-teal-500 text-gray-50 rounded-xl cursor-pointer hover:bg-teal-400"
                      :to="{ name: 'JudgeIndex', params: { key: 'contest' }, query: { q: this.contest.id } }"
                    >問題を見る</router-link>
                  </div>
                </div>
                <div v-else class="flex justify-center items-center mt-16 mb-8">
                  <button
                    class="text-center py-[12px] px-12 text-xl font-medium bg-teal-500 text-gray-50 rounded-xl cursor-pointer hover:bg-teal-400"
                    @click="contestJoin(this.contest.id)"
                  >参加する</button>
                </div>
              </div>
            </div>

            <!-- ランキング -->
            <div
              class="border-x-2 border-b-2 border-t bg-white border-gray-200 rounded-b-lg"
              v-else-if="selectedTab === 'ranking'"
            >
              <div class="flex flex-col bg-white w-full rounded-b">
                <!-- v-else-if="selectedTab === 'ranking'" -->
                <!-- ランキング表示 -->
                <div class="mx-8 my-5">
                  <div
                    class="border-b-2 border-blue-900 pb-2 flex px-8 justify-between items-center text-2xl font-bold mt-5"
                  >現在のランキング</div>
                  <div
                    class="border-b-2 border-blue-900 pb-2 flex px-8 justify-between items-center text-xl font-bold mx-8"
                  >
                    <div class="w-full grid grid-cols-5 gap-4 items-center mt-5">
                      <div class="col-span-1 w-full flex text-xl items-center">
                        <div>ランキング（位）</div>
                      </div>
                      <div class="col-span-2 w-full flex text-xl items-center">
                        <div>ユーザーネーム</div>
                      </div>
                      <div class="col-span-1 w-full flex text-xl items-center">
                        <div>スコア（点）</div>
                      </div>
                      <div class="col-span-1 w-full flex text-xl items-center"></div>
                    </div>
                  </div>

                  <!-- ランキング表示 -->
                  <div v-if="this.contest != null">
                    <div v-for="user in this.contest.member_rank" :key="user.id">
                      <div class="bg-gray-200 mt-5 mx-8">
                        <div class="w-full grid grid-cols-5 gap-4 items-center px-8 py-1">
                          <div
                            class="col-span-1 w-full flex text-xl font-semibold justify-center items-center"
                          >
                            <div>[[user.rank||" - "]]位</div>
                          </div>
                          <div class="col-span-2 w-full flex text-xl items-center">
                            <div class="flex flex-row items-center text-gray-700">
                              <!--ユーザーアイコン-->
                              <div class="flex h-[2.5rem] w-[2.5rem]">
                                <img
                                  class="object-cover aspect-square rounded-full"
                                  :src="user.icon"
                                  alt="Image Description"
                                />
                              </div>
                              <!--ユーザーネーム-->
                              <p
                                class="text-lg pl-4 hover:underline cursor-pointer"
                              >[[user.user_name||""]]</p>
                            </div>
                          </div>
                          <div class="col-span-1 w-full flex text-xl font-semibold items-center">
                            <div>[[user.total_score||""]]点</div>
                          </div>
                          <router-link
                            class="col-span-1 w-full flex text-lg justify-center items-center hover:underline cursor-pointer"
                            :to="{ name: 'UserShow', params: { id: user.user_id } }"
                          >詳細を見る</router-link>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
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
import moment from "moment";
// import StarRating from "vue-star-rating";

export default {
  name: "JudgeContest",
  mixins: [commonMethods],
  props: {
    msg: String
  },
  data() {
    return {
      contest: [],
      currentuser: {
        id: ""
      },
      selectedTab: "contest-detail",
      member: {
        member: []
      }
    };
  },
  computed: {
    endTime: function() {
      return function(endtime) {
        let date = "";
        if (endtime != null) {
          date = moment(endtime).format("M月D日k時m分");
        }
        return date;
      };
    }
  },
  async created() {
    await this.checkCookieExpiration();
    setInterval(this.checkCookieExpiration, 60000);
    if (this.$store.getters.isAuthenticated) {
      await this.getCurrentUser();
    }
    this.getContest();
  },
  watch: {
    currentuser: function() {
      this.checkJoin(this.currentuser.id);
    }
  },
  methods: {
    getContest() {
      axios
        .get(`/api/v1/judge/grouplist/${this.$route.params.id}`)
        .then(response => {
          this.contest = response.data;
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    contestJoin(id) {
      if (!this.$store.getters.isAuthenticated) {
        alert("ログインして下さい");
        this.$router.push({ name: "LoginForm" });
      } else {
        this.contest.member.push(this.currentuser.id);
        delete this.contest["member_rank"];
        console.log("memm", this.contest.member);
        console.log("id", this.contest);
        /*
        axios
          .put(`/api/v1/judge/group/${id}/`, this.contest)
          .then(response => {
            console.log("status:", response.status);
            console.log("axiosGetData:", response.data);
            this.$router.push({
              name: "JudgeIndex",
              params: { key: "content" },
              query: { q: this.contest }
            });
          })
          .catch(err => {
            console.log("axiosGetErr", err);
          });
          */
        this.member.member = [this.currentuser.id];
        axios
          .put(`/api/v1/judge/group_join/${id}/`, this.member)
          .then(response => {
            console.log("status:", response.status);
            console.log("axiosGetData:", response.data);
            this.$router.push({
              name: "JudgeIndex",
              params: { key: "contest" },
              query: { q: this.contest.id }
            });
          })
          .catch(err => {
            console.log("axiosGetErr", err);
          });
      }
    },
    changeTab(tab) {
      this.selectedTab = tab;
    },
    checkJoin() {
      console.log("tetet", this.currentuser.id);
      if (this.contest.member && this.contest.member.includes) {
        return !this.contest.member.includes(this.currentuser.id);
      } else {
        console.error(
          "this.contest.member is undefined or does not have includes method"
        );
      }
    }
    // showJoin(){
    //   this.$router.push({ name: 'JudgeIndex', params: { key: 'contest' }, query: { q: this.contest.id } });
    // },
  }
};
</script>
<style scoped></style>