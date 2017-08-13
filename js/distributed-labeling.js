/**
 * distributed-labeling.js
 * Library of JavaScript functions for distributed labeling.
 */
var expert_mode;

$('#user_button').click(function () {
    expert_mode = false;
});

$('#expert_button').click(function () {
    expert_mode = true;
});

$('#save_table_button').click(function () {
    var strSelectedLabels = "";
    $('#data_table').find("input:checked").each(function () {
        if (strSelectedLabels != "")
            strSelectedLabels += "," + $(this).attr("value");
        else
            strSelectedLabels += $(this).attr("value");
    });
    if (strSelectedLabels.length == 0) {
        bootbox.alert('No data is available to save');
        return;
    }
    //alert(strSelectedLabels);
    $.ajax({
        url:'save_table.py',
        type: 'POST',
        data: {'checked_options':strSelectedLabels},
        success: function(result) {
            //console.log('save_table_result');
            //console.log(result);
            //alert(result);
            result = jQuery.parseJSON(result);
            //alert(result.Time)
            bootbox.alert('Data successfully saved !!!');
            $("#message").html("In this session, data last saved at " + result.Time);
            js_get_summary_fn()
            $('#view_label_types').find('input:checkbox').removeAttr('checked');
            }, 
        error: function(jqXHR, textstatus, errorthrown) {
            alert(errorthrown)
        }
    });
});
$('#view_lt_button').click(function () {
    var strSelectedIds = "";
    $('#view_label_types').find("input:checked").each(function () {
        if (strSelectedIds != "")
            strSelectedIds += "," + $(this).attr("id");
        else
            strSelectedIds += $(this).attr("id");
    });
    if (strSelectedIds.length == 0) {
        bootbox.alert('Select at least one label type');
        return
    }
    //alert(strSelectedIds);
    $.ajax({
        url: 'view_labels.py',
        type: 'POST',
        data: {'checked_options': strSelectedIds}, // An object with the key 'submit' and value 'true;
        success: function (result) {
            fill_table_data(result);
            $('.mur_class').remove();
            js_paginate_data_table();
        }
    });
});
$('#update_summary_button').click(function () {
    js_get_summary_fn();
});
function js_save_table_fn() {
    $.ajax({
        url: 'save_table.py',
        type: 'POST',
        data: {'checked_labels': strSelectedLabels}, // An object with the key 'submit' and value 'true;
        success: function (result) {
            console.log(result);
            alert(result);
            //result = jQuery.parseJSON(result);
            bootbox.alert('Data successfully saved !!!');
            //$("#message").html("In this session, data last saved at " + result.Time);
            js_get_summary_fn();
            $('#view_label_types').find('input:checkbox').removeAttr('checked');
            },
         error: function (jqXHR, textStatus, errorThrown) {
            //callbackfn("Error getting the data")
            alert(errorThrown)
        }
    });
}
function js_get_summary_fn() {
    $.ajax({
        url: 'get_expert_summary.py',
        type: 'GET',
        success: function (results) {
            results = jQuery.parseJSON(results);
            var trHTML = '';
            var fooresults = results.foo;
            trHTML = '<thead> <tr>';
            trHTML += '<th> Label Type</th> <th> Num. </th>';
            trHTML += '</thead>'
            $.each(fooresults, function (i, item) {
                trHTML += '<tr>';
                trHTML += '<td>' + item.label + '</td>';
                trHTML += '<td>' + item.value + '</td>';
                trHTML += '<tr>'
            });
            $('#records_table').html(trHTML);
        }
    });
}
function js_get_modal_info() {
    $.ajax({
        url: 'get_modal_info.py',
        type: 'GET',
        success: function (results) {
            results = jQuery.parseJSON(results);
            var trHTML = '';
            var inHtml = results.modal_data;
            $('#table-model-contents').html(inHtml);
        }
    });
}
$(document).ready(function () {
    // //{#    alert('Going to...')#}
    js_get_summary_fn();
    // //{#        js_get_modal_info();#}
    // //{# Get table #}
    $.ajax({
        url: 'get_table.py',
        type: 'GET',
        success: function (results) {
            fill_table_data(results);
        }
    });
    // //{#        setTimeout(myFunction, 3000);#}
    setTimeout(function () {
        $(document).trigger('afterready');
    }, 1500);
}); // document ready closing
$(document).bind('afterready', function () {
    // //{#        alert('Calling pagination')#}
    // call your code here that you want to run after all $(document).ready() calls have run
    js_paginate_data_table();
});
function js_paginate_data_table() {
    $("#data_table").simplePagination({
        perPage: 20,
        // CSS classes to custom the pagination
        containerClass: 'mur_class',
        previousButtonClass: 'btn btn-primary btn-sm',
        nextButtonClass: 'btn btn-primary btn-sm',
// text for next and prev buttons
        previousButtonText: 'Previous',
        nextButtonText: 'Next',
// initial page
        currentPage: 1
    });
}
function fill_table_data(result) {
    results = jQuery.parseJSON(result);
    //{#  Fill header #}
    var thHtml = '';
    var header = results.columns;
    //{#            alert(header)#}
    thHtml = '<thead> <tr>';
    $.each(header, function (i, item) {
        if (item != results['label']) {
            thHtml += '<th>' + item + '</th>'
        }
    });
    thHtml += ' </tr> </thead>';
    //{#            alert(thHtml);#}
    var tbHtml = '<tbody>';
    //{# fill rows #}
    if (expert_mode) {
        var labels = ['Unlabeled', 'User-Yes', 'User-No', 'User-Unsure',
        'Expert-Yes', 'Expert-No', 'Expert-Unsure'];
    } else {
        var labels = ['Unlabeled', 'User-Yes', 'User-No', 'User-Unsure'];
    }

    for (i = 0; i < results.ltable.length; i++) {
        lrow = results.ltable[i];
        rrow = results.rtable[i];
        lbl = lrow[results.label];
        lid = lrow['DRUG ID'];
        rid = rrow['DRUG ID'];
        id = lrow[results.id];
        //{#                alert(lid);#}
        //{#                alert(rid);#}
        //{#  fill row from ltable #}
        tbHtml += '<tr style="background-color:#ffffe5">';
        $.each(header, function (i, item) {
            if (item != results['label']) {
                tbHtml += '<td>' + lrow[item] + '</td>'
            }
        });
        tbHtml += '</tr>';
        //{#                alert(tbHtml)#}
        //{#  fill row from rtable #}
        tbHtml += '<tr style="background-color:#ffffe5">';
        $.each(header, function (i, item) {
            if (item != results['label']) {
                tbHtml += '<td>' + rrow[item] + '</td>'
            }
        });
        tbHtml += '</tr>';
        //{#  fill check box row #}
        tbHtml += '<tr>';
        tbHtml += '<td colspan="9">';
        tbHtml += '<div style="width: 100%; text-align: left;">';
        for (var k = 0; k < labels.length; k++) {
            tbHtml += '<input style="margin-left: 20px" type="radio" name="';
            tbHtml += id + '_' + lid + '_' + rid;
            tbHtml += '" value="';
            tbHtml += id + '_' + lid + '_' + rid + '_' + k;
            tbHtml += '"';
            if (k == lbl) {
                tbHtml += ' checked'
            }
            tbHtml += '> <label for="' + id + '_' + lid + '_' + rid + '">' + labels[k] + ' </label>';
        }
        //{#            tbHtml += '<button type="button" style="margin-left: 20px" class="btn btn-default btn-sm" data-toggle="modal" data-target=';#}
        //{#            tbHtml += '"#' + lid + '_' + rid + '"';#}
        //{#            tbHtml += '>View Tuple Pairs</button>';#}
        var fname = lid + '_' + rid + '.html';
//{#            var url = {{ url_for('static', filename='tuplepairpages/') }} ;#}
//{#            var url = '{{  url_for('static', filename='tuplepairpages') }}' + '/' + fname;#}
        var url = 'tuplepairpages/' + fname;
        tbHtml += '<a href="'+ url +'" ';
        tbHtml += ' target="_blank" style="margin-left: 20px" type="submit" class="btn btn-default" > View Tuple Pairs </a>';
        //{#<a href="http://www.example.com" target="_blank" id="code" type="submit" class="btn btn-default" >#}
        //{#     Generate Code</a>#}
        tbHtml += '</div></td></tr>';
    }
    tbHtml += '</tbody>';
    var tHtml = thHtml + tbHtml;
    //{#            alert(thHtml);#}
    //{#            alert(tbHtml);#}
    // {#console.log(tbHtml);#}
    $('#data_table').innerHTML = '';
    $('#data_table').html(tHtml);
}