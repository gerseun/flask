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
            $.post(window.location.pathname, JSON.stringify(exp_arr), function(data, textStatus, xhr) {
            //console.log(data);
            $OUTPUT.html(data);
            //var arr = JSON.parse(data);
            //fill_tables(arr, $el);
            });
          }
        });
        console.log('Search added to:');
        console.log(el);
      }
    });
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

  function first_call() {
    var val = {};
    var name = 'firstCall';
    val[name] = page_class;
    console.log(val);
    $.post(window.location.pathname, JSON.stringify(val), function(data, textStatus, xhr) {
    //$('#output_text').text(JSON.stringify(data));
      console.log(data);
      $('output_text').html(data);
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
      $.post(window.location.pathname, JSON.stringify(exp_arr), function(data) {
        $('#output_text').html(data);
      }).fail(function() {
        console.log('Function: export, Error: database connection error');
      });
    }
  });
});
