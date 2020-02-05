var list_art = [];
var list_comp = [];
var list_imp = [];
var page_class = "";


$(document).ready(function() {
  page_class = $('.container').attr('id');

  function add_search($el, arr) {
    $el.each(function(index, el) {
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
            $OUTPUT.text(JSON.stringify(msg));
            //$.post(PHP_LINK, exp_arr, function(data, textStatus, xhr) {
            //console.log(data);
            //$OUTPUT.html(data);
            //var data2 = JSON.parse(data);
            //fill_tables(data2, $el);
          //});
          }
        });
        console.log('Search added');
      }
    });
  };

  function first_call() {
    var val = {};
    var name = 'firstCall';
    val[name] = page_class;

    $.post('/NuovoArticolo', val, function(data, textStatus, xhr) {
      $('#output_text').text(JSON.stringify(data));
    //var data = JSON.parse(test1);
    //$OUTPUT.html(JSON.stringify(data));
      //var arr = JSON.parse(data);
    if (data.hasOwnProperty('first_call')) {
      if (data['first_call'].hasOwnProperty('list_art')) {
        list_art = data['first_call']['list_art'];
        add_search($('.search_art'), list_art);
      }
      if (data['first_call'].hasOwnProperty('list_comp')) {
        list_comp = data['first_call']['list_comp'];
        add_search($('.search_comp'), list_comp);
      }
      if (data['first_call'].hasOwnProperty('list_imp')) {
        list_imp = data['first_call']['list_imp'];
        add_search($('.search_imp'), list_imp);
      }
    } else {
      console.log('Func: first_call, Error: json wrong structure');
    }
  },'JSON').fail(function() {
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

  function get_table($table) {
    var arr = [];
    var headers_id = [];
    var check = false;
    $table.find('th:not(.control)').each(function(index, el) {
      headers_id.push($(this).attr('id'));
    });

    $table.find('tr:not(:hidden)').each(function(index, el) {
      var $td = $(this).find('td');
      var val = {};
      check = headers_id.some(function(h, i) {
        var myval = "";
        var count = 0;

        //if ($td.eq(i).children('input').length) {
          //myval = $td.eq(i).children('input').val();
        //} else {
          myval = $td.eq(i).text();
        //}
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

  $('#export_btn').click(function(event) {
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

    if (!check) {
      exp_arr[page_class] = v_arr;
      //exp_arr[page_class] = JSON.stringify(v_arr);
      //$('#output_text').text(JSON.stringify(exp_arr));
      console.log(exp_arr);
      $.post('/NuovoArticolo', exp_arr, function(data) {
        $('#output_text').html(data);
      }).fail(function() {
        console.log('Function: export, Error: database connection error');
      });
    }
  });
});
