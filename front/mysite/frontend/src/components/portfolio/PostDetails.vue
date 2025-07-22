<template>
  <div class="article-show mx-auto my-3 w-10/12">
    <div class="flex">
      <div class="w-full p-4">
        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="mt-6">
            <!--カテゴリー・ジャンル-->
            <div class="w-5/6 mx-auto flex items-center justify-between text-gray-600 gap-20">
              <div v-if="portfolio.category_id && portfolio.ganre_id">
                <router-link
                  :to="{ name: 'PostList', params: { key: 'category' }, query: { q: portfolio.category_id.name } }"
                  class="px-4 sm:text-lg md:mb-6 hover:underline"
                  v-bind="{ ...$attrs }">[[portfolio.category_id.name||""]]</router-link>
                <a>
                  <font-awesome-icon class="px-1" icon="angle-right" />
                </a>
                <router-link :to="{ name: 'PostList', params: { key: 'genre' }, query: { q: portfolio.ganre_id.name } }"
                  class="px-4 sm:text-lg md:mb-6 hover:underline"
                  v-bind="{ ...$attrs }">[[portfolio.ganre_id.name||""]]</router-link>
              </div>
              <div v-if="portfolio.user_id">
                <div v-if="portfolio.user_id.id === currentuser.id">
                  <router-link :to="{ name: 'PostEdit', params: { id: portfolio.id } }"
                  class="w-1/4 text-center px-10 py-2.5 mr-2 mb-2 text-lg font-medium bg-gray-200 text-gray-700 rounded-xl cursor-pointer sm:w-min hover:bg-teal-500 hover:text-gray-50">編集する</router-link>
                </div>
              </div>
            </div>
            <div class="w-5/6 mx-auto px-4">
              <!--投稿日-->
              <div class="mt-6 mb-3 pl-1 text-xl text-gray-700 flex justify-start">
                [[formatDate(portfolio.created_date||"2023-01-01T00:00:00.000000+09:00")]]
              </div>
              <!--投稿タイトル-->
              <h1 class="mb-3 text-left text-3xl font-bold text-gray-800 sm:text-4xl md:mb-6">[[portfolio.title||""]]</h1>
              <div v-if="portfolio.user_id" class="flex">
                <div class="flex items-center gap-4 mb-4">
                  <router-link :to="{ name: 'UserShow', params: { id: portfolio.user_id.id } }">
                    <!--ユーザーアイコン-->
                    <div class="flex h-[3rem] w-[3rem]">
                      <img class="object-cover aspect-square rounded-full" :src="portfolio.user_id.icon"
                        alt="Image Description" />
                    </div>
                  </router-link>
                  <!--ユーザーネーム-->
                  <router-link :to="{ name: 'UserShow', params: { id: portfolio.user_id.id } }">
                    <p class="font-semibold text-2xl text-gray-700 flex hover:underline">
                      [[portfolio.user_id.username||""]]
                    </p>
                  </router-link>
                </div>
              </div>
              <!--タグ-->
              <div class="mb-1 md:mb-1">
                <div class="flex">
                  <div v-for="tag in portfolio.tag" :key="tag.id">
                    <div class="border-2 border-gray-600 hover:bg-teal-500 hover:border-teal-500 rounded-xl mr-3">
                      <router-link :to="{ name: 'PostList', params: { key: 'tag' }, query: { q: tag } }"
                        class="px-4 flex items-center font-semibold text-gray-700 hover:text-white"
                        v-bind="{ ...$attrs }">
                        <font-awesome-icon class="px-1" icon="tag" />[[tag||""]]
                      </router-link>
                    </div>
                  </div>
                </div>
              </div>
              <!--評価・閲覧数-->
              <div class="pr-2 pb-2 flex items-center justify-end grid-cols-2 gap-4">
                <div class="flex items-center">
                  <button type="button" :class="{
                    'text-gray-600 font-semibold rounded-lg text-base px-2 text-center': !isLike,
                    'text-red-500 font-semibold rounded-lg text-base px-2 text-center': isLike
                  }" @click="likePortfolio">
                    <font-awesome-icon class="flex px-1 text-xl items-center" icon="heart" />
                  </button>
                  <p class="flex items-center text-xl text-gray-700">[[likeCount||""]]</p>
                </div>
                <div class="flex items-center">
                  <a>
                    <font-awesome-icon class="flex items-center px-2 text-xl text-gray-700" icon="eye" />
                  </a>
                  <a class="flex items-center text-xl text-gray-700">[[portfolio.view_count+1||""]]</a>
                </div>
              </div>
            </div>
            <!--サムネイル画像の表示-->
            <div>
              <img :src="portfolio.title_image" class="p-4 w-5/6 mx-auto" />
            </div>
            <!-- ビデオの表示 -->
            <div v-if="portfolio.movie" class="p-4 w-5/6 mx-auto">
              <video controls>
                <source :src="portfolio.movie" type="video/mp4" />Your browser does not support the video tag.
              </video>
            </div>
            <!-- 本文 -->
            <mavon-editor class="z-1 w-5/6 mx-auto" v-model="portfolio.sentence" language="ja" :boxShadow="false"
              :subfield="false" defaultOpen="preview" :toolbars="false" :toolbarsFlag="false" />
          </div>
        </div>
      </div>
    </div>

    <!--ユーザープロフィール-->
    <div class="p-4">
      <div class="bg-white rounded-lg shadow-lg p-6">
        <div v-if="portfolio.user_id" class="p-2 w-5/6 mx-auto">
          <div class="flex justify-start gap-16">
            <div class="w-2/5">
              <div class="flex items-center gap-2 mb-2">
                <router-link :to="{ name: 'UserShow', params: { id: portfolio.user_id.id } }">
                  <!--ユーザーアイコン-->
                  <div class="flex h-[5rem] w-[5rem]">
                    <img class="object-cover aspect-square rounded-full" :src="portfolio.user_id.icon"
                      alt="Image Description" />
                  </div>
                </router-link>
                <!--ユーザーネーム-->
                <div class="ml-2">
                  <router-link :to="{ name: 'UserShow', params: { id: portfolio.user_id.id } }">
                    <p class="flex font-semibold text-3xl text-gray-700 hover:underline">
                      [[portfolio.user_id.username||""]]</p>
                  </router-link>

                  <!--メールアドレス-->
                  <p class="text-gray-700 text-lg flex justify-start">[[portfolio.user_id.email||""]]</p>
                </div>
              </div>

              <div class="px-4">
                <div v-if="portfolio.user_id.school">
                  <div class="flex items-center pt-2">
                    <!--学校名-->
                    <div class="mr-2">
                      <font-awesome-icon icon="school" />
                    </div>
                    <div v-if="portfolio.user_id.school.name">
                      <p class="text-gray-700 hover:underline cursor-pointer text-lg"
                        @click="() => searchSchoolUser(portfolio.user_id.school.name, null, null,null,null)">
                        [[portfolio.user_id.school.name||""]]</p>
                    </div>
                    <div v-else>
                      <p class="text-gray-700 text-lg">未登録</p>
                    </div>
                    <!--学年-->
                    <div v-if="portfolio.user_id.school.grade">
                      <p class="text-gray-700 flex text-lg pl-2">[[portfolio.user_id.school.grade||""]]年生</p>
                    </div>
                  </div>
                  <div class="flex items-center pt-1">
                    <!--学部-->
                    <div v-if="portfolio.user_id.school.faculty">
                      <p class="text-gray-700 flex text-lg">[[portfolio.user_id.school.faculty||""]]</p>
                    </div>
                    <!--学科-->
                    <div v-if="portfolio.user_id.school.department">
                      <p class="text-gray-700 flex text-lg pl-2">[[portfolio.user_id.school.department||""]]</p>
                    </div>
                  </div>
                </div>
                <!--自己紹介-->
                <p class="text-left text-gray-600 flex justify-start pt-2">[[portfolio.user_id.introduction||""]]</p>
              </div>
            </div>
            <!--他の投稿-->
            <div class="grid grid-cols-3 gap-4 items-center">
              <div v-for="portfolio in userPortfolios" :key="portfolio.id">
                <router-link :to="{ name: 'PostDetails', params: { id: portfolio.id } }"
                  class="group relative flex h-48 w-48 flex-col overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-32 xl:h-64 z-10">
                  <div
                    class="group relative flex h-48 flex-col overflow-hidden rounded-lg bg-gray-100 shadow-lg md:h-64 xl:h-96 z-10">
                    <!--サムネイル画像-->
                    <img :src="portfolio.title_image" loading="lazy" alt="Photo by Minh Pham"
                      class="absolute inset-0 h-full w-full py-0 object-cover object-center transition duration-200 group-hover:scale-110 z-2" />
                    <div
                      class="pointer-events-none absolute inset-0 bg-gradient-to-t from-black to-transparent md:via-transparent">
                    </div>
                    <div>
                      <!--投稿日-->
                      <span
                        class="absolute block right-0 rounded-bl-lg top-0 bg-gray-900 text-sm font-semibold text-gray-200">
                        <div class="my-1 mx-3">[[formatDate(portfolio.created_date||"2023-01-01T00:00:00.000000+09:00")]]
                        </div>
                      </span>
                    </div>
                    <div>
                      <div class="flex justify-between">
                        <!--タイトル-->
                        <h2
                          class="absolute h-4/5 w-4/5 p-2 flex items-end text-xl text-left font-semibold text-white transition duration-100">
                          [[portfolio.title||""]]</h2>
                        <!--評価ボタン-->
                      </div>
                      <ul>
                        <li class="absolute bottom-0 w-full h-1/5 bg-white">
                          <div class="absolute">
                            <!--ジャンル-->
                            <router-link
                              :to="{ name: 'PostList', params: { key: 'genre' }, query: { q: portfolio.ganre_id.name } }"
                              class="px-2 pt-1 text-xs font-semibold flex justify-start text-gray-700 transition duration-100 hover:underline"
                              v-bind="{ ...$attrs }">[[portfolio.ganre_id.name||""]]</router-link>
                          </div>
                        </li>
                      </ul>
                    </div>
                  </div>
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!--コメント欄-->
    <div class="p-4">
      <div class="bg-white rounded-lg shadow-lg px-6 py-10">
        <h1 class="mb-6 w-5/6 mx-auto text-center flex justify-start text-3xl font-bold text-teal-600">
          <font-awesome-icon class="px-2 text-3xl text-teal-600" icon="comments" />コメント
        </h1>
        <!--コメント記入フォーム-->
        <form class="form-horizontal" v-on:submit.prevent="addComment">
          <div class="flex justify-center items-center w-5/6 mx-auto">
            <div class="relative w-full mr-2 z-0 flex">
              <textarea v-model="commentForm.text"
                class="bg-gray-100 border-gray-100 border text-gray-800 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                rows="2" placeholder="コメントを入力してください" maxlength="200"></textarea>
            </div>
            <!--コメント送信ボタン-->
            <button type="submit"
              class="inline-flex justify-center items-center pl-3 py-2 pr-2 text-gray-500 hover:text-teal-600 hover:bg-gray-100 rounded-full cursor-pointer">
              <svg class="w-6 h-6 rotate-90" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
                viewBox="0 0 18 20">
                <path
                  d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z" />
              </svg>
            </button>
          </div>
        </form>
        <!--コメントの表示-->
        <div v-for="comment in commentList" :key="comment.id">
          <div class="mt-4 w-5/6 mx-auto">
            <div class="flex items-center justify-between pt-2">
              <div class="flex items-center">
                <!--コメント主の情報-->
                <a href="profile">
                  <div class="flex h-[3rem] w-[3rem]">
                    <img class="object-cover aspect-square rounded-full" :src="comment.user.icon"
                      alt="Image Description" />
                  </div>
                </a>
                <a href="profile" class="text-gray-700 text-[22px] pl-3 hover:underline">[[comment.user.username||""]]</a>
              </div>
            </div>
            <!--コメント-->
            <div class="flex justify-start items-start ml-6">
              <a class="text-[21px] text-left pt-3 pb-2 text-xl text-gray-800">[[comment.text||""]]</a>
            </div>
            <div class="flex justify-start items-center ml-6 mb-1">
              <!-- コメントした日時 -->
              <div class="text-gray-700 text-base">[[formatDate(comment.created_at||"2023-01-01T00:00:00.000000+09:00")]]
              </div>
              <!--返信記入フォームを開くボタン-->
              <button @click="toggleReplyForm(comment.id)"
                class="text-gray-500 hover:text-teal-600 text-[17px] font-semibold px-2 py-1 ml-3">
                <font-awesome-icon class="mr-1 text-xl" icon="reply" />返信
              </button>
            </div>
            <!--返信記入フォーム-->
            <form v-if="replyFormVisible[comment.id]" class="form-horizontal" v-on:submit.prevent="addReply(comment.id)">
              <div class="flex items-center">
                <div class="relative w-full ml-6 mr-2 py-2.5 z-0 flex">
                  <textarea v-model="replyForm.text"
                    class="bg-gray-100 border-gray-100 border text-gray-800 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                    rows="2" placeholder="コメントを入力してください" maxlength="200"></textarea>
                </div>
                <!--返信送信ボタン-->
                <button type="submit"
                  class="inline-flex justify-center items-center pl-3 py-2 pr-2 text-gray-500 hover:text-teal-600 hover:bg-gray-100 rounded-full cursor-pointer">
                  <svg class="w-6 h-6 rotate-90" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor"
                    viewBox="0 0 18 20">
                    <path
                      d="m17.914 18.594-8-18a1 1 0 0 0-1.828 0l-8 18a1 1 0 0 0 1.157 1.376L8 18.281V9a1 1 0 0 1 2 0v9.281l6.758 1.689a1 1 0 0 0 1.156-1.376Z" />
                  </svg>
                </button>
              </div>
            </form>
            <div v-for="reply in comment.reply" :key="reply.id" class="border-l-[3px] border-gray-200 ml-6 py-3 pb-2">
              <div class="flex items-center justify-between">
                <div class="flex items-center pl-4">
                  <!--返信主の情報-->
                  <a href="profile">
                    <div class="flex h-[2rem] w-[2rem]">
                      <img class="object-cover aspect-square rounded-full" :src="reply.user.icon"
                        alt="Image Description" />
                    </div>
                  </a>
                  <a href="profile" class="text-gray-700 text-[19px] pl-2 hover:underline">[[reply.user.username||""]]</a>
                </div>
              </div>
              <!-- 返信 -->
              <div class="flex justify-start items-start">
                <a class="flex text-[19px] text-left py-2 pl-4 text-gray-800">[[reply.text||""]]</a>
              </div>
              <div class="flex justify-start items-center">
                <!-- コメントした日時 -->
                <div class="text-gray-700 text-base pl-4">
                  [[formatDate(comment.created_at||"2023-01-01T00:00:00.000000+09:00")]]</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- ページ上部移動のボタン -->
    <button type="button" class="fixed z-50 bottom-16 right-10 h-[5rem] w-[5rem] text-2xl font-bold text-white
    bg-lime-600 hover:bg-teal-700 rounded-full shadow-lg cursor-pointer" @click="PageTop">TOP</button>
  </div>
