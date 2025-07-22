<template>
  <div>
    <div v-if="backimages[count]" :key="count" class="fixed w-full h-screen top-0">
      <div
        class="w-full h-full bg-cover bg-center animate-fade-in"
        :style="`background-image: url(${backimages[count].title_image})`"
      ></div>
    </div>
    <!-- ログインフォーム -->
    <div class="flex flex-col items-center justify-center mx-auto md:h-screen lg:py-0 opacity-90">
      <div
        class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700 mx-auto mt-5 mb-5 drop-shadow-xl"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-teal-500 md:text-2xl dark:text-white text-center font-mono"
          >ログイン</h1>
          <form class="space-y-4 md:space-y-6" v-on:submit.prevent="login()">
            <!-- フローティングラベル（メールアドレス） -->
            <div class="relative z-0 my-4 flex">
              <input
                type="email"
                name="email"
                id="email"
                class="block py-2.5 px-0 w-full text-base text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-300 peer focus:border-b-4"
                placeholder=" "
                v-model="User.email"
                required
              />
              <label
                for="email"
                class="absolute text-base text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-90 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-6 text-left"
              >メールアドレス</label>
            </div>
            <!-- フローティングラベル（パスワード） -->
            <div class="relative z-0 my-auto flex">
              <input
                :type="inputType"
                name="password"
                id="password"
                class="block py-2.5 px-0 w-full text-base text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-300 peer focus:border-b-4"
                placeholder=" "
                v-model="User.password"
                required
              />
              <span class="input-icon absolute right-0 top-0 bottom-0 flex items-center pr-2">
                <span :class="iconType" @click="onClick">
                  <font-awesome-icon class="px-1" :icon="['fas', iconType]" />
                </span>
              </span>
              <label
                for="password"
                class="absolute text-base text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-90 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-6 text-left"
              >パスワード</label>
            </div>
            <!--ログインボタン-->
            <div class="text-center mt-6">
              <button
                type="submit"
                class="w-1/2 text-white bg-gradient-to-r from-teal-400 via-teal-500 to-teal-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-teal-400 shadow-lg shadow-teal-500/70 font-medium rounded-full text-base px-5 py-2.5 text-center mr-2 mb-2"
              >ログイン</button>
            </div>
            <!--新規作成ボタン-->
            <div>
              <p class="text-base text-center font-light text-gray-500 dark:text-gray-400">
                アカウントを持っていますか？
                <router-link
                  :to="{ name: 'SignupForm'}"
                  class="font-medium text-blue-600 hover:underline dark:text-blue-500"
                >新規作成</router-link>
              </p>
            </div>
          </form>
          <!--or-->
          <!-- <div class="inline-flex items-center justify-center w-full">
            <hr class="w-full h-px bg-gray-400 border-0 dark:bg-gray-700" />
            <span
              class="absolute px-3 text-lg font-medium text-gray-700 -translate-x-1/2 bg-white left-1/2 dark:text-white dark:bg-gray-900"
            >or</span>
          </div>-->
          <!--googleログイン認証-->
          <!-- <div class="group block mx-auto w-1/2 border-gray-500">
            <GoogleLogin :callback="loginWithGoogle" popup-type="TOKEN">
              <v-btn style="height:55px;width:210px">
                <img
                  src="../assets/signin-assets/google_signin_buttons/web/1x/btn_google_signin_light_normal_web.png"
                  style="height:50px"
                />
              </v-btn>
            </GoogleLogin>
          </div>-->
        </div>
      </div>
    </div>
    <div v-if="backimages[count]" class="fixed bottom-12 flex opacity-90">
      <div class="bg-gray-900 bg-opacity-60 rounded-lg flex items-center mx-4 my-4 px-3 py-1 gap-2">
        <router-link
          :to="{ name: 'UserShow', params: { id: backimages[count].user_id.id } }"
          class="flex items-center"
        >
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
</template>

