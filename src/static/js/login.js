/*
Login. Guarda el idUsuario en una variable global. Comprueba que la contraseña y usuario correspondan a traves
de una llamada API
 */

function getUsuarios() {

  $.ajax({
    method: "GET",
    url: "/api/usuarios",
    dataType: "json",

    success: function (data) {

      console.log(data);
      doWork(data);
    },
    error: function(data) {
      alert("Ha habido un error!");

    }
  });

}

// Comprueba que existe dicho usuario y que su contraseña es correcta
function doWork(usuarios){
   var cnt = 0;
   console.log('llego');

  for(var i in usuarios){

    if(usuarios[i]['Usuario'] == $("#login").val()) {
        if (usuarios[i]['PSS'] == $("#password").val()) {
            // save user name
            localStorage.setItem("Usuario", $("#login").val());
            location.href = "/html/home";
            ctn=0;
            break;
        }
        else {
            alert("Contraseña incorrecta")
            $("#password").val("");
            cnt=0;
            break;
        }
    }
    cnt = i;
  }

  if(cnt == usuarios.length-1) {
          alert("Usuario incorrecto")
          $("#login").val("");
          $("#password").val("");
  }



}


$(document).ready(function() {
    $("#btnSubmit").click(function(){
		getUsuarios();
    });
});



$(function () {
  $('[data-toggle="popover"]').popover()
})
