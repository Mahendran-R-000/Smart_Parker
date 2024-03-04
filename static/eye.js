function eyelistener(password,openEye) {

  if (openEye.getAttribute("class")==="far fa-eye-slash"){
  openEye.setAttribute("class","far fa-eye hide");
  password.setAttribute("type", "text");
  }
  else{openEye.setAttribute("class","far fa-eye-slash");
  password.setAttribute("type", "password");
}}