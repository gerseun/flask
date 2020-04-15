var list_art = [];
var list_comp = [];
var list_imp = [];
var page_class = "";


$(document).ready(function() {
  jQuery.fn.pop = [].pop;
  jQuery.fn.shift = [].shift;
  page_class = $('.container').attr('id');

  function add_row($table, n) {
    for (var i = 0; i < n; i++) {
      var $clone = $table.find('tr.hide').clone(true, true).removeClass('hide');
      $table.append($clone);
    }
  };

  $('.table-add').click(function() {
    var $parent_table = $(this).parents('table');
    add_row($parent_table, 1);
  });

  $('.table-remove').click(function(event) {
    $(this).parents('tr').detach();
  });

  function get_table($table) {
    var t_arr = [];
    $table.find('tr:not(:hidden)').each(function(index, el) {
      if (index > 0) {
        var r_arr = {};
       $(this).find('td:not(.control)').each(function(index, el) {
         r_arr[$(this).attr('headers')] = $(this).text();
       });
       t_arr.push(r_arr);
      }
    });
    return t_arr;
  };

  function check_array(arr){
    var dataRGEX = /^(0?[1-9]|[12][0-9]|3[01])[\/](0?[1-9]|1[012])[\/\-]\d{4}$/;
    var bool = true;
    $.each(arr, function(index, el) {
      $.each(el, function(i, e) {
        if (!['id_comp','id_art','id_imp'].includes(i)) {
          if (e == ""){
            bool = false;
            alert('Tutti i valori devono essere completi.\nTranne l\'ID');
            return false;
          }
          if (['data_ord','data_cons_art','data_cons_comp'].includes(i)){
            if (!dataRGEX.test(e)) {
              bool = false;
              alert('La data deve avere formato:\n01\/01\/2000');
              return false;
            }
          }
        }
      });
      if (!bool) {
        return false
      }
    });
    return bool;
  };

  $('#export_btn').click(function(){
    var page_arr = {};
    $('.container').find('table').each(function(index, el) {
      var t_arr = get_table($(this));
      if (check_array(t_arr)){
        page_arr[$(this).attr('id')] = t_arr;
      } else {
        return false;
      }
    });
    console.log(page_arr);
  });

/*
  function fill_tables(data, $el) {
    if ($el.attr('id') == 'first_cell') {
        $('.container').find('table').each(function(index, el) {
          var table_name = $(this).attr('id');
          fill_table($(this), data[table_name]);
        });
    } else {
      var $row = $el.parent('tr');
      var $table = $el.parents('table');
      var table_name = $table.attr('id');
      fill_row($row, data[table_name]);
    }
  };

  function fill_table($table, arr) {
    var table_name = $table.attr('class');
    var headers = get_tableHeaders($table);
    var $rows = $table.find('tr:not(:hidden)');
    $rows.shift();
    if ($rows.length < arr.length) {
      add_row($table, arr.length - $rows.length); // Add rows is JSON has more
    } else {
      $rows.each(function(index, el) {
        if (index > arr.length - 1) { // Remove rows if JSON has more
          $(this).detach();
        }
      });
    }
    var $rows = $table.find('tr:not(:hidden)'); // Find rows
    $rows.shift();

    $rows.each(function(index, el) { // Pass every row and add value to table
      var $td = $(this).find('td');
      headers.forEach((h, i) => {
        if (arr[index].hasOwnProperty(h)) {
          $td.eq(i).text(arr[index][h]);
          $td.eq(i).attr('contenteditable', 'false');
        }
      });
    });
  };

  function fill_row($row, arr) {
    var headers = get_tableHeaders($row);
    var $td = $row.find('td');
    //console.log($td.eq(0));
    headers.forEach(function(h, i) {
      if (arr[0].hasOwnProperty(h)) {
        $td.eq(i).text(arr[0][h]);
        $td.eq(i).attr('contenteditable', 'false');
      }
    });
  };

  function get_table($table) {
    var arr = [];
    var headers = [];
    var check = false;
    headers = get_tableHeaders($table);
    $rows = $table.find('tr:not(:hidden)');
    $rows.shift();
    $rows.each(function(index, el) {
      var $td = $(this).find('td');
      var val = {};
      headers.forEach((item, i) => {
        myval = $td.eq(i).text();
        val[item] = myval;
      });
      arr.push(val);
    });
    return ([headers, arr]);
  };

  function check_array(headers, arr){
    var dataRGEX = /^(0?[1-9]|[12][0-9]|3[01])[\/](0?[1-9]|1[012])[\/\-]\d{4}$/;
    var check = true;
    headers.forEach((item, i) => {
      if (!['id_comp','id_art','id_imp'].includes(item)){
        var value = arr[0][item]
        if (value == ""){
          check = false;
          alert('Tutti i valori devono essere completi.\nTranne l\'ID');
          return false;
        }
        if (['data_ord','data_cons_art','data_cons_comp'].includes(item)){
          if (!dataRGEX.test(value)) {
            check = false;
            alert('La data deve avere formato:\n01\/01\/2000');
            return false;
          }
        }
      }
    });
    return check;
  };

  function get_tableHeaders($el) {
    var headers = [];
    if ($el.is('table')) {
      $el.find('th:not(.control)').each(function() { // Get table headers id
        headers.push($(this).attr('id'));
      });
    } else {
      var $table = $el.parents('table');
      $table.find('th:not(.control)').each(function() { // Get table headers id
        headers.push($(this).attr('id'));
      });
    }
    return headers;
  };

  function export_tables(){
    var pagina = $('.container').attr('id');
    var azione = 'ins_nuovo';
    var path = '/test'
    var exp_arr = {};
    var v_arr = {};
    var check = true;
    $('.container').find('table').each(function(index, el) {
      var val = get_table($(this));
      if (val[1].length > 0) {
        if (check_array(val[0],val[1])) {
          v_arr[$(this).attr('id')] = val[1];
        }else{
          check = false;
          return false;
        }
      }
    });
    if (check) {
      var messaggio = v_arr;
      var send = {};
      send['pagina'] = pagina;
      send['azione'] = azione;
      send['messaggio'] = messaggio;
      $.post(path, JSON.stringify(send), function(data, textStatus, xhr) {
        console.log(data);
      });
    }
  };

  function send_message(pagina, azione, messaggio, path){
    if ($.type(path) === 'undefined') {
        path = window.location.pathname;
    }
    var answer = '';
    var send = {};
    send['pagina'] = pagina;
    send['azione'] = azione;
    send['messaggio'] = messaggio;

    var r = $.post(path, JSON.stringify(send))
      .fail(function() {
        console.log('send_message: sending failed');
      });
    return r;
  };

  function request_list(){
    var pagina = $('.container').attr('id');
    var azione = 'first_call';
    var messaggio = '';
    var path = '/test';
    var send = {};
    send['pagina'] = pagina;
    send['azione'] = azione;
    send['messaggio'] = messaggio;
    $.post(path, JSON.stringify(send), function(data, textStatus, xhr) {
      data = JSON.parse(data);
      if (data['azione'] == "first_call") {
        var arr = data['messaggio'];
        if (arr.hasOwnProperty('list_art')) {
          list_art = arr['list_art'];
          add_autocomp($('.search_art:not(:hidden)'), list_art);
        }
        if (arr.hasOwnProperty('list_comp')) {
          list_comp = arr['list_comp'];
          add_autocomp($('.search_comp:not(:hidden)'), list_comp);
        }
        if (arr.hasOwnProperty('list_imp')) {
          list_imp = arr['list_imp'];
          add_autocomp($('.search_imp:not(:hidden)'), list_imp);
        }
      }
    });
  };

  function add_autocomp($el, arr) {
    $el.each(function(index, el) {
      if (!($(this).parent('tr').hasClass('hide'))) {
        $(this).autocomplete({
          autoFocus: true,
          source: arr,
          minLength: 1,
          select: function(event, ui) {
            $element = this;
            var val = ui.item.value;
            var pagina = $('.container').attr('id');
            var azione = $(this).attr('class').split(' ')[0];
            var messaggio = val;
            var path = '/test';
            var send = {};
            send['pagina'] = pagina;
            send['azione'] = azione;
            send['messaggio'] = messaggio;
            $.post(path, JSON.stringify(send), function(data, textStatus, xhr) {
              var arr = JSON.parse(data);
              fill_tables(arr['messaggio'], $el);
            });
          }
        });
        console.log('Search added to:');
      }
    });
  };

  function add_row($table, n) {
    for (var i = 0; i < n; i++) {
      var $clone = $table.find('tr.hide').clone(true, true).removeClass('hide');
      $table.append($clone);
      var $first_cell = $clone.find('td').first();
      if ($first_cell.hasClass('search_art')) {
        add_autocomp($first_cell, list_art);
      } else if ($first_cell.hasClass('search_comp')) {
        add_autocomp($first_cell, list_comp);
      } else if ($first_cell.hasClass('search_imp')) {
        add_autocomp($first_cell, list_imp);
      }
    }
  };

  function request_list_lt(){
    var pagina = $('.container').attr('id');
    var azione = 'first_call';
    var messaggio = '';
    var path = '/test';
    var send = {};
    send['pagina'] = pagina;
    send['azione'] = azione;
    send['messaggio'] = messaggio;
    $.post(path, JSON.stringify(send), function(data, textStatus, xhr) {
      data = JSON.parse(data);
      if (data['azione'] == "first_call") {
        var arr = data['messaggio'];
        if (arr.hasOwnProperty('list_art')) {
          list_art = arr['list_art'];
        }
        if (arr.hasOwnProperty('list_comp')) {
          list_comp = arr['list_comp'];
        }
        if (arr.hasOwnProperty('list_imp')) {
          list_imp = arr['list_imp'];
          add_autocomp_lt($('.search_imp:not(:hidden)'), list_imp);
        }
      }
    });
  };

  function add_autocomp_lt($el, arr) {
    $el.each(function(index, el) {
      if (!($(this).parent('tr').hasClass('hide'))) {
        $(this).autocomplete({
          autoFocus: true,
          source: arr,
          minLength: 1,
          select: function(event, ui) {
            $element = this;
            var val = ui.item.value;
            var pagina = $('.container').attr('id');
            var azione = $(this).attr('class').split(' ')[0];
            var messaggio = val;
            var path = '/test';
            var send = {};
            send['pagina'] = pagina;
            send['azione'] = azione;
            send['messaggio'] = messaggio;
            $.post(path, JSON.stringify(send), function(data, textStatus, xhr) {
              var arr = JSON.parse(data);
              console.log(data);
            });
          }
        });
        console.log('Search added to: lt');
      }
    });
  };

  $('#load_btn').click(request_list);

  if (['newArticolo','newComponente','newImpegno'].includes($('.container').attr('id'))) {
    request_list();
    $('#export_btn').click(export_tables);
    $('.table-add').click(function() {
      var $parent_table = $(this).parents('table');
      add_row($parent_table, 1);
    });

    $('.table-remove').click(function(event) {
      $(this).parents('tr').detach();
    });
  }

  if (['listaTaglio'].includes($('.container').attr('id'))){
    request_list_lt();
    $('.table-add').click(function() {
      var $parent_table = $(this).parents('table');
      var $clone = $parent_table.find('tr.hide').clone(true, true).removeClass('hide');
      $parent_table.append($clone);
    });
    $('.table-remove').click(function(event) {
      $(this).parents('tr').detach();
    });

    dialog_box = $('#dialog').dialog({
      autoOpen: false,
      height:'auto',
      width:'auto',
      resizable:false,
      modal:true,
      buttons:{
        'Salva': function() {
          $( this ).dialog( "close" );
        },
        'Stampa': function() {
          $( this ).dialog( "close" );
        }
      }
    });
    $('#test_btn').click(function(event) {
      //$('#dialog').attr('hidden', 'false');
      dialog_box.dialog( "open" );
    });
  }*/
});
