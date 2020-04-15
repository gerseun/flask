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
    add_autocomp();
  };

  $('.table-add').click(function() {
    var $table = $(this).parents('table');
    add_row($table, 1);
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
    var arr_id = ['id_comp','id_art','id_imp','id_riga_art','id_riga_comp'];
    var bool = true;
    $.each(arr, function(index, el) {
      $.each(el, function(i, e) {
        if (!arr_id.includes(i)) {
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

  function fill_row($row, arr) {
    $.each(arr, function(index, el) {
      var $cell = $row.find('td[headers="'+index+'"]');
      $cell.text(el);
      $cell.attr('contenteditable', 'false');
    });
  };

  function fill_tables(arr){
    $.each(arr, function(t_ind, t_arr) {
      var $table = $('.container').find('#'+t_ind+'');
      var $rows = $table.find('tr:not(:hidden)');
      if ($rows.length-1 < t_arr.length) {
        add_row($table, t_arr.length-($rows.length-1));
      } else {
        $rows.each(function(index, el) {
          if (index > t_arr.length) {
            $(this).detach();
          }
        });
      }
      $table.find('tr:not(:hidden)').each(function(index, el) {
        if (index > 0) {
          fill_row($(this), t_arr[index-1]);
        }
      });
    });
  };

  function add_autocomp() {
    $('.search_art:not(.ui-autocomplete-input), .search_comp:not(.ui-autocomplete-input), .search_imp:not(.ui-autocomplete-input)').each(function(index, el) {
      $cell = $(this);
      var arr = [];
      if ($(this).hasClass('search_art')) {
        arr = list_art;
      }
      if ($(this).hasClass('search_comp')) {
        arr = list_comp;
      }
      if ($(this).hasClass('search_imp')) {
        arr = list_imp;
      }
      if (!($(this).parent('tr').hasClass('hide'))) {
        $cell.autocomplete({
          autoFocus: true,
          source: arr,
          minLength: 1,
          select: function(event, ui) {
            $cell = $(this);
            var send = {};
            send['pagina'] = $('.container').attr('id');;
            send['azione'] = $(this).attr('class').split(' ')[0];
            send['messaggio'] = ui.item.value;
            $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
              var arr = JSON.parse(data);
              //console.log(arr);
              if ($cell.attr('id') == 'first_cell') {
                fill_tables(arr['messaggio']);
              } else {
                fill_row($cell.parent('tr'), arr['messaggio'][$cell.parents('table').attr('id')][0]);
              }
            });
          }
        });
        console.log('Search added to:');
      }
    });
  };

  function first_call(){
    var send = {};
    send['pagina'] = $('.container').attr('id');
    send['azione'] = 'first_call';
    send['messaggio'] = '';
    $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
      data = JSON.parse(data);
      list_art = data['messaggio']['list_art'];
      list_comp = data['messaggio']['list_comp'];
      list_imp = data['messaggio']['list_imp'];
      add_autocomp();
    });
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
    var send = {};
    send['pagina'] = $('.container').attr('id');;
    send['azione'] = 'ins_nuovo';
    send['messaggio'] = page_arr;
    $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
      console.log(data);
    });
  });

  first_call();

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

  $('#load_btn').click();
/*
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
*/
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
  }
});
