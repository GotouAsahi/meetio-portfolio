<template>
  <div class="article-show mx-auto my-3 w-10/12">
    <div class="flex">
      <div class="w-full p-4">
        <div class="bg-white rounded-lg shadow-lg p-6">
          <div class="mt-0">
            <div class="article-show mx-auto my-3 w-10/12">
              <div class="flex">
                <div class="w-full p-4">
                  <div
                    class="border-b-4 border-blue-900 bg-white pb-2 flex px-8 justify-between items-center text-3xl font-bold"
                  >[[this.test.title||""]]</div>
                  <div class="my-8 px-12 py-8 border-4 border-blue-300">
                    <div class="border-b-2 border-blue-900 dark:border-gray-700">
                      <div class="flex space-x-2 px-5 justify-between items-end">
                        <div
                          class="font-semibold hs-tab-active:border-teal-500 hs-tab-active:text-teal-600 inline-flex items-center gap-2 border-transparent text-2xl whitespace-nowrap text-gray-700"
                        >問題</div>
                      </div>
                    </div>
                    <mavon-editor
                      v-model="this.test.problem"
                      language="ja"
                      :subfield="false"
                      :boxShadow="false"
                      defaultOpen="preview"
                      :toolbars="false"
                      :toolbarsFlag="false"
                      style="font-size: 20px; text-align: left; margin-left: 0px;"
                    />

                    <div class="border-b-2 border-blue-900 dark:border-gray-700">
                      <div class="pt-8 flex space-x-2 px-5 justify-between items-end">
                        <div
                          class="font-semibold hs-tab-active:border-teal-500 hs-tab-active:text-teal-600 inline-flex items-center gap-2 border-transparent text-2xl whitespace-nowrap text-gray-700"
                        >サンプルケース</div>
                      </div>
                    </div>
                    <mavon-editor
                      v-model="this.test.sample_explanation"
                      language="ja"
                      :boxShadow="false"
                      :subfield="false"
                      defaultOpen="preview"
                      :toolbars="false"
                      :toolbarsFlag="false"
                      style="font-size: 20px; text-align: left; margin-left: 0px;"
                    />
                  </div>

                  <div class="bg-gray-200 rounded-lg px-6 py-2 mt-12">
                    <div class="my-2">
                      <div class="article-post mx-auto">
                        <form class="border-1 border-gray-900" v-on:submit.prevent="AddJudge">
                          <div class="flex justify-between items-center mb-4">
                            <div class="font-semibold text-2xl text-gray-700">解答コード入力欄</div>
                            <select
                              id="underline_select"
                              v-model="value.language"
                              @change="changeEditorLanguage"
                              class="bg-white border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-100 hover:border-gray-200 focus:ring-2 focus:ring-blue-400 focus:border-blue-300 focus:ring-opacity-50 focus:outline-none w-1/6 p-2.5"
                            >
                              <option
                                class="rounded-lg"
                                v-for="lang in langList"
                                :key="lang.name"
                                :value="lang.name"
                              >
                                [[
                                lang.name ||""]]
                              </option>
                            </select>
                          </div>
                          <div ref="editor" class="editor-container"></div>
                          <!--登録ボタン-->
                          <div class="mt-4 flex justify-end text-center gap-10">
                            <button
                              v-if="juge === false"
                              type="button"
                              class="text-white bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-blue-400 shadow-lg shadow-blue-500/70 font-medium rounded-full text-lg w-1/5 px-5 py-2.5 text-center mb-2"
                              @click="TestJudge"
                            >テスト</button>
                            <button
                              v-if="juge === false"
                              type="button"
                              class="text-white bg-gradient-to-r from-teal-400 via-teal-500 to-teal-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-teal-400 shadow-lg shadow-teal-500/70 font-medium rounded-full text-lg w-1/5 px-5 py-2.5 text-center mb-2"
                              @click="AddJudge"
                            >解答</button>
                            <!--ジャッジ中のボタンレイアウト-->
                            <button
                              v-if="juge === true"
                              disabled
                              type="button"
                              class="flex items-center text-white bg-gradient-to-r from-orange-400 via-orange-500 to-orange-600 shadow-lg font-medium rounded-full text-lg w-1/5 px-5 py-2.5 text-center mb-2"
                            >
                              <span>テスト中</span>
                              <div class="loader ml-2"></div>
                            </button>
                          </div>
                        </form>
                      </div>
                    </div>
                  </div>

                  <!--テスト表示-->
                  <div v-if="this.scoreflag">
                    <div class="my-8 p-8 border-4 border-blue-300">
                      <div
                        class="border-b-2 border-blue-900 pb-1 flex space-x-2 px-5 justify-between items-center text-lg font-semibold"
                      >かかった時間</div>
                      <div
                        class="py-3 flex px-8 text-xl"
                      >[[this.ansMinute||"-"]]分[[this.ansSecond||"-"]]秒</div>
                      <div
                        class="border-b-2 border-blue-900 pb-1 flex space-x-2 px-5 justify-between items-center text-lg font-semibold mt-5"
                      >スコア</div>
                      <div class="flex flex-row justify-between items-center mt-8 mx-16">
                        <div class="w-7/12 my-auto">
                          <div v-if="this.test.difficulty==0">
                            <div class="text-9xl font-bold text-red-600">
                              <div v-if="this.ans.judge_status[0]=='AC'">
                                10
                              </div>
                              <div v-else>
                                0
                              </div>
                            </div>
                            <div class="grid grid-flow-row-dense grid-cols-3 grid-rows-1">
                              <div
                                class="col-span-2 flex justify-end text-6xl font-bold mr-4 text-gray-700"
                              >/</div>
                              <div
                                class="col-span-1 flex justify-start text-6xl font-bold text-gray-800"
                              >10</div>
                            </div>
                          </div>
                          <div v-else>
                            <div class="text-9xl font-bold text-red-600">[[this.ans.score]]</div>
                            <div class="grid grid-flow-row-dense grid-cols-3 grid-rows-1">
                              <div
                                class="col-span-2 flex justify-end text-6xl font-bold mr-4 text-gray-700"
                              >/</div>
                              <div
                                class="col-span-1 flex justify-start text-6xl font-bold text-gray-800"
                              >[[this.maxScore||""]]</div>
                            </div>
                          </div>
                        </div>

                        <div class="w-5/12">
                          <table class="border-collapse border border-slate-400 w-full">
                            <thead>
                              <tr>
                                <th class="border bg-gray-200 border-slate-300 w-1/2 py-2">テストケース</th>
                                <th class="border bg-gray-200 border-slate-300 w-1/2 py-2">結果</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr
                                v-for="(anscase, index) in ans.judge_status"
                                :key="anscase.id"
                                :value="index.id"
                              >
                                <td class="border border-slate-300 py-2">ケース[[index + 1||""]]</td>
                                <td class="border border-slate-300 py-2">[[anscase||""]]</td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>

                      <div class="flex flex-row justify-center items-center w-10/12 mt-16 mx-auto">
                        <!--戻るボタン-->
                        <div class="text-center w-1/2">
                          <router-link
                            :to="{ name: 'JudgeTop' }"
                            class="text-white bg-gradient-to-r from-teal-400 via-teal-500 to-teal-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-teal-400 shadow-lg shadow-teal-500/70 font-medium rounded-full text-lg w-1/2 px-5 py-2.5 text-center mr-2 mb-2"
                          >トップに戻る</router-link>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-else-if="this.testScoreflag">
                    <div class="my-8 p-8 border-4 border-blue-300">
                      <div
                        class="border-b-2 border-blue-900 pb-1 flex space-x-2 px-5 justify-between items-center text-lg font-semibold"
                      >テスト結果</div>
                      <div class="flex flex-row justify-center items-center mt-8 mx-16">
                        <div class="w-6/12">
                          <table class="border-collapse border border-slate-400 w-full">
                            <thead>
                              <tr>
                                <th class="border bg-gray-200 border-slate-300 w-1/2 py-2">テストケース</th>
                                <th class="border bg-gray-200 border-slate-300 w-1/2 py-2">テスト結果</th>
                              </tr>
                            </thead>
                            <tbody>
                              <tr
                                v-for="(anscase, index) in testAns.sample_status"
                                :key="anscase.id"
                                :value="index.id"
                              >
                                <td class="border border-slate-300 py-2">ケース[[index + 1||""]]</td>
                                <td class="border border-slate-300 py-2">[[anscase||""]]</td>
                              </tr>
                            </tbody>
                          </table>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import commonMethods from "@/mixins/commonMethods";
