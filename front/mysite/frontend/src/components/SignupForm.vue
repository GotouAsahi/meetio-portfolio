<template>
  <div>
    <div v-if="backimages[count]" :key="count" class="fixed w-full h-screen top-0">
      <div
        class="w-full h-full bg-cover bg-center animate-fade-in"
        :style="`background-image: url(${backimages[count].title_image})`"
      ></div>
    </div>
    <!-- 新規登録フォーム -->
    <div class="flex flex-col items-center justify-center mx-auto md:h-screen lg:py-0 opacity-90">
      <div
        class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700 mx-auto mt-5 mb-5 drop-shadow-xl"
      >
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1
            class="text-xl font-bold leading-tight tracking-tight text-teal-500 md:text-2xl dark:text-white text-center font-mono"
          >新規登録</h1>
          <form class="space-y-4 md:space-y-6" v-on:submit.prevent="signup()">
            <!-- フローティングラベル（メールアドレス） -->
            <div class="relative z-0 my-4 flex">
              <input
                type="email"
                name="email"
                id="email"
                class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-300 peer focus:border-b-4"
                placeholder=" "
                v-model="User.email"
                required
              />
              <label
                for="email"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-90 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-6 text-left"
              >メールアドレス</label>
            </div>
            <!-- フローティングラベル（パスワード） -->
            <div class="relative z-0 my-auto flex">
              <input
                :type="inputType.password"
                name="password"
                id="password"
                class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-300 peer focus:border-b-4"
                placeholder=" "
                v-model="User.password"
                required
              />
              <span class="input-icon absolute right-0 top-0 bottom-0 flex items-center pr-2">
                <span :class="getIconClass('password')" @click="onClick('password')">
                  <font-awesome-icon class="px-1" :icon="['fas', getIconType('password')]" />
                </span>
              </span>
              <label
                for="password"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-90 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-6 text-left"
              >パスワード</label>
              
            </div>
            
            <p class="pass_validation">※6文字以上の英数字で大文字、小文字、数字を含めてください</p>
            
            <!-- フローティングラベル（パスワード再入力） -->
            <div class="relative z-0 my-auto flex">
              <input
                :type="inputType.confirm_password"
                name="confirm_password"
                id="confirm_password"
                class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-300 peer focus:border-b-4"
                placeholder=" "
                v-model="User.confirm_password"
                required
              />
              <span class="input-icon absolute right-0 top-0 bottom-0 flex items-center pr-2">
                <span
                  :class="getIconClass('confirm_password')"
                  @click="onClick('confirm_password')"
                >
                  <font-awesome-icon class="px-1" :icon="['fas', getIconType('confirm_password')]" />
                </span>
              </span>
              <label
                for="confirm_password"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-90 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-6 text-left"
              >パスワード再入力</label>
            </div>
            <!--ユーザー名-->
            <div class="relative z-0 w-full mb-6 group flex">
              <input
                type="text"
                name="floating_first_name"
                id="floating_first_name"
                class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-300 peer focus:border-b-4"
                placeholder=" "
                v-model="User.username"
                required
              />
              <label
                for="floating_first_name"
                class="peer-focus:font-medium absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-90 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-6"
              >氏名</label>
            </div>
            <!--新規登録ボタン-->
            <div class="text-center">
              <button
                type="submit"
                class="w-1/2 text-white bg-gradient-to-r from-teal-400 via-teal-500 to-teal-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-teal-400 shadow-lg shadow-teal-500/70 font-medium rounded-full text-base px-5 py-2.5 text-center mr-2 mb-2"
              >新規登録</button>
            </div>
            <!--ログイン画面遷移ボタン-->
            <p class="text-sm font-light text-center text-gray-500 dark:text-gray-400">
              すでにアカウントを持っている方はこちら
              <router-link
                class="font-medium text-blue-600 hover:underline dark:text-blue-500"
                to="login"
              >ログイン</router-link>
            </p>
          </form>
          <!--or-->
          <!-- <div class="inline-flex items-center justify-center w-full">
            <hr class="w-full h-px bg-gray-400 border-0 dark:bg-gray-700" />
            <span
              class="absolute px-3 text-lg font-medium text-gray-700 -translate-x-1/2 bg-white left-1/2 dark:text-white dark:bg-gray-900"
            >or</span>
          </div> -->
          <!--googleログイン認証-->
          <!-- <div class="group block mx-auto w-1/2 border-gray-500">
            <GoogleLogin :callback="signupWithGoogle" popup-type="TOKEN">
              <v-btn style="height:55px;width:210px">
                <img
                  src="../assets/signin-assets/google_signin_buttons/web/1x/btn_google_signin_light_normal_web.png"
                  style="height:50px"
                />
              </v-btn>
            </GoogleLogin>
          </div> -->
        </div>
      </div>
    </div>
    <div v-if="backimages[count]" class="fixed bottom-12 flex opacity-90">
      <div
        class="bg-gray-900 bg-opacity-60 rounded-lg flex items-center mx-4 my-4 mt-60 px-3 py-1 gap-2"
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
</template>

