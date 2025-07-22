<template>
  <div class="article-post mx-auto my-10 w-10/12">
    <div class="border-b-4 border-teal-800 mb-4 flex space-x-2 px-5 py-1 justify-between items-end">
      <div
        class="font-semibold inline-flex items-end gap-2 border-transparent text-[28px] whitespace-nowrap text-gray-700"
      >投稿作成</div>
    </div>

    <form class="border-1 border-gray-900" v-on:submit.prevent="AddPortfolio">
      <div
        class="mt-4 mx-auto w-full first-line:max-w-sm bg-white border-t border-x border-gray-200 rounded-t-3xl"
      >
        <!-- タイトル -->
        <div class="pt-2 pb-1 px-12">
          <div class="relative fle mb-7 w-3/4 mt-5">
            <div class="flex gap-12">
              <label for="username" class="block mb-1 text-lg text-left text-gray-900">タイトル</label>
              <div class="block mb-1 text-lg text-left text-red-500">＊必須</div>
            </div>
            <input
              type="title"
              name="title"
              id="title"
              v-model="portfolio.title"
              class="bg-gray-100 border-gray-100 border text-gray-900 text-lg rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
              placeholder=" "
            />
          </div>
          <!--サムネイル-->
          <div class="mt-10 text-left">
            <label class="block mb-2 text-lg font-medium text-gray-900" for="file_input">サムネイル画像選択</label>
            <label class="w-full">
              <input
                type="file"
                @change="onImageUploaded"
                ref="preview_image"
                class="w-1/2 text-lg text-grey-500 file:mr-5 file:py-2 file:px-6 file:rounded-full file:border-0 file:text-base file:font-medium file:bg-gray-200 file:text-gray-700 hover:file:cursor-pointer hover:file:bg-teal-500 hover:file:text-white"
                required
              />
            </label>
            <div v-if="portfolio.title_image" class="w-[500px] mt-2">
              <img :src="portfolio.title_image" />
            </div>
            <p class="mt-1 ml-2 text-base text-gray-500" id="file_input_help">PNG, JPGかつ1MB以下のみ</p>
          </div>
          <!-- ビデオ -->
          <div class="mt-10 text-left">
            <label class="block mb-2 text-lg font-medium text-gray-900" for="file_input">ビデオ・サウンド選択</label>
            <label class="w-full">
              <input
                type="file"
                ref="preview_movie"
                class="w-1/2 text-lg text-grey-500 file:mr-5 file:py-2 file:px-6 file:rounded-full file:border-0 file:text-base file:font-medium file:bg-gray-200 file:text-gray-700 hover:file:cursor-pointer hover:file:bg-teal-500 hover:file:text-white"
                required2
                @change="handleVideoUpload"
                accept="video/mp4, video/x-m4v, audio/mpeg, audio/mp3"
              />
            </label>
            <div v-if="movie_preview" class="mt-2">
              <video controls width="400" height="300" :key="movie_key">
                <source :src="movie_preview" type="video/mp4" />Your browser does not support the video tag.
              </video>
            </div>
            <p class="mt-1 ml-2 text-base text-gray-500" id="file_input_help">MP4, MP3かつ40MB以下のみ</p>
          </div>
          <!--カテゴリ-->
          <div class="mt-10 mb-2 w-1/2">
            <div class="flex gap-2">
              <label for="profession" class="block mb-2 text-lg text-left text-gray-900">カテゴリ選択</label>
              <div class="block mb-1 text-lg text-left text-red-500">＊必須</div>
            </div>
            <div class="flex flex-row items-center text-base sm:flex-row sm:space-y-0 sm:space-x-4">
              <div class="relative w-3/4 z-0 flex">
                <select
                  id="underline_select"
                  v-model="portfolio.category_id"
                  @change="updateGenres"
                  class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                >
                  <option
                    class="rounded-lg"
                    v-for="category in categoryList"
                    :value="category.value"
                    :key="category.value"
                    :selected="category.value === portfolio.category_id"
                  >[[ category.label ||""]]</option>
                </select>
              </div>
              <input
                type="button"
                v-on:click="templateIn()"
                value="テンプレートを適用"
                class="w-full text-center py-2.5 px-6 text-base font-medium bg-gray-200 text-gray-700 rounded-xl cursor-pointer sm:w-min hover:bg-teal-500 hover:text-gray-50 mb-4"
              />
            </div>
          </div>
          <!--ジャンル-->
          <div class="mt-10 mb-2 w-1/3">
            <div class="flex gap-2">
              <label for="profession" class="block mb-2 text-lg text-left text-gray-900">ジャンル選択</label>
              <div class="block mb-1 text-lg text-left text-red-500">＊必須</div>
            </div>
            <select
              id="underline_select_genre"
              v-model="portfolio.ganre_id"
              class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
            >
              <option
                v-for="genre in genres"
                :value="genre.value"
                :key="genre.value"
                :selected="genre.value === portfolio.ganre_id"
              >[[ genre.label ||""]]</option>
            </select>
          </div>
          <p
            class="text-left ml-1 mb-1 text-base text-gray-700 peer-invalid:visible"
          >※カテゴリを選択すると表示されます</p>
          <!--タグ-->
          <div class="mt-10 mb-1">
            <label for="username" class="block mb-1 text-lg text-left text-gray-900">タグ</label>
            <div class="flex flex-row items-center text-base sm:flex-row sm:space-y-0 sm:space-x-4">
              <div class="relative w-3/4 z-0 flex">
                <vue3-simple-typeahead
                  class="simple-typeahead bg-gray-100 border-gray-100 border text-gray-900 text-lg rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                  ref="typeahead"
                  v-model="tagInput"
                  @keydown.enter.prevent="addTag"
                  placeholder=" "
                  :items="tagList"
                  :minInputLength="1"
                  :itemProjection="itemProjectionFunction"
                  @selectItem="selectItemEventHandler"
                ></vue3-simple-typeahead>
              </div>
              <input
                type="button"
                v-on:click="addTag"
                value="追加"
                class="w-full text-center py-2.5 px-6 text-lg font-medium bg-gray-200 text-gray-700 rounded-xl cursor-pointer sm:w-min hover:bg-teal-500 hover:text-gray-50 mb-4"
              />
            </div>
          </div>
          <p
            class="text-left ml-1 mb-1 text-base text-gray-700 peer-invalid:visible"
          >※20文字以下で入力してください</p>
          <div class="px-2 py-1 mb-3 flex flex-wrap rounded-lg bg-gray-100">
            <span
              v-for="tag in portfolio.tag"
              :key="tag"
              class="flex flex-wrap pl-4 pr-2 py-1 m-1 justify-between items-center text-base font-medium rounded-full cursor-pointer bg-gray-50 text-gray-700 border-2 border-gray-600 hover:bg-teal-500 hover:text-gray-50 hover:border-teal-500"
            >
              [[ tag ||""]]
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5 ml-3 hover:text-gray-300"
                viewBox="0 0 20 20"
                fill="currentColor"
                @click="removeTag(tag)"
              >
                <path
                  fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clip-rule="evenodd"
                />
              </svg>
            </span>
          </div>
        </div>
      </div>

      <!--マークダウン-->
      <div class="mx-auto w-full first-line:max-w-sm bg-white border-x border-gray-200">
        <div class="items-start justify-start text-gray-900 text-lg pb-2 px-12 gap-2">
          <div class="flex flex-row">
          <label class="mb-2">本文</label>
          <div class="flex items-center text-lg text-left text-red-500 mb-2 ml-10">＊必須</div>
        </div>
          <p
            class="text-left mb-1 text-base text-gray-700 peer-invalid:visible"
          >※本文を20000文字以下で入力してください</p>
        </div>
      </div>
      <div class="px-12 bg-white border-x border-gray-200">
        <mavon-editor
          :toolbars="markdownOption"
          @imgAdd="imgAdd"
          @save="downloadMarkdown"
          language="ja"
          font-size="17px"
          :autofocus="false"
          v-model="portfolio.sentence"
        />
      </div>
      <div
        class="mx-auto w-full h-8 first-line:max-w-sm bg-white border-x border-b rounded-b-3xl border-gray-200"
      >
        <div class="text-white select-none">
          <label>a</label>
        </div>
      </div>

      <!--登録ボタン-->
      <div class="mt-10 flex justify-center text-center gap-20">
        <div>
          <input
            type="button"
            v-on:click="AddDraft"
            value="下書きを保存する"
            class="w-1/5 text-center px-5 py-2.5 mr-2 mb-2 text-lg font-medium bg-gray-200 text-gray-700 rounded-xl cursor-pointer sm:w-min hover:bg-teal-500 hover:text-gray-50"
          />
        </div>
        <div>
          <input
            type="button"
            v-on:click="AddPortfolio"
            value="投稿する"
            class="w-1/5 text-center px-14 py-2.5 mr-2 mb-2 text-lg font-medium bg-gray-200 text-gray-700 rounded-xl cursor-pointer sm:w-min hover:bg-teal-500 hover:text-gray-50"
          />
          <!-- <button type="button"
            class="w-1/5 text-center px-5 py-2.5 mr-2 mb-2 text-lg font-medium bg-gray-200 text-gray-700 rounded-xl cursor-pointer hover:bg-teal-500 hover:text-gray-50"
          @click="AddPortfolio">投稿する</button>-->
        </div>
      </div>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import settingMethods from "@/mixins/settingMethods";