<script>
import axios from "axios";
import settingMethods from "@/mixins/settingMethods";
import validationMethods from "@/mixins/validationMethods.js";
import searchMethods from "@/mixins/searchMethods";

export default {
  name: "LoginForm",
  mixins: [settingMethods, validationMethods, searchMethods],
  props: {
    msg: String
  },
  data() {
    return {
      count: 0,
      isChecked: false,
      iconType: "eye",
      User: {
        email: "",
        password: ""
      },
      backimages: [],
      accessToken: null,
      googleClientId: process.env.VUE_APP_GOOGLE_CLIENT_ID
    };
  },
  created() {
    this.searchTopImg();
  },
  computed: {
    inputType: function() {
      return this.isChecked ? "text" : "password";
    }
  },
  mounted() {
    this.startImageRotation();
  },
  methods: {
    validateForm() {
      try {
        this.validateRequired(
          this.User.email,
          "メールアドレスを入力してください。"
        );
        this.validateRequired(
          this.User.password,
          "パスワードを入力してください。"
        );
        return true;
      } catch (error) {
        alert(error.message);
        return false;
      }
    },
    login() {
      if (!this.validateForm()) {
        return; // フォームのバリデーションが失敗した場合はログイン処理を中断
      }
      axios
        .post("/api/v1/auth/jwt/create/", this.User)
        .then(response => {
          const token = response.data.access;
          this.$cookies.set("token", token, 60 * 60 * 24 * 7);
          this.$store.dispatch("login");
          window.location.href = "/";
        })
        .catch(err => {
          console.log("axiosGetErr", err);
          alert("ログインに失敗しました。"); // エラーメッセージを表示
        });
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
    onClick: function() {
      this.isChecked = !this.isChecked;
      this.iconType = this.isChecked ? "eye-slash" : "eye";
    },
    /*
    searchLikeOrder2() {
      axios
        .get(`/api/v1/portfolio/top_image/`)
        .then(response => {
          this.portfolios = response.data;

          // Promise.allを使用して非同期の画像読み込みを待つ
          const imageLoadingPromises = this.portfolios.map(portfolio => {
            return new Promise(resolve => {
              this.finish(portfolio, resolve);
            });
          });

          // すべての画像が読み込まれたらstartImageRotationを呼び出す
          Promise.all(imageLoadingPromises).then(() => {
            this.imgflag = true;
            this.startImageRotation();
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
          console.log(img);
        }

        // コールバックを呼び出してPromise.allを進める
        callback();
      };
      img.src = obj.title_image;
    },
    */
    async loginWithGoogle(googleData) {
      console.log("Google Login response", googleData);
      if (googleData) {
        await this.convertToken(googleData.access_token);
        const userDetail = await this.verifyToken(googleData.tokenId);
        console.log("User Detail response", userDetail);
      }
    },
    convertToken(googleData) {
      axios
        .post("/api/v1/auth/convert-token/", {
          token: googleData,
          backend: "google-oauth2",
          grant_type: "convert_token",
          client_id: process.env.VUE_APP_DRF_CLIENT_ID,
          client_secret: process.env.VUE_APP_DRF_CLIENT_SECRET
        })
        .then(response => {
          const token = response.data.access;
          this.$cookies.set("token", token, 60 * 60 * 24 * 7);
          // window.location.href = "/";
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
          return token;
        })
        .catch(err => {
          console.error("Error while sending access token to the server:", err);
        });
    },
    verifyToken(googleToken) {
      const token = googleToken;
      axios
        .post("/api/v1/verify-token/", {
          tokenId: token
        })
        .then(response => {
          return response.data;
        })
        .catch(err => {
          console.log("Error Verify Token", err);
        });
    }
  }
};
</script>
<style scoped></style>


tokenId="Y5fzjOCLlnG7Op3vV3xmhggmsPtbBN"
http POST http://127.0.0.1:8000/verify-token/ tokenId=${tokenId}