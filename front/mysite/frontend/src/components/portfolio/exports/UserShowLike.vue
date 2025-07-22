<template>
    <div class="flex flex-row w-full">
      <button
        @click="changeFavorite('follow')"
        :class="{
          'basis-1/2 py-3 hover:text-teal-600 bg-white border-x-0 border-gray-200 border-b-4 border-b-teal-600 text-teal-600':
            selectedFavorite === 'follow',
          'basis-1/2 py-3 text-gray-700 hover:text-teal-600 bg-white border-b-2 border-gray-200':
            selectedFavorite !== 'follow',
        }"
      >
        <font-awesome-icon icon="person" size="xl" />
        <font-awesome-icon
          class="mr-2"
          icon="person-dress"
          size="xl"
        />フォロー中のユーザー
      </button>
      <button
        class="border-l-2 border-gray-200"
        @click="changeFavorite('portfolio')"
        :class="{
          'basis-1/2 py-3 hover:text-teal-600 bg-white border-l-2 border-gray-200 border-b-4 border-b-teal-600 text-teal-600':
            selectedFavorite === 'portfolio',
          'basis-1/2 py-3 text-gray-700 hover:text-teal-600 bg-white border-b-2 border-gray-200':
            selectedFavorite !== 'portfolio',
        }"
      >
        <font-awesome-icon
          class="mr-2"
          icon="file-lines"
          size="xl"
        />お気に入りの作品
      </button>
    </div>
    <!-- フォロー子タブ -->
    <div class="w-full mb-5 mx-10" v-if="selectedFavorite === 'follow'">
      <!-- フォローユーザー一覧 -->
      <div
        class="flex justify-center text-xl mt-5"
        v-for="follows in this.relationship.follows"
        :key="follows"
      >
        <!--ユーザー一覧-->
        <div
          class="w-full bg-white h-full rounded-lg shadow border border-gray-200 px-6 py-4 z-2"
        >
          <!--ユーザーアイコン-->
          <div class="grid grid-flow-col-dense grid-cols-7 grid-rows-1">
            <div class="col-span-1">
              <img
                class="object-cover aspect-square rounded-full"
                :src="follows.usericon"
                alt="Image Description"
              />
            </div>
            <div class="col-span-4 w-full flex items-center">
              <div class="flex flex-col pl-4">
                <!--ユーザーネーム-->
                  <router-link
                    :to="{ name: 'UserShow', params: { id: follows.id } }"
                  >
                    <p
                      class="text-2xl text-left font-semibold text-gray-900 hover:underline"
                    >
                      [[follows.username||""]]
                    </p>
                  </router-link>
              </div>
            </div>

            <!-- 気になるボタン -->
            <div class="col-span-2 flex justify-end items-start w-full items-center">
              <div class="block text-right cursor-pointer">
                <div v-if="follows.id !== currentuser.id">
                  <button
                    type="button"
                    :class="{
                      'text-gray-500 border border-gray-300 hover:bg-neutral-50 hover:text-teal-500 font-semibold rounded-lg text-base px-3 py-1.5 mb-1 text-center':
                        !isFollowing(follows),
                      'text-teal-500 border border-teal-500 hover:bg-neutral-50 hover:text-teal-500 font-semibold rounded-lg text-base px-3 py-1.5 mb-1 text-center':
                        isFollowing(follows),
                    }"
                    @click="followUser(follows)"
                  >
                    <font-awesome-icon
                      class="mr-1 mb-px"
                      icon="star"
                      size="lg"
                    />気になる
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- 作品子タブ -->
    <div
      v-if="selectedFavorite === 'portfolio'"
      class="w-full mb-5 mx-10 flex flex-col justify-center"
    >
      <div
        v-for="portfolio in likeUserPortfolios['results']"
        :key="portfolio.id"
      >
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

                <!-- フォローユーザー -->
                <div class="flex flex-row text-gray-700 ml-2">
                  <div class="w-1/2">
                    <div class="flex flex-row items-center text-gray-700">
                      <router-link
                        :to="{
                          name: 'UserShow',
                          params: { id: portfolio.user_id.id },
                        }"
                      >
                        <!--ユーザーアイコン-->
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
                        :to="{
                          name: 'UserShow',
                          params: { id: portfolio.user_id.id },
                        }"
                      >
                        <p class="font-semibold text-lg pl-2 hover:underline">
                          [[portfolio.user_id.username||""]]
                        </p>
                      </router-link>
                    </div>
                  </div>
                  <!--評価・閲覧数-->
                  <!--いいね-->
                  <div class="w-1/2 flex flex-row justify-end mr-4">
                    <div class="items-center flex flex-row mr-3">
                      <!--評価ボタン-->
                      <button
                        type="button"
                        :class="{
                          'text-gray-500 hover:text-red-500':
                            !isLike(portfolio),
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
          </div>
        </router-link>
      </div>
      <!--ページネーション-->
      <div class="w-full mt-5 mx-10">
        <nav aria-label="Page navigation example">
          <ul class="inline-flex -space-x-px text-base h-10">
            <li>
              <!--戻るボタンで戻れるときのレイアウト-->
              <a
                href="#"
                v-if="likeUserPortfolios['has_previous'] === true"
                @click.prevent.stop="
                  getLikePortfolioNumber(this.likePortfolioCurrentPage - 1)
                "
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
                v-if="likeUserPortfolios['has_previous'] === false"
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
            <li
              v-for="(n, key) in likeUserPortfolios['total_pages']"
              :key="key"
            >
              <a
                href="#"
                v-if="likePortfolioCurrentPage === n"
                aria-current="page"
                @click.prevent.stop="getLikePortfolioNumber(n)"
                class="flex items-center justify-center px-4 h-10 border border-gray-300 bg-green-50 text-teal-600 text-lg font-semibold"
              >
                [[ n ||""]]
              </a>
              <a
                href="#"
                v-else
                @click.prevent.stop="getLikePortfolioNumber(n)"
                class="flex items-center justify-center px-4 h-10 text-teal-500 border border-gray-300 bg-white hover:bg-gray-50 hover:text-teal-600 hover:font-semibold leading-tight"
              >
                [[ n ||""]]
              </a>
            </li>
            <li>
              <!--進むボタンで進めるときのレイアウト-->
              <a
                href="#"
                v-if="likeUserPortfolios['has_next'] === true"
                @click.prevent.stop="
                  getLikePortfolioNumber(this.likePortfolioCurrentPage + 1)
                "
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
                v-if="likeUserPortfolios['has_next'] === false"
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
    </div>
