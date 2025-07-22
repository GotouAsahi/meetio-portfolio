import axios from 'axios';

export default {
  methods: {
    checkCookieExpiration() {
      const cookieValue = this.getCookie("token"); // クッキーの値を取得

      if (!cookieValue) {
        // クッキーが存在しない場合、再ログイン
        // alert("ログインして下さい");
        this.$store.dispatch("logout");
        // this.$router.push({ name: "LoginForm" });
      } else {
        const expirationDate = new Date(cookieValue); // クッキーの有効期限を取得
        const now = new Date();

        if (now > expirationDate) {
          // クッキーの有効期限が切れた場合、再ログインダイアログを表示
          // alert("ログインして下さい");
          this.$store.dispatch("logout");
          // this.$router.push({ name: "LoginForm" });
        } else {
          this.$store.dispatch("login");
        }
      }
    },
    getCookie(name) {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.startsWith(name + "=")) {
          const jwtToken = cookie.substring(name.length + 1);
          const jwtPayload = jwtToken.split(".")[1];
          try {
            const decodedPayload = atob(jwtPayload);
            const payloadData = JSON.parse(decodedPayload);
            if (payloadData && payloadData.exp) {
              // 有効期限を取得して返す
              const expirationDate = new Date(payloadData.exp * 1000);
              return expirationDate;
            }
          } catch (error) {
            console.error("JWTデコードエラー:", error);
            return null;
          }
        }
      }
      return null;
    },
    checkLoggedIn() {
      axios
        .get("/api/v1/auth/users/me/", {
          withCredentials: true,
          headers: {
            Authorization: 'JWT ' + this.$cookies.get("token")
          }
        })
        .then(() => {
        })
        .catch((error) => {
          console.log("axiosGetErr", error);
          this.$router.push({ name: "LoginForm" });
        });
    },
    getCurrentUser() {
      return new Promise((resolve, reject) => {
        axios
          .get("/api/v1/auth/users/me/", {
            withCredentials: true,
            headers: {
              Authorization: 'JWT ' + this.$cookies.get("token")
            }
          })
          .then((response) => {
            this.currentuser.id = response.data.id;
            this.currentuser.username = response.data.username;
            this.currentuser.email = response.data.email;
            resolve(); // Promiseを正常に完了
          })
          .catch((error) => {
            console.log("axiosGetErr", error);
            reject(error); // エラー時にPromiseを拒否
          });
      });
    },
    isCurrentUser() {
      return this.currentuser.id === this.user.id;
    },
    isNullCurrentUser() {
      return this.currentuser.id === null || this.user.id === null
    },
    formatDate(date) {
      const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
      return new Date(date).toLocaleDateString('ja-JP', options);
    },
    getCategory() {
      axios.get("/api/v1/portfolio/category/")
        .then(response => {
          const data = response.data;
          this.categoryList = data.map(item => ({
            value: item.id,
            label: item.name
          }));
        })
        .catch(error => {
          console.log(error);
        });
    },
    getGenre() {
      axios.get("/api/v1/portfolio/ganre/")
        .then(response => {
          const data = response.data;
          const genre_volume = [7, 6, 4, 3, 5, 7]

          let startIndex = 0;
          for (let i = 0; i < genre_volume.length; i++) {
            const chunkSize = genre_volume[i];
            const genreChunk = data.slice(startIndex, startIndex + chunkSize).map(item => ({
              value: item.id,
              label: item.name
            }));
            this.genreList.push(genreChunk);
            startIndex += chunkSize;
          }
          // 格納したジャンルリストを表示
        })
        .catch(error => {
          console.log(error);
        });
    },
    likeCount(portfolio) {
      return portfolio.like_count ? portfolio.like_count.length : 0;
    },
    isLike(portfolio) {
      return (
        portfolio.like_count &&
        portfolio.like_count.includes(this.currentuser.id)
      );
    },
    InitialValue() {
      this.carouselIndex = 0;
    },
    carouselPrev() {
      this.carouselIndex--;
    },
    carouselNext() {
      this.carouselIndex++;
    },
  },
};