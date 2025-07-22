export default {
  methods: {
    validateRequired(value, errorMessage) {
      if (!value) {
        throw new Error(errorMessage);
      }
    },
    validateContext(text){
      if(text.length > 20001){
        throw new Error('本文を20000文字以下にしてください。');
      }
    },
    validateEmailFormat(email) {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(email)) {
        throw new Error('正しいメールアドレスの形式ではありません。');
      }
    },
    validatePasswordMatch(password, confirmPassword) {
      if (password !== confirmPassword) {
        throw new Error('パスワードが一致しません。');
      }
    },
    validatePasswordLength(password) {
      if (password.length < 6) {
        throw new Error('パスワードは6文字以上で入力してください。');
      }
    },
    validatePasswordFormat(password) { //使ってない
      const passwordRegex = /^(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[0-9])/;
      if (!passwordRegex.test(password)) {
        throw new Error('パスワードは少なくとも1つの大文字、1つの小文字、1つの数字を含む必要があります。');
      }
      if(password.match(/[^A-Za-z0-9]+/)){
        throw new Error('パスワードは英数字のみにしてください。');
      }
    },
  },
};