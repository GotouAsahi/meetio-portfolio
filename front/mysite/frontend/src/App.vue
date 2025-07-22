<template>
  <div class="bg-gray-100 flex flex-col h-full z-50 body">
    <!--ヘッダー部-->
    <div
      :class="{ 'px-10 top-3 z-50 sticky': $route.path === '/', 'px-10 top-3 z-50 mt-3': $route.path !== '/' }"
    >
      <div id="app-a">
        <!--HeaderViewコンポーネント呼び出し-->
        <HeaderView @input-keyword="searchInput" />
      </div>
    </div>

    <router-view
      :searchUsers="searchUsers"
      :searchSchoolKey="searchSchoolKey"
      :searchPortfolios="searchPortfolios"
    ></router-view>

    <!--フッター部-->
    <div class="sticky mt-auto">
      <div id="app">
        <!--FooterViewコンポーネント呼び出し-->
        <FooterView />
      </div>
    </div>
  </div>
</template>

<script>
import HeaderView from "./components/HeaderView.vue";
import FooterView from "./components/FooterView.vue";

export default {
  name: "App",
  components: {
    // コンポーネントに登録する
    HeaderView,
    FooterView
  },
  data() {
    return {
      searchUsers: [],
      searchSchoolKey: [],
      searchPortfolios: []
    };
  },
  methods: {
    updateSchoolUser(searchSchoolUsers, searchSchoolKey) {
      this.searchUsers = searchSchoolUsers;
      this.searchSchoolKey = searchSchoolKey;
    },
    updatePortfolios(searchPortfolios) {
      this.searchPortfolios = searchPortfolios;
    },
    searchSchoolUserKey(searchSchoolUsers) {
      this.searchUsers = searchSchoolUsers;
    },
    searchSchoolUserKeyClear() {
      this.searchUsers = "";
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  /*フォントによって日本語の斜体が効かない */
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  /* color: #2c3e50; */
  /* margin-top: 60px; */
}

.user-icon {
  border-radius: 50%;
}

.body {
  background-image: linear-gradient(0deg, transparent 62px, #e5e7eb 64px), linear-gradient(90deg,  transparent 62px, #e5e7eb 64px);
background-size: 64px 64px;
}
</style>