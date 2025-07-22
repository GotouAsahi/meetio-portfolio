<template>
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
        <div
          v-for="(portfolio) in portfolios"
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
                    class="absolute h-4/5 w-4/5 p-2 flex items-end text-xl font-semibold text-white transition duration-100"
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
</template>

<script>
import settingMethods from "@/mixins/settingMethods";
import commonMethods from "@/mixins/commonMethods";
import searchMethods from "@/mixins/searchMethods";

export default {
  name: "TopFollow.vue",
  mixins: [settingMethods, commonMethods, searchMethods],
  props: ["portfolios", "currentuser"],
  data() {
    return {
      user: [],
      like_list: {
        like_count: []
      },
      categoryList: [
        { id: 0, name: "technology", label: "Technology" },
        { id: 1, name: "business", label: "Business" },
        { id: 2, name: "creative", label: "Creative" },
        { id: 3, name: "sound", label: "Sound" },
        { id: 4, name: "video", label: "Video" },
        { id: 5, name: "design", label: "Design" }
      ],
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
      hoverImg_resize: false,
    };
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
  mounted() {
    this.getGenre();
    window.addEventListener("DOMContentLoaded", () => {
      this.domFlag = true;
    });
  },
  methods: {
    mouseOverAction(portfolio) {
      this.hoverIndex = portfolio.id;
      this.hoverFlag = "visible";
      this.hoverImage = portfolio.title_image;
      this.hoverFlag = "hidden";
      clearTimeout(this.timer);
      this.hoverImg_resize =  false,
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
            ) + 30;
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
            if (this.hoverImg_resize == false) {
              this.content_left =
                this.$refs[this.hoverIndex][0]["offsetLeft"] -
                this.carouselIndex *
                5 *
                this.$refs[this.hoverIndex][0]["offsetWidth"] -
                this.$refs[this.img_style].width;
            } else {
              this.content_left =
                this.$refs[this.hoverIndex][0]["offsetLeft"] -
                this.carouselIndex *
                5 *
                this.$refs[this.hoverIndex][0]["offsetWidth"] -
                600
            }
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
  }
};
</script>
<style>
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
</style>