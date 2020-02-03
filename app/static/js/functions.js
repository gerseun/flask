$('#export_btn').click(function(event) {
  var arr = {};
  var name = 'asd';
  arr[name] = 'ciao';
  var json = {};
  json['new'] = JSON.stringify(arr);;
  //var json = JSON.parse(arr);
  //var obj = { name: "John", age: 30, city: "New York" };
  //var myJSON = JSON.stringify(obj);
  //$('#output_text').html(JSON.stringify(data));
  $.post('/NuovoArticolo', json, function(data, textStatus, xhr) {
    $('#output_text').html(data);
  });
});
