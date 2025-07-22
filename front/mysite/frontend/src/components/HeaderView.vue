<template>
  <!--ヘッダー部-->
  <header class="bg-lime-600 bg-opacity-90 rounded-full flex items-center justify-between px-10 py-4">
    <div class="w-2/5 flex justify-start grid-cols-3 gap-10">
      <!--ロゴ-->
      <a href="/" class="text-white inline-flex items-center gap-2.5 text-2xl font-bold md:text-3xl" aria-label="logo">
        <img src="../assets/img/meetio_white.png" />
      </a>

      <!--サーチエリア-->
      <form class="flex items-center w-full" @submit.prevent="searchMethod(keyword)">
        <div class="relative w-full">
          <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
            <!--<font-awesome-icon class="px-1" icon="magnifying-glass" />-->
          </div>
          <input type="text" v-model="keyword" ref="searchInput"
            class="bg-gray-50 text-gray-900 text-sm rounded-l-full block w-full p-2.5 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 focus:ring-opacity-50 focus:outline-none"
            placeholder="記事検索" />
        </div>
        <button type="submit"
          class="bg-gray-200 w-10 h-10 p-2.5 flex justify-center items-center text-lg font-medium rounded-r-full text-gray-600 border-2 focus:ring-2 focus:ring-teal-500 focus:border-teal-500 focus:ring-opacity-50 focus:outline-none hover:bg-teal-500 hover:text-white">
          <font-awesome-icon class="px-1 mr-1" icon="magnifying-glass" />
        </button>
      </form>
    </div>

    <div v-if="this.$store.getters.isAuthenticated">
      <div class="h-10 flex grid-cols-5 gap-6">
        <!--カテゴリー・ジャンルボタン-->
        <nav role="navigation">
          <ul>
            <li class="menu-item-ca">
              <p
                class="inline-block pl-2.5 pr-4 pt-2 pb-3 text-gray-100 items-center text-sm font-semibold cursor-pointer md:text-base">
                <font-awesome-icon class="px-1" icon="shapes" />カテゴリー
              </p>
              <ul class="sub-menu-ca bg-lime-600 p-1">
                <li v-for="category in categoryList" :key="category.id">
                  <router-link :to="{ name: 'PostList', params: { key: 'category' }, query: { q: category.label } }"
                    class="p-2 border-[3px] border-lime-600 border-opacity-0 hover:border-opacity-100 hover:opacity-100 hover:border-b-white w-full h-full text-white text-base hover:font-semibold"
                    v-bind="{ ...$attrs }">[[category.label||""]]</router-link>
                </li>
              </ul>
            </li>
          </ul>
        </nav>

        <!--ユーザー検索ボタン-->
        <router-link :to="{ name: 'SchoolUser' }"
          class="inline-block pl-2.5 pr-4 pt-2 pb-3 border-b-[3px] border-lime-600 border-opacity-0 hover:border-opacity-100 hover:border-white text-gray-100 items-center text-sm font-semibold hover:text-white md:text-base">
          <font-awesome-icon class="px-1" icon="users" />ユーザー検索
        </router-link>
        <!--投稿ボタン-->
        <router-link :to="{ name: 'PostView' }"
          class="inline-block pl-2.5 pr-4 pt-2 pb-3 border-b-[3px] border-lime-600 border-opacity-0 hover:border-opacity-100 hover:border-white text-gray-100 items-center text-sm font-semibold hover:text-white md:text-base">
          <font-awesome-icon class="px-1" icon="pen" />記事投稿
        </router-link>

        <!--スキルチェックボタン-->
        <router-link :to="{ name: 'JudgeTop' }"
          class="inline-block pl-2.5 pr-4 pt-2 pb-3 border-b-[3px] border-lime-600 border-opacity-0 hover:border-opacity-100 hover:border-white text-gray-100 items-center text-sm font-semibold hover:text-white md:text-base">
          <font-awesome-icon class="px-1" icon="check" />スキルチェック
        </router-link>

        <!--アイコンボタン・ドロップダウンメニュー-->
        <nav role="navigation">
          <ul>
            <li class="menu-item">
              <a>
                <img v-if="this.currentuser.icon" class="object-cover h-[2.5rem] w-[2.5rem] aspect-square rounded-full"
                  :src="currentuserIcon" alt="Image Description" />
                <div v-else class="inline-block h-[2.5rem] w-[2.5rem]"></div>
              </a>
              <ul class="sub-menu bg-lime-600 p-1">
                <li>
                  <button
                    class="p-2 border-[3px] border-lime-600 opacity-100 hover:border-b-white w-full h-full text-white text-base hover:font-semibold"
                    @click="profile">マイプロフィール</button>
                </li>
                <li>
                  <button
                    class="p-2 border-[3px] border-lime-600 opacity-90 hover:opacity-100 hover:border-b-white w-full h-full text-white text-base hover:font-semibold"
                    @click="draft">下書き一覧</button>
                </li>
                <li>
                  <button
                    class="p-2 border-[3px] border-lime-600 opacity-90 hover:opacity-100 hover:border-b-white w-full h-full text-white text-base hover:font-semibold"
                    @click="help">ヘルプページ</button>
                </li>
                <hr class="my-1">
                <li>
                  <button
                    class="p-2 border-[3px] border-lime-600 opacity-90 hover:opacity-100 hover:border-b-white w-full h-full text-white text-base hover:font-semibold"
                    @click="logout">サインアウト</button>
                </li>
              </ul>
            </li>
          </ul>
        </nav>
      </div>
    </div>
    <div v-else class="h-10 flex grid-cols-5 gap-6">
      <!--カテゴリー・ジャンルボタン-->
      <nav role="navigation">
        <ul>
          <li class="menu-item-ca">
            <p
              class="inline-block pl-2.5 pr-4 pt-2 pb-3 text-gray-100 items-center text-sm font-semibold cursor-pointer md:text-base">
              <font-awesome-icon class="px-1" icon="shapes" />カテゴリー
            </p>
            <ul class="sub-menu-ca bg-lime-600">
              <li v-for="category in categoryList" :key="category.id">
                <router-link :to="{ name: 'PostList', params: { key: 'category' }, query: { q: category.label } }"
                  class="p-2 hover:bg-teal-500 w-full h-full text-white"
                  v-bind="{ ...$attrs }">[[category.label||""]]</router-link>
              </li>
            </ul>
          </li>
        </ul>
      </nav>

      <!--学校検索ボタン-->
      <router-link :to="{ name: 'SchoolUser' }"
        class="inline-block pl-2.5 pr-4 pt-2 pb-3 border-b-[3px] border-lime-600 border-opacity-0 hover:border-opacity-100 hover:border-white text-gray-100 items-center text-sm font-semibold hover:text-white md:text-base">
        <font-awesome-icon class="px-1" icon="users" />ユーザー検索
      </router-link>

      <!--スキルチェックボタン-->
      <router-link :to="{ name: 'JudgeTop' }"
        class="inline-block pl-2.5 pr-4 pt-2 pb-3 border-b-[3px] border-lime-600 border-opacity-0 hover:border-opacity-100 hover:border-white text-gray-100 items-center text-sm font-semibold hover:text-white md:text-base">
        <font-awesome-icon class="px-1" icon="check" />スキルチェック
      </router-link>
      <router-link to="/signup"
        class="inline-block rounded-full pl-2.5 pr-4 pt-2 pb-3 text-gray-100 items-center text-sm font-semibold hover:text-gray-300 md:text-base">新規登録</router-link>
      <router-link to="/login"
        class="inline-block rounded-full pl-2.5 pr-4 pt-2 pb-3 text-gray-100 items-center text-sm font-semibold hover:text-gray-300 md:text-base">ログイン</router-link>
    </div>
  </header>
