<template>
  <div>
    <div v-if="backimages[count]" :key="count" class="absolute h-96 w-full top-0">
      <div
        class="w-full h-full bg-cover bg-center animate-slide-in-right"
        :style="`background-image: url(${backimages[count].title_image})`"
      >
        <div class="flex opacity-90">
          <div
            class="bg-gray-900 bg-opacity-60 rounded-lg flex items-center mx-10 my-4 mt-72 px-3 py-1 gap-2"
          >
            <router-link :to="{ name: 'UserShow', params: { id: backimages[count].user_id.id } }" class="flex items-center">
              <div class="flex h-[2.5rem] w-[2.5rem]">
                <img
                  class="object-cover aspect-square rounded-full"
                  :src="backimages[count].user_id.icon"
                  alt="Image Description"
                />
              </div>
              <div>
              <router-link :to="{ name: 'PostDetails', params: { id: backimages[count].id } }">
              <div
                class="font-semibold flex text-white text-lg pl-2 hover:underline"
              >[[backimages[count].title||""]]</div>
              </router-link>
              <div
                class="font-semibold flex text-white text-xs pl-2 hover:underline"
              >[[backimages[count].user_id.username||""]]</div>
              </div>
            </router-link>
          </div>
        </div>
      </div>
    </div>
    <div class="relative pt-10 bg-lime-600 h-2 z-20 shadow-md top-72"></div>
    <div class="relative mx-auto my-3 w-10/12 pt-72">
      <!--最新の投稿-->
      <div class="border-b-4 border-teal-800">
        <div class="pt-8 pb-2 flex space-x-2 px-5 justify-between items-center">
          <div
            type="button"
            class="font-semibold hs-tab-active:border-teal-500 hs-tab-active:text-teal-600 inline-flex items-center gap-2 border-transparent text-2xl whitespace-nowrap text-gray-600"
          >最近の投稿</div>
          <router-link
            :to="{name: 'PostList',params: { key: 'post' }}"
            class="text-gray-500 hover:text-teal-500 hover:font-semibold"
          >一覧表示</router-link>
        </div>
      </div>
      
      <div class="carousel">
        <div
          @click="carouselPrev"
          class="carousel_prev"
          :class="{ no_carousel_prev: (portfolios.length <= 4) || (carouselIndex === 0) }"
        >
          <font-awesome-icon class="text-gray-900" icon="circle-chevron-left" />
        </div>
        <div class="carousel_list_outer">
          <div :class="[hoverImg_resize == true ? 'hover_resize' : 'hover_content']">
            <!--ホバーしたとき画像拡大-->
            <img
              :src="hoverImage"
              :ref="img_style"
              :style="{ transform: `translate(${content_left}px, ${content_height}px)`, visibility: hoverFlag}"
            />
          </div>
          <div
            class="carousel_list"
            ref="margin_search"
            :style="{ transform: 'translate(-' + carouselIndex + '00%, 0)' }"
          >
             <!--ロードが完了するまで透明の作品を表示（ロード前と後では画面の上下が激しいため）５つ表示してます-->
            <div class="carousel_item2" v-if="loadingImg">
              <div class="group relative flex h-48 flex-col overflow-hidden rounded-lg bg-gradient-to-b from-slate-300 to-slate-800 shadow-lg md:h-64 xl:h-80 z-20 flex-1" >
              </div>
            </div>
            <div class="carousel_item2" v-if="loadingImg">
              <div class="group relative flex h-48 flex-col overflow-hidden rounded-lg bg-gradient-to-b from-slate-300 to-slate-800 shadow-lg md:h-64 xl:h-80 z-20 flex-1" >
              </div>
            </div>
            <div class="carousel_item2" v-if="loadingImg">
              <div class="group relative flex h-48 flex-col overflow-hidden rounded-lg bg-gradient-to-b from-slate-300 to-slate-800 shadow-lg md:h-64 xl:h-80 z-20 flex-1" >
              </div>
            </div>
            <div class="carousel_item2" v-if="loadingImg">
              <div class="group relative flex h-48 flex-col overflow-hidden rounded-lg bg-gradient-to-b from-slate-300 to-slate-800 shadow-lg md:h-64 xl:h-80 z-20 flex-1" >
              </div>
            </div>
            <div class="carousel_item2" v-if="loadingImg">
              <div class="group relative flex h-48 flex-col overflow-hidden rounded-lg bg-gradient-to-b from-slate-300 to-slate-800 shadow-lg md:h-64 xl:h-80 z-20 flex-1" >
              </div>
            </div>
          
            <div
              v-for="portfolio in portfolios"
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
                    loading="lazy"
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
                      <div class="my-1 mx-3">[[formatDate(portfolio.created_date||"2023-01-01T00:00:00.000000+09:00")]]</div>
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
                            v-bind="{...$attrs}"
                          >[[portfolio.ganre_id.name||""]]</router-link>

                          <div class="flex items-center bottom-0 p-2 pt-0">
                            <!--ユーザーアイコン-->
                            <router-link
                              :to="{ name: 'UserShow', params: { id: portfolio.user_id.id } }"
                            >
                              <div class="flex h-[2.5rem] w-[2.5rem]">
                                <img
                                  class="object-cover aspect-square rounded-full"
                                  :src="portfolio.user_id.icon"
                                  alt="Image Description"
                                />
                              </div>
                            </router-link>

                            <!--ユーザーネーム-->
                            <router-link
                              :to="{ name: 'UserShow', params: { id: portfolio.user_id.id } }"
                            >
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
        </div>
        <div
          @click="carouselNext"
          class="carousel_next"
          :class="{ no_carousel_next: (portfolios.length <= 5) || (carouselIndex === carouselIndexMax) }"
        >
          <font-awesome-icon class="text-gray-900" icon="circle-chevron-right" />
        </div>
      </div>

      <!--人気の投稿-->
      <div class="border-b-4 border-teal-800">
        <div class="pt-8 pb-2 flex space-x-2 px-5 justify-between items-center">
          <div
            type="button"
            class="font-semibold hs-tab-active:border-teal-500 hs-tab-active:text-teal-600 inline-flex items-center gap-2 border-transparent text-2xl whitespace-nowrap text-gray-600"
          >人気の投稿</div>
          <router-link
            :to="{name: 'PostList',params: { key: 'like' }}"
            class="text-gray-500 hover:text-teal-500 hover:font-semibold"
          >一覧表示</router-link>
        </div>
      </div>
      
      <TopLike
        :likeportfolios="likeOrderPortfolios"
        :portfolios="portfolios"
        :currentuser="currentuser"
        @genre-searched="handleGenreSearched"
      />

      <!--フォロー中-->
      <div v-if="this.$store.getters.isAuthenticated">
        <div class="border-b-4 border-teal-800">
          <div class="pt-8 pb-2 flex space-x-2 px-5 justify-between items-center">
            <div
              type="button"
              class="font-semibold hs-tab-active:border-teal-500 hs-tab-active:text-teal-600 inline-flex items-center gap-2 border-transparent text-2xl whitespace-nowrap text-gray-600"
            >フォロー中</div>
            <router-link
              :to="{name: 'PostList',params: { key: 'follow' }}"
              class="text-gray-500 hover:text-teal-500 hover:font-semibold"
            >一覧表示</router-link>
          </div>
        </div>
        <TopFollow :portfolios="followUserPortfolios" :currentuser="currentuser" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import settingMethods from "@/mixins/settingMethods";
