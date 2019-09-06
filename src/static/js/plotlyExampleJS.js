var data = [{
  values: $('#counterValues').val(),
  labels: ['Andando', 'Corriendo', 'Nadando', 'Sentado', 'Tumbado', 'Spinning', 'Subir Escaleras'],
  type: 'pie'
}];

Plotly.newPlot('myDiv', data, {}, {showSendToCloud:true});

var data2 = [{
  x: ['Andando', 'Corriendo', 'Nadando', 'Sentado', 'Tumbado', 'Spinning', 'Subir Escaleras'],
  y: $('#counterValues').val(),
  type: 'bar'
}];

Plotly.newPlot('myDiv2', data2, {}, {showSendToCloud:true});