</template>

<script>
import axios from "axios";
import commonMethods from "@/mixins/commonMethods";
import searchMethods from "@/mixins/searchMethods";

export default {
  data() {
    return {
      keyword: "",
      searchResults: [],
      currentuser: {
        id: "",
        icon: ""
      },
      categoryList: []
    };
  },
  mixins: [commonMethods, searchMethods],
  async created() {
    await this.checkCookieExpiration();
    if(this.$store.getters.isAuthenticated) {
      this.getUserProfile();
      }
  },
  computed: {
    currentuserIcon() {
      return this.$store.state.icon;
    }
  },
  mounted() {
    this.getCategory();
  },
  methods: {
    profile() {
      this.$router.push(`/user/${this.currentuser.id}`);
    },
    draft() {
      this.$router.push({ name: "DraftList", params: { id: this.currentuser.id  } });
    },
    help() {
      this.$router.push({ name: `HelpPage` });
    },
    logout() {
      this.$cookies.remove("token");
      this.$store.dispatch("logout");
      this.$router.push({ name: "LoginForm" });
    },
    getUserProfile() {
      axios
        .get("/api/v1/auth/users/me/", {
          withCredentials: true,
          headers: {
            Authorization: "JWT " + this.$cookies.get("token")
          }
        })
        .then(response => {
          this.currentuser.id = response.data.id;
          return axios
            .get(`/api/v1/index/${this.currentuser.id}/`)
            .then(response => {
              this.currentuser.icon = response.data.icon;
              this.$store.commit("setIcon", this.currentuser.icon);
            });
        })
        .catch(error => {
          console.log("axiosGetErr", error);
        });
    },
    searchMethod(key) {
      this.$router.push({ name: 'PostList', params: { key: 'search' }, query: { q: key } })
    }
  }
};
</script>

<style>
nav>ul>li {
  position: relative;
}

nav a {
  color: #0bd;
  text-decoration: none;
}

nav ul a:hover {
  color: #0090aa;
}

nav .sub-menu {
  position: absolute;
  width: 180px;
  top: 50px;
  right: -40px;
  opacity: 0;
  visibility: hidden;
  transition: 0.5s;
}

nav .sub-menu a {
  color: #fff;
  padding: 5px;
  display: block;
}

nav .sub-menu a:hover {
  color: #fff;
}

nav .menu-item:hover ul {
  opacity: 1;
  visibility: visible;
}

nav .sub-menu-ca {
  position: absolute;
  justify-content: center;
  width: 180px;

  left: -28px;
  top: 50px;
  opacity: 0;
  visibility: hidden;
  transition: 0.8s;
}

nav .sub-menu-ca a {
  color: #fff;
  padding: 5px;
  display: block;
}

nav .sub-menu-ca a:hover {
  color: #fff;
}

nav .menu-item-ca:hover ul {
  opacity: 1;
  visibility: visible;
}
</style>