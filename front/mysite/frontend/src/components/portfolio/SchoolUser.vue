<template>
  <div class="relative mx-auto my-3 w-10/12 mt-10">
    <div class="border-b-4 border-teal-800 mb-3 flex space-x-2 px-5 py-2 justify-between items-end">
      <div
        class="font-semibold hs-tab-active:border-teal-500 hs-tab-active:text-teal-600 inline-flex items-end gap-2 border-transparent text-2xl whitespace-nowrap text-gray-700"
      >ユーザー検索</div>
    </div>
    <div class="flex items-center justify-start gap-4 px-5">
      <form
        class="flex items-end gap-4"
        @submit.prevent="searchSchoolUser(schoolKey[0], schoolKey[1], schoolKey[2], schoolKey[3])"
      >
        <div class="z-30">
          <p class="text-left text-[17px] mb-1 text-gray-700">学校名</p>
          <vue3-simple-typeahead
            class="simple-typeahead bg-gray-200 border-gray-200 border text-gray-900 text-lg rounded-lg hover:bg-gray-300 hover:border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5 z-30"
            ref="typeahead"
            v-model="schoolKey[0]"
            placeholder=" "
            :items="suggestSchools"
            :minInputLength="1"
            :itemProjection="itemProjectionFunction"
            @selectItem="selectSchoolItemEventHandler"
          ></vue3-simple-typeahead>
        </div>
        <div class="z-30">
          <p class="text-left text-[17px] mb-1 text-gray-700">学科選択</p>
          <vue3-simple-typeahead
            class="simple-typeahead bg-gray-200 border-gray-200 border text-gray-900 text-lg rounded-lg hover:bg-gray-300 hover:border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5 z-30"
            ref="typeahead"
            v-model="schoolKey[1]"
            placeholder=" "
            :items="suggestDepartment"
            :minInputLength="1"
            :itemProjection="itemProjectionFunction"
            v-on:focus="searchDepartment"
            v-on:onBlur="clearDepartmentSuggest"
            @selectItem="selectDepartmentItemEventHandler"
          ></vue3-simple-typeahead>
        </div>
        <div class="z-30">
          <p class="text-left text-[17px] mb-1 text-gray-700">得意言語</p>
          <vue3-simple-typeahead
            class="simple-typeahead bg-gray-200 border-gray-200 border text-gray-900 text-lg rounded-lg hover:bg-gray-300 hover:border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5 z-20"
            ref="typeahead"
            v-model="schoolKey[3]"
            placeholder=" "
            :items="langList"
            :minInputLength="1"
            :itemProjection="itemProjectionFunction"
            @selectItem="selectLanguageItemEventHandler"
          ></vue3-simple-typeahead>
        </div>
        <div class="z-30">
          <p class="text-left text-[17px] mb-1 text-gray-700">学年</p>
          <select
            v-model="schoolKey[2]"
            class="px-6 py-[13px] block text-lg rounded-lg bg-gray-200 border-gray-200 border text-gray-900 hover:bg-gray-300 hover:border-gray-300 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none z-20"
          >
            <option value>全学年</option>
            <option value="1">1年</option>
            <option value="2">2年</option>
            <option value="3">3年</option>
            <option value="4">4年</option>
            <option value="5">5年</option>
            <option value="6">6年</option>
          </select>
        </div>
        <button
          type="submit"
          class="px-4 py-3 block rounded-lg text-base text-gray-900 bg-gray-200 border-gray-200 border-2 focus:outline-none focus:ring-0 hover:border-teal-500 peer hover:bg-teal-500 hover:text-white"
        >
          <font-awesome-icon class="px-1" icon="magnifying-glass" />
        </button>
      </form>
    </div>

    <!--検索したすべてのアイテム数-->
    <div
      class="flex px-5 pt-5 text-[20px] text-gray-700 font-semibold"
    >検索総件数：[[schoolUsers.count||"-"]]件</div>
    <!--ユーザー一覧-->
    <div v-if="schoolUsers['results']">
      <div class="pt-5 grid grid-cols-2 gap-4 px-5">
        <div v-for="user in schoolUsers['results'][0].user" :key="user.id">
          <div class="bg-white h-full rounded-lg shadow-md pl-4 pr-2 py-4 flex">
            <div class="w-1/3 border-r border-gray-200">
              <div class="flex flex-col">
                <router-link :to="{ name: 'UserShow', params: { id: user.id } }">
                  <!--ユーザーアイコン-->
                  <div class="flex flex-wrap justify-center items-center">
                    <div class="h-20 w-20">
                      <img
                        class="object-cover aspect-square rounded-full"
                        :src="user.icon"
                        alt="Image Description"
                      />
                    </div>
                  </div>
                  <!--ユーザーネーム-->
                  <p
                    class="text-2xl pt-2 font-semibold text-gray-900 hover:underline"
                  >[[user.username||""]]</p>
                </router-link>
              </div>
              <div v-if="user.school" class="flex flex-col mx-4">
                <!--学校-->
                <div class="text-lg text-gray-900 cursor-default">
                  <font-awesome-icon class="px-1" icon="school" />[[user.school.name||"未登録"]]
                </div>
                <!--学科-->
                <div class="flex justify-between my-1">
                  <div class="text-base text-left text-gray-900">学科</div>
                  <div class="text-base text-right text-gray-900">[[user.school.department||"未登録"]]</div>
                </div>
                <!--得意言語-->
                <div class="flex justify-between my-1">
                  <div class="text-base text-left text-gray-900">言語</div>
                  <div class="text-base text-right text-gray-900">[[user.likelanguage||"未登録"]]</div>
                </div>
                <!--学年-->
                <div class="flex justify-between mt-1">
                  <div class="text-base text-left text-gray-900">学年</div>
                  <div class="text-base text-right text-gray-900">[[user.school.grade||" - "]]年生</div>
                </div>
              </div>
            </div>
            <!--ユーザーの投稿-->
            <div class="grid grid-cols-2 gap-3 ml-2">
              <div v-for="post in schoolUsers['results'][1].portfolios[user.id]" :key="post.id">
                <div v-show="post.user_id.id === user.id">
                  <router-link
                    :to="{ name: 'PostDetails', params: { id: post.id } }"
                    class="group relative flex h-48 w-48 flex-col overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-32 xl:h-64 z-10"
                  >
                    <div
                      class="group relative flex h-48 flex-col overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-64 xl:h-96 z-10"
                    >
                      <img
                        :src="post.title_image"
                        loading="lazy"
                        alt="Photo by Minh Pham"
                        class="absolute inset-0 h-full w-full py-0 object-cover object-center transition duration-200 group-hover:scale-110 z-2"
                      />
                      <div
                        class="pointer-events-none absolute inset-0 bg-gradient-to-t from-gray-800 to-transparent md:via-transparent"
                      ></div>

                      <div>
                        <span
                          class="absolute block right-0 rounded-bl-lg top-0 bg-gray-900 text-sm font-semibold text-gray-200"
                        >
                          <div
                            class="my-1 mx-3"
                          >[[formatDate(post.created_date||"2023-01-01T00:00:00.000000+09:00")]]</div>
                        </span>
                      </div>

                      <div class="relative mt-auto p-2 bottom-0 text-left">
                        <h2
                          class="text-xl font-semibold text-white transition duration-100"
                        >[[post.title||""]]</h2>
                      </div>
                    </div>
                  </router-link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!--ページネーション-->
    <nav aria-label="Page navigation example" class="my-8">
      <ul class="inline-flex -space-x-px text-base h-10">
        <li>
          <!--戻るボタンで戻れるときのレイアウト-->
          <a
            href="#"
            v-if="schoolUsers['has_previous'] === true"
            @click.prevent.stop="getNumber(this.currentPage - 1)"
            class="flex items-center justify-center px-4 h-10 ml-0 leading-tight text-gray-600 bg-white border border-gray-300 rounded-l-lg hover:bg-gray-50 hover:text-teal-600 hover:font-semibold cursor-pointer"
          >
            <span class="sr-only">Previous</span>
            <svg
              class="w-3 h-3"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 6 10"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M5 1 1 5l4 4"
              />
            </svg>
          </a>
          <!--戻るボタンで戻れない時のレイアウト-->
          <a
            href="#"
            v-if="schoolUsers['has_previous'] === false"
            class="flex items-center justify-center px-4 h-10 ml-0 leading-tight text-gray-500 bg-gray border border-gray-300 rounded-l-lg pointer-events-none"
          >
            <span class="sr-only">Previous</span>
            <svg
              class="w-3 h-3"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 6 10"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1"
                d="M5 1 1 5l4 4"
              />
            </svg>
          </a>
        </li>
        <li v-for="(n, key) in schoolUsers['total_pages']" :key="key">
          <a
            href="#"
            v-if="currentPage === n"
            aria-current="page"
            @click.prevent.stop="getNumber(n)"
            class="flex items-center justify-center px-4 h-10 border border-gray-300 bg-white hover:bg-gray-50 text-teal-600 text-lg font-semibold"
          >
            [[
            n ||""]]
          </a>
          <a
            href="#"
            v-else
            @click.prevent.stop="getNumber(n)"
            class="flex items-center justify-center px-4 h-10 text-teal-500 border border-gray-300 bg-white hover:bg-gray-50 hover:text-teal-600 hover:font-semibold leading-tight"
          >
            [[
            n ||""]]
          </a>
        </li>
        <li>
          <!--進むボタンで進めるときのレイアウト-->
          <a
            href="#"
            v-if="schoolUsers['has_next'] === true"
            @click.prevent.stop="getNumber(this.currentPage + 1)"
            class="flex items-center justify-center px-4 h-10 ml-0 leading-tight text-gray-600 bg-white border border-gray-300 rounded-r-lg hover:bg-gray-50 hover:text-teal-600 hover:font-semibold cursor-pointer"
          >
            <span class="sr-only">Next</span>
            <svg
              class="w-3 h-3"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 6 10"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="m1 9 4-4-4-4"
              />
            </svg>
          </a>
          <!--進むボタンで進めれないときのレイアウト-->
          <a
            href="#"
            v-if="schoolUsers['has_next'] === false"
            class="flex items-center justify-center px-4 h-10 ml-0 leading-tight text-gray-500 bg-gray border border-gray-300 rounded-r-lg pointer-events-none"
          >
            <span class="sr-only">Next</span>
            <svg
              class="w-3 h-3"
              aria-hidden="true"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 6 10"
            >
              <path
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="1"
                d="m1 9 4-4-4-4"
              />
            </svg>
          </a>
        </li>
      </ul>
    </nav>
  </div>
