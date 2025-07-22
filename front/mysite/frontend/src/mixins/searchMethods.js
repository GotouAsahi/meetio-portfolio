import axios from 'axios';

export default {
  methods: {
    searchWord(keyword, page) {
      // const key = "search"
      this.keyword = ""
      axios
        .get('/api/v1/portfolio/search/', {
          params: {
            keyword: keyword,
            page: page,
          },
        })
        .then(response => {
          this.portfolios = response.data
          // this.$root.updatePortfolio(response.data, keyword, key);
          // this.$router.push({ name: 'PostList', params: { key: key }, query: { q: keyword } });
          this.loading = false;
        })
        .catch(error => {
          // エラーハンドリング
          console.error(error);
        });
    },
    searchCategory(category) {
      // const key = "category"
      const categoryMapping = {
        "テクノロジー": "technology",
        "ビジネス": "business",
        "クリエイティブ": "creative",
        "サウンド": "sound",
        "ビデオ": "video",
        "デザイン": "design"
      };
      const keyword = categoryMapping[category] || category;
      axios
        .get(`/api/v1/portfolio/${keyword}/`)
        .then((response) => {
          this.portfolios = response.data
          // this.$root.updatePortfolio(response.data, category, key);
          // this.$router.push({ name: 'PostList', params: { key: key }, query: { q: category } });
          this.loading = false;
        })
        .then(response => {
          console.log("status:", response.status)
          console.log("axiosGetData:", response.data)
        })
        .catch(err => {
          console.log("axiosGetErr", err)
        })
    },
    searchGenre(genre) {
      // const key = "genre"
      axios
        .get(`/api/v1/portfolio/ganresearch/`, {
          params: {
            keyword: genre,
          },
        })
        .then((response) => {
          this.portfolios = response.data
          // this.$root.updatePortfolio(response.data, genre.label, key);
          // this.$router.push({ name: 'PostList', params: { key: key }, query: { q: genre } });
          this.loading = false;
        })
        .then(response => {
          console.log("status:", response.status)
          console.log("axiosGetData:", response.data)
        })
        .catch(err => {
          console.log("axiosGetErr", err)
        })
    },
    searchTag(tag) {
      // const key = "tag"
      axios
        .get(`/api/v1/portfolio/tagsearch/`, {
          params: {
            keyword: tag
          },
        })
        .then((response) => {
          // this.carsel_flag = true
          this.portfolios = response.data
          // this.$root.updatePortfolio(response.data, tag, key);
          // this.$router.push({ name: 'PostList', params: { key: key }, query: { q: tag } });
          this.loading = false;
        })
        .then(response => {
          console.log("status:", response.status)
          console.log("axiosGetData:", response.data)
        })
        .catch(err => {
          console.log("axiosGetErr", err)
        })
    },
    searchLikeOrder(event, key, keyword) {
      event.preventDefault();
      let url = null;
      switch (key) {
        case 'category':
          url = '?Category=' + keyword
          break
        case 'genre':
          url = '?Genre=' + keyword
          break
        case 'tag':
          url = '?Tag=' + keyword
          break
        case 'search':
          url = '?Keyword=' + keyword
      }
      axios
        .get(`/api/v1/portfolio/like_count_sort_all/${url}`)
        .then((response) => {
          this.evacuationPortfolios = this.portfolios
          this.portfolios = response.data
          // this.$root.updatePortfolio(response.data, keyword, key);
          // this.$root.updateGenre(this.searchResults, genre.name);
          // this.$router.push({ name: 'PostList', params: { key: keyword } });
          this.switchflag = false;
        })
        .catch(err => {
          console.log("axiosGetErr", err)
        })
    },
    searchSchoolUser(name, department, grade, language, currentPage) {
      axios
        .get(`/api/v1/GrandeSearch/`, {
          params: {
            name: name,
            department: department,
            grade: grade,
            language: language,
            page: currentPage
          },
        })
        .then((response) => {
          this.schoolUsers = response.data
          this.$root.searchSchoolUserKeyClear()
          console.log("status:", response.status)
          console.log("axiosGetData:", response.data)
          console.log("testll", response.data)
          this.$router.push({ name: 'SchoolUser' });
        })
        .catch(err => {
          console.log("axiosGetErr", err)
        })
    },
    searchTopImg() {
      axios
        .get(`/api/v1/portfolio/top_image/`)
        .then(response => {
          const pf = response.data;

          // Promise.allを使用して非同期の画像読み込みを待つ
          const imageLoadingPromises = pf.map(portfolio => {
            return new Promise(resolve => {
              this.finish(portfolio, resolve);
            });
          });

          // すべての画像が読み込まれたらstartImageRotationを呼び出す
          Promise.all(imageLoadingPromises).then(() => {
            // this.startImageRotation();
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
    likePortfolio(event, portfolio) {
      event.preventDefault();
      if (!this.$store.getters.isAuthenticated) {
        alert("ログインして下さい");
        this.$router.push({ name: "LoginForm" });
      }
      this.like_list.like_count = [this.currentuser.id];
      if (this.isLike(portfolio)) {
        portfolio.like_count = portfolio.like_count.filter(
          userId => userId !== this.currentuser.id
        );
      } else {
        portfolio.like_count.push(this.currentuser.id);
      }
      axios
        .put(`/api/v1/portfolio/like/${portfolio.id}/`, this.like_list)
        .then(response => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
  },
};