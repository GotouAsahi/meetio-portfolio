<template>
  <!--↓のdivを消すとエラーを吐くので消さないでください（refが関係してる）消したい場合は志多まで-->
  <div class="relative mx-auto my-3 w-10/12 mt-10" ref="margin_search">
    <div v-if="this.indexflag">
      <div class="border-b-4 border-teal-800 pb-2 flex space-x-2 px-5 justify-between items-end">
        <div
          class="font-semibold hs-tab-active:border-teal-500 hs-tab-active:text-teal-600 inline-flex items-end gap-2 border-transparent text-2xl whitespace-nowrap text-gray-700"
        >[[this.$route.query.q||""]]</div>
        <div>
          <div
            class="hs-tab-active:font-semibold hs-tab-active:border-teal-500 hs-tab-active:text-teal-600 px-5 inline-flex items-end gap-2 whitespace-nowrap text-gray-500 hover:text-teal-500 hover:font-semibold"
            id="tabs-with-underline-item-2"
            data-hs-tab="#tabs-with-underline-2"
            aria-controls="tabs-with-underline-2"
            role="tab"
          >
            <button
              v-bind:disabled="this.switchflag"
              v-bind:class="{ 'text-teal-500 font-semibold': switchflag }"
              @click="event => newArrivalOrder(event)"
            >最新の投稿順</button>
          </div>
          <div
            class="hs-tab-active:font-semibold hs-tab-active:border-teal-500 hs-tab-active:text-teal-600 inline-flex items-end gap-2 whitespace-nowrap text-gray-500 hover:text-teal-500 hover:font-semibold"
            id="tabs-with-underline-item-3"
            data-hs-tab="#tabs-with-underline-3"
            aria-controls="tabs-with-underline-3"
            role="tab"
          >
            <button
              v-bind:disabled="!this.switchflag"
              v-bind:class="{ 'text-teal-500 font-semibold': !switchflag }"
              @click="event => searchLikeOrder(event, this.$route.params.key, this.$route.query.q)"
            >人気の投稿順</button>
          </div>
        </div>
      </div>
    </div>
    <div v-else>
      <div class="border-b-4 border-teal-800 pb-2 flex space-x-2 px-5 justify-between items-end">
        <div
          class="font-semibold hs-tab-active:border-teal-500 hs-tab-active:text-teal-600 inline-flex items-end gap-2 border-transparent text-2xl whitespace-nowrap text-gray-700"
        >[[this.keyword||""]]</div>
      </div>
    </div>
    <div v-if="this.$route.params.key == 'category'">
      <div class="grid grid-cols-3 p">
        <div v-for="genre in genreList[getCategoryKey()]" :key="genre.value" class="py-4">
          <router-link
            :to="{ name: 'PostList', params: { key: 'genre' }, query: { q: genre.label } }"
            class="w-full text-center py-2.5 px-6 text-base font-medium bg-gray-200 text-gray-700 rounded-xl cursor-pointer sm:w-min hover:bg-teal-500 hover:text-gray-50 mb-4"
            v-bind="{ ...$attrs }"
          >[[genre.label||""]]</router-link>
        </div>
      </div>
    </div>
    <div class="hover_content" ref="hover_content">
      <!--ホバーしたとき画像拡大-->
      <img
        :src="hoverImage"
        :ref="img_style"
        :style="{ transform: `translate(${content_left}px, ${content_height}px)`, visibility: hoverFlag }"
      />
    </div>
    <!--ロードが完了するまで透明の作品を表示（ロード前と後では画面の上下が激しいため）-->
    <div
      class="group relative flex h-48 flex-col overflow-hidden rounded-lg bg-gray-100 md:h-64 xl:h-96 z-10"
      v-if="loading"
    ></div>
    <!--検索したすべてのアイテム数-->
    <div
      class="flex px-5 pt-5 text-[20px] text-gray-700 font-semibold"
    >検索総件数：[[portfolios.count||"-"]]件</div>
    <!--ここからグリッドレイアウト-->
    <div class="py-[10px] items-center justify-between grid grid-cols-5 gap-8" ref="test">
      <div
        v-for="portfolio in portfolios['results']"
        :key="portfolio.id"
        class="carousel_item"
        :ref="portfolio.id"
        v-on:mouseover="mouseOverAction(portfolio)"
        v-on:mouseleave="mouseLeaveAction"
      >
        <router-link :to="{ name: 'PostDetails', params: { id: portfolio.id } }">
          <div
            class="group relative flex h-48 flex-col overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-64 xl:h-80 z-10"
          >
            <!--サムネイル画像-->
            <img
              :src="portfolio.title_image"
              @load="load"
              alt="Photo by Minh Pham"
              class="absolute inset-0 h-full w-full object-cover object-center transition duration-200 group-hover:scale-110 z-2"
            />
            <div
              class="pointer-events-none absolute inset-0 bg-gradient-to-t from-black to-transparent md:via-transparent"
            ></div>

            <div>
              <!--投稿日-->
              <span
                class="absolute block right-0 rounded-bl-lg bg-gray-900 text-sm font-semibold text-gray-200"
              >
                <div
                  class="my-1 mx-3"
                >[[formatDate(portfolio.created_date||"2023-01-01T00:00:00.000000+09:00")]]</div>
              </span>
            </div>

            <div>
              <div class="flex justify-between">
                <!--タイトル-->
                <h2
                  class="absolute h-4/5 w-4/5 p-2 flex items-end text-xl text-left font-semibold text-white transition duration-100"
                >[[portfolio.title||""]]</h2>

                <!--評価ボタン-->
                <div class="absolute flex h-4/5 p-2 items-end right-0">
                  <div class="flex items-center">
                    <button
                      type="button"
                      :class="{
                      'text-white hover:text-red-500': !isLike(portfolio),
                      'text-red-500 hover:text-white': isLike(portfolio)
                    }"
                      @click="event => likePortfolio(event, portfolio)"
                    >
                      <font-awesome-icon class="pr-2 text-lg" icon="heart" />
                    </button>
                    <!--評価数-->
                    <p class="block text-lg text-white">[[likeCount(portfolio)||""]]</p>
                  </div>
                </div>
              </div>

              <ul>
                <li class="absolute bottom-0 w-full h-1/5 bg-white">
                  <div class="absolute">
                    <!--ジャンル-->
                    <router-link
                      :to="{ name: 'PostList', params: { key: 'genre' }, query: { q: portfolio.ganre_id.name } }"
                      class="px-2 pt-1 text-xs font-semibold flex justify-start text-gray-900 transition duration-100 hover:underline"
                      v-bind="{ ...$attrs }"
                    >[[portfolio.ganre_id.name||""]]</router-link>

                    <div class="flex items-center bottom-0 p-2 pt-0">
                      <!--ユーザーアイコン-->
                      <router-link :to="{ name: 'UserShow', params: { id: portfolio.user_id.id } }">
                        <div class="flex h-[2.5rem] w-[2.5rem]">
                          <img
                            class="object-cover aspect-square rounded-full"
                            :src="portfolio.user_id.icon"
                            alt="Image Description"
                          />
                        </div>
                      </router-link>

                      <!--ユーザーネーム-->
                      <router-link :to="{ name: 'UserShow', params: { id: portfolio.user_id.id } }">
                        <p
                          class="font-semibold text-gray-900 text-xl pl-2 hover:underline"
                        >[[portfolio.user_id.username||""]]</p>
                      </router-link>
                    </div>
                  </div>
                </li>
              </ul>
            </div>
          </div>
        </router-link>
      </div>
    </div>
    <!--ページネーション-->
    <nav aria-label="Page navigation example" class="my-8">
      <ul class="inline-flex -space-x-px text-base h-10">
        <li>
          <!--戻るボタンで戻れるときのレイアウト-->
          <a
            href="#"
            v-if="portfolios['has_previous'] === true"
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
            v-if="portfolios['has_previous'] === false"
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
        <li v-for="(n, key) in portfolios['total_pages']" :key="key">
          <a
            href="#"
            v-if="currentPage === n"
            aria-current="page"
            @click.prevent.stop="getNumber(n)"
            class="flex items-center justify-center px-4 h-10 border border-gray-300 bg-green-50 text-teal-600 text-lg font-semibold"
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
            v-if="portfolios['has_next'] === true"
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
            v-if="portfolios['has_next'] === false"
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
  name: "PostList.vue",
  mixins: [settingMethods, commonMethods, searchMethods],

  data() {
    return {
      portfolios: [],
      evacuationPortfolios: [],
      user: [],
      currentuser: {
        id: ""
      },
      like_list: {
        like_count: []
      },
      genreList: [],
      keyword: null,
      key: null,
      carouselIndex: 0,
      hoverFlag: "hidden",
      hoverIndex: 1,
      content_height: 0,
      content_left: 0,
      domFlag: false,
      content_margin: 0,
      content_padding: 0,
      timer: null,
      img_style: "ho",
      carsel_flag: true,
      selectedPortfolios: null,
      switchflag: true,
      q: this.$route.query.q,
      indexflag: true,
      currentPage: 1,
      loading: true
    };
  },
  watch: {
    "$route.params.key": {
      handler: function(search) {
        console.log(search);
        this.q = this.$route.query.q;
        this.changePortfolio();
      },
      deep: true,
      immediate: true
    },
    "portfolio.title_image": function(val, oldVal) {
      console.log(val + " old = " + oldVal);
    }
  },
  async created() {
    this.checkCookieExpiration();
    this.changePortfolio();
    setInterval(this.checkCookieExpiration, 60000);
    if (this.$store.getters.isAuthenticated) {
      await this.getCurrentUser(); // Promiseを待つ
    }
    if (this.$route.params.key == "post") {
      this.indexflag = false;
      this.keyword = "最近の投稿一覧";
      this.getPortfolios();
    } else if (this.$route.params.key == "like") {
      this.indexflag = false;
      this.keyword = "人気の投稿一覧";
      this.getLikeOrder();
    } else if (this.$route.params.key == "follow") {
      try {
        this.indexflag = false;
        this.keyword = "フォロー中一覧";
        this.getFollowPortfolio(); // Promiseが完了した後に実行
      } catch (error) {
        console.error("Error:", error);
      }
    }
  },
  mounted() {
    this.getGenre();
    window.addEventListener("DOMContentLoaded", () => {
      this.domFlag = true;
    });
  },
  methods: {
    getPortfolios() {
      axios
        .get(`/api/v1/portfolio/post_pagination/`, {
          params: {
            page: this.currentPage
          }
        })
        .then(response => {
          this.portfolios = response.data;
          console.log("status:", response.status);
          console.log("follow:", response.data);
          this.loading = false;
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    getFollowPortfolio() {
      axios
        .get(`/api/v1/portfolio/followUserPost_Pagination/`, {
          params: {
            id: this.currentuser.id,
            page: this.currentPage
          }
        })
        .then(response => {
          this.portfolios = response.data;
          console.log("status:", response.status);
          console.log("follow:", response.data);
          this.loading = false;
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    getLikeOrder() {
      axios
        .get(`/api/v1/portfolio/like_count_sort_pagination/`, {
          params: {
            page: this.currentPage
          }
        })
        .then(response => {
          this.portfolios = response.data;
          console.log("status:", response.status);
          console.log("follow:", response.data);
          this.loading = false;
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    handleGenreSearched(data, likedata, keyword) {
      // データを受け取り、親コンポーネントのデータにセットするなどの処理を行う
      this.portfolios = data;
      this.likeOrderPortfolios = likedata;
      this.keyword = keyword;
    },
    mouseOverAction(portfolio) {
      this.hoverIndex = portfolio.id;
      this.hoverFlag = "visible";
      this.hoverImage = portfolio.title_image;
      this.hoverFlag = "hidden";
      clearTimeout(this.timer);
      this.timer = setTimeout(() => {
        if (this.$refs[this.hoverIndex][0] != null) {
          this.hoverFlag = "visible";
          /**親divのmarginを取り出し、余分な高さ(margin)を消す */
          this.content_margin =
            parseInt(
              window
                .getComputedStyle(this.$refs["margin_search"])
                .getPropertyValue("margin-top")
            ) + 25;
          this.content_height =
            this.$refs[this.hoverIndex][0]["offsetTop"] -
            this.$refs["hover_content"]["offsetTop"];
          /**ホバーした時作品が520以上左に寄っている場合はホバー画像を右に出す。520以下なら画像を左に出す。 */
          if (
            this.$refs[this.hoverIndex][0]["offsetLeft"] -
              this.carouselIndex * 1190 >=
            520
          ) {
            this.content_left =
              this.$refs[this.hoverIndex][0]["offsetLeft"] -
              this.carouselIndex * 1190 -
              this.$refs[this.img_style].width;
          } else {
            this.content_left =
              this.$refs[this.hoverIndex][0]["offsetLeft"] -
              this.carouselIndex * 1190 +
              this.$refs[this.hoverIndex][0]["offsetWidth"];
          }
        }
      }, 500);
    },
    mouseLeaveAction() {
      this.hoverFlag = "hidden";
      //志多
      window.clearTimeout(this.timer);
    },
    style_change(selectedPortfolios) {
      this.carsel_flag = false;
      this.selectedPortfolios = selectedPortfolios;
    },
    newArrivalOrder(event) {
      event.preventDefault();
      this.portfolios = this.evacuationPortfolios;
      this.switchflag = true;
    },
    getCategoryKey() {
      let categoryKey = null;
      switch (this.$route.query.q) {
        case "テクノロジー":
          categoryKey = 0;
          break;
        case "ビジネス":
          categoryKey = 1;
          break;
        case "クリエイティブ":
          categoryKey = 2;
          break;
        case "サウンド":
          categoryKey = 3;
          break;
        case "ビデオ":
          categoryKey = 4;
          break;
        case "デザイン":
          categoryKey = 5;
          break;
      }
      return categoryKey;
    },
    changePortfolio() {
      const key = this.$route.params.key;
      const value = this.q;
      this.evacuationPortfolios = [];
      this.switchflag = true;
      switch (key) {
        case "category":
          this.searchCategory(value);
          break;
        case "genre":
          this.searchGenre(value);
          break;
        case "search":
          this.searchWord(value, this.currentPage);
          break;
        case "tag":
          this.searchTag(value);
          break;
      }
    },
    getNumber(number) {
      this.currentPage = Number(number);
      if (this.$route.params.key == "post") {
        this.getPortfolios();
      } else if (this.$route.params.key == "follow") {
        this.getFollowPortfolio();
      } else if (this.$route.params.key == "like") {
        this.getLikeOrder();
      } else if (this.$route.params.key == "search") {
        this.searchWord(this.q, this.currentPage);
      }
    }
  }
};
</script>
<style>
nav .tag-menu {
  position: absolute;
  width: 100%;
  background: #4b5563;

  opacity: 0;
  visibility: hidden;
  transition: 0.5s;
  z-index: 10;
}

nav .tag-menu a {
  color: #fff;
  padding: 5px;
  display: block;
}

nav .tag-menu a:hover {
  color: #fff;
}

nav .tag-menu-2 {
  position: absolute;
  width: 150%;
  opacity: 0;
  visibility: hidden;
  transition: 0.5s;
  top: 60px;
  left: -50px;
}

nav .tag-menu-2 a {
  color: #fff;
  padding: 5px;
  display: block;
}

nav .tag-menu-2 a:hover {
  color: #fff;
}

nav .menu-item:hover ul {
  opacity: 1;
  visibility: visible;
}

.slide {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 300px;
  margin: auto;
  background: #fff;
}

.slide img {
  display: block;
  position: absolute;
  width: inherit;
  height: inherit;
  object-fit: cover;
  left: 100%;
  animation: slide-anime 35s ease infinite;
}

.slide img:nth-of-type(1) {
  animation-delay: 0s;
}

.slide img:nth-of-type(2) {
  animation-delay: 7s;
}

.slide img:nth-of-type(3) {
  animation-delay: 14s;
}

.slide img:nth-of-type(4) {
  animation-delay: 21s;
}

.slide img:nth-of-type(5) {
  animation-delay: 28s;
}

@keyframes slide-anime {
  0% {
    left: 100%;
  }

  2% {
    left: 0;
  }

  18% {
    left: 0;
  }

  20% {
    left: -100%;
  }

  100% {
    left: -100%;
  }
}

.category-banner {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 300px;
  margin: auto;
  background: #fff;
}

.category-banner img {
  width: inherit;
  height: inherit;
  object-fit: cover;
  left: 100%;
}

.hover_content {
  position: absolute;
  pointer-events: none;
  z-index: 40;
  display: relative;
}

.hover_content img {
  width: auto;
  height: 450px;
  margin: 0 10 0;
}
.example {
  width: 100%;
  grid-row: 1/2;
  grid-column: 1/2;
  width: 100%;
  height: 100%;
  border: 1px solid #333;
  background: red;
  z-index: 100;
}
</style>