</template>





<script>
import axios from "axios";
import settingMethods from "@/mixins/settingMethods";
import commonMethods from "@/mixins/commonMethods";
import searchMethods from "@/mixins/searchMethods";
import { langSearchlist } from "@/data/judgeform.js";

export default {
  name: "schoolUser",
  mixins: [settingMethods, commonMethods, searchMethods],
  props: [
    "searchUsers",
    "searchSchoolKey",
    "searchResults",
    "searchPortfolios"
  ],
  data() {
    return {
      schoolUsers: [],
      schoolKey: [null, null, null, null],
      portfolios: [],
      currentPage: 1,
      suggestAll: [],
      suggestSchools: [],
      suggestDepartment: [],
      langList: langSearchlist,
      SchoolPortfolios: [],
      userPortfolios: []
    };
  },
  created() {
    this.checkCookieExpiration();
    setInterval(this.checkCookieExpiration, 60000);
    if (!this.searchUsers || this.searchUsers.length === 0) {
      console.log("No Users", this.searchUsers);
    } else {
      this.searchSchoolUser(
        this.searchUsers,
        null,
        null,
        null,
        null,
        );
        alert(this.searchUsers)
        console.log('test = ', this.schoolUsers)
    }
    this.schoolSuggest();
  },
  watch: {
    searchPortfolios: {
      handler(newPortfolios) {
        this.SchoolPortfolios = newPortfolios;
      },
      immediate: true
    }
  },
  methods: {
    getNumber(number) {
      this.currentPage = Number(number);
      this.searchSchoolUser(
        this.schoolKey[0],
        this.schoolKey[1],
        this.schoolKey[2],
        this.schoolKey[3],
        this.currentPage
      );
    },
    schoolSuggest() {
      axios
        .get("/api/v1/school/school_suggest/")
        .then(response => {
          this.suggestAll = response.data;
          for (let obj of this.suggestAll) {
            if (this.suggestSchools.indexOf(obj["name"]) === -1) {
              this.suggestSchools.push(obj["name"]);
            }
          }
          console.log("uuuuuuu", this.suggestSchools);
        })
        .catch(error => {
          // エラーハンドリング
          console.error(error);
        });
    },
    selectUserPortfolios(user) {
      this.userPortfolios = [];
      for (let obj of this.SchoolPortfolios) {
        if (obj["user_id"]["id"] === user) {
          this.userPortfolios.push(obj);
        }
      }
      return this.userPortfolios;
    },
    selectSchoolItemEventHandler(item) {
      this.schoolKey[0] = item;
    },
    selectDepartmentItemEventHandler(item) {
      this.schoolKey[1] = item;
    },
    selectLanguageItemEventHandler(item) {
      this.schoolKey[3] = item;
    },
    searchDepartment() {
      for (let obj of this.suggestAll) {
        if (obj["name"] == this.schoolKey[0])
          this.suggestDepartment.push(obj["department"]);
        console.log(this.schoolKey[0]);
      }
      console.log(this.suggestDepartment);
    },
    clearDepartmentSuggest() {
      this.suggestDepartment.splice(0);
    }
  }
};
</script>
<style>
.loader,
.loader:after {
  border-radius: 50%;
  width: 5em;
  height: 5em;
  position: relative;
}

.loader {
  margin: auto;
  font-size: 10px;
  position: relative;
  text-indent: -9999em;
  border-top: 1.1em solid rgba(255, 255, 255, 0.2);
  border-right: 1.1em solid rgba(255, 255, 255, 0.2);
  border-bottom: 1.1em solid rgba(255, 255, 255, 0.2);
  border-left: 1.1em solid #ffffff;
  -webkit-transform: translateZ(0);
  -ms-transform: translateZ(0);
  transform: translateZ(0);
  -webkit-animation: load8 1.1s infinite linear;
  animation: load8 1.1s infinite linear;
}

@-webkit-keyframes load8 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }

  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

@keyframes load8 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }

  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
</style>