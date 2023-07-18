function add_or_remove_favorite(item, csrf_token) {
    let url = item.data('product_id'),
        heart = item.find('.bi');
    $.get(
        url
    ).done(function (data) {
        if (data.is_favorite === true) {
            heart.addClass('bi-heart-fill').removeClass('bi-heart')
        } else {
            heart.addClass('bi-heart').removeClass('bi-heart-fill')
        }
    }).fail(function (error) {
        console.log(error)
    })
}