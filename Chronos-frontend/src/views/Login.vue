<template>
    <div id="container">
        <form id="loginForm" action="">
            <h2>登陆您的账号</h2>
            <div class="input">
                <input type="text" placeholder="User Name or E-mail" id="account" v-model="account">
            </div>
            <div class="input">
                <input type="password" placeholder="Password" id="userPassword" v-model="password">
            </div>
            <div id="action">
                <span><router-link to="/signup">注册账号</router-link></span>
            </div>
            <div id="loginButton">
                <button class="login-button" id="btnLogin" @click.prevent="onBtnLoginClick">登陆</button>
            </div>
        </form>
    </div>
</template>
<script>
import router from '@/router';
import axios from 'axios';
    const BACKEND_PATH = import.meta.env.VITE_BACKEND_PATH;
    console.log(BACKEND_PATH);
    export default {
        name: 'login',
        
        data(){
            return {
                account: '',
                password: '',
                
            }
        },
        methods:{
            onBtnLoginClick(){
                let isSuccess = false;
                axios.get(BACKEND_PATH+'/login?username=' + this.account + '&password=' + this.password)
                .then(response => {
                    if (response.data.length > 0) {
                        const userInfo = response.data[0];
                        sessionStorage.setItem("uuid", userInfo.uuid);
                        sessionStorage.setItem("accessToken", userInfo.accessToken);
                        sessionStorage.setItem("isLoggedIn", true);
                        alert("登录成功！");
                        router.push({ path: '/' }).then(() => router.go(0));;
                    } else {
                        // Handle the case where the array is empty
                        alert("登录失败：用户不存在或密码错误");
                    }
                    isSuccess = true;
                })
                .catch(error => console.error('Error fetching token:', error));
            }
        }
        
    }
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
    min-height: 479px;
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