</template>

<script>
import axios from "axios";
import settingMethods from "@/mixins/settingMethods";
import commonMethods from "@/mixins/commonMethods";
import searchMethods from "@/mixins/searchMethods";

export default {
  name: "PostDetails",
  mixins: [settingMethods, commonMethods, searchMethods],
  props: {
    msg: String
  },
  data() {
    return {
      portfolio: {},
      user: [],
      userPortfolios: {},
      commentList: [],
      currentuser: {
        id: null
      },
      commentForm: {
        user: "",
        text: "",
        target: ""
      },
      replyForm: {
        user: "",
        text: ""
      },
      replyFormVisible: {},
      like_list: {
        like_count: []
      },
      categoryword: "",
      searchResults: []
    };
  },
  created() {
    this.checkCookieExpiration();
    setInterval(this.checkCookieExpiration, 60000);
    this.commentList.forEach(comment => {
      this.$set(this.replyFormVisible, comment.id, false);
    });
  },
  watch: {
    $route() {
      this.reloadData();
    }
  },
  mounted() {
    this.getPortfolio();
    if (this.$store.getters.isAuthenticated) {
      this.getCurrentUser();
    }
  },
  computed: {
    likeCount() {
      return this.portfolio.like_count ? this.portfolio.like_count.length : 0;
    },
    isLike() {
      return (
        this.portfolio.like_count &&
        this.portfolio.like_count.includes(this.currentuser.id)
      );
    }
  },
  methods: {
    getPortfolio() {
      axios
        .get(`/api/v1/portfolio/index/${this.$route.params.id}`)
        .then(getResponse => {
          console.log("GET status:", getResponse.status);
          console.log("GET axiosGetData:", getResponse.data);
          // ポートフォリオデータを設定
          this.portfolio = getResponse.data;
          return axios.put(
            `/api/v1/portfolio/index/${this.$route.params.id}/`,
            this.portfolio
          );
        })
        .then(putResponse => {
          console.log("PUT status:", putResponse.status);
          console.log("PUT axiosGetData:", putResponse.data);

          // その他の処理を追加できます
          this.getComment();
          this.getUserPortfolio();
        })
        .catch(err => {
          console.log("axiosGetErr / axiosPutErr", err);
          axios
            .get(
              `/api/v1/portfolio/myindex/${this.$route.params.id}`,
              {
                withCredentials: true,
                headers: {
                  Authorization: "JWT " + this.$cookies.get("token")
                }
              }
            )
            .then(getResponse => {
              console.log("GET status:", getResponse.status);
              console.log("GET axiosGetData:", getResponse.data);
              // ポートフォリオデータを設定
              this.portfolio = getResponse.data;

              this.getComment();
              this.getUserPortfolio();
            })
            .catch(err => {
              console.log("axiosGetErr / axiosPutErr", err);
            });
        });
    },
    getUserPortfolio() {
      axios
        .get(`/api/v1/portfolio/userindex/`, {
          params: {
            id: this.portfolio.user_id.id
          }
        })
        .then(response => {
          const sortedData = response.data['results'].sort((a, b) => {
            // ソート基準となるフィールドを指定
            return new Date(b.update_date) - new Date(a.update_date);
          });

          // 最新の2つの記事を取得
          this.userPortfolios = sortedData.slice(0, 3);
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    getComment() {
      axios
        .get("/api/v1/portfolio/comment/", {
          params: {
            target: encodeURI(this.portfolio.id)
          }
        })
        .then(response => (this.commentList = response.data))
        .then(response => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    async addComment() {
      if (!this.$store.getters.isAuthenticated) {
        alert("ログインして下さい");
        this.$router.push({ name: "LoginForm" });
      }
      await this.getCurrentUser();
      this.commentForm.user = this.currentuser.id;
      this.commentForm.target = this.portfolio.id;
      axios
        .post("/api/v1/portfolio/comment/", this.commentForm)
        .then(response => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
          this.commentForm.text = "";
          this.getComment();
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    async addReply(commentId) {
      if (!this.$store.getters.isAuthenticated) {
        alert("ログインして下さい");
        this.$router.push({ name: "LoginForm" });
      }
      await this.getCurrentUser();
      this.replyForm.user = this.currentuser.id;
      axios
        .post("/api/v1/portfolio/reply/", this.replyForm, {
          params: {
            id: encodeURI(commentId)
          }
        })
        .then(response => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
          this.replyForm.text = "";
          this.getComment();
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    toggleReplyForm(commentId) {
      this.replyFormVisible[commentId] = !this.replyFormVisible[commentId];
    },
    async likePortfolio() {
      if (!this.$store.getters.isAuthenticated) {
        alert("ログインして下さい");
        this.$router.push({ name: "LoginForm" });
      }
      await this.getCurrentUser();
      this.like_list.like_count = [this.currentuser.id];
      if (this.isLike) {
        this.portfolio.like_count = this.portfolio.like_count.filter(
          userId => userId !== this.currentuser.id
        );
      } else {
        this.portfolio.like_count.push(this.currentuser.id);
      }
      axios
        .put(
          `/api/v1/portfolio/like/${this.$route.params.id}/`,
          this.like_list
        )
        .then(response => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    reloadData() {
      this.getPortfolio();
    },
    PageTop() {
      window.scroll({ top: 0, behavior: "smooth" });
    },
  }
};
</script>
<style >
.article-show .v-show-content {
  z-index: 2;
  background-color: transparent !important;
  padding: 0px 16px 24px !important;
  border-radius: 2% !important;
}

.article-show .markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4,
.markdown-body h5 {
  margin-top: 0px !important;
  margin: 15px 0px 5px !important;
  padding: 24px 0px 0px !important;
  border-bottom: none !important;
}

.article-show .markdown-body p {
  margin-bottom: 24px !important;
}

.article-show .v-note-wrapper {
  z-index: 2;
  border: none !important;
}

.article-show ul {
  list-style-type: initial !important;
}

.article-show ol {
  list-style-type: decimal !important;
}</style>