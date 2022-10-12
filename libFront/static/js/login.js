let login_title=document.querySelector('.login-title');
let register_title=document.querySelector('.register-title');
let login_box=document.querySelector('.login-box');
let register_box=document.querySelector('.register-box');

login_title.addEventListener('click',()=>{
    if(login_box.classList.contains('slide-up')){
        register_box.classList.add('slide-up');
        login_box.classList.remove('slide-up');
    }
})
register_title.addEventListener('click',()=>{
    if(register_box.classList.contains('slide-up')){
        login_box.classList.add('slide-up');
        register_box.classList.remove('slide-up');
    }
})

let login_button1=document.querySelector(".button1");
let login_button2=document.querySelector(".button2");
login_button1.addEventListener('click',()=>{
	if(login_button2.classList.contains('b')){
		login_button2.classList.remove('b');
		login_button1.classList.add('b');
	}
})
login_button2.addEventListener('click',()=>{
	if(login_button1.classList.contains('b')){
		login_button1.classList.remove('b');
		login_button2.classList.add('b');
	}
})
