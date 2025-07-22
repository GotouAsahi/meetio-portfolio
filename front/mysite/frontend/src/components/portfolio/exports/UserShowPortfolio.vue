<template>
    <!-- 自分のプロフィールを見た場合 -->
    <div v-if="this.isCurrentUser()" class="w-full mb-5 mx-10 bg-white">
      <div v-for="portfolio in userPortfolios['results']" :key="portfolio.id">
        <router-link
          :to="{ name: 'PostDetails', params: { id: portfolio.id } }"
        >
          <div
            class="h-64 w-full mt-5 group relative flex flex-col overflow-hidden items-center bg-white border border-gray-200 rounded-lg shadow md:flex-row hover:bg-gray-100 z-2"
          >
            <div class="w-4/12">
              <!--サムネイル-->
              <img
                class="object-cover aspect-video w-[232px] h-64 border-r border-gray-200 transition duration-200 rounded-l-lg group-hover:scale-110 z-1"
                :src="portfolio.title_image"
                alt
              />
            </div>
            <!--作品情報-->
            <div class="w-8/12">
              <div
                class="flex flex-col justify-between p-4 leading-normal text-gray-700"
              >
                <!--日付-->
                <p class="mr-4 font-normal text-gray-700 text-right">
                  [[formatDate(portfolio.created_date||"2023-01-01T00:00:00.000000+09:00")]]
                </p>
                <!--タイトル-->
                <h5
                  class="flex justify-start ml-3 mb-3 text-xl font-bold tracking-tight text-gray-700 dark:text-white"
                >
                  [[portfolio.title||""]]
                </h5>
                <!--ジャンル/カテゴリ-->
                <p
                  class="ml-3 mb-2 text-left text-lg font-semibold text-gray-700"
                >
                  [[portfolio.ganre_id.name||""]]
                </p>
                <!--タグ-->
                <div class="md:mb-2">
                  <div class="flex flex-wrap justify-start">
                    <div v-for="tag in portfolio.tag" :key="tag.id">
                      <div
                        class="mb-2 ml-3 border-2 border-gray-600 hover:bg-teal-500 hover:border-teal-500 rounded-xl"
                      >
                        <router-link
                          :to="{
                            name: 'PostList',
                            params: { key: 'tag' },
                            query: { q: tag },
                          }"
                          class="px-4 flex items-center font-semibold text-gray-600 hover:text-white"
                          v-bind="{ ...$attrs }"
                        >
                          <font-awesome-icon
                            class="px-1"
                            icon="tag"
                          />[[tag||""]]
                        </router-link>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- 公開・非公開 -->
                <div class="flex flex-row text-gray-700 ml-3">
                  <div class="w-1/2">
                    <div v-if="portfolio.is_public" class="flex justify-start">
                      <font-awesome-icon
                        icon="earth-americas"
                        size="xl"
                        class="text-gray-700 mr-2"
                      />公開中
                    </div>
                    <div v-else class="flex justify-start">
                      <font-awesome-icon
                        icon="lock"
                        size="xl"
                        class="text-gray-700 mr-1"
                      />非公開
                    </div>
                  </div>
                  <!--評価・閲覧数-->
                  <!--いいね-->
                  <div class="w-1/2 flex flex-row justify-end mr-4">
                    <div class="items-center flex flex-row mr-3">
                      <!--評価ボタン-->
                      <font-awesome-icon
                        class="px-2 text-gray-700"
                        icon="heart"
                      />
                      <!--評価数-->
                      <p class="block text-base text-gray-700">
                        [[likeCount(portfolio)||""]]
                      </p>
                    </div>
                    <!-- 閲覧数 -->
                    <div class="flex items-center">
                      <a>
                        <font-awesome-icon
                          class="px-2 text-gray-800"
                          icon="eye"
                        />
                      </a>
                      <a class="text-base block text-gray-800"
                        >[[portfolio.view_count+1||""]]</a
                      >
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </router-link>
      </div>
    </div>
    <!-- 他人のプロフィールを見た場合 -->
    <div v-else class="w-full mb-5 mx-10 bg-white">
      <div v-for="portfolio in userPortfolios['results']" :key="portfolio.id">
        <router-link
          :to="{ name: 'PostDetails', params: { id: portfolio.id } }"
        >
          <div
            class="h-64 w-full mt-5 group relative flex flex-col overflow-hidden items-center bg-white border border-gray-200 rounded-lg shadow md:flex-row hover:bg-gray-100 z-2"
          >
            <div class="w-4/12">
              <!--サムネイル-->
              <img
                class="object-cover aspect-video w-[232px] h-64 border-r border-gray-200 transition duration-200 rounded-l-lg group-hover:scale-110 z-1"
                :src="portfolio.title_image"
                alt
              />
            </div>
            <!--作品情報-->
            <div class="w-8/12">
              <div
                class="flex w-full flex-col justify-between p-4 leading-normal text-gray-700"
              >
                <!--日付-->
                <p class="mr-4 font-normal text-gray-700 text-right">
                  [[formatDate(portfolio.created_date||"2023-01-01T00:00:00.000000+09:00")]]
                </p>
                <!--タイトル-->
                <h5
                  class="flex justify-start ml-3 mb-3 text-xl font-bold tracking-tight text-gray-700 dark:text-white"
                >
                  [[portfolio.title||""]]
                </h5>
                <!--ジャンル/カテゴリ-->
                <p
                  class="ml-3 mb-2 text-left text-lg font-semibold text-gray-700"
                >
                  [[portfolio.ganre_id.name||""]]
                </p>
                <!--タグ-->

                <div class="md:mb-2">
                  <div class="flex flex-wrap justify-start">
                    <div v-for="tag in portfolio.tag" :key="tag.id">
                      <div
                        class="mb-2 ml-3 border-2 border-gray-600 hover:bg-teal-500 hover:border-teal-500 rounded-xl"
                      >
                        <router-link
                          :to="{
                            name: 'PostList',
                            params: { key: 'tag' },
                            query: { q: tag },
                          }"
                          class="px-4 flex items-center font-semibold text-gray-600 hover:text-white"
                          v-bind="{ ...$attrs }"
                        >
                          <font-awesome-icon
                            class="px-1"
                            icon="tag"
                          />[[tag||""]]
                        </router-link>
                      </div>
                    </div>
                  </div>
                </div>

                <!--いいね-->
                <!--評価・閲覧数-->
                <div
                  class="w-full flex flex-row justify-end pr-4 text-gray-700"
                >
                  <div class="items-center flex flex-row mr-3">
                    <!--評価ボタン-->
                    <button
                      type="button"
                      :class="{
                        'text-gray-500 hover:text-red-500': !isLike(portfolio),
                        'text-red-500 hover:text-gray-500': isLike(portfolio),
                      }"
                      @click="(event) => likePortfolio(event, portfolio)"
                    >
                      <font-awesome-icon class="px-2" icon="heart" />
                    </button>
                    <!--評価数-->
                    <p class="block text-sm text-black">
                      [[likeCount(portfolio)||""]]
                    </p>
                  </div>
                  <!-- 閲覧数 -->
                  <div class="flex items-center">
                    <a>
                      <font-awesome-icon
                        class="px-2 text-gray-800"
                        icon="eye"
                      />
                    </a>
                    <a class="text-base block text-gray-800"
                      >[[portfolio.view_count+1||""]]</a
                    >
                  </div>
                </div>
              </div>
            </div>
          </div>
        </router-link>
      </div>
    </div>
    <!--ページネーション-->
    <div class="w-full mb-5 mx-10 bg-white">
      <nav aria-label="Page navigation example">
        <ul class="inline-flex -space-x-px text-base h-10">
          <li>
            <!--戻るボタンで戻れるときのレイアウト-->
            <a
              href="#"
              v-if="userPortfolios['has_previous'] === true"
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
              v-if="userPortfolios['has_previous'] === false"
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
          <li v-for="(n, key) in userPortfolios['total_pages']" :key="key">
            <a
              href="#"
              v-if="currentPage === n"
              aria-current="page"
              @click.prevent.stop="getNumber(n)"
              class="flex items-center justify-center px-4 h-10 border border-gray-300 bg-green-50 text-teal-600 text-lg font-semibold"
            >
              [[ n ||""]]
            </a>
            <a
              href="#"
              v-else
              @click.prevent.stop="getNumber(n)"
              class="flex items-center justify-center px-4 h-10 text-teal-500 border border-gray-300 bg-white hover:bg-gray-50 hover:text-teal-600 hover:font-semibold leading-tight"
            >
              [[ n ||""]]
            </a>
          </li>
          <li>
            <!--進むボタンで進めるときのレイアウト-->
            <a
              href="#"
              v-if="userPortfolios['has_next'] === true"
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
              v-if="userPortfolios['has_next'] === false"
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