import commonMethods from "@/mixins/commonMethods";
import validationMethods from "@/mixins/validationMethods.js";
import { templatethumbnail, templateList } from "@/data/postview.js";
import { saveAs } from "file-saver";

function generateRandomString(length) {
  const characters =
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
  const currentTimestamp = new Date()
    .toISOString()
    .replace(/[-T:.Z]/g, "")
    .slice(0, 14); // YYYYMMDDHHmmss 形式に変換
  let randomString = "";
  randomString += currentTimestamp;
  for (let i = 0; i < length; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length);
    randomString += characters.charAt(randomIndex);
  }
  return randomString;
}

export default {
  name: "PostView",
  mixins: [settingMethods, commonMethods, validationMethods],
  props: {
    msg: String
  },
  data() {
    return {
      value: "",
      portfolio: {
        user_id: "",
        category_id: "",
        ganre_id: "",
        title: "",
        title_image: null,
        sentence: "",
        tag: [],
        movie: "",
        is_public: true
      },
      movie_preview: null,
      movie_key: 0,
      currentuser: {
        id: ""
      },
      categoryList: [],
      genreList: [],
      tagInput: "",
      genres: [],
      selectedTitleImage: null,
      lastSelectedTitleImage: null,
      sentenceImage: [],
      tagList: [],
      templatethumbnail: templatethumbnail,
      templateList: templateList
    };
  },
  async created() {
    await this.checkCookieExpiration();
    if (!this.$store.getters.isAuthenticated) {
      alert("ログインして下さい");
      this.$router.push({ name: "LoginForm" });
    }
    setInterval(this.checkCookieExpiration, 60000);
    this.checkLoggedIn();
    this.getCurrentUser();
    this.getCategory();
  },
  mounted() {
    this.getGenre();
    this.getTag();
  },
  methods: {
    AddPortfolio() {
      if (!this.validateForm()) {
        return;
      }
      this.portfolio.user_id = this.currentuser.id;
      // 画像削除処理
      const regex = /!\[.*?\]\(\d+\)/g;
      let match;
      while ((match = regex.exec(this.portfolio.sentence))) {
        this.sentenceImage.push(match[1]);
      }
      this.sentenceImage.forEach(image => {
        if (!this.portfolio.sentence.includes(image.url)) {
          this.deleteImageFromServer(image);
        }
      });
      if (this.portfolio.title_image === null) {
        this.portfolio.title_image = this.templatethumbnail[
          this.portfolio.category_id - 1
        ];
      }
      const formData = new FormData();
      formData.append("user_id", this.portfolio.user_id);
      formData.append("category_id", this.portfolio.category_id);
      formData.append("ganre_id", this.portfolio.ganre_id);
      formData.append("title", this.portfolio.title);
      formData.append("sentence", this.portfolio.sentence);
      formData.append("is_public", this.portfolio.is_public);
      this.portfolio.tag.forEach(tag => {
        formData.append("tag", tag);
      });
      formData.append("title_image", this.portfolio.title_image);
      formData.append("movie", this.portfolio.movie);

      for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
      }
      axios
        .post("/api/v1/portfolio/post/", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          this.portfolios = response.data;
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
          this.$router.push({ name: "TopList" });
        })
        .catch(err => {
          console.log("axiosPostErr", err);
        });
    },

    AddDraft() {
      if (!this.validateForm()) {
        return;
      }
      this.portfolio.user_id = this.currentuser.id;
      // 画像削除処理
      const regex = /!\[.*?\]\(\d+\)/g;
      let match;
      while ((match = regex.exec(this.portfolio.sentence))) {
        this.sentenceImage.push(match[1]);
      }
      this.sentenceImage.forEach(image => {
        if (!this.portfolio.sentence.includes(image.url)) {
          this.deleteImageFromServer(image);
        }
      });
      if (this.portfolio.title_image === null) {
        this.portfolio.title_image = this.templatethumbnail[
          this.portfolio.category_id - 1
        ];
      }
      const formData = new FormData();
      formData.append("user_id", this.portfolio.user_id);
      formData.append("category_id", this.portfolio.category_id);
      formData.append("ganre_id", this.portfolio.ganre_id);
      formData.append("title", this.portfolio.title);
      formData.append("sentence", this.portfolio.sentence);
      formData.append("is_public", this.portfolio.is_public);
      this.portfolio.tag.forEach(tag => {
        formData.append("tag", tag);
      });
      formData.append("title_image", this.portfolio.title_image);
      formData.append("movie", this.portfolio.movie);

      for (var pair of formData.entries()) {
        console.log(pair[0] + ": " + pair[1]);
      }
      axios
        .post("/api/v1/portfolio/draft/", formData, {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        })
        .then(response => {
          this.portfolios = response.data;
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
          this.$router.push({ name: "DraftList", params: { id: this.currentuser.id  } });
        })
        .catch(err => {
          console.log("axiosPostErr", err);
        });
    },

    imgAdd(_, img) {
      const fileSize = img.size;
      //MB単位のファイルサイズに計算
      const fileMib = fileSize / 1024 ** 2;
      //10MB以下の場合は処理をする
      if (fileMib <= 10) {
        // 画像ファイルの拡張子を取得
        const extension = img.name.split(".").pop();

        // ランダムな名前を生成
        const randomName = generateRandomString(30);

        // 生成したランダムな名前と拡張子を組み合わせて新しいファイル名を作成
        const newFileName = `sentence_image_${randomName}.${extension}`;

        // FormDataオブジェクトを作成して画像ファイルを追加
        const formData = new FormData();
        formData.append("image", img, newFileName);

        // 画像をアップロードするAPIにFormDataを送信
        axios
          .post("/api/v1/portfolio/image/", formData)
          .then(response => {
            const imageInfo = {
              id: response.data.id,
              url: response.data.image
            };
            const imageUrl = response.data.image;

            // Markdownの画像の部分を生成したURLに変更
            const regex = /!\[.*?\]\(\d+\)/g;
            let count = 1;
            this.portfolio.sentence = this.portfolio.sentence.replace(
              regex,
              () => {
                const replacedImage = `![image${count}](${imageUrl})`;
                count++;
                return replacedImage;
              }
            );
            this.sentenceImage.push(imageInfo);
          })
          .catch(error => {
            console.error("Image upload error:", error);
          });
      } else {
        alert("10MB以下の画像をアップロードしてください。");
      }
    },
    deleteImageFromServer(image) {
      axios
        .delete(`/api/v1/portfolio/image/${image.id}/`)
        .then(() => {
          console.log("Image deleted successfully");
        })
        .catch(error => {
          console.error("Image deletion error:", error);
        });
    },
    onImageUploaded() {
      const file = this.$refs.preview_image.files[0];
      if (!file) {
        return;
      }
      const fileSize = file.size;
      //MB単位のファイルサイズに計算
      const fileMib = fileSize / 1024 ** 2;
      //10MB以下の場合は処理をする
      if (fileMib <= 10) {
        const extension = file.name.split(".").pop();
        const randomName = generateRandomString(20);
        const newFileName = `thumbnail_${randomName}+.${extension}`;
        const formData = new FormData();
        formData.append("image", file, newFileName);
        axios
          .post("/api/v1/portfolio/titleimage/", formData)
          .then(response => {
            const imageUrl = response.data;
            // 画像削除処理
            this.selectedTitleImage = imageUrl;
            if (this.lastSelectedTitleImage) {
              this.deleteTitleImageFromServer(this.lastSelectedTitleImage);
            }
            this.lastSelectedTitleImage = this.selectedTitleImage;
            this.portfolio.title_image = this.selectedTitleImage.image;
          })
          .catch(error => {
            console.error("Image upload error:", error);
          });
      } else {
        alert("10MB以下の画像をアップロードしてください。");
        /* エラーを吐くためコメントアウト
        document.getElementById('TitleImage').value = '';
        */
        return;
      }
    },
    deleteTitleImageFromServer(image) {
      axios
        .delete(`/api/v1/portfolio/titleimage/${image.id}/`)
        .then(() => {
          console.log("Image deleted successfully");
        })
        .catch(error => {
          console.error("Image deletion error:", error);
        });
    },
    handleVideoUpload(event) {
      const file = event.target.files[0]; // 選択されたファイルを取得
      if (!file) {
        this.portfolio.movie = "";
        this.movie_preview = "";
        return;
      }
      const fileSize = file.size;
      //MB単位のファイルサイズに計算
      const fileMib = parseInt(fileSize / 1024 ** 2);
      //40MB以下の場合は処理をする
      if (fileMib <= 40) {
        this.portfolio.movie = file;
        const reader = new FileReader();
        reader.onload = () => {
          this.movie_preview = reader.result; // ビデオURLを設定
          this.movie_key++;
        };
        reader.readAsDataURL(file); // ファイルを読み込む
      } else {
        alert("40MB以下のビデオをアップロードしてください。");
        this.portfolio.movie = "";
        this.movie_preview = "";
        /*エラーを吐くためコメントアウト
        document.getElementById('video').value = '';
        */
        return;
      }
    },
    updateGenres() {
      const categoryIndex = this.portfolio.category_id - 1;
      this.genres = this.genreList[categoryIndex];
    },
    selectItemEventHandler(item) {
      this.tagInput = item;
      this.addTag();
    },
    addTag() {
      const trimmedTags = this.tagInput.split(",").map(tag => tag.trim());
      trimmedTags.forEach(tag => {
        if (
          tag &&
          !this.portfolio.tag.includes(tag) &&
          tag.length <= 20 &&
          this.portfolio.tag.length < 5
        ) {
          this.portfolio.tag.push(tag);
          this.tagInput = "";
          this.$refs.typeahead.clearInput();
        }
      });
    },
    removeTag(tag) {
      const index = this.portfolio.tag.indexOf(tag);
      if (index > -1) {
        this.portfolio.tag.splice(index, 1);
      }
    },
    validateForm() {
      try {
        this.validateRequired(
          this.portfolio.title,
          "タイトルを入力してください。"
        );
        this.validateRequired(
          this.portfolio.category_id,
          "カテゴリを選択してください。"
        );
        this.validateRequired(
          this.portfolio.ganre_id,
          "ジャンルを選択してください。"
        );
        this.validateRequired(
          this.portfolio.sentence,
          "本文を入力してください。"
        );
        this.validateContext(this.portfolio.sentence);
        return true;
      } catch (error) {
        alert(error.message);
        return false;
      }
    },
    getTag() {
      axios
        .get("/api/v1/portfolio/taglist/")
        .then(response => {
          this.tagList = response.data.map(item => item.name);
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    templateIn() {
      const categoryIndex = this.portfolio.category_id - 1;
      if (categoryIndex != -1) {
        this.portfolio.sentence = this.templateList[categoryIndex].text;
      }
    },
    downloadMarkdown() {
      // Blobオブジェクトを作成
      const blob = new Blob([this.portfolio.sentence], {
        type: "text/markdown"
      });

      // ファイルをダウンロード
      saveAs(blob, "portfolio.md");
    }
  }
};
</script>

<style>
* {
  box-sizing: border-box;
}

ul,
li {
  margin: 0;
  padding: 0;
}

.selectBox {
  position: relative;
  width: 10em;
  height: 60px;
}

.selectBox select {
  position: absolute;
  left: 100%;
  top: 100%;
  width: 100%;
  height: 100%;
}

.selectBox__output {
  display: flex;
  align-items: center;
  position: relative;
  width: 100%;
  height: 100%;
  padding: 1em;
  border: 1px solid #ccc;
  background-color: #fff;
  border-radius: 5px;
  z-index: 2;
}

.selectBox__output::after {
  display: block;
  position: absolute;
  right: 3%;
  top: 50%;
  font-family: "CONDENSEicon";
  transform: translateY(-50%);
  content: "û";
}

.selectBox__output.open::after {
  transform: translateY(-50%) rotate(180deg);
}

.selectBox__selector {
  position: absolute;
  left: 0;
  top: calc(100% - 1px);
  width: 100%;
  border: 1px solid #ccc;
  background-color: #fff;
  transform-origin: left top;
  z-index: 10;
}

.selectBox__selectorItem {
  width: 100%;
  padding: 0.75em;
}

.selectBox__selectorItem + .selectBox__selectorItem {
  border-top: 1px solid #ccc;
}

.selectBox__selectorItem:hover {
  background-color: #0d61ad;
  color: #fff;
}

.accodion-enter-active,
.accodion-leave-active {
  transition: 0.5s;
  overflow: hidden;
}

.accodion-enter,
.accodion-leave-to {
  transform: scaleY(0);
}

.accodion-leave,
.accodion-enter-to {
  transform: scaleY(1);
}

.article-post .simple-typeahead {
  position: relative !important;
  width: 100% !important;
}

.article-post .simple-typeahead > input {
  margin-bottom: 3px !important;
  outline: none !important;
  width: 100% !important;
}

.article-post ul {
  list-style-type: initial !important;
}

.article-post ol {
  list-style-type: decimal !important;
}
</style>