</template>

<script>
import axios from "axios";
import settingMethods from "@/mixins/settingMethods";
import commonMethods from "@/mixins/commonMethods";
import searchMethods from "@/mixins/searchMethods";

export default {
  name: "UserShowLike",
  mixins: [settingMethods, commonMethods, searchMethods],
  props: ["user", "currentuser"],
  data() {
    return {
      selectedFavorite: "follow",
      relationship: {
        follows: [],
      },
      follows: {
        follows: [],
      },
      likeUserPortfolios: [],
      likePortfolioCurrentPage: 1,
      likeUserCurrentPage: 1,
      myRelationship: [],
    };
  },
  mounted() {
    this.getfollow();
    this.getLikePortfolio();
  },
  created() {
    this.getMyfollow();
    console.log("user = ", this.user.id);
  },
  methods: {
    changeFavorite(favoritetab) {
      this.selectedFavorite = favoritetab;
    },
    getLikePortfolio() {
      axios
        .get(`/api/v1/portfolio/like_userShow_pagination`, {
          params: {
            id: this.$route.params.id,
            page: this.likePortfolioCurrentPage,
          },
        })
        .then((response) => (this.likeUserPortfolios = response.data))
        .then((response) => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch((err) => {
          console.log("axiosGetErr", err);
        });
    },
    getfollow() {
      axios
        .get(`/api/v1/FollowList/${this.$route.params.id}/`)
        .then((response) => (this.relationship = response.data))
        .then((response) => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch((err) => {
          console.log("axiosGetErr", err);
        });
    },
    getMyfollow() {
      console.log("jjjjjjjjjjjj", this.currentuser.id);
      axios
        .get(`/api/v1/FollowList/${this.currentuser.id}/`)
        .then((response) => {
          this.myRelationship = response.data;
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch((err) => {
          console.log("axiosGetErr", err);
        });
    },
    followUser(user) {
      if (!this.$store.getters.isAuthenticated) {
        alert("ログインして下さい");
        this.$router.push({ name: "LoginForm" });
      }
      this.follows.follows = [user.id];
      console.log("aaaaa", user);
      axios
        .put(`/api/v1/Follow/${this.currentuser.id}/`, this.follows)
        .then((response) => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
          this.getfollow();
          this.getMyfollow();
        })
        .catch((err) => {
          console.log("axiosGetErr", err);
        });
    },
    isFollowing(user) {
      if (this.myRelationship.follows) {
        for (let i = 0; i < this.myRelationship.follows.length; i++) {
          if (this.myRelationship.follows[i].id === user.id) {
            return true;
          }
        }
        return false;
      }
    },
    getLikePortfolioNumber(number) {
      this.likePortfolioCurrentPage = Number(number);
      this.getLikePortfolio();
      window.scroll({ top: 0, behavior: "auto" });
    },
    getLikeUserNumber(number) {
      this.likePortfolioCurrentPage = Number(number);
      this.getLikePortfolio();
      window.scroll({ top: 0, behavior: "auto" });
    },
  },
};
</script>