import * as monaco from "monaco-editor";
import metadata from "monaco-editor/esm/metadata";
import { langlist, templateList } from "@/data/judgeform.js";

export default {
  name: "JudgeForm",
  mixins: [commonMethods],
  props: {
    msg: String
  },
  data() {
    return {
      test: [],
      maxScore: 0,
      value: {
        language: "C",
        code: `#include < stdio.h >
int main(void) {
    printf("Hello World");
    return 0;
}`,
        user_id: null,
        problem_id: null,
        group_id: null
      },
      currentuser: {
        id: null
      },
      ans: [],
      ansTime: 0,
      ansMinute: 0,
      ansSecond: 0,
      juge: false,
      langList: langlist,
      scoreflag: false,
      score: 0,
      testAns: [],
      testScoreflag: false,
      templateList: templateList
    };
  },
  async created() {
    await this.checkCookieExpiration();
    if (!this.$store.getters.isAuthenticated) {
      alert("ログインして下さい");
      this.$router.push({ name: "LoginForm" });
    } else {
      setInterval(this.checkCookieExpiration, 60000);
      this.getTest();
      this.getCurrentUser();
      this.ansTime = performance.now();
    }
  },
  mounted() {
    console.log(metadata.languages);
    this.editor = monaco.editor.create(this.$refs.editor, {
      value: this.value.code,
      language: "c", // テキストエディタ言語
      lineNumbers: "on", // 行番号表示
      roundedSelection: true, // 選択範囲を角丸に
      scrollBeyondLastLine: false, // 最終行以降のスクロール
      readOnly: false, // 読取専用
      theme: "vs-dark" // テーマ
    });
  },
  beforeUnmount() {
    this.editor.dispose();
  },
  methods: {
    getTest() {
      axios
        .get(`/api/v1/judge/list/${this.$route.params.id}/`)
        .then(response => {
          this.test = response.data;
          this.maxScore = this.test.difficulty * 10;
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    AddJudge() {
      if (this.juge == false) {
        this.testScoreflag = false;
        this.value.code = this.editor.getValue();
        this.value.user_id = this.currentuser.id;
        this.value.problem_id = this.test.id;
        this.value.group_id = this.$route.params.group_id;
        const elapsedTime = performance.now() - this.ansTime;
        this.juge = true;
        this.ansMinute = Math.floor(elapsedTime / 60000);
        this.ansSecond = Math.floor((elapsedTime % 60000) / 1000);
        axios
          .post("/api/v1/judge/post/", this.value)
          .then(response => {
            this.ans = response.data;
            this.scoreflag = true;
            this.juge = false;
            console.log("axiosGetData:", response.data);
            console.log("status:", response.status);
            this.score = this.ans.score;
            console.log("aaa", this.score);
          })
          .catch(err => {
            const res = err.response.data.error;
            console.log("axiosPostErr", err);
            alert(res);
            this.juge = false;
          });
      }
    },
    changeEditorLanguage() {
      const selectedLanguageName = this.value.language;
      const selectedLanguageObject = this.langList.find(
        lang => lang.name === selectedLanguageName
      );
      const selectedLanguageValue = selectedLanguageObject.value;

      // 言語に対応するテンプレートを取得
      const selectedTemplate = this.templateList.find(
        template => template.language === selectedLanguageValue
      );
      this.editor.setValue(selectedTemplate.text);

      monaco.editor.setModelLanguage(
        this.editor.getModel(),
        selectedLanguageValue
      );
    },
    TestJudge() {
      if (this.juge == false) {
        this.scoreflag = false;
        this.value.code = this.editor.getValue();
        this.value.user_id = this.currentuser.id;
        this.value.problem_id = this.test.id;
        this.value.group_id = this.$route.params.group_id;
        this.juge = true;
        axios
          .post("/api/v1/judge/sample_test/", this.value)
          .then(response => {
            this.testAns = response.data;
            this.testScoreflag = true;
            this.juge = false;
            console.log("axiosGetData:", response.data);
            console.log("status:", response.status);
          })
          .catch(err => {
            console.log("axiosPostErr", err);
          });
      }
    }
  }
};
</script>
<style>
.editor-container {
  height: 400px;
}

.monaco-editor .view-line {
  text-align: left;
}

.loader,
.loader:after {
  border-radius: 50%;
  width: 5em;
  height: 5em;
  position: relative;
}

.loader {
  margin: auto;
  font-size: 10px;
  position: relative;
  text-indent: -9999em;
  border-top: 1.1em solid rgba(255, 255, 255, 0.2);
  border-right: 1.1em solid rgba(255, 255, 255, 0.2);
  border-bottom: 1.1em solid rgba(255, 255, 255, 0.2);
  border-left: 1.1em solid #ffffff;
  -webkit-transform: translateZ(0);
  -ms-transform: translateZ(0);
  transform: translateZ(0);
  -webkit-animation: load8 1.1s infinite linear;
  animation: load8 1.1s infinite linear;
}

@-webkit-keyframes load8 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }

  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

@keyframes load8 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }

  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
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