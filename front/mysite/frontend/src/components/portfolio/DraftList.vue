<template>
  <div class="relative mx-auto my-3 w-10/12 mt-10" ref="margin_search">
    <div class="border-b-4 border-teal-800 pb-2 flex space-x-2 px-5 justify-between items-end">
      <div
        class="font-semibold hs-tab-active:border-teal-500 hs-tab-active:text-teal-600 inline-flex items-end gap-2 border-transparent text-2xl whitespace-nowrap text-gray-700">
        下書きリスト</div>
    </div>
    <!--ここからグリッドレイアウト-->
    <div class="py-[10px] flex items-center justify-between grid grid-cols-5 grid gap-8" ref="test">
      <div v-for="portfolio in portfolios['results']" :key="portfolio.id" class="carousel_item" :ref="portfolio.id"
        v-on:mouseover="mouseOverAction(portfolio)" v-on:mouseleave="mouseLeaveAction">
        <router-link :to="{ name: 'DraftEdit', params: { id: portfolio.id } }">
          <div
            class="group relative flex h-48 flex-col overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-64 xl:h-80 z-10">
            <!--サムネイル画像-->
            <img :src="portfolio.title_image" loading="lazy" alt="Photo by Minh Pham"
              class="absolute inset-0 h-full w-full object-cover object-center transition duration-200 group-hover:scale-110 z-2" />
            <div
              class="pointer-events-none absolute inset-0 bg-gradient-to-t from-black to-transparent md:via-transparent">
            </div>

            <div>
              <!--投稿日-->
              <span class="absolute block right-0 rounded-bl-lg bg-gray-900 text-sm font-semibold text-gray-200">
                <div class="my-1 mx-3">[[formatDate(portfolio.created_date||"2023-01-01T00:00:00.000000+09:00")]]</div>
              </span>
            </div>

            <div>
              <div class="flex justify-between">
                <!--タイトル-->
                <h2
                  class="absolute h-4/5 w-4/5 p-2 flex items-end text-xl text-left font-semibold text-white transition duration-100">
                  [[portfolio.title||""]]</h2>
              </div>

              <ul>
                <li class="absolute bottom-0 w-full h-1/5 bg-white">
                  <div class="absolute">
                    <!--ジャンル-->
                    <router-link
                      :to="{ name: 'PostList', params: { key: 'genre' }, query: { q: portfolio.ganre_id.name } }"
                      class="px-2 pt-1 text-xs font-semibold flex justify-start text-gray-900 transition duration-100 hover:underline"
                      v-bind="{ ...$attrs }">[[portfolio.ganre_id.name||""]]</router-link>

                    <div class="flex items-end bottom-0 p-2 pt-0">
                      <!--ユーザーアイコン-->
                      <router-link :to="{ name: 'UserShow', params: { id: portfolio.user_id.id } }">
                        <div class="flex h-[2.5rem] w-[2.5rem]">
                          <img class="object-cover aspect-square rounded-full" :src="portfolio.user_id.icon"
                            alt="Image Description" />
                        </div>
                      </router-link>

                      <!--ユーザーネーム-->
                      <router-link :to="{ name: 'UserShow', params: { id: portfolio.user_id.id } }">
                        <p class="font-semibold text-gray-900 text-xl pl-2 hover:underline">
                          [[portfolio.user_id.username||""]]</p>
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
    <div class="hover_content" ref="hover_content">
      <!--ホバーしたとき画像拡大-->
      <img :src="hoverImage" :ref="img_style"
        :style="{ transform: `translate(${content_left}px, ${content_height}px)`, visibility: hoverFlag }" />
    </div>
    <div class="text-center">
      <v-pagination v-model="currentPage" :length="portfolios['total_pages']" rounded="circle" color="green"
        :total-visible="6" @click="getNumber"></v-pagination>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import settingMethods from "@/mixins/settingMethods";
import commonMethods from "@/mixins/commonMethods";
import searchMethods from "@/mixins/searchMethods";

export default {
  name: "DraftList.vue",
  mixins: [settingMethods, commonMethods, searchMethods],
  beforeRouteUpdate(to, from, next) {
    if (to.query.q !== from.query.q) {
      // クエリパラメータ 'q' が変更された場合の処理をここに記述
      this.q = to.query.q;
      this.changePortfolio();
    }
    next();
  },
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
      currentPage: 1
    };
  },
  async created() {
    this.checkCookieExpiration();
    setInterval(this.checkCookieExpiration, 60000);
    if (this.$store.getters.isAuthenticated) {
      await this.getCurrentUser(); // Promiseを待つ
    }
    this.getUser();
  },
  mounted() {
    this.getGenre();
    window.addEventListener("DOMContentLoaded", () => {
      this.domFlag = true;
    });
  },
  methods: {
    getUser() {
      axios
        .get(`/api/v1/index/${this.$route.params.id}`)
        .then(response => {
          this.user = response.data;
          this.editUser = { ...response.data };
          if (this.user.school === null) {
            this.user.school = {
              name: "",
              faculty: "",
              department: "",
              grade: "",
              graduation_year: "",
              introduction: ""
            };
          } else {
            this.editSchool = { ...response.data.school };
            this.is_school = true;
          }
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
          this.getCurrentUserDraftPortfolio();
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    getCurrentUserDraftPortfolio() {
      if (!this.isCurrentUser) {
        return;
      }
      axios
        .get(`/api/v1/portfolio/mydraft/`, {
          withCredentials: true,
          headers: {
            Authorization: "JWT " + this.$cookies.get("token")
          },
          params: {
            id: this.user.id
          }
        })
        .then(response => {
          this.portfolios = response.data;
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
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
          this.content_margin =
            parseInt(
              window
                .getComputedStyle(this.$refs["margin_search"])
                .getPropertyValue("margin-top")
            ) + 25;
          this.content_height =
            this.$refs[this.hoverIndex][0]["offsetTop"] - this.$refs["hover_content"]["offsetTop"];
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
          this.searchWord(value);
          break;
        case "tag":
          this.searchTag(value);
          break;
      }
    },
    getNumber() {
      if (this.$route.params.key == "post") {
        this.getPortfolios();
      } else if (this.$route.params.key == "follow") {
        this.getFollowPortfolio();
      } else if (this.$route.params.key == "like") {
        this.getLikeOrder();
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
</style>
