<template>
    <div id="container">
        <form id="loginForm" action="">
            <h2>注册</h2>
            <div class="input">
                <input type="text" placeholder="User Name or E-mail" id="account" v-model="account">
            </div>
            <div class="input">
                <input type="password" placeholder="Password" id="userPassword" v-model="password">
            </div>
            <div id="action">
                <span><router-link to="/login">返回登陆</router-link></span>
            </div>
            <div id="loginButton">
                <button class="login-button" id="btnLogin" @click.prevent="onBtnLoginClick">注册</button>
            </div>
        </form>
    </div>
</template>
<script>
import axios from 'axios';
const BACKEND_PATH = import.meta.env.VITE_BACKEND_PATH;
console.log(BACKEND_PATH);
export default {
    name: 'register',
    data() {
        return {
            account: '',
            password: '',
        };
    },
    methods: {
        async onBtnLoginClick() {
            try {
                const response = await axios.post(BACKEND_PATH+'/register', {
                    username: this.account,
                    password: this.password
                });
                if(response.data.error){
                    alert('注册失败: 用户名已存在');
                    return;
                }
                else{
                    alert('注册成功');
                }
                
                this.$router.push({ name: 'login' });
            } catch (error) {
                if (error.response && error.response.data.error) {
                    alert(`注册失败: ${error.response.data.error}`);
                } else {
                    alert('注册失败: 发生未知错误');
                }
            }
        }
    }
};
</script>
<style scoped>
    #container{
    height:70%;
    width:63%;
    position: absolute;
    left:50%;
    top:50%;
    transform: translateX(-50%) translateY(-50%);
    min-width: 315px;
    min-height: 453px;
    max-width: 670px;
    max-height: 496px;
}
form{
    border:1px solid #a9a9a9;
    border-radius: 12px;
    height:90%;
    top: 50%;
    font-family: "Gill Sans", sans-serif;
    box-shadow: 0 16px 32px rgba(0, 0, 0, 0.1);
    padding: 20px;
}
h2{
    text-align: center;
    font-size: 30px;
    margin-bottom: 60px;
}
.input{
    position: relative;
    font-size: 40px;
    height:50px;
    margin-left: 10%;
    margin-right: 10%;
    margin-bottom: 40px;
}
input[type="password"]{
    font-family: "Gill Sans", sans-serif;
    font-size: 20px;
    height:99%;
    width: 96%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    padding-left: 3%;
    border: 0.5px solid #6e7275;
    
}
#account{
    font-family: "Gill Sans", sans-serif;
    font-size: 20px;
    height:99%;
    width: 96%;
    place-self: center;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
    padding-left: 3%;
    border: 0.5px solid #6e7275;
}
#action{
    margin-left: 10%;
    margin-right: 10%;
    display: flex;
    justify-content:space-between;
}
#loginButton{
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50px;
    margin-top: 20px;
}
#redirectInfo{
    color: red;
    margin-left: 10%;
    display: none;
}
.login-button{
    padding: 10px 20px;
    background-color: #1878de; 
    color: #fff; 
    border: none;
    border-radius: 5px;
    font-size: 16px;
    cursor: pointer;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>