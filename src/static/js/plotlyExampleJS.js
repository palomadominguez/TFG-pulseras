var data = [{
  values: $('#counterValues').val().split(","),
    //values: Array.from($('#counterValues').val()),

  labels: ['Dormir', 'Andar', 'Correr', 'Estar de pie', 'Montar bicicleta', 'Nadar', 'Bailar',
      'Desplazarse con transporte publico', 'Estar sentado', 'Sensor en reposo', 'Gimnasia', 'On the go'],
  type: 'pie'
}];
console.log(data, $('#counterValues').val())
Plotly.newPlot('myDiv', data, {}, {showSendToCloud:true});

var data2 = [{
  x: ['Dormir', 'Andar', 'Correr', 'Estar de pie', 'Montar bicicleta', 'Nadar', 'Bailar',
      'Desplazarse con transporte publico', 'Estar sentado', 'Sensor en reposo', 'Gimnasia', 'On the go'],
  y: $('#counterValues').val(),
  type: 'bar'
}];

Plotly.newPlot('myDiv2', data2, {}, {showSendToCloud:true});