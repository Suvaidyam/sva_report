import{e as m,l as d,A as e,B as n,J as o,k as p,m as u,u as f,ac as l,P as _,O as w}from"./index-B8JMEHnM.js";const g={class:"m-3 flex flex-row items-center justify-center"},B=m({__name:"Login",setup(x){function r(a){let t=new FormData(a.target);l.login.submit({email:t.get("email"),password:t.get("password")})}return(a,t)=>{const s=o("Input"),i=o("Button"),c=o("Card");return p(),d("div",g,[e(c,{title:"Login to your FrappeUI App!",class:"w-full max-w-md mt-4"},{default:n(()=>[u("form",{class:"flex flex-col space-y-2 w-full",onSubmit:w(r,["prevent"])},[e(s,{required:"",name:"email",type:"text",placeholder:"johndoe@email.com",label:"User ID"}),e(s,{required:"",name:"password",type:"password",placeholder:"••••••",label:"Password"}),e(i,{loading:f(l).login.loading,variant:"solid"},{default:n(()=>[_("Login")]),_:1},8,["loading"])],32)]),_:1})])}}});export{B as default};
