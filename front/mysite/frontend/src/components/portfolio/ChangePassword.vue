<template>
  <div>
    <!-- 新規登録フォーム -->
    <div class="flex flex-col items-center justify-center mx-auto md:h-screen lg:py-0 opacity-90">
      <div
        class="w-full bg-white rounded-lg shadow dark:border md:mt-0 sm:max-w-md xl:p-0 dark:bg-gray-800 dark:border-gray-700 mx-auto mt-5 mb-5 drop-shadow-xl">
        <div class="p-6 space-y-4 md:space-y-6 sm:p-8">
          <h1 class="text-xl font-bold leading-tight tracking-tight md:text-2xl dark:text-white text-teal-500">パスワード変更</h1>
          <form class="space-y-4 md:space-y-6" v-on:submit.prevent="changePassword()">
            <div class="relative z-0 my-auto flex">
              <input :type="inputType.current_password" name="password" id="password"
                class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-300 peer focus:border-b-4"
                placeholder=" " v-model="form.current_password" required />
              <label for="password"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-90 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-6 text-left">現在のパスワード</label>
            </div>
            <!-- フローティングラベル（パスワード） -->
            <div class="relative z-0 my-auto flex">
              <input :type="inputType.password" name="password" id="password"
                class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-300 peer focus:border-b-4"
                placeholder=" " v-model="form.new_password" required />
              <span class="input-icon absolute right-0 top-0 bottom-0 flex items-center pr-2">
                <span :class="getIconClass('password')" @click="onClick('password')">
                  <font-awesome-icon class="px-1" :icon="['fas', getIconType('password')]" />
                </span>
              </span>
              <label for="password"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-90 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-6 text-left">パスワード</label>
            </div>
            <!-- フローティングラベル（パスワード再入力） -->
            <div class="relative z-0 my-auto flex">
              <input :type="inputType.confirm_password" name="confirm_password" id="confirm_password"
                class="block py-2.5 px-0 w-full text-sm text-gray-900 bg-transparent border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-300 peer focus:border-b-4"
                placeholder=" " v-model="form.confirm_password" required />
              <span class=" input-icon absolute right-0 top-0 bottom-0 flex items-center pr-2">
                <span :class="getIconClass('confirm_password')" @click="onClick('confirm_password')">
                  <font-awesome-icon class="px-1" :icon="['fas', getIconType('confirm_password')]" />
                </span>
              </span>
              <label for="confirm_password"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-6 scale-90 top-3 -z-10 origin-[0] peer-focus:left-0 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-90 peer-focus:-translate-y-6 text-left">パスワード再入力</label>
            </div>
            <div>
            </div>
            <!--新規登録ボタン-->
            <div class="text-center">
              <button type="submit"
                class="w-1/2 text-white bg-gradient-to-r from-teal-400 via-teal-500 to-teal-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-teal-400 shadow-lg shadow-teal-500/70 font-medium rounded-full text-base px-5 py-2.5 text-center mr-2 mb-2"
                >パスワード変更</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import settingMethods from "@/mixins/settingMethods";
import commonMethods from '@/mixins/commonMethods';
import validationMethods from '@/mixins/validationMethods.js';

export default {
  name: "ChangePassword",
  mixins: [settingMethods, commonMethods, validationMethods],
  props: {
    msg: String,
  },
  data() {
    return {
      icons: {
        password: {
          type: 'eye',
          checked: false,
        },
        confirm_password: {
          type: 'eye',
          checked: false,
        },
      },
      currentuser: {
        email: "",
      },
      form: {
        current_password: "",
        new_password: "",
        confirm_password: "",
      },
      apiData: {
        email: "",
        password: "",
      }
    };
  },
  created() {
    // this.checkLoggedIn();
    this.checkCookieExpiration();
    setInterval(this.checkCookieExpiration, 60000);
    this.getCurrentUser()
  },
  computed: {
    inputType: function () {
      return {
        password: this.icons.password.checked ? "text" : "password",
        confirm_password: this.icons.confirm_password.checked ? "text" : "password",
      };
    },
  },
  methods: {
    validateForm() {
      try {
        this.validateRequired(this.form.current_password, '現在のパスワードを入力してください。');
        this.validateRequired(this.form.confirm_password, '新しいパスワードを入力してください。');
        this.validateRequired(this.form.confirm_password, '新しいパスワードを再入力してください。');
        this.validatePasswordMatch(this.form.new_password, this.form.confirm_password);
        this.validatePasswordLength(this.form.new_password);
        this.validatePasswordFormat(this.form.new_password);
        return true;
      } catch (error) {
        alert(error.message);
        return false;
      }
    },
    changePassword() {
      if (!this.validateForm()) {
        return;
      }
      axios.post("/api/v1/change_password/", this.form, {
        withCredentials: true,
        headers: {
          Authorization: 'JWT ' + this.$cookies.get("token")
        }
      })
        .then(response => {
          console.log("status:", response.status)
          alert(response.data.message)
          this.apiData.email = this.currentuser.email;
          this.apiData.password = this.form.new_password;
          return axios.post("/api/v1/auth/jwt/create/", this.apiData);
        })
        .then(response => {
          const token = response.data.access;
          this.$cookies.set('token', token, 60 * 60 * 24 * 7);
          window.location.href = "/";
        })
        .catch(err => {
          const res = err.response.data[0];
            console.log("axiosPostErr", err);
            alert(res);
        })
    },
    getIconType(key) {
      return this.icons[key].type;
    },
    getIconClass(key) {
      return this.icons[key].checked ? 'fa-eye-slash' : 'fa-eye';
    },
    onClick(key) {
      this.icons[key].checked = !this.icons[key].checked;
      this.icons[key].type = this.icons[key].checked ? 'eye-slash' : 'eye';
    },
  },
};
</script>
<style scoped></style>