export default {
  name: "UserShowPortfolio",
  mixins: [settingMethods, commonMethods, searchMethods],
  props: ["user", "currentuser"],
  data() {
    return {
      userPortfolios: [],
      currentPage: 1,
    };
  },
  methods: {
    getUserPortfolio() {
      if (!this.isCurrentUser()) {
        axios
          .get(`/api/v1/portfolio/userindex/`, {
            params: {
              id: this.user.id,
              page: this.currentPage,
            },
          })
          .then((response) => {
            this.userPortfolios = response.data;
            console.log("status:", response.status);
            console.log("axiosGetData:", response.data);
          })
          .catch((err) => {
            console.log("axiosGetErr", err);
          });
      } else if (this.isCurrentUser) {
        axios
          .get(`/api/v1/portfolio/myindex/`, {
            withCredentials: true,
            headers: {
              Authorization: "JWT " + this.$cookies.get("token"),
            },
            params: {
              id: this.user_id,
              page: this.currentPage,
            },
          })
          .then((response) => {
            this.userPortfolios = response.data;
            console.log("status:", response.status);
            console.log("axiosGetData:", response.data);
          })
          .catch((err) => {
            console.log("axiosGetErr", err);
          });
      }
    },
    getNumber(number) {
      this.currentPage = Number(number);
      this.getUserPortfolio();
      window.scroll({ top: 0, behavior: "auto" });
    },
  },
  created() {
    this.getUserPortfolio();
    console.log("user = ", this.user.id);
  },
};
</script>
