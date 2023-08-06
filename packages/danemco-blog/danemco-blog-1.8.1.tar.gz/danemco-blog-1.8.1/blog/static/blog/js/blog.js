function blog_article_archive_show_hide_div(div_id, what) {
    var div_elm = document.getElementById(div_id+"_"+ what);
    var arrow_elm = document.getElementById(div_id+"_open_close");

    if (div_elm.style.display == "none") {
        document.getElementById(div_id+"_"+ what).style.display = 'block';
        arrow_elm.innerHTML = "&#x25BC;";
    } else {
        document.getElementById(div_id+"_"+ what).style.display = 'none';
        arrow_elm.innerHTML = "&#x25B6;";
    }
}

var elems = document.getElementsByClassName('blog-article-archive-expand-collapse');

for (var i = 0; i < elems.length; i++) {
    elems[i].style.visibility = 'visible';
}
