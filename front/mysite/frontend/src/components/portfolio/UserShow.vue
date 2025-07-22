<template>
  <div>
    <div class="absolute w-full top-0">
      <!--バナー画像-->
      <div class="opacity-100">
        <img
          v-if="this.user.banner"
          class="absolute w-full h-[288px] object-cover z-0"
          :src="this.user.banner"
        />
      </div>
      <!--バナー編集-->
      <div
        v-if="isNullCurrentUser()"
        class="absolute w-full h-[288px] object-cover bg-gray-600 z-1"
      ></div>
      <div v-else-if="this.isCurrentUser()" class="absolute w-full z-1 opacity-50">
        <div class="flex items-center justify-center bg-gray-600">
          <label
            for="dropzone-file"
            class="flex flex-col items-center justify-center w-full h-[288px] object-cover cursor-pointer bg-transprant hover:bg-sky-600 hover:bg-opacity-30"
          >
            <div class="flex flex-col items-center justify-center pt-5 pb-6">
              <font-awesome-icon class="text-white mb-4" icon="cloud-arrow-up" size="2xl" />
              <p class="mb-1 text-[19px] text-white font-semibold drop-shadow-lg">画像を選択してカバー画像を設定する</p>
              <p class="text-[17px] text-white">最適なサイズ : 3200 × 400px</p>
            </div>
            <input
              id="dropzone-file"
              type="file"
              @change="bannerUploaded"
              ref="preview"
              class="hidden"
            />
          </label>
        </div>
        <div class="absolute bottom-0 right-0 mr-20 mb-5">
          <label
            for="profile-icon"
            class="inline-flex justify-center items-center w-12 h-12 select-none bg-gray-800 bg-opacity-40 focus:ring hover:bg-teal-600 normal-case rounded-full cursor-pointer z-1 overflow-visible appearance-none"
          >
            <font-awesome-icon class="text-white opacity-100" icon="pen" size="lg" />
            <input
              id="profile-icon"
              type="file"
              @change="bannerUploaded"
              ref="banner_preview"
              class="hidden"
            />
          </label>
        </div>
        <div class="absolute bottom-0 right-0 mr-6 mb-5">
          <label
            for="trash-icon"
            v-on:click="deleteBannerButton"
            class="inline-flex justify-center items-center w-12 h-12 select-none bg-gray-800 bg-opacity-40 focus:ring hover:bg-teal-600 normal-case rounded-full cursor-pointer z-1 overflow-visible appearance-none"
          >
            <font-awesome-icon class="text-white opacity-100" icon="trash" size="lg" />
          </label>
        </div>
      </div>
    </div>
    <!-- モーダル -->
    <div class="mx-auto mt-3 mb-10 w-9/12 z-10">
      <!-- Main modal -->
      <div v-if="showModal" class="modal-overlay">
        <div
          id="defaultModal"
          tabindex="-1"
          aria-hidden="true"
          class="flex top-0 left-0 w-screen h-screen items-center justify-center z-50 overflow-x-hidden overflow-y-auto md:inset-0"
        >
          <div class="relative w-full max-w-3xl h-screen">
            <!-- Modal content -->
            <div class="relative bg-white rounded-3xl shadow">
              <!-- Modal header -->
              <div
                class="flex items-start justify-between mx-4 py-4 px-2 border-b-2 border-teal-800"
              >
                <h3 class="text-xl font-bold text-gray-700 ml-1 mt-2">プロフィール編集</h3>
                <button
                  type="button"
                  @click="closeModal"
                  class="text-gray-700 bg-transparent hover:text-teal-500 rounded-lg text-lg w-8 h-8 mt-1 ml-auto inline-flex justify-center items-center"
                  data-modal-hide="defaultModal"
                >
                  <font-awesome-icon icon="xmark" size="xl" />
                  <span class="sr-only">Close modal</span>
                </button>
              </div>
              <!-- Modal body -->
              <div class="block h-max py-5 px-10 bg-white">
                <!--アイコン画像編集-->
                <div class="mb-7">
                  <p
                    class="mb-1 text-left text-base font-semibold leading-relaxed text-gray-700"
                  >プロフィールアイコン</p>
                  <div class="mx-5">
                    <div class="flex w-28 h-28">
                      <div class="relative w-[128px]">
                        <img
                          v-if="this.editUser.icon"
                          class="object-cover aspect-square rounded-full overflow-hidden z-0"
                          :src="this.editUser.icon"
                          alt="Rounded avatar"
                        />
                        <img
                          v-else-if="this.user.icon"
                          class="object-cover aspect-square rounded-full overflow-hidden z-0"
                          :src="this.user.icon"
                          alt="Rounded avatar"
                        />
                        <div class="absolute bottom-0 right-0 cursor-pointer">
                          <label
                            for="profile-icon"
                            class="inline-flex justify-center items-center w-12 h-12 select-none bg-black bg-opacity-40 focus:ring hover:bg-opacity-50 normal-case rounded-full cursor-pointer z-10 overflow-visible appearance-none"
                          >
                            <font-awesome-icon class="text-white opacity-100" icon="pen" size="lg" />
                            <input
                              id="profile-icon"
                              type="file"
                              @change="iconUploaded"
                              ref="iconpreview"
                              style="opacity: 0; position: absolute; width: 100%; height: 100%; top: 0; left: 0;"
                            />
                          </label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <!-- メールアドレス編集 -->
                <div class="mb-7 w-3/4">
                  <label
                    for="email"
                    class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                  >メールアドレス</label>
                  <input
                    type="email"
                    id="email"
                    v-model="editUser.email"
                    class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                    placeholder=" "
                  />
                </div>
                <!-- 姓名編集 -->
                <div class="mb-7 w-3/4">
                  <label
                    for="username"
                    class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                  >氏名</label>
                  <input
                    type="text"
                    id="username"
                    v-model="editUser.username"
                    class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                    placeholder=" "
                  />
                </div>
                <!-- ニックネーム編集 -->
                <div class="mb-7 w-3/4">
                  <label
                    for="nickname"
                    class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                  >ニックネーム</label>
                  <input
                    type="text"
                    id="nickname"
                    v-model="editUser.nickname"
                    class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                    placeholder=" "
                  />
                </div>
                <!--性別編集-->
                <label class="block mb-1 text-[15px] font-semibold text-gray-900 text-left">性別</label>
                <div class="flex flex-wrap gap-y-3 ml-1 mb-7">
                  <!--男性-->
                  <div class="flex items-center select-none cursor-pointer">
                    <input
                      type="radio"
                      name="hs-radio-vertical-group"
                      v-model="this.editUser.gender"
                      value="1"
                      class="shrink-0 mb-0.5 mr-0.5 h-5 w-5 border-gray-200 rounded-full text-blue-600 cursor-pointer"
                      id="hs-radio-vertical-group-1"
                      checked
                    />
                    <label
                      for="hs-radio-vertical-group-1"
                      class="text-lg text-gray-500 hover:text-gray-600 ml-1 mr-5 cursor-pointer"
                    >男性</label>
                  </div>
                  <!--女性-->
                  <div class="flex items-center select-none cursor-pointer">
                    <input
                      type="radio"
                      name="hs-radio-vertical-group"
                      v-model="this.editUser.gender"
                      value="2"
                      class="shrink-0 mb-0.5 h-5 w-5 border-gray-200 rounded-full text-blue-600 cursor-pointer"
                      id="hs-radio-vertical-group-2"
                    />
                    <label
                      for="hs-radio-vertical-group-2"
                      class="text-lg text-gray-500 hover:text-gray-600 ml-1 mr-5 cursor-pointer"
                    >女性</label>
                  </div>
                  <!--その他-->
                  <div class="flex items-center select-none cursor-pointer">
                    <input
                      type="radio"
                      name="hs-radio-vertical-group"
                      v-model="this.editUser.gender"
                      value="3"
                      class="shrink-0 mb-0.5 h-5 w-5 border-gray-200 rounded-full text-blue-600 cursor-pointer"
                      id="hs-radio-vertical-group-3"
                    />
                    <label
                      for="hs-radio-vertical-group-3"
                      class="text-lg text-gray-500 hover:text-gray-600 ml-1 mr-5 cursor-pointer"
                    >表示しない</label>
                  </div>
                </div>
                <!-- 職業編集（dropdownの方がいいかも） -->
                <div class="mb-7 w-3/4">
                  <label
                    for="profession"
                    class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                  >職業</label>
                  <select
                    id="profession"
                    v-model="editUser.Profession"
                    class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                  >
                    <option value disabled selected>選択してください</option>
                    <option value="学生">学生</option>
                    <option value="社会人">社会人</option>
                    <option value="その他">その他</option>
                  </select>
                </div>
                <div v-if="this.editUser.Profession==='学生'">
                  <!-- 学校区分編集 -->
                  <div class="mb-7 w-3/4">
                    <label
                      for="classification"
                      class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                    >学校区分</label>
                    <input
                      type="text"
                      id="classification"
                      v-model="editSchool.classification"
                      class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                      placeholder=" "
                    />
                  </div>
                  <!-- 学校名編集 -->
                  <div class="mb-7 w-3/4">
                    <label
                      for="schoolName"
                      class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                    >学校名</label>
                    <input
                      type="text"
                      id="schoolName"
                      v-model="editSchool.name"
                      class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                      placeholder=" "
                    />
                  </div>
                  <!--学部編集-->
                  <div class="mb-7 w-3/4">
                    <label
                      for="faculty"
                      class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                    >学部</label>
                    <input
                      type="text"
                      id="faculty"
                      v-model="editSchool.faculty"
                      class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                      placeholder=" "
                    />
                  </div>
                  <!--学科編集-->
                  <div class="mb-7 w-3/4">
                    <label
                      for="department"
                      class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                    >学科</label>
                    <input
                      type="text"
                      id="department"
                      v-model="editSchool.department"
                      class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                      placeholder=" "
                    />
                  </div>
                  <!--学年編集-->
                  <div class="mb-7 w-3/4">
                    <label
                      for="grade"
                      class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                    >学年</label>
                    <select
                      id="grade"
                      v-model="editSchool.grade"
                      class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                    >
                      <option value="1" selected>1</option>
                      <option value="2">2</option>
                      <option value="3">3</option>
                      <option value="4">4</option>
                      <option value="5">5</option>
                      <option value="6">6</option>
                    </select>
                  </div>
                  <!--卒業年度編集-->
                  <div class="mb-7 w-3/4">
                    <label
                      for="graduation_year"
                      class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                    >卒業年度</label>
                    <input
                      type="text"
                      id="graduation_year"
                      v-model="editSchool.graduation_year"
                      class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                      placeholder=" "
                    />
                  </div>
                </div>
                <!-- 自己紹介編集 -->
                <div class="flex-wrap mb-7 w-full">
                  <label
                    for="introduct"
                    class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                  >自己紹介</label>
                  <textarea
                    id="introduct"
                    v-model="editUser.introduction"
                    class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full min-h-[145px] p-2.5"
                    placeholder="200文字以下で入力してください"
                    maxlength="200"
                  ></textarea>
                </div>
                <!-- 外部リンク編集 -->
                <div class="mb-7 w-3/4">
                  <label
                    for="github"
                    class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                  >GitHub</label>
                  <input
                    type="text"
                    id="github"
                    v-model="editUser.github"
                    class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                    placeholder=" "
                  />
                </div>
                <div class="mb-7 w-3/4">
                  <label
                    for="x"
                    class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                  >X</label>
                  <input
                    type="text"
                    id="x"
                    v-model="editUser.twitter"
                    class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                    placeholder=" "
                  />
                </div>
                <div class="mb-7 w-3/4">
                  <label
                    for="instagram"
                    class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                  >Instagram</label>
                  <input
                    type="text"
                    id="instagram"
                    v-model="editUser.instagram"
                    class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                    placeholder=" "
                  />
                </div>
                <div class="mb-7 w-3/4">
                  <label
                    for="facebook"
                    class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                  >Facebook</label>
                  <input
                    type="text"
                    id="facebook"
                    v-model="editUser.facebook"
                    class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                    placeholder=" "
                  />
                </div>
                <div class="mb-7 w-3/4">
                  <label
                    for="pixiv"
                    class="block mb-1 text-[15px] font-semibold text-left text-gray-900"
                  >pixiv</label>
                  <input
                    type="text"
                    id="pixiv"
                    v-model="editUser.pixiv"
                    class="bg-gray-100 border-gray-100 border text-gray-900 text-base rounded-lg hover:bg-gray-200 hover:border-gray-200 focus:ring-2 focus:ring-teal-500 focus:border-cyan-300 focus:ring-opacity-50 focus:outline-none block w-full p-2.5"
                    placeholder=" "
                  />
                </div>
                <!--スカウト-->
                <label class="block mb-1 text-[15px] font-semibold text-gray-900 text-left">スカウト</label>
                <div class="flex flex-wrap gap-y-3 ml-1 mb-7">
                  <!--受け付ける-->
                  <div class="flex items-center select-none cursor-pointer">
                    <input
                      type="radio"
                      name="scout_receive"
                      v-model="this.editUser.scout_receive"
                      value="true"
                      class="shrink-0 mb-0.5 mr-0.5 h-5 w-5 border-gray-200 rounded-full text-blue-600 cursor-pointer"
                      id="scout_receive_true"
                    />
                    <label
                      for="scout_receive_true"
                      class="text-lg text-gray-500 hover:text-gray-600 ml-1 mr-5 cursor-pointer"
                    >受け付ける</label>
                  </div>
                  <!--受け付けない-->
                  <div class="flex items-center select-none cursor-pointer">
                    <input
                      type="radio"
                      name="scout_receive"
                      v-model="this.editUser.scout_receive"
                      value="false"
                      class="shrink-0 mb-0.5 h-5 w-5 border-gray-200 rounded-full text-blue-600 cursor-pointer"
                      id="scout_receive_false"
                    />
                    <label
                      for="scout_receive_false"
                      class="text-lg text-gray-500 hover:text-gray-600 ml-1 mr-5 cursor-pointer"
                    >受け付けない</label>
                  </div>
                </div>
                <!-- パスワード編集 -->
                <div class="flex mb-7 w-3/4">
                  <p class="text-[18px] font-medium text-gray-900">
                    パスワードの変更は
                    <a
                      href="/user/password"
                      class="text-blue-600 dark:text-blue-500 hover:underline"
                    >こちら</a>
                  </p>
                </div>
              </div>
              <!-- Modal footer -->
              <div
                class="flex items-center justify-center mx-4 py-4 px-2 border-t-2 border-gray-200"
              >
                <!--保存ボタン-->
                <div v-if="this.isCurrentUser()">
                  <input
                    type="submit"
                    v-on:click="editProfile"
                    value="変更を保存"
                    class="w-1/3 text-center px-14 py-2.5 mr-2 mb-2 text-lg font-medium bg-gray-200 text-gray-700 rounded-xl cursor-pointer sm:w-min hover:bg-teal-500 hover:text-gray-50"
                  />
                </div>

                <!-- <button
                  v-if="this.isCurrentUser()"
                  type="submit"
                  @click="editProfile"
                  class="w-1/3 text-white bg-gradient-to-r from-teal-400 via-teal-500 to-teal-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-teal-400 shadow-lg shadow-teal-500/70 font-medium rounded-full text-[17px] px-5 py-2.5 text-center mx-auto mb-3"
                >変更を保存</button>-->
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="flex flex-wrap">
        <!--左側カラム-->
        [[this.myRelationship.length||""]]
        <div class="w-4/12 z-0" v-on:scroll="onScroll">
          <div>
            <div class="h-max p-5 max-w-sm bg-white border-2 border-gray-200 rounded-lg shadow-lg">
              <!--気になるボタン-->
              <div v-if="this.isNullCurrentUser()" class="block text-right cursor-pointer"></div>
              <div v-else-if="!this.isCurrentUser()" class="block text-right cursor-pointer">
                <button
                  type="button"
                  :class="{
                  'text-gray-500 border border-gray-300 hover:bg-neutral-50 hover:text-teal-500 font-semibold rounded-lg text-base px-3 py-1.5 mb-1 text-center': !isFollowing(this.user),
                  'text-teal-500 border border-teal-500 hover:bg-neutral-50 hover:text-teal-500 font-semibold rounded-lg text-base px-3 py-1.5 mb-1 text-center': isFollowing(this.user)
                }"
                  @click="followUser(this.user)"
                >
                  <font-awesome-icon class="mr-1 mb-px" icon="star" size="lg" />気になる
                </button>
              </div>
              <!--アイコン画像-->
              <div class="flex flex-wrap justify-center items-center">
                <div class="flex w-28 h-28">
                  <img
                    class="object-cover aspect-square rounded-full overflow-hidden items-center z-0"
                    :src="this.user.icon"
                    alt="Rounded avatar"
                  />
                </div>
              </div>
              <div class="p-5">
                <!--ニックネーム-->
                <h4
                  class="mb-1 text-2xl font-bold tracking-tight text-gray-800"
                >[[user.nickname||""]]</h4>
                <!--本名-->
                <div class="flex justify-center">
                  <h5
                    class="mb-3 mr-2 text-xl font-bold tracking-tight text-gray-800"
                  >[[user.username||""]]</h5>
                  <!--アイコン表示（男性・女性の切り替え）-->
                  <div class="mt-px">
                    <!--男性アイコン-->
                    <font-awesome-icon
                      v-if="user.gender === 1"
                      icon="mars"
                      size="lg"
                      style="color: #608fe2;"
                    />
                    <!--女性アイコン-->
                    <font-awesome-icon
                      v-else-if="user.gender === 2"
                      icon="venus"
                      size="lg"
                      style="color: #e15183;"
                    />
                  </div>
                </div>
                <!--外部リンク-->
                <div class="flex justify-center gap-2 mb-3">
                <div v-if="user.github">
                  <a
                    :href=user.github
                  >
                    <img src="../../assets/img/github_icon.svg" width="30" height="30" />
                  </a>
                </div>
                <div v-if="user.twitter">
                  <a
                    :href=user.twitter
                  >
                    <img src="../../assets/img/x_icon.svg" width="30" height="30" />
                  </a>
                </div>
                <div v-if="user.instagram">
                  <a
                    :href=user.instagram
                  >
                    <img src="../../assets/img/instagram_icon.svg" width="30" height="30" />
                  </a>
                </div>
                <div v-if="user.facebook">
                  <a
                    :href=user.facebook
                  >
                    <img src="../../assets/img/facebook_icon.svg" width="30" height="30" />
                  </a>
                </div>
                <div v-if="user.pixiv">
                  <a
                    :href=user.pixiv
                  >
                    <img src="../../assets/img/pixiv_icon.png" width="30" height="30" />
                  </a>
                </div>
                </div>
                <div v-if="this.user.Profession === '学生'">
                  <div class="flex justify-center cursor-pointer">
                    <div class="mt-px mr-2">
                      <font-awesome-icon icon="school" />
                    </div>
                    <p
                      class="mb-3 text-lg font-normal text-gray-700 hover:underline"
                      @click="() => searchSchool(user.school.name)"
                    >[[user.school.name||"未登録"]]</p>
                  </div>
                  <div class="flex flex-wrap my-3">
                    <p class="w-4/12 font-normal text-gray-700 text-left">学部</p>
                    <p
                      class="w-8/12 pl-1 font-normal text-right text-gray-700"
                    >[[user.school.faculty||"未登録"]]</p>
                  </div>
                  <div class="flex flex-wrap my-3">
                    <p class="w-4/12 font-normal text-gray-700 text-left">学科</p>
                    <p
                      class="w-8/12 pl-1 font-normal text-right text-gray-700"
                    >[[user.school.department||"未登録"]]</p>
                  </div>
                  <div class="flex flex-wrap my-3">
                    <p class="w-4/12 font-normal text-gray-700 text-left">学年</p>
                    <p
                      class="w-8/12 pl-1 font-normal text-right text-gray-700"
                    >[[user.school.grade||"-"]]年生</p>
                  </div>
                  <div class="flex flex-wrap my-3">
                    <p class="w-4/12 font-normal text-gray-700 text-left">卒業年度</p>
                    <p
                      class="w-8/12 pl-1 font-normal text-right text-gray-700"
                    >[[user.school.graduation_year||" - "]]年</p>
                  </div>
                </div>
                <div class="my-3">
                  
                  <div v-if="user.introduction">
                    <p
                      class="text-left mt-1 font-normal text-gray-700 p-2"
                    >[[user.introduction||""]]</p>
                  </div>
                </div>
                <!--自分のプロフィール見たとき-->
                <div class="mt-5 text-center">
                  <div
                    v-if="this.isNullCurrentUser()"
                    class="class=w-3/4 rounded-full text-base px-5 py-2.5 text-center mr-2 mb-2"
                  ></div>
                  <div v-else-if="this.isCurrentUser()">
                    <input
                      type="button"
                      v-on:click="openModal"
                      value="プロフィールを編集する"
                      class="w-3/4 text-center px-5 py-2.5 mr-2 mb-2 text-lg font-medium bg-gray-200 text-gray-700 rounded-xl cursor-pointer sm:w-min hover:bg-teal-500 hover:text-gray-50"
                    />
                  </div>

                  <div v-else>
                    <div v-if="this.user.scout_receive == true">
                      <input
                        type="button"
                        v-on:click="emailpost"
                        value="連絡する"
                        class="w-3/4 text-center px-20 py-2.5 mr-2 mb-2 text-lg font-medium bg-gray-200 text-gray-700 rounded-xl cursor-pointer sm:w-min hover:bg-teal-500 hover:text-gray-50"
                      />
                    </div>
                    
                  </div>

                  <!-- <button
                    v-else-if="this.isCurrentUser()"
                    type="button"
                    @click="openModal"
                    class="w-3/4 text-white bg-gradient-to-r from-teal-400 via-teal-500 to-teal-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-teal-400 shadow-lg shadow-teal-500/70 font-medium rounded-full text-base px-5 py-2.5 text-center mr-2 mb-2"
                  >プロフィールを編集する</button>-->
                  <!--他人のプロフィール見たとき-->
                  <!-- <button
                    v-else
                    type="button"
                    @click="emailpost"
                    class="w-3/4 text-white bg-gradient-to-r from-teal-400 via-teal-500 to-teal-600 hover:bg-gradient-to-br focus:ring-4 focus:outline-none focus:ring-teal-400 shadow-lg shadow-teal-500/70 font-medium rounded-full text-base px-5 py-2.5 text-center mr-2 mb-2"
                  >連絡する</button>-->
                </div>
              </div>
            </div>

            <!--おすすめユーザー-->
            <div v-if="this.isNullCurrentUser()"></div>
            <div v-else-if="this.isCurrentUser()">
              <div
                class="h-max p-5 mt-4 max-w-sm bg-white border-2 border-gray-200 rounded-lg shadow-lg"
              >
                <p class="text-2xl font-bold">おすすめユーザー</p>
                <div v-for="recommend in recommendList" :key="recommend.id">
                  <div class="flex flex-wrap items-center gap-2 pt-4">
                    <router-link
                      :to="{ name: 'UserShow', params: { id: recommend.user_id.id } }"
                      class="flex gap-2"
                    >
                      <img
                        :src="recommend.user_id.icon"
                        loading="lazy"
                        class="flex w-16 h-16 object-cover aspect-square rounded-full overflow-hidden items-center z-0"
                      />
                      <div>
                        <!--ユーザー名-->
                        <p class="flex text-xl font-semibold">[[recommend.user_id.username||""]]</p>
                        <!--メールアドレス-->
                        <p class="flex text-sm">[[recommend.user_id.email||""]]</p>
                        <!--学校名-->
                        <div v-if="recommend.user_id.school">
                          <p class="flex">
                            <font-awesome-icon class="pr-1" icon="school" />[[recommend.user_id.school.name||""]]
                          </p>
                        </div>
                      </div>
                    </router-link>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!--右側カラム-->
        <div class="w-8/12 mt-44 px-5 z-0">
          <div class="text-base font-bold">
            <div class="flex flex-row tabs">
              <button
                class="border-2 border-gray-200 rounded-tl-lg"
                @click="changeTab('skill-check')"
                :class="{
                'tab basis-1/3 px-10 py-3 hover:text-teal-600 bg-white border-gray-200 border-b-4 border-b-teal-600 text-teal-600': selectedTab === 'skill-check',
                'tab basis-1/3 px-10 py-3 text-gray-700 hover:text-teal-600 bg-white border-t-2 border-b-2 border-gray-200': selectedTab !== 'skill-check'
              }"
              >スキルチェック</button>
              <button
                @click="changeTab('portfolio')"
                :class="{
                'tab basis-1/3 px-10 py-3 hover:text-teal-600 bg-white border-x-0 border-t-2 border-gray-200 border-b-4 border-b-teal-600 text-teal-600': selectedTab === 'portfolio',
                'tab basis-1/3 px-10 py-3 text-gray-700 hover:text-teal-600 bg-white border-t-2 border-b-2 border-gray-200': selectedTab !== 'portfolio'
              }"
              >ポートフォリオ</button>
              <button
                class="border-2 border-gray-200 rounded-tr-lg"
                @click="changeTab('favorites')"
                :class="{
                'tab basis-1/3 px-10 py-3 hover:text-teal-600 bg-white border-2 border-gray-200 border-b-4 border-b-teal-600 text-teal-600': selectedTab === 'favorites',
                'tab basis-1/3 px-10 py-3 text-gray-700 hover:text-teal-600 bg-white border-t-2 border-b-2 border-gray-200': selectedTab !== 'favorites'
              }"
              >お気に入り</button>
            </div>
            <div class="border-x-2 border-b-2 border-t bg-white border-gray-200 rounded-b-lg">
              <div class="bg-white rounded-lg">
                <!-- スキルチェック -->
                <div class="mx-2 mb-5" v-if="selectedTab === 'skill-check'">
                  <div class="text-gray-700 py-3">
                  問題の正解数を棒グラフ、回答した言語の割合を円グラフで表示します。
                </div>
                  <UserSkillCheck v-if="displayStatus" :user="user" />
                </div>
                <!--ポートフォリオ-->
                <div
                  v-else-if="selectedTab === 'portfolio'"
                  class="flex flex-wrap bg-white w-full rounded-b"
                >
                  <UserPortfolio v-if="displayStatus" :user="user" :currentuser="currentuser"></UserPortfolio>
                </div>
                <!-- お気に入り -->
                <div
                  v-else-if="selectedTab === 'favorites'"
                  class="flex flex-wrap bg-white w-full rounded-b"
                >
                  <UserLike v-if="displayStatus" :user="user" :currentuser="currentuser"></UserLike>
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
import settingMethods from "@/mixins/settingMethods";
import commonMethods from "@/mixins/commonMethods";
import searchMethods from "@/mixins/searchMethods";
import UserLike from "@/components/portfolio/exports/UserShowLike";
import UserPortfolio from "@/components/portfolio/exports/UserShowPortfolio";
import UserSkillCheck from "@/components/portfolio/exports/UserShowSkill";

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
  name: "UserShow",
  mixins: [settingMethods, commonMethods, searchMethods],
  props: {
    msg: String
  },
  components: {
    UserSkillCheck,
    UserLike,
    UserPortfolio
  },
  data() {
    return {
      currentuser: {
        id: null,
        email: ""
      },
      displayStatus: false,
      user: {
        id: null,
        username: "",
        nickname: "",
        icon: "",
        banner: "",
        email: "",
        Profession: "",
        introduction: "",
        gender: "",
        github: "",
        twitter: "",
        instagram: "",
        facebook: "",
        pixiv: "",
        followers: [],
        school: ""
      },
      editUser: {
        username: "",
        nickname: "",
        icon: "",
        banner: "",
        email: "",
        Profession: "",
        introduction: "",
        gender: "",
        github: "",
        twitter: "",
        instagram: "",
        facebook: "",
        pixiv: "",
        followers: [],
        school: null,
        scout_receive:"",
      },
      school: [],
      editSchool: {
        classification: "",
        name: "",
        faculty: "",
        department: "",
        grade: null,
        graduation_year: null
      },
      is_school: false,
      relationship: {
        follows: []
      },
      follows: {
        follows: []
      },
      selectedTab: "skill-check",
      selectedFavorite: "follow",
      currentUserPortfolios: [],
      like_list: {
        like_count: []
      },
      scout: {
        to_email: ""
      },
      showModal: false,
      isModalOpen: false,
      selectedIcon: null,
      lastSelectedIcon: null,
      selectedBanner: null,
      lastSelectedBanner: null,
      myRelationship: [],
      recommendList: []
    };
  },
  watch: {
    $route() {
      //リロード
      this.$router.go({ path: this.$router.currentRoute.path, force: true });
    },
    "currentuser.id": function() {
      this.getMyfollow();
    }
  },
  async created() {
    this.checkCookieExpiration();
    setInterval(this.checkCookieExpiration, 60000);
    if (this.$store.getters.isAuthenticated) {
      await this.getCurrentUser();
    }
    this.getUser();
  },
  mounted() {
    this.getfollow();
  },
  methods: {
    isFollowing(user) {
      if (this.myRelationship.follows) {
        for (let i = 0; i < this.myRelationship.follows.length; i++) {
          if (this.myRelationship.follows[i].id === user.id) {
            return true;
          }
        }
        return false;
      }
    },
    getUser() {
      axios
        .get(`/api/v1/index/${this.$route.params.id}`)
        .then(response => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
          this.user = response.data;
          this.displayStatus = true;
          this.editUser = { ...response.data };
          if (this.user.school === null) {
            this.user.school = {
              name: "",
              faculty: "",
              department: "",
              grade: "",
              graduation_year: "",
              introduction: ""
            };
          } else {
            this.editSchool = { ...response.data.school };
            this.is_school = true;
          }

          this.getRecommendUser();
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    getfollow() {
      axios
        .get(`/api/v1/FollowList/${this.$route.params.id}/`)
        .then(response => (this.relationship = response.data))
        .then(response => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    getMyfollow() {
      console.log("jjjjjjjjjjjj", this.currentuser.id);
      axios
        .get(`/api/v1/FollowList/${this.currentuser.id}/`)
        .then(response => {
          this.myRelationship = response.data;
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    followUser(user) {
      if (!this.$store.getters.isAuthenticated) {
        alert("ログインして下さい");
        this.$router.push({ name: "LoginForm" });
      }
      this.follows.follows = [user.id];
      console.log("aaaaa", user);
      axios
        .put(`/api/v1/Follow/${this.currentuser.id}/`, this.follows)
        .then(response => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
          this.getfollow();
          this.getMyfollow();
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    changeTab(tab) {
      this.selectedTab = tab;
    },
    changeFavorite(favoritetab) {
      this.selectedFavorite = favoritetab;
    },
    emailpost() {
      if (!this.$store.getters.isAuthenticated) {
        alert("ログインして下さい");
        this.$router.push({ name: "LoginForm" });
      }
      this.scout.to_email = this.user.email;
      axios
        .post("/api/v1/portfolio/email/", this.scout, {
          withCredentials: true,
          headers: {
            Authorization: "JWT " + this.$cookies.get("token")
          }
        })
        .then(response => {
          console.log("response", response.data);
          alert("スカウトメールを送信しました");
        })
        .catch(error => {
          console.log("error", this.scout);
          console.log("axiosGetErr", error);
          alert("メールの送信に失敗しました");
        });
    },
    openModal() {
      this.showModal = true;
      this.isModalOpen = true;
      document.body.classList.add("modal-open");
    },
    closeModal() {
      this.$router.go({ path: this.$router.currentRoute.path, force: true });
      this.showModal = false;
      this.isModalOpen = false;
      document.body.classList.remove("modal-open");
    },
    iconUploaded() {
      const file = this.$refs.iconpreview.files[0];
      if (!file) {
        return;
      }
      const extension = file.name.split(".").pop();
      const randomName = generateRandomString(20);
      const newFileName = `icon_${randomName}+.${extension}`;
      const formData = new FormData();
      formData.append("image", file, newFileName);
      axios
        .post("/api/v1/Icon/", formData)
        .then(response => {
          const imageUrl = response.data;
          // 画像削除処理
          this.selectedIcon = imageUrl;
          if (this.lastSelectedIcon) {
            this.deleteIconFromServer(this.lastSelectedIcon);
          }
          this.lastSelectedIcon = this.selectedIcon;
          this.editUser.icon = this.selectedIcon.image;
        })
        .catch(error => {
          console.error("Image upload error:", error);
        });
    },
    deleteIconFromServer(image) {
      axios
        .delete(`/api/v1/Icon/${image.id}/`)
        .then(() => {
          console.log("Image deleted successfully");
        })
        .catch(error => {
          console.error("Image deletion error:", error);
        });
    },
    bannerUploaded() {
      let file = this.$refs.preview.files[0];
      const banner_file = this.$refs.banner_preview.files[0];
      if (banner_file) {
        file = banner_file;
      }
      if (!file) {
        return;
      }
      // 画像が読み込まれた後に画像の幅を確認する
      const image = new Image();
      image.src = URL.createObjectURL(file);
      image.onload = () => {
        // 画像サイズの制限をかける（横幅の制限）
        const maxWidth = window.innerWidth * (3 / 4); // 画面幅の4分の3に制限

        if (image.width < maxWidth) {
          alert("画像が小さすぎます");
          return;
        }
        const extension = file.name.split(".").pop();
        const randomName = generateRandomString(20);
        const newFileName = `banner_${randomName}+.${extension}`;
        const formData = new FormData();
        formData.append("image", file, newFileName);
        axios
          .post("/api/v1/Banner/", formData)
          .then(response => {
            const imageUrl = response.data;
            // 画像削除処理
            this.selectedBanner = imageUrl;
            if (this.lastSelectedBanner) {
              this.deleteBannerFromServer(this.lastSelectedBanner);
            }
            this.lastSelectedBanner = this.selectedBanner;
            this.editUser.banner = this.selectedBanner.image;
            this.user.banner = this.selectedBanner.image;
            return this.editProfileSchool()
              .then(() => {
                return axios.put(
                  `/api/v1/post/${this.currentuser.id}/`,
                  this.editUser
                );
              })
              .then(response => {
                console.log("status:", response.status);
                console.log("axiosGetData:", response.data);
              });
          })
          .catch(error => {
            console.error("Image upload error:", error);
          });
      };
    },
    deleteBannerFromServer(image) {
      axios
        .delete(`/api/v1/Banner/${image.id}/`)
        .then(() => {
          console.log("Image deleted successfully");
        })
        .catch(error => {
          console.error("Image deletion error:", error);
        });
    },
    deleteBannerButton() {
      const image = this.user.banner;
      const trimmedImage = image.replace("/api/v1/media/", "");
      axios
        .get(`/api/v1/Banner/`, {
          params: {
            image: trimmedImage
          }
        })
        .then(response => {
          console.log("axiosGetData:", response.data);
          this.deleteBannerFromServer(response.data[0]);
          this.user.banner = null;
          this.editUser.banner = null;
          axios.put(`/api/v1/post/${this.currentuser.id}/`, this.editUser);
        })
        .catch(error => {
          console.error("Image deletion error:", error);
        });
    },
    editProfile() {
      return this.editProfileSchool()
        .then(() => {
          return axios.put(
            `/api/v1/post/${this.currentuser.id}/`,
            this.editUser
          );
        })
        .then(response => {
          console.log("status:", response.status);
          console.log("axiosGetData:", response.data);
          this.$store.commit("setIcon", this.editUser.icon);
          console.log('edit = ',this.editUser)
          this.closeModal();
        })
        .catch(err => {
          console.log("axiosGetErr", err);
        });
    },
    editProfileSchool() {
      console.log("editSchool", this.editSchool);
      if (!this.is_school && this.editUser.Profession === "学生") {
        return axios
          .post(`/api/v1/school/school/`, this.editSchool)
          .then(response => {
            this.editUser.school = response.data.id;
            console.log("status:", response.status);
            console.log("axiosGetData:", response.data);
          })
          .catch(err => {
            console.log("axiosGetErr", err);
          });
      } else if (this.is_school && this.editUser.Profession === "学生") {
        return axios
          .put(
            `/api/v1/school/school/${this.editUser.school.id}/`,
            this.editSchool
          )
          .then(response => {
            this.editUser.school = this.editUser.school.id;
            console.log("status:", response.status);
            console.log("axiosGetData:", response.data);
          })
          .catch(err => {
            console.log("axiosGetErr", err);
          });
      } else if (this.is_school && this.editUser.Profession !== "学生") {
        this.editUser.school = this.editUser.school.id;
        return Promise.resolve(); // 学生でない場合は空のPromiseを返す
      } else {
        this.editUser.school = null;
        return Promise.resolve(); // 学生でない場合は空のPromiseを返す
      }
    },
    getRecommendUser() {
      if (!this.isCurrentUser) {
        return;
      }
      axios
        .get("/api/v1/judge/recommend/", {
          withCredentials: true,
          headers: {
            Authorization: "JWT " + this.$cookies.get("token")
          }
        })
        .then(response => {
          this.recommendList = response.data;
          console.log("axiosGetData:", response.data);
        })
        .catch(error => {
          console.log("axiosGetErr", error);
        });
    },
    searchSchool(userSchool) {
      this.$root.searchSchoolUserKey(userSchool);
      this.$router.push({ name: "SchoolUser" });
    }
  }
};
</script>


<style scoped>
.image {
  position: relative;
  overflow: hidden;
  width: 100%;
  height: 300px;
  margin: auto;
}

.image img {
  display: block;
  position: absolute;
  width: inherit;
  height: inherit;
  object-fit: cover;
  top: 0;
}

body.modal-open {
  overflow: hidden;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  /* 背景の透明度を指定 */
  z-index: 9998;
  /* モーダルよりも一つ小さいZインデックスを指定 */
}
</style>