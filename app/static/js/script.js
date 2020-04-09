var list_art = [];
var list_comp = [];
var list_imp = [];
var page_class = "";


$(document).ready(function() {
  page_class = $('.container').attr('id');

  /*

  function fill_tables(data, $el) {
    if ($el.attr('id') == 'first_cell') {
      $('.container').find('table').each(function(index, el) {
        var table_name = $(this).attr('id');
        fill_table($(this), data[page_class][table_name]);
      });
    } else {
      var $row = $el.parent('tr');
      var $table = $el.parents('table');
      var table_name = $table.attr('id');
      console.log(data);
      console.log(data['search_comp']);
      console.log(data['search_comp'][table_name]);
      fill_row($row, data['search_comp'][table_name]);
    }
  };

  function fill_table($table, arr) {
    var table_name = $table.attr('class');
    var headers = get_tableHeaders($table);
    var $rows = $table.find('tr:not(:hidden)');
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

    $rows.each(function(index, el) { // Pass every row and add value to table
      var $td = $(this).find('td');
      headers.forEach(function(h, i) {
        if ($td.eq(i).children('input').length) {
          $td.eq(i).children('input').val(arr[index][h]);
        } else {
          $td.eq(i).text(arr[index][h]);
        }
        make_editable($td.eq(i), false,true);
      });
    });
  };

  function fill_row($row, arr) {

    var headers = get_tableHeaders($row);
    var $td = $row.find('td');
    headers.forEach(function(h, i) {

      console.log($td.eq(i));
      //if ($td.eq(i).children('input').length) {
        //$td.eq(i).children('input').val(arr[0][h]);
        //$td.eq(i).children('input').val(arr[h]);
      //} else {
        $td.eq(i).text(arr[h]);
      //}
      //make_editable($td.eq(i), false,false);
    });

  };

  function first_call() {
    var val = {};
    var name = 'firstCall';
    val[name] = page_class;
    console.log(val);
    $.post(window.location.pathname, JSON.stringify(val), function(data, textStatus, xhr) {
    //$('#output_text').text(JSON.stringify(data));
      //console.log(data);
      //$('output_text').html(data);
    //var data = JSON.parse(test1);
    //$OUTPUT.html(JSON.stringify(data));
      var arr = JSON.parse(data);

      if (arr.hasOwnProperty('firstCall')) {
        if (arr['firstCall'].hasOwnProperty('list_art')) {
          list_art = arr['firstCall']['list_art'];
          add_search($('.search_art'), list_art);
        }
        if (arr['firstCall'].hasOwnProperty('list_comp')) {
          list_comp = arr['firstCall']['list_comp'];
          add_search($('.search_comp'), list_comp);
        }
        if (arr['firstCall'].hasOwnProperty('list_imp')) {
          list_imp = arr['firstCall']['list_imp'];
          add_search($('.search_imp'), list_imp);
        }
      } else {
        console.log('Func: first_call, Error: json wrong structure');
      }
    }).fail(function() {
      console.log('Func: first_call, Error: server call fail');
    });
  };

  function add_row($table, n) {
    for (var i = 0; i < n; i++) {
      var $clone = $table.find('tr.hide').clone(true, true).removeClass('hide');
      $table.append($clone);
      //if (!$clone.find('input').hasClass('.hasDatepicker')) {
        //add_datepicker($clone.find('input'));
      //}
      var $first_cell = $clone.find('td').first();
      if ($first_cell.hasClass('search_art')) {
        add_search($first_cell, list_art);
      } else if ($first_cell.hasClass('search_comp')) {
        add_search($first_cell, list_comp);
      } else if ($first_cell.hasClass('search_imp')) {
        add_search($first_cell, list_imp);
      }
    }
  };



  $('#load_btn').click(function(event) {
    first_call();
  });

  $('.table-add').click(function() {
    var $parent_table = $(this).parents('table');
    add_row($parent_table, 1);
  });
  $('.table-remove').click(function(event) {
    $(this).parents('tr').detach();
  });

  if (!check) {

    //exp_arr[page_class] = JSON.stringify(v_arr);
    //$('#output_text').text(JSON.stringify(exp_arr));
    console.log(exp_arr);
    $.post(window.location.pathname, JSON.stringify(exp_arr), function(data) {
      $('#output_text').html(data);
    }).fail(function() {
      console.log('Function: export, Error: database connection error');
    });
  }


  */

  function get_table($table) {
    var arr = [];
    var headers_id = [];
    var check = false;
    headers_id = get_tableHeaders($table);
    $table.find('tr:not(:hidden)').each(function(index, el) {
      var $td = $(this).find('td');
      var val = {};
      check = headers_id.some(function(h, i) {
        var myval = "";
        myval = $td.eq(i).text();
        val[h] = myval;
        return (myval == "" && i != (headers_id.length - 1));
      });
      if (check) {
        return true;
      };
      arr.push(val);
    });
    if (check) {
      return true;
    }
    return (arr);
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
    var page = $('.container').attr('id');
    var action = 'ins_nuovo_articolo';
    var message = '';
    var answer = '';

    var exp_arr = {};
    var v_arr = {};
    var check = false;
    $('.container').find('table').each(function(index, el) {
      var val = get_table($(this));
      if (typeof val === 'boolean') {
        alert('Tutte i valori devono essere completi.\nTranne l\'ID');
        check = true;
        return;
      }
      v_arr[$(this).attr('id')] = val;
    });
    message = JSON.stringify(v_arr);

    var r = send_message(page, action, message, '/test');
    r.done(function(data){
      if ($.type(data) === "string") {
        console.log(data);
      } else {
        console.log('export: received message not a string');
      }
    });
  };

  function send_message(page, action, message, path){
    if ($.type(path) === 'undefined') {
        path = window.location.pathname;
    }
    var answer = '';
    var condition1 = $.type(page)==='string';
    var condition2 = $.type(action)==='string';
    var condition3 = $.type(message)==='string';
    var send = {};

    if (condition1 & condition2 & condition3) {
      send['page'] = page;
      send['action'] = action;
      send['message'] = message;

      var r = $.post(path, JSON.stringify(send))
      .fail(function() {
        console.log('send_message: sending failed');
      });
      return r;
    }else{
      console.log("send_message: not a string");
    }
    console.log('3 + ' + answer);
  };

  function request_list(){
    var page = $('.container').attr('id');
    var action = 'get_list_autocomp';
    var message = '';
    var answer = '';
    var r = send_message(page, action, message, '/test');
    r.done(function(data){
      if ($.type(data) === "string") {
        data = JSON.parse(data);
        if (data[action] == "get_list_autocomp") {
          arr = data[message];
          if (arr.hasOwnProperty('list_art')) {
            list_art = arr['list_art'];
            add_autocomp($('.search_art'), list_art);
          }
          if (arr.hasOwnProperty('list_comp')) {
            list_comp = arr['list_comp'];
            add_autocomp($('.search_comp'), list_comp);
          }
          if (arr.hasOwnProperty('list_imp')) {
            list_imp = arr['list_imp'];
            add_autocomp($('.search_imp'), list_imp);
          }
        }
      } else {
        console.log('export: received message not a string');
      }
    });
  };

  function add_autocomp($el, arr) {
    $el.each(function(index, el) {
      $element = $(this);
      if (!($(this).parent('tr').hasClass('hide'))) {
        $(this).autocomplete({
          autoFocus: true,
          source: arr,
          minLength: 1,
          select: function(event, ui) {
            var exp_arr = {};
            var msg = {};
            var val = ui.item.value;
            var el_class = $(this).attr('class').split(' ')[0];
            exp_arr[page_class + '_' + el_class] = val;
            $.post(window.location.pathname, JSON.stringify(exp_arr), function(data, textStatus, xhr) {
            //console.log(data);
            $('output_text').html(data);
            var arr = JSON.parse(data);
            fill_tables(arr, $element);
            });
          }
        });
        console.log('Search added to:');
      }
    });
  };

  $('#export_btn').click(export_tables);
  $('#load_btn').click(request_list);
});
