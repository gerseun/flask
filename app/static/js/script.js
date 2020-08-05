var list_art = [];
var list_comp = [];
var list_imp = [];
var page_class = "";


$(document).ready(function() {
  jQuery.fn.pop = [].pop;
  jQuery.fn.shift = [].shift;
  page_class = $('.container').attr('id');

  //funzione di ricerca automatica per Scadenze
  if(page_class == "scad"){
    var text = ""
    var send = {};
    send['pagina'] = $('.container').attr('id');
    send['azione'] = 'scaduti';
    send['messaggio'] = text;
    $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
      var arr = JSON.parse(data);
      $('.loader').hide();
      console.log(arr);
      fill_tables(arr['messaggio'], $('.container'));
    })
    .fail(function(){
      alert('Errore invio dati');
      location.reload();
    });
  }

  if(page_class == "newOrdine"){
    $('#input_field').focus();
    $('#input_field').focusout(function(event) {
      var text = $(this).val();
      if (text == '') {

      }else {
        var send = {};

        send['pagina'] = $('.container').attr('id');
        send['azione'] = 'azioneOrdine';
        send['messaggio'] = text;
        $('.loader').show();
        $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
          var arr = JSON.parse(data);
          console.log(arr);
          $('.loader').hide();
          fill_tables(arr['messaggio'], $('.container'));
        })
        .fail(function(){
          alert('Errore invio dati');
          location.reload();
        });
      }
    });
  }

  if(page_class == "newMagazzino"){
    $('#input_field').focus();
    $('#input_field').focusout(function(event) {
      var text = $(this).val();
      if (text == '') {

      }else {
        var send = {};

        send['pagina'] = $('.container').attr('id');
        send['azione'] = 'azioneMagazzino';
        send['messaggio'] = text;
        $('.loader').show();
        $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
          var arr = JSON.parse(data);
          $('.loader').hide();
          console.log(arr);
          fill_tables(arr['messaggio'], $('.container'));
        })
        .fail(function(){
          alert('Errore invio dati');
          location.reload();
        });
      }
    });
  }

  if(page_class == "PageAvanzamento" || page_class == "insManuale"){
    $('#input_field').focus();
    $('#input_field').focusout(function(event) {
      var text = $(this).val();
      if (text == '') {

      }else {

        $('.container .t_Avanzamento').find('tr').each(function(index, el) {
          if (index > 1) {
            el.remove();
            $('#dialog'+(index-1)+'').dialog( "destroy" );
          }
        });

        var send = {};

        send['pagina'] = $('.container').attr('id');
        send['azione'] = 'azioneAvanzamento';
        send['messaggio'] = text;
        $('.loader').show();
        $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
          $('.loader').hide();
          var arr = JSON.parse(data);
          console.log(arr);

          fill_tables(arr['messaggio'], $('.container'));

          $('.container .t_Avanzamento').eq(0).find('tr:not(:hidden)').each(function(index, el) {
            if (index > 0){
              $(this).addClass('dialog'+index+'');

              var send2 = {};
              send2['pagina'] = $('.container').attr('id');
              send2['azione'] = 'azioneAvanzamento2';
              send2['messaggio'] = $(this).find('.search_imp_av').text();

              $.post('/test', JSON.stringify(send2), function(data2, textStatus, xhr) {
                var arr2 = JSON.parse(data2);

                var $clone = $('#dialog_Avanzamento').clone(true, true).removeClass('hide');
                $clone.attr('id', 'dialog'+index+'');

                $t_art = $clone.find('.t_art');
                $t_art_rows = $t_art.find('tr');
                fill_row($t_art_rows.eq(1), arr2['messaggio']['t_art'][0]);

                $t_imp = $clone.find('.t_imp');
                $t_imp_rows = $t_imp.find('tr');
                fill_row($t_imp_rows.eq(1), arr2['messaggio']['t_imp'][0]);

                $t_comp = $clone.find('.t_comp');
                $t_comp_rows = $t_comp.find('tr');
                if ($t_comp_rows.length-2 < arr2['messaggio']['t_art'][0]['t_comp'].length) {
                  add_row($t_comp, arr2['messaggio']['t_art'][0]['t_comp'].length);
                }
                $t_comp.find('tr').each(function(index, el) {
                  if (index>1) {
                    if(page_class == "insManuale"){
                      fill_row($(this), arr2['messaggio']['t_art'][0]['t_comp'][index-2]);
                    }
                    else{
                      fill_row_avanzamento($(this), arr2['messaggio']['t_art'][0]['t_comp'][index-2]);
                    }
                  }
                });

                $clone.dialog({
                  autoOpen: false,
                  height: 'auto',
                  width:'auto',
                  resizable:false,
                  modal:true,
                  create: function(event,ui){
                    $('.container .t_Avanzamento').eq(0).find('tr:not(:hidden)').eq(index).find('.open-dialog').click(function(event) {
                      $('#dialog'+index+'').dialog( "open" );


                    });
                  },
                  buttons:{
                    'Salva': function() {
                      var arr = {};
                      var send = {};
                      arr["t_comp"] = get_table($(this).find('table.t_comp').eq(0));
                      arr["t_art"] = get_table($(this).find('table.t_art').eq(0));
                      arr["t_imp"] = get_table($('.container').find('table.t_imp').eq(0));

                      send['pagina'] = $('.container').attr('id');
                      send['azione'] = 'salva_file';
                      send['messaggio'] = arr;

                      if(page_class == "insManuale"){
                        console.log(send);
                        $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
                          console.log(data);
                        }).fail(function(){
                          alert('Errore invio dati');
                          location.reload();
                        });
                      }

                      $( this ).dialog( "close" );
                    }
                  }
                });
              }).fail(function(){
                alert('Errore invio dati');
                location.reload();
              });
            }
          });
        })
        .fail(function(){
          alert('Errore invio dati');
          location.reload();
        });
      }
    });
  }

  if(page_class == "newTaglio" || page_class == "newCarico" || page_class == "newProdIso"){

    $('#input_field').focus();
    $('#input_field').focusout(function(event) {
      var text = $(this).val();
      $(this).val('');
      if (text == '') {

      }else {
        //ricerco il prodotto da aggiungere
        var send = {};
        send['pagina'] = $('.container').attr('id');
        send['azione'] = 'azioneIsorella';
        send['messaggio'] = text;
        $('.loader').show();
        $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
          var arr = JSON.parse(data);
          //console.log(arr['messaggio']['t_compTaglio'][0]);
          if (arr['messaggio']){
            //qua deve aggiungere e compilare la tabella
            //aggiungo una riga alla tabella
            var $table = $('#tabella_isorella');
            add_row($table, 1);
            //compilo la riga
            var $rows = $table.find('tr:not(:hidden)'); //prendo tutte le righe
            console.log($rows);
            var $row = $rows.eq($rows.length-1)
            fill_row($row, arr['messaggio']['t_compIsorella'][0]);
            $('.loader').hide();
            $('#input_field').focus();
          }
        }).fail(function(){
          alert('Errore invio dati');
          location.reload();
        });
      }
    });
  }

  function add_row($table, n) {
    for (var i = 0; i < n; i++) {
      var $clone = $table.find('tr.hide').clone(true, true).removeClass('hide');
      $table.append($clone);
    }
    if ($('.container').attr('id') == 'listaTaglio') {
      //add_autocomp($table);
    } else {
      add_autocomp($('.container'));
    }
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
         if ($(this).attr('headers') == "id_produzione") {
           r_arr[$(this).attr('headers')] = $(this).find('select').val();
         } else {
           r_arr[$(this).attr('headers')] = $(this).text();
         }
       });
       t_arr.push(r_arr);
      }
    });
    return t_arr;
  };

  function check_array(arr){
    var bool = true
    var check_id = ['id_comp','id_art','id_imp','id_riga_art','id_riga_comp', 'id_riga_imp_comp','id_artcomp', 'id_riga_imp', 'grezzo', 'cod_ordine'];
    var check_data = ['data_ord','data_cons_art','data_cons_comp', 'scadenza'];
    var dataRGEX = /^(0?[1-9]|[12][0-9]|3[01])[\/](0?[1-9]|1[012])[\/\-]\d{4}$/;
    $.each(arr, function(index, el) {
      $.each(el, function(i, e) {
        if (!check_id.includes(i)) {
          if ((e == "") && (!check_data.includes(i))) {
            alert('Tutti i valori devono essere completi.\nTranne l\'ID');
            bool = false;
            return false;
          }else{
            if ((check_data.includes(i)) && !(e == "")) {
              if (!dataRGEX.test(e)) {
                alert('La data deve avere formato:\n01\/01\/2000');
                bool = false;
                return false;
              }
            }
          }
        }
      });
    });
    return bool;
  };

  function fill_row($row, arr) {
    //console.log(arr)
    $.each(arr, function(index, el) {
      var $cell = $row.find('td[headers*="'+index+'"]');
      if (index != "id_produzione") {
        $cell.text(el);
      } else {
        $cell.find('select').val(el);
      }
      if (['cod_imp', 'cod_comp', 'cod_art'].includes(index)) {
        $row.addClass(index);
      }
      if (['newImpegno','newArticolo','newComponente'].includes($('.container').attr('id'))) {
        if (['qt_comp', 'qt_art','data_cons_art','data_cons_comp', 'cod_ordine', 'scadenza'].includes(index)) {
          $cell.attr('contenteditable', 'true');
        }else {
          $cell.attr('contenteditable', 'false');
        }
      }
      else if (['newOrdine'].includes($('.container').attr('id'))) {
        if (['cod_ordine', 'scadenza'].includes(index)) {
          $cell.attr('contenteditable', 'true');
        }else {
          $cell.attr('contenteditable', 'false');
        }
      }
    });
  };

  function fill_row_avanzamento($row, arr) {

    var prod =  arr["id_produzione"];

    $.each(arr, function(index, el) {

      var $cell = $row.find('td[headers*="'+index+'"]');
      $cell.addClass('color_' + prod);

      if (index != "id_produzione") {
        $cell.text(el);
      } else {
        $cell.find('select').val(el);
      }

      if (['cod_imp', 'cod_comp', 'cod_art'].includes(index)) {
        $row.addClass(index);
      }
      if (['newImpegno','newArticolo','newComponente'].includes($('.container').attr('id'))) {
        if (['qt_comp', 'qt_art','data_cons_art','data_cons_comp', 'cod_ordine', 'scadenza'].includes(index)) {
          $cell.attr('contenteditable', 'true');
        }else {
          $cell.attr('contenteditable', 'false');
        }
      }
      else if (['newOrdine'].includes($('.container').attr('id'))) {
        if (['cod_ordine', 'scadenza'].includes(index)) {
          $cell.attr('contenteditable', 'true');
        }else {
          $cell.attr('contenteditable', 'false');
        }
      }
    });
  };

  function fill_tables(arr, $div){
    $.each(arr, function(t_ind, t_arr) {
      var $table = $div.find('.'+t_ind+'');
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

  function add_autocomp($div) {
    $div.find('.search_art, .search_comp, .search_imp').filter(':not(.ui-autocomplete-input)').each(function(index, el) {
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
            $('.loader').show();
            $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
              var arr = JSON.parse(data);
              //console.log(arr);
              if ($cell.attr('id') == 'first_cell') {
                fill_tables(arr['messaggio'], $('.container'));
              } else {
                fill_row($cell.parent('tr'), arr['messaggio'][$cell.parents('table').attr('class')][0]);
              }
              $('.loader').hide();
            })
            .fail(function(){
              alert('Errore autocompletamento');
            });
          }
        });
        console.log('Search added');
      }
    });
    $('.loader').hide();
    $('.container').show();
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
      if (data['pagina'] == 'listaTaglio') {
        add_autocomp_lt();
      } else {
        add_autocomp($('.container'));
      }
    })
    .fail(function() {
      alert('Errore importazione array autocompletamento');
    });
  };

  $('#export_btn').click(function(){
    var page_arr = {};
    var bool_arr = [];
    $('.container').find('table').each(function(index, el) {
      var t_arr = get_table($(this));
      if (check_array(t_arr)){
        page_arr[$(this).attr('class')] = t_arr;
        bool_arr[index] = true;
      }else {
        bool_arr[index] = false;
      }
    });
    if (!(bool_arr.includes(false))) {
      var send = {};
      send['pagina'] = $('.container').attr('id');
      send['azione'] = 'ins_nuovo';
      send['messaggio'] = page_arr;
      $('.loader').show();
      $('.container').hide();
      $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
        console.log(data);
        location.reload();
      })
      .fail(function(){
        alert('Errore invio dati');
        location.reload();
      });
    }
  });

  /*$('#downloadFile').click(function(){
    var page_arr = {};
    var bool_arr = [];
    $('.container').find('table').each(function(index, el) {
      var t_arr = get_table($(this));
      if (check_array(t_arr)){
        page_arr[$(this).attr('class')] = t_arr;
        bool_arr[index] = true;
      }else {
        bool_arr[index] = false;
      }
    });
    if (!(bool_arr.includes(false))) {
      var send = {};
      send['pagina'] = $('.container').attr('id');;
      send['azione'] = 'ins_nuovo';
      send['messaggio'] = page_arr;
      $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
        console.log(data);
      }).done(function(res){
        $("#tmpFrame").attr('src', 'URL-TO-EXCEL-FILE');
      });
    }
  });*/

  $('#test_btn').click(function(event) {
    var page_arr = {};
    var bool_arr = [];
    $('.container').find('table').each(function(index, el) {
      var t_arr = get_table($(this));
      if (check_array(t_arr)){
        page_arr[$(this).attr('class')] = t_arr;
        bool_arr[index] = true;
      }else {
        bool_arr[index] = false;
      }
    });
    if (!(bool_arr.includes(false))) {
      var send = {};
      send['pagina'] = $('.container').attr('id');
      send['azione'] = 'ins_nuovo';
      send['messaggio'] = page_arr;
      $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
        console.log(data);
        window.open('http://localhost:5000/cassone');
        //window.location('http://localhost:5000/cassone');
      });
    }
  });

  if (['newArticolo','newComponente','newImpegno', 'listaTaglio'].includes($('.container').attr('id'))) {
    first_call();
  }

  function create_dialog(i, r_row) {
    var send = {};
    var qt = "";
    send['pagina'] = $('.container').attr('id');
    send['azione'] = 'search_Produzione_Articolo';
    send['messaggio'] = r_row['id_riga_imp'];
    qt = r_row['qt_art'];

    $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
      var arr = JSON.parse(data);
      //console.log(arr);
      var $clone = $('#dialog0').clone(true, true).removeClass('hide');
      $clone.attr('id', 'dialog'+i+'');
      $t_art = $clone.find('.t_art');
      $t_art_rows = $t_art.find('tr');
      fill_row($t_art_rows.eq(1), r_row);
      $t_comp = $clone.find('.t_comp');
      $t_comp_rows = $t_comp.find('tr');
      if ($t_comp_rows.length-2 < arr['messaggio'].length) {
        add_row($t_comp, arr['messaggio'].length);
      }
      $t_comp.find('tr').each(function(index, el) {
        if (index>1) {
          fill_row($(this), arr['messaggio'][index-2]);
          $(this).find('td[headers*="qt_comp"]').each(function(index, el) {
            //if ($(this).text()=="") {
              //$(this).text(qt);
            //}else {
              $(this).attr('contenteditable', 'true');
              //$(this).text($(this).text()*qt);
            //}
          });
        }
      });
      $clone.dialog({
        autoOpen: false,
        height: 'auto',
        width:'auto',
        resizable:false,
        modal:true,
        create: function(event,ui){
          add_autocomp($(this));
          $('.container table').eq(1).find('tr:not(:hidden)').eq(i).find('.open-dialog').click(function(event) {
            $('#dialog'+i+'').dialog( "open" );
          });
        },
        buttons:{
          /*'Salva': function() {
            var arr = {};
            var send = {};
            arr["t_comp"] = get_table($(this).find('table.t_comp').eq(0));
            send['pagina'] = $('.container').attr('id');;
            send['azione'] = 'aggiorna_comp';
            send['messaggio'] = arr;
            $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
              console.log(data);
            });
            $( this ).dialog( "close" );
          },*/
          'Salva': function() {
            var arr = {};
            var send = {};
            arr["t_comp"] = get_table($(this).find('table.t_comp').eq(0));
            arr["t_art"] = get_table($(this).find('table.t_art').eq(0));
            arr["t_imp"] = get_table($('.container').find('table.t_imp').eq(0));

            send['pagina'] = $('.container').attr('id');
            send['azione'] = 'salva_file';
            send['messaggio'] = arr;
            $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
              console.log(data);
              $('.loader').hide();
            })
            .fail(function() {
              alert('Errore salvataggio lista taglio');
              location.reload();
            });
            $( this ).dialog( "close" );
            $('.loader').show();
          }
        }
      });
    })
    .fail(function() {
      alert('Errore invio lista taglio');
      location.reload();
    });
  };

  function add_autocomp_lt($el, arr) {
    $('.search_imp_lt:not(.ui-autocomplete-input)').each(function(index, el) {
      $cell = $(this);
      var arr = [];
      if (!($(this).parent('tr').hasClass('hide'))) {
        $cell.autocomplete({
          autoFocus: true,
          source: list_imp,
          minLength: 1,
          select: function(event, ui) {
            $cell = $(this);
            var send = {};
            send['pagina'] = $('.container').attr('id');;
            send['azione'] = $(this).attr('class').split(' ')[0];
            send['messaggio'] = ui.item.value;
            $('.loader').show();
            $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
              var arr = JSON.parse(data);
              //console.log(arr['messaggio']);
              var p_arr = {};
              p_arr['t_imp'] = arr['messaggio']['t_imp'];
              p_arr['t_art'] = arr['messaggio']['t_art'];
              p_arr['t_comp'] = arr['messaggio']['t_comp'];

              $('.container .t_art').find('tr').each(function(index, el) {
                if (index > 1) {
                  el.remove();
                  $('#dialog'+(index-1)+'').dialog( "destroy" );
                }
              });

              if ($cell.attr('id') == 'first_cell') {
                fill_tables(arr['messaggio'], $('.container'));
              } else {
                fill_row($cell.parent('tr'), arr['messaggio'][$cell.parents('table').attr('class')][0]);
              }

              $('.container .t_art').eq(0).find('tr:not(:hidden)').each(function(index, el) {
                if (index > 0){
                  $(this).addClass('dialog'+index+'');
                  create_dialog(index, arr['messaggio']['t_art'][index-1]);
                }
              });
              $('.loader').hide();
              /*
              if (arr['messaggio']['t_comp'].length > 0) {
                var $comp_dg = $('#dialog_comp').removeClass('hide');
                $comp_dg.dialog({
                  autoOpen: false,
                  height: 'auto',
                  width:'auto',
                  resizable:false,
                  modal:true,
                  create: function(event,ui){
                    $t_comp = $('#dialog_comp').find('.t_comp');
                    $t_comp_rows = $t_comp.find('tr');
                    if ($t_comp_rows.length-2 < arr['messaggio']['t_comp'].length) {
                      add_row($t_comp, arr['messaggio']['t_comp'].length);
                    }
                    $t_comp.find('tr').each(function(index, el) {
                      if (index>1) {
                        fill_row($(this), arr['messaggio']['t_comp'][index-2]);
                      }
                      $(this).find('td[headers*="qt_comp"]').attr('contenteditable', 'true');
                    });
                    $('.open-dialog-comp').click(function(event) {
                      $('#dialog_comp').dialog( "open" );
                    });
                  },
                  buttons:{
                    'Salva': function() {
                      var arr = {};
                      var send = {};
                      arr["t_comp"] = get_table($(this).find('table.t_comp').eq(0));
                      arr["t_imp"] = get_table($('.container').find('table.t_imp').eq(0));

                      send['pagina'] = $('.container').attr('id');
                      send['azione'] = 'salva_file_comp';
                      send['messaggio'] = arr;
                      console.log(send);
                      $.post('/test', JSON.stringify(send), function(data, textStatus, xhr) {
                        console.log(data);
                      });
                      $( this ).dialog( "close" );
                    }
                  }
                });
              }*/
            })
            .fail(function() {
              alert('Errore autocompletamento');
              location.reload();
            });
          }
        });
        console.log('Search added to: lt');
        $('.loader').hide();
        $('.container').show();
      }
    });
  };
});

/*
var today = new Date();
var dd = String(today.getDate()).padStart(2, '0');
var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
var yyyy = today.getFullYear();

today = mm + '/' + dd + '/' + yyyy;
document.write(today);
*/
