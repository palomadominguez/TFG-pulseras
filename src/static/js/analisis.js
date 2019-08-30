updateInforme()

// function to call XHR and update county dropdown
function updateInforme() {

    var paciente_ =  String($('#idPaciente').val())
    var paciente = paciente_.substring(0, paciente_.length - 2);

    $.ajax({
        method: "GET",
        url: "/api/informes/" + paciente,
        dataType: "json",
        success: function (data) {
          console.log(data);
        $('#idInforme')[0].options.length = 0;
            console.log('problema');
          for (var i in data) {
              var id = data[i]['_idInforme'];
              console.log('llego');
              console.log(i);
              console.log(id);
              $('#idInforme').append(new Option(id, id));
            }
        },
        error: function(data) {
          alert("Ha habido un error!" + paciente);

        }
      });
}

$('#idPaciente').change(function() {
    updateInforme()
});