import commonMethods from "@/mixins/commonMethods";
import searchMethods from "@/mixins/searchMethods";
import TopLike from "@/components/portfolio/exports/TopLike";
import TopFollow from "@/components/portfolio/exports/TopFollow";

export default {
  name: "TopList.vue",
  mixins: [settingMethods, commonMethods, searchMethods],
  data() {
    return {
      portfolios: [],
      likeOrderPortfolios: [],
      followUserPortfolios: [],
      user: [],
      currentuser: {
        id: ""
      },
      like_list: {
        like_count: []
      },
      categoryList: [],
      genreList: [],
      keyword: "",
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
      selectedPortfolios: null,
      loadingImg: true,
      backimages: [],
      count: 0,
      imgportfoloss: [],
      hoverImg_resize: false,
    };
  },
  components: {
    TopLike,
    TopFollow
  },
  computed: {
    carouselIndexMax() {
      this.InitialValue();
      if (this.portfolios.length % 5 == 0) {
        return parseInt(this.portfolios.length / 5 - 1);
      } else {
        return parseInt(this.portfolios.length / 5);
      }
    }
  },
  async created() {
    this.checkCookieExpiration();
    setInterval(this.checkCookieExpiration, 60000);
    // this.isCurrentUser;
    this.getPortfolios();
    this.searchLikeOrder2();
    try {
      await this.getCurrentUser(); // Promiseを待つ
      this.getFollowPortfolio(); // Promiseが完了した後に実行
    } catch (error) {
      console.error("Error:", error);
    }
  },
  mounted() {
    this.getCategory();
    this.getGenre();
    window.addEventListener("DOMContentLoaded", () => {
      this.domFlag = true;
    });
    this.startImageRotation();
  },
  methods: {
    getPortfolios() {
      axios
        .get("/api/v1/portfolio/new_portfolio/")
        .then(response => {
          this.portfolios = response.data;
          this.loadingImg = false;
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
          this.getLikeOrder();
          
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    getFollowPortfolio() {
      axios
        .get(`/api/v1/portfolio/followUserPost/`, {
          params: {
            id: this.currentuser.id
          }
        })
        .then(response => {
          this.followUserPortfolios = response.data;
          console.log("status:", response.status);
          console.log("follow:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    getLikeOrder() {
      axios
        .get(`/api/v1/portfolio/like_count_sort/`)
        .then(response => {
          this.likeOrderPortfolios = response.data;
          console.log("status:", response.status);
          console.log("like:", response.data);
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
      this.hoverImg_resize = false;
      this.timer = setTimeout(() => {
        if (this.$refs[this.hoverIndex][0] != null) {
          console.log('hover = ', this.$refs[this.img_style].width)
          if(this.$refs[this.img_style].width > 600){
            this.hoverImg_resize = true;
            this.hoverFlag = "visible";
          }
          else{
            this.hoverImg_resize = false;
            this.hoverFlag = "visible";
          }
          /**親divのmarginを取り出し、余分な高さ(margin)を消す */
          this.content_margin =
            parseInt(
              window
                .getComputedStyle(this.$refs["margin_search"])
                .getPropertyValue("margin-top")
            ) + 25;
          this.content_height =
            this.$refs[this.hoverIndex][0]["offsetTop"] - this.content_margin;
          /**ホバーした時作品が520以上右に寄っている場合はホバー画像を左に出す。520以下なら画像を右に出す。 */
          if (
            this.$refs[this.hoverIndex][0]["offsetLeft"] -
              this.carouselIndex *
                5 *
                this.$refs[this.hoverIndex][0]["offsetWidth"] >=
            520
          ) {
            if(this.hoverImg_resize == false){
              this.content_left =
              this.$refs[this.hoverIndex][0]["offsetLeft"] -
              this.carouselIndex *
                5 *
                this.$refs[this.hoverIndex][0]["offsetWidth"] -
              this.$refs[this.img_style].width;
            }else{
               this.content_left =
              this.$refs[this.hoverIndex][0]["offsetLeft"] -
              this.carouselIndex *
                5 *
                this.$refs[this.hoverIndex][0]["offsetWidth"] -
              600
            }
            /*
            this.content_left =
              this.$refs[this.hoverIndex][0]["offsetLeft"] -
              this.carouselIndex *
                5 *
                this.$refs[this.hoverIndex][0]["offsetWidth"] -
              this.$refs[this.img_style].width;
            */
          } else {
            this.content_left =
              this.$refs[this.hoverIndex][0]["offsetLeft"] -
              this.carouselIndex *
                5 *
                this.$refs[this.hoverIndex][0]["offsetWidth"] +
              this.$refs[this.hoverIndex][0]["offsetWidth"];
          }
        }
      }, 500);
    },
    mouseLeaveAction() {
      this.hoverImg_resize = false;
      this.hoverFlag = "hidden";
      //志多
      window.clearTimeout(this.timer);
    },
    startImageRotation() {
      setInterval(() => {
        if (this.count >= this.backimages.length - 1) {
          this.count = 0;
        } else {
          this.count += 1;
        }
      }, 10000);
    },
    searchLikeOrder2() {
      axios
        .get(`/api/v1/portfolio/top_image/`)
        .then(response => {
          this.imgportfolios = response.data;

          // Promise.allを使用して非同期の画像読み込みを待つ
          const imageLoadingPromises = this.imgportfolios.map(portfolio => {
            return new Promise(resolve => {
              this.finish(portfolio, resolve);
            });
          });

          // すべての画像が読み込まれたらstartImageRotationを呼び出す
          Promise.all(imageLoadingPromises).then(() => {
          });
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },

    finish(obj, callback) {
      var img = new Image();
      img.onload = () => {
        // 画像の横幅が1400以上なら画像を追加
        if (img.width >= 1440 && img.height >= 860) {
          this.backimages.push(obj);
          console.log(obj);
        }

        // コールバックを呼び出してPromise.allを進める
        callback();
      };
      img.src = obj.title_image;
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
.hover_resize {
  position: absolute;
  pointer-events: none;
  z-index: 40;
  display: relative;
}
.hover_resize img {
  width: 600px;
  height: auto;
  margin: 0 10 0;
}

.VueCarousel-slide .slider-inner {
  height: 100%;
  background-color: #62caaa;
  display: flex;
  justify-content: center;
  align-items: center;
  color: #fff;
  border: 2px solid #fff;
  font-size: 30px;
  border-radius: 10px;
}

.carousel {
  display: flex;
  align-items: center;
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
}

.carousel_list {
  display: flex;
  align-items: center;
  transition: 0.3s;
  flex-shrink: 0;
}
.carousel_list2 {
  position: absolute;
}
.carousel_item {
  padding: 10px;
  flex: 0 0 20%;
  align-items: center;
  justify-content: center;
}
.carousel_item2 {
  
  padding: 10px;
  width: 20%;
  align-items: center;
  justify-content: center;
}
</style>