<script>
import axios from "axios";
import settingMethods from "@/mixins/settingMethods";
import validationMethods from "@/mixins/validationMethods.js";
import searchMethods from "@/mixins/searchMethods";

export default {
  name: "SignupForm",
  mixins: [settingMethods, validationMethods, searchMethods],
  props: {
    msg: String
  },
  data() {
    return {
      count: 0,
      icons: {
        password: {
          type: "eye",
          checked: false
        },
        confirm_password: {
          type: "eye",
          checked: false
        }
      },
      User: {
        email: "",
        username: "",
        password: "",
        confirm_password: ""
      },
      backimages: [],
    };
  },
  created() {
    this.searchTopImg();
  },
  computed: {
    inputType: function() {
      return {
        password: this.icons.password.checked ? "text" : "password",
        confirm_password: this.icons.confirm_password.checked
          ? "text"
          : "password"
      };
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
        this.validateEmailFormat(this.User.email);
        this.validateRequired(
          this.User.password,
          "パスワードを入力してください。"
        );
        this.validateRequired(
          this.User.confirm_password,
          "パスワードを再入力してください。"
        );
        this.validatePasswordMatch(
          this.User.password,
          this.User.confirm_password
        );
        this.validatePasswordLength(this.User.password);
        this.validateRequired(
          this.User.username,
          "氏名を入力してください。"
        );
        this.validatePasswordFormat(this.User.password);
        return true;
      } catch (error) {
        alert(error.message);
        return false;
      }
    },
    signup() {
      if (!this.validateForm()) {
        return;
      }
      const email = this.User.email;
      const password = this.User.password;
      const apiData = {
        email,
        password
      };
      axios
        .post("/api/v1/register/", this.User)
        .then(response => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);

          return axios.post("/api/v1/auth/jwt/create/", apiData);
        })
        .then(response => {
          const token = response.data.access;
          this.$cookies.set("token", token, 60 * 60 * 24 * 7);
          window.location.href = "/";
        })
        .catch(err => {
          console.log("axiosGetErr", err);
          const obj = JSON.parse(err["request"]["response"]);
          if ("email" in obj) {
            const message = obj["email"].toString().replace(/\s+/g, "");
            alert(message); // エラーメッセージを表示
          } else {
            alert("新規登録に失敗しました。"); // エラーメッセージを表示
          }
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
    getIconType(key) {
      return this.icons[key].type;
    },
    getIconClass(key) {
      return this.icons[key].checked ? "fa-eye-slash" : "fa-eye";
    },
    onClick(key) {
      this.icons[key].checked = !this.icons[key].checked;
      this.icons[key].type = this.icons[key].checked ? "eye-slash" : "eye";
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
          console.log(this.backimages);
        }

        // コールバックを呼び出してPromise.allを進める
        callback();
      };
      img.src = obj.title_image;
    },
    */
    async signupWithGoogle(googleData) {
      console.log("Google signup response", googleData);
      if (googleData) {
        const userVerifiedData = await this.verifyToken(googleData.tokenId);
        console.log("User Detail response", userVerifiedData);
        const status = await this.registerUser(userVerifiedData);
        console.log(status);
      }
    },
    registerUser(user_data) {
      console.log("Register User response", user_data);
      const username = user_data["name"];
      const email = user_data["email"];
      axios
        .post("/api/v1/register", {
          username: username,
          email: email
        })
        .then(response => {
          const { username, email } = response.data;
          return { username, email };
        })
        .catch(err => {
          console.log("Error Regigster User", err);
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
<style scoped>
.pass_validation{
  font-size: 12px;
  text-align: left;
  color: red;
}
</style>
