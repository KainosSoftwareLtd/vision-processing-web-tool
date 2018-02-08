function toggleUpload() {
    $("#upload-area").toggle();
}

function postTags() {
    console.log('posting tags');
    var tag = $("#itemsTag").val();
    var itemIds = [];
    var selected = $(".ui-selected");
    for (var i = 0; i < selected.length; i++) {
        itemIds.push(selected[i].firstElementChild.id);
    }
    var data = {
        'tag': tag,
        'ids': itemIds
    }
    $.post('/tag', data)
    console.log('finished posting tags');
}

function test() {
    console.log('Hello, world!');
}