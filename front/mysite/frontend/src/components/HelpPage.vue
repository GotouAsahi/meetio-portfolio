<template>
  <div>
    <div class="relative mx-auto my-3 w-10/12 mt-10" ref="margin_search">
      <div class="border-b-4 border-teal-800 pb-2 flex space-x-2 px-5 justify-between items-end">
        <div
          class="font-semibold hs-tab-active:border-teal-500 hs-tab-active:text-teal-600 inline-flex items-end gap-2 border-transparent text-2xl whitespace-nowrap text-gray-700"
        >ヘルプページ</div>
      </div>
    </div>
    <div class="mx-auto my-3 w-10/12">
      <div class="flex gap-4">
        <div class="article-show bg-white rounded-lg shadow-lg p-6 w-10/12">
          <h2
            id="meetio"
            class="border-b-2 mb-3 text-left text-3xl font-bold text-gray-800"
          >Meetioとは</h2>
          <p>
            <b class="text-lime-600">Meetio</b>は学生・クリエイター向けのポートフォリオの公開とプログラミングスキルの可視化を組み合わせたサービスです。
            <b class="text-lime-600">Meetio</b>では自分の作品に加えて情報分野の学生向けにプログラミングスキルもポートフォリオとして公開することができます。
            また、チーム開発の経験を積みたい学生向けにユーザー検索の機能が充実しており、学校・学科・得意なプログラミング言語から検索することでチーム開発のメンバー探しに使用することもできます。
            <br />このことから情報系の学生には特に使いやすいサービスになっています。
          </p>
          <h2
            id="portfolio"
            class="border-b-2 my-3 mt-9 text-left text-3xl font-bold text-gray-800"
          >ポートフォリオ</h2>
          <h3 id="homepage" class=" text-left text-2xl font-bold text-gray-800">ホーム画面</h3>
          <p>
            ホーム画面では最近の投稿、人気の投稿、フォローしているユーザーの投稿を見ることができます。
            <br />また、一覧表示を押すことでそれぞれの投稿を一覧画面で表示することができます。
          </p>
          <h5 id="newpost" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">最近の投稿</h5>
          <p class="pl-3">最近の投稿では過去7日間に投稿されたものを新規投稿順で表示しています。</p>
          <h5 id="likepost" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">人気の投稿</h5>
          <p class="pl-3">人気の投稿では過去7日間に投稿されたものをいいねが多い順で表示しています。</p>
          <h5 id="followpost" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">フォロー中</h5>
          <p class="pl-3">フォロー中ではフォローをしているユーザーの投稿を新規投稿順で表示しています。</p>
          <h3 id="function" class="mt-3 text-left text-2xl font-bold text-gray-800">機能</h3>
          <h5 id="likefun" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">いいね機能</h5>
          <p class="pl-3">
            記事の一覧画面や記事の詳細画面から♥マークを押すことでいいねすることができます。
            <br />いいねをした記事はマイプロフィールのお気に入りの投稿から確認することができます。
          </p>
          <h5 id="commentfun" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">コメント機能</h5>
          <p class="pl-3">記事の最下部から記事に対してのコメントやコメントのリプライを投稿することができます。</p>

          <h5 id="scoutfun" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">スカウト機能</h5>
          <p class="pl-3">
            他のユーザーのプロフィール画面から連絡するボタンを押すことで下記文面のスカウトメールを送ることできます。
            <br />------------------------------------------------------------------------
            <br />タイトル：○○さんからスカウトが来ています！！
            <br />本文：
            ○○さんからスカウトが来ています！
            <br />ぜひ○○さんの詳細を見てみましょう！！
            <br />http://184.73.208.222/user/○○
            <br />○○さんのメールアドレス：example@example.com
            <br />------------------------------------------------------------------------
          </p>
          <h5 id="scoutfun" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">フォロー機能</h5>
          <p class="pl-3">
            他のユーザーのプロフィール画面から気になるボタンを押すことでフォローをすることができます。フォローをしたユーザーはマイプロフィールのフォロー中のユーザーから確認することができます。
            <br />また、ホーム画面のフォロー中の投稿からフォロー中のユーザーのみの投稿を見ることができます。
            <br />フォローの解除は再度気になるボタンを押すことで解除できます。
          </p>
          <h3 id="articlesearch" class="mt-3 text-left text-2xl font-bold text-gray-800">記事検索</h3>
          <h5 id="charsearch" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">文字検索</h5>
          <p class="pl-3 text-gray-800">
            ヘッダーの検索バーから記事の検索をすることができます。
            <br /><b>タイトル</b>
            <br /><b>本文</b>
            <br /><b>カテゴリー</b>
            <br /><b>ジャンル</b>
            <br /><b>タグ</b>
            <br />の中に検索した文字を含む記事を表示します。
          </p>
          <h5 id="catesearch" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">カテゴリー検索</h5>
          <p class="pl-3">ヘッダーのカテゴリー検索から検索をすることができます。</p>
          <h5 id="genresearch" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">ジャンル検索</h5>
          <p class="pl-3">カテゴリーの検索後に画面上部に表示されるジャンルをクリックすることでジャンルを絞り込んで検索をすることができます。</p>
          <h5 id="tagsearch" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">タグ検索</h5>
          <p class="pl-3">記事詳細の画面上部に表示されるタグをクリックすることでそのタグがついた他の記事が表示されます。</p>
          <h5 id="usersearch" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">ユーザー検索</h5>
          <p class="pl-3">
            ユーザー検索画面では学校・学科・学年・得意言語からユーザー学校名を入力することで、学科入力の際に関連する学科が表示されます。
            <br />また、得意言語は本サイトのスキルチェックで扱っている言語に限定しています。
          </p>
          <h3 id="portfoliopost" class="mt-3 text-left text-2xl font-bold text-gray-800">ポートフォリオの投稿</h3>
          <h5 id="post" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">投稿</h5>
          <p class="pl-3 text-gray-800">
            投稿画面では注意事項に気を付けながら必須項目と任意項目を入力することで投稿することができます。
            <br /><b>タイトル</b>
            <br />100文字までタイトルとして設定できます。
            <br /><b>サムネイル画像</b>
            <br />PNG、JPGかつ1MB以下の画像のみ設定できます。
            <br />画像を選択しなかった場合はテンプレート画像がサムネイルに設定されます。
            <br /><b>ビデオ・サウンド</b>
            <br />MP4、MP3かつ40MB以下のファイルのみ設定できます。
            <br /><b>カテゴリ選択</b>
            <br />カテゴリの選択後に「テンプレートを適用」ボタンを押すことでカテゴリに沿った本文が作成されます。
            <br /><b>ジャンル選択</b>
            <br />カテゴリを選択することでそのカテゴリのジャンルが表示されます。
            <br /><b>タグ</b>
            <br />20文字以下のタグを5個まで設定できます。
            <br />他のユーザーが同様のタグで投稿していた場合はサジェストとして表示されます。
            <br /><b>本文</b>
            <br />マークダウン記法で20000文字以下の文字を設定できます。
            <br />エディタの詳しい使い方はマークダウンエディタの使い方を確認してください。
          </p>
          <h5 id="edit" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">編集</h5>
          <p class="pl-3">
            自分が投稿したポートフォリオの画面上部の編集するボタンを押すことで編集ができます。
            <br />基本は投稿と同様ですが編集画面では公開と非公開の切り替えを行うことができます。
            <br />マイプロフィールから現在の記事の公開ステータスが確認できます。
          </p>
          <h5 id="draft" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">下書き</h5>
          <p class="pl-3">
            必須項目を入力後、投稿画面の画面最下部の「下書きを保存する」をクリックすることで現在の状態を下書きとして保存することができます。
            <br />下書き一覧から自分の下書きをそれぞれ確認することができます。
            <br />下書きでは下書きの更新、記事として投稿、下書きの削除をすることができます。
          </p>
          <h3
            id="mdeditorhow"
            class="mt-3 text-left text-2xl font-bold text-gray-800"
          >マークダウンエディタの使い方</h3>
          <p class="pl-3">更新予定</p>
          <h3 id="myprofile" class="mt-3 text-left text-2xl font-bold text-gray-800">マイプロフィール</h3>
          <h5 id="myprofileedit" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">プロフィール編集</h5>
          <p class="pl-3">
            プロフィール編集ではメールアドレスや氏名をはじめとした自分のプロフィールを編集することができます。
            <br />また、職業を学生に変更することで初期では未登録の学校や学科を登録することができるようになります。
            <br />GithubやXなどの自分のページのURL登録することもできます。
          </p>
          <h5 id="recouser" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">おすすめユーザー</h5>
          <p class="pl-3">おすすめユーザーの欄はスキルチェックで問題を解いた場合に同じ言語で問題を回答しているユーザーが表示されます。</p>
          <h5 id="mpskillcheck" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">スキルチェック</h5>
          <p class="pl-3">スキルチェックのタブには自分の難易度別の問題の回答数と回答した言語の割合がグラフとして表示されます。</p>
          <h5 id="mpportfolio" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">ポートフォリオ</h5>
          <p class="pl-3">
            ポートフォリオのタブには自分が今まで投稿したポートフォリオが表示されます。
            <br />また、非公開の記事も自分のページのみ表示されています。
          </p>
          <h5 id="mplike" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">お気に入り</h5>
          <p class="pl-3">お気に入りではフォロー中のユーザーといいねした記事が表示されます。</p>
          <h2
            id="skillcheck"
            class="border-b-2 my-3 mt-9 text-left text-3xl font-bold text-gray-800"
          >スキルチェック</h2>
          <h3 id="contest" class="mt-3 text-left text-2xl font-bold text-gray-800">大会</h3>
          <p class="pl-3">
            開催中の大会に参加することで他のユーザーとプログラミングスキルを競うことができます。
            <br />大会への参加は大会詳細画面の「参加する」ボタンから参加できます。
          </p>
          <h3 id="quespage" class="mt-3 text-left text-2xl font-bold text-gray-800">問題画面</h3>
          <h5 id="question" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">問題</h5>
          <p class="pl-3 text-gray-800">
            実際の問題が記載されている欄になります。
            <br /><b>問題文</b>
            <br />問題の詳細が記載されています。
            <br /><b>制約</b>
            <br />問題文に出る変数と入力される変数の制約が記載されています。
            <br /><b>入力</b>
            <br />入力される形式が記載されています。
            <br /><b>出力</b>
            <br />求められる出力が記載されています。
          </p>
          <h5 id="samplecase" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">サンプルケース</h5>
          <p class="pl-3 text-gray-800">
            テストする際のサンプルケースが記載されている欄になります。
            <br /><b>入力例</b>
            <br />実際に入力される値が記載されています。
            <br /><b>出力例</b>
            <br />求められる出力が記載されています。
          </p>
          <h5 id="answer" class="mt-3 text-left pl-3 text-xl font-bold text-gray-800">解答コード入力欄</h5>
          <p class="pl-3">
            言語の選択とコードを入力する欄です。
            <br />言語を選択することで言語に対応するハイライトがされるようになっています。
          </p>
          <h3 id="language" class="mt-3 text-left text-2xl font-bold text-gray-800">対応言語</h3>
          <p class="pl-3">"C", "C++", "Dart", "Go", "Java", "Javascript", "Perl", "Php", "Python3", "R", "Ruby", "Swift", "Typescript"</p>
          <h3 id="evamethod" class="mt-3 text-left text-2xl font-bold text-gray-800">評価方法</h3>
          <p class="pl-3">
            難易度×10/テストケースの数×AC数
            <br />例：難易度5、テストケースが7個で4個ACできた場合。
            <br />5×10/7×4 ⇒ 28.571... 切り捨てるので28点。
            <br />計算途中では小数点以下切り捨てしていません。
          </p>
          <h2 id="rule" class="border-b-2 my-3 mt-9 text-left text-3xl font-bold text-gray-800">法律・規約など</h2>
          <p>更新予定</p>
          <h2 id="inquiry" class="border-b-2 my-3 mt-9 text-left text-3xl font-bold text-gray-800">お問い合わせ</h2>
          <p>
            <a href="https://forms.gle/humqCi7Cb3UEbt86A">こちら</a> のフォームからお願いいたします。
          </p>
        </div>
        <div class="w-3/12 h-1 top-3 sticky">
          <h1 class="mb-3 text-xl text-left pl-8 font-bold text-gray-800">目次</h1>
          <div class="text-left pl-8">
            <a
              v-bind:href="'#'+'meetio'"
              class="text-xl text-gray-600 hover:text-teal-500 hover:font-semibold"
            >Meetioとは</a>
            <br />
            <a
              v-bind:href="'#'+'portfolio'"
              class="text-xl text-gray-600 hover:text-teal-500 hover:font-semibold"
            >ポートフォリオ</a>
            <br />
            <a
              v-bind:href="'#'+'homepage'"
              class="text-lg pl-3 text-gray-600 hover:text-teal-500 hover:font-semibold"
            >ホーム画面</a>
            <br />
            <a
              v-bind:href="'#'+'function'"
              class="text-lg pl-3 text-gray-600 hover:text-teal-500 hover:font-semibold"
            >機能</a>
            <br />
            <a
              v-bind:href="'#'+'articlesearch'"
              class="text-lg pl-3 text-gray-600 hover:text-teal-500 hover:font-semibold"
            >記事検索</a>
            <br />
            <a
              v-bind:href="'#'+'portfoliopost'"
              class="text-lg pl-3 text-gray-600 hover:text-teal-500 hover:font-semibold"
            >ポートフォリオの投稿</a>
            <br />
            <a
              v-bind:href="'#'+'mdeditorhow'"
              class="text-lg pl-3 text-gray-600 hover:text-teal-500 hover:font-semibold"
            >マークダウンエディタの使い方</a>
            <br />
            <a
              v-bind:href="'#'+'myprofile'"
              class="text-lg pl-3 text-gray-600 hover:text-teal-500 hover:font-semibold"
            >マイプロフィール</a>
            <br />
            <a
              v-bind:href="'#'+'skillcheck'"
              class="text-xl text-gray-600 hover:text-teal-500 hover:font-semibold"
            >スキルチェック</a>
            <br />
            <a
              v-bind:href="'#'+'contest'"
              class="text-lg pl-3 text-gray-600 hover:text-teal-500 hover:font-semibold"
            >大会</a>
            <br />
            <a
              v-bind:href="'#'+'quespage'"
              class="text-lg pl-3 text-gray-600 hover:text-teal-500 hover:font-semibold"
            >問題画面</a>
            <br />
            <a
              v-bind:href="'#'+'language'"
              class="text-lg pl-3 text-gray-600 hover:text-teal-500 hover:font-semibold"
            >対応言語</a>
            <br />
            <a
              v-bind:href="'#'+'evamethod'"
              class="text-lg pl-3 text-gray-600 hover:text-teal-500 hover:font-semibold"
            >評価方法</a>
            <br />
            <a
              v-bind:href="'#'+'rule'"
              class="text-xl text-gray-600 hover:text-teal-500 hover:font-semibold"
            >法律・規約など</a>
            <br />
            <a
              v-bind:href="'#'+'inquiry'"
              class="text-xl text-gray-600 hover:text-teal-500 hover:font-semibold"
            >お問い合わせ</a>
            <br />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import commonMethods from "@/mixins/commonMethods";

export default {
  name: "HelpPage",
  mixins: [commonMethods],
  props: {
    msg: String
  },
  data() {
    return {};
  },
  created() {
    this.checkCookieExpiration();
    setInterval(this.checkCookieExpiration, 60000);
  },
  methods: {}
};
</script>
<style scoped>
.article-show {
  text-align: left;
}
</style>