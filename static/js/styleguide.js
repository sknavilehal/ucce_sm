var allIcons = [];
var allEntries = [];

var curProgress = 0;
var curProgressTimer;

var curGaugeProgress = 0;
var curGaugeTimer;

function checkTheme() {
    var theme = getStorageData('uikit-theme');
    if (theme) {
        $('#themeSwitcher .dropdown__menu a').removeClass('selected');
        if (theme === 'Dark') {
            $('#theme-dark').addClass('selected');
        } else {
            $('#theme-default').addClass('selected');
        }
        switchTheme(theme);
    }
}
function getStorageData(key) {
    return localStorage.getItem(key);
}
function setStorageData(key, value) {
    localStorage.setItem(key, value);
}
function getQueryParam(key) {
    var url = window.location.search.substring(1);
    var urlVars = url.split('&');
    for (var ii = 0; ii < urlVars.length; ii++) {
        var urlParam = urlVars[ii].split('=');
        if (urlParam[0] === key) {
            return urlParam[1];
        }
    }
}
function setQueryParam(key, value) {
    if (history.pushState) {
        var params = new URLSearchParams(window.location.search);
        params.set(key, value);
        var newUrl = window.location.protocol + "//" + window.location.host + window.location.pathname + '?' + params.toString();
        window.history.pushState({path:newUrl},'',newUrl);
    }
}
function populateSearchEntries() {
    allEntries = [];
    var entries = $('#search-dictionary .searchable');
    for (var ii=0;ii<entries.length;ii++) {
        var retObj = {};
        for (var yy=0;yy<entries[ii].attributes.length;yy++) {
            var attrObj = entries[ii].attributes[yy];
            if (attrObj.name === "data-ref") { retObj.ref = attrObj.value };
            if (attrObj.name === "data-depth") { retObj.depth = attrObj.value };
            if (attrObj.name === "data-name") { retObj.name = attrObj.value };
            if (attrObj.name === "data-description") { retObj.description = attrObj.value };
            if (attrObj.name === "data-group") { retObj.group = attrObj.value };
        }
        var category = retObj.ref.substring(0, retObj.ref.indexOf('-'));
        retObj.ref = 'section-' + category + '.html#' + retObj.ref;
        allEntries.push(retObj);
    }
}
function populateSearchIcons() {
    allIcons = $('#icon-container .panel-icon');
    setIcons(allIcons);
}
function removeClassWildcard($element, removals) {
    if (removals.indexOf('*') === -1) {
        // Use native jQuery methods if there is no wildcard matching
        $element.removeClass(removals);
        return $element;
    }

    var patt = new RegExp('\\s' +
            removals.replace(/\*/g, '[A-Za-z0-9-_]+').split(' ').join('\\s|\\s') +
            '\\s', 'g');

    $element.each(function (i, it) {
        var cn = ' ' + it.className + ' ';
        while (patt.test(cn)) {
            cn = cn.replace(patt, ' ');
        }
        it.className = $.trim(cn);
    });

    return $element;
}
function addCards(cnt) {
    $('main #grid').empty();
    for (var ii=1;ii<=cnt;ii++) {
        $('main #grid').append('<div class="card"><div class="card__body"><h3 class="text-uppercase base-margin-bottom">Card '+ii+'</h3><div class="flex"><div class="form-group form-group--inline"><div class="form-group__text"><input id="grid-card-cols" type="number" value="1"><label>Columns</label></div></div><div class="form-group form-group--inline"><div class="form-group__text"><input id="grid-card-rows" type="number" value="1"><label>Rows</label></div></div></div></div>');
    }
    wireCards();
}
function wireCards() {
    $('main #grid .card').click(function() {
        if ($(this).parent().hasClass('grid--selectable')) {
            $(this).toggleClass('selected');
        }
    });
    $('main #grid-cards').change(function() {
        addCards($(this).val());
    });
    $('main #grid .card #grid-card-cols').click(function(e) {
        e.stopPropagation();
    });
    $('main #grid .card #grid-card-cols').change(function() {
        removeClassWildcard($(this).closest('.card'), 'card--col-*');
        $(this).closest('.card').addClass('card card--col-'+$(this).val());
    });
    $('main #grid .card #grid-card-rows').click(function(e) {
        e.stopPropagation();
    });
    $('main #grid .card #grid-card-rows').change(function() {
        removeClassWildcard($(this).closest('.card'), 'card--row-*');
        $(this).closest('.card').addClass('card card--row-'+$(this).val());
    });
}
function calcSearchWindowHeight() {
    var el = $('#search-results');
    var maxHeight = ($(window).height() - $('#search-kit').offset().top - $('#search-kit').height() - 40);
    el.css('max-height', maxHeight + 'px');
}
function shouldHideSidebar() {
    if (window.innerWidth < 768) {
        $('#styleguideSidebar').addClass('sidebar--hidden');
    } else {
        $('#styleguideSidebar').addClass('sidebar--mini');
        $('#styleguideSidebar').removeClass('sidebar--hidden');
    }
}
function startGaugeAnimation() {
    curGaugeTimer = setTimeout(function () {
        curGaugeProgress += Math.floor(Math.random() * 10);
        curGaugeProgress = (curGaugeProgress >= 100) ? 100 : curGaugeProgress;
        $('main #gauge-example').attr('data-percentage', curGaugeProgress);
        $('main #gauge-example #gauge-example-value').html(curGaugeProgress);
        if (curGaugeProgress !== 100) {
            startGaugeAnimation();
        }
    }, 100);
}
function startProgressAnimation() {
    curProgressTimer = setTimeout(function () {
        curProgress += Math.floor(Math.random() * 10);
        curProgress = (curProgress >= 100) ? 100 : curProgress;
        $('main #progressbar-size .progressbar').attr('data-percentage', curProgress);
        $('main #progressbar-size .progressbar .progressbar__label').html(curProgress + '%');
        if (curProgress !== 100) {
            startProgressAnimation();
        }
    }, 100);
}
function jumpTo(ref) {
    document.location.href = "section-"+ref+".html#"+ref;
}
function doNav(url) {
    shouldHideSidebar();
    document.location.href = url;
}
function updateUrl(ref, pattern) {
    var path = window.location.pathname;
    var url = path + '#' + ref;
    history.pushState({ id: url }, 'Cisco UI Kit - ' + ref, url);

    startPageAnimation(pattern);
}
function checkUrlAndSetupPage(url) {
    if (url.lastIndexOf('#') != -1) {
        var anchor = url.substring(url.lastIndexOf('#') + 1);
        var str = _.split(anchor, '-')[1];
        var str = str.toLowerCase().replace(/\b[a-z]/g, function(letter) {
            return letter.toUpperCase();
        });

        // Remove any existing active classes
        $('#styleguideTabs > li.tab').removeClass('active');
        $('#styleguideTabs-content > .tab-pane').removeClass('active');

        // Add the active class to the appropriate elements
        $('#styleguideTabs #styleguideTabs-'+str).addClass('active');
        $('#styleguideTabs-content #styleguideTabs-'+str+'-content').addClass('active');

        setTimeout(function() {
            // Now scroll to the appropriate anchor (if specified in the url)
            var el = document.getElementById(anchor + '-tmp');
            if (el !== null) {
                el.scrollIntoView();
            }
        }, 100);
    }
    else if (url.indexOf('index.html') !== -1) {
        $('#rootSidebar #section-gettingStarted').addClass('selected');
    }
}
function startPageAnimation(pattern) {
    if (pattern === 'Gauge') {
        curGaugeProgress = 0;
        startGaugeAnimation();
    } else if (pattern === 'Progressbar') {
        curProgress = 0;
        startProgressAnimation();
    }
}
function doGlobalSearch(searchStr, forceFlag) {
    var results = [];
    searchStr = searchStr.toLowerCase();
    for (var ii=0;ii<allEntries.length;ii++) {
        var entry = allEntries[ii];
        if (entry.depth === "3") {
            if ((entry.name.toLowerCase().indexOf(searchStr) !== -1) || (entry.ref.toLowerCase().indexOf(searchStr) !== -1) || forceFlag) {
                results.push(entry);
            }
        }
    }
    $('#search-results').empty();
    var str = '<a class="text-italic disabled"> Found ' + results.length + ' results</a>';
    _.forEach(_.groupBy(results, 'group'), function(value, key) {
        str += '<div class="dropdown__group"><div class="dropdown__group-header">' + key + '</div>';
        _.each(value, function(result) {
            str += '<a href="' + result.ref + '">' + result.name + '</a>';
        });
        str += '</div>';
    });
    $('#search-results').append(str);
    calcSearchWindowHeight();
}
function searchIcons(icon) {
    var ret = [];
    for (var ii=0;ii<allIcons.length;ii++) {
        if (allIcons[ii].innerText.indexOf(icon) !== -1) {
            ret.push(allIcons[ii]);
        }
    }
    return ret;
}
function clearSearch() {
    setIcons(allIcons);
}
function setActiveSlide(slide, animation) {
    $(slide).siblings().removeClass('active');
    $(slide).parent().parent().find('.carousel__slide').removeClass('active slideInLeftSmall slideInRightSmall fadeIn');
    $(slide).addClass('active');
    $(slide).parent().parent().find('#'+slide.id+'-content').addClass('active '+animation);
}
function setIcons (icons) {
    $('#icon-container').empty();
    $('#icon-container').append(icons);
    $('#icon-count').text(icons.length);
    $('#icon-total-count').text(allIcons.length);
}
function debounce (func, wait) {
    var timeout;
    var context = this, args = arguments;
    clearTimeout(timeout);
    timeout = setTimeout(function () {
        func.apply(context, args);
    }, wait || 0);
}
function openModal (id) {
    $('#modal-backdrop').removeClass('hide');
    $('#'+id).before('<div id="'+id+'-placeholder"></div>').detach().appendTo('body').removeClass('hide');
}
function closeModal (id) {
    $('#'+id).detach().prependTo(('#'+id+'-placeholder')).addClass('hide');
    $('#modal-backdrop').addClass('hide');
}
function switchTheme(theme) {
    if (theme === 'Dark') {
        $('#theme-main').attr('href','assets/css/cui-styleguide-dark.min.css');
        $('#theme-code').attr('href', 'public/js/atom-one-dark.css');
    } else {
        $('#theme-main').attr('href','assets/css/cui-styleguide.min.css');
        $('#theme-code').attr('href', 'public/js/atom-one-light.css');
    }
    setStorageData('uikit-theme', theme);
}

$(document).ready(function() {

    // Wire the icon search
    $('#icon-search-input').on('input', function() {
        var searchStr = $('#icon-search-input').val();
        if (searchStr !== '') {
            setIcons(searchIcons(searchStr));
        }
        else {
            clearSearch();
        }
    });

    // Wire the global search
    $('#search-kit').on('click', function() {
        if ($('#search-kit').val() === '') {
            doGlobalSearch('', true);
        }
        calcSearchWindowHeight();
    });
    $('#search-kit').on('input', function() {
        doGlobalSearch($('#search-kit').val(), false);
    });

    // Wire the gauge reset button
    $('#gauge-start').click(function() {
        if (curGaugeTimer) { clearTimeout(curGaugeTimer); }
        curGaugeProgress = 0;
        startGaugeAnimation();
    });

    // Wire the progressbar reset button
    $('#progressbar-start').click(function() {
        if (curProgressTimer) { clearTimeout(curProgressTimer); }
        curProgress = 0;
        startProgressAnimation();
    });

    // Wire the header sidebar toggle button
    $('#sidebar-toggle').click(function() {
        $('#styleguideSidebar').toggleClass('sidebar--mini');
        $('#sidebar-toggle span:first-child').removeClass();
        if ($('#styleguideSidebar').hasClass('sidebar--mini')) {
            $('#sidebar-toggle span:first-child').addClass('icon-list-menu');
        } else {
            $('#sidebar-toggle span:first-child').addClass('icon-toggle-menu');
        }
    });

    $('#mobile-sidebar-toggle').click(function() {
        $('#styleguideSidebar').removeClass('sidebar--mini');
        $('#styleguideSidebar').toggleClass('sidebar--hidden');
    });

    // Wire the sidebar drawer open/close toggles
    $('#styleguideSidebar .sidebar__drawer > a').click(function(e) {
        e.stopPropagation();
        $(this).parent().siblings().removeClass('sidebar__drawer--opened');
        $(this).parent().toggleClass('sidebar__drawer--opened');
    });

    // Wire the sidebar selected item
    $('#styleguideSidebar .sidebar__item > a').click(function() {
        $('#styleguideSidebar .sidebar__item').removeClass('sidebar__item--selected');
        $(this).parent().addClass('sidebar__item--selected');
    });

    // Wire the sidebar examples
    $('main .sidebar__drawer > a').click(function() {
        $(this).parent().toggleClass('sidebar__drawer--opened');
    });
    $('main .sidebar__item > a').click(function() {
        $(this).parent().siblings().removeClass('sidebar__item--selected');
        $(this).parent().addClass('sidebar__item--selected');
    });

    // Wire the button group examples
    $('main .btn-group .btn').click(function() {
        $(this).siblings().removeClass('selected');
        $(this).addClass('selected');
    });

    // Wire the markup toggles
    $('main .markup').removeClass('active');
    $('main .markup-toggle').click(function() {
        $(this).parent().next().toggleClass('hide');
        $(this).parent().toggleClass('active');

        if ($(this).hasClass('active')) {
            $(this).find('.markup-label').text('Hide code');
        }
        else if (!$(this).hasClass('active')) {
            $(this).find('.markup-label').text('View code');
        }
    });

    // Wire the markup clipboard
    $('main .clipboard-toggle').click(function() {
        clipboard.copy($(this).parent().parent().find('code.code-raw').text());
        $(this).addClass('text-bold').text('Copied!');
    });

    // Wire the tabs
    $('main li.tab').click(function() {
        $(this).siblings().removeClass('active');
        var tabsId = this.id.substring(0, this.id.indexOf('-'));
        $('main #'+tabsId+'-content > .tab-pane').removeClass('active');
        $(this).addClass('active');
        $('main #'+this.id+'-content').addClass('active');
    });

    // Wire pagination
    $('main ul.pagination > li > a').click(function() {
        var el = $(this).parent().siblings().find('.active');
        $(this).parent().siblings().removeClass('active');
        $(this).parent().addClass('active');
    });

    // Wire closeable alerts
    $('main .alert .alert__close').click(function() {
        $(this).parent().addClass('hide');
    });

    // Wire the Card pattern examples
    $('main a.card').click(function() {
        $(this).toggleClass('selected');
    });

    // Wire the Advanced Grid example
    $('main #grid-group').click(function() {
        $(this).parent().find('#grid-group').removeClass('selected');
        var cls = 'grid--' + $(this).text();
        $('main .grid').removeClass('grid--3up');
        $('main .grid').removeClass('grid--4up');
        $('main .grid').removeClass('grid--5up');
        $('main .grid').addClass(cls);
        $(this).addClass('selected');
    });

    $('main #grid-cards').change(function() {
        addCards($(this).val());
    });

    $('main #grid-gutters').change(function() {
        $('main #grid').css('gridGap', $(this).val()+'px');
    });

    $('main #grid-selectable').change(function() {
        $('main #grid').toggleClass('grid--selectable');
        $('main .grid .card').removeClass('selected');
    });

    addCards(15);

    // Wire the carousel examples
    $('main .carousel__controls a.dot').click(function() {
        setActiveSlide(this, 'fadeIn');
    });
    $('main .carousel__controls a.back').click(function() {
        var last = $(this).parent().find('a.dot').last();
        var cur = $(this).parent().find('a.dot.active');
        var active = cur.prev();
        if (active[0].id === "") {
            active = last;
        }
        setActiveSlide(active[0], 'slideInLeftSmall');
    });
    $('main .carousel__controls a.next').click(function() {
        var first = $(this).parent().find('a.dot').first();
        var cur = $(this).parent().find('a.dot.active');
        var active = cur.next();
        if (active[0].id === "") {
            active = first;
        }
        setActiveSlide(active[0], 'slideInRightSmall');
    });

    // Wire the dropdown examples
    $('main .dropdown').click(function(e) {
        e.stopPropagation();
        var el = $(this).find('input');
        if (!el.hasClass('disabled') && !el.attr('disabled') && !el.hasClass('readonly') && !el.attr('readonly')) {
            $(this).toggleClass('active');
        }
    });
    $('main .dropdown .dropdown__menu a').click(function(e) {
        e.stopPropagation();

        var origVal = $(this).parent().parent().find('input').val();
        var newVal = $(this).text();

        $(this).parent().find('a').removeClass('selected');
        $(this).addClass('selected');
        $(this).parent().parent().find('input').val($(this).text());
        $(this).parent().parent().removeClass('active');

        var id = $(this).parent().parent()[0].id;
        if (id === 'themeSwitcher') {
            switchTheme($(this).text());
        }
    });

    // Close dropdowns and open sidebar drawers on clicks outside the dropdowns
    $(document).click(function() {
        $('main .dropdown').removeClass('active');
        $('#styleguideSidebar .sidebar__drawer').removeClass('sidebar__drawer--opened');
    });

    // Wire the masonry layout dropdowns
    $('main #masonry-columns-dropdown').change(function() {
        $('main #masonry-columns-example').removeClass();
        $('main #masonry-columns-example').addClass('masonry masonry--cols-' + this.value);
    });
    $('main #masonry-gaps-dropdown').change(function() {
        $('main #masonry-gaps-example').removeClass();
        $('main #masonry-gaps-example').addClass('masonry masonry--gap-' + this.value);
    });

    // Wire the selectable tables
    $('main .table.table--selectable tbody > tr').click(function() {
        $(this).toggleClass('active');
    });
    // Wire the table wells example
    $('main #table-wells tbody > tr').click(function() {
        $(this).find('td span.icon-chevron-up').removeClass('icon-chevron-up').addClass('icon-chevron-down');
        $(this).find('td span.icon-chevron-down').removeClass('icon-chevron-down').addClass('icon-chevron-up');
        $(this).next().toggleClass('hide');
    });

    // Wire the global modifiers
    $('main #global-animation').change(function() {
        $('body').toggleClass('cui--animated');
    });
    $('main #global-headermargins').change(function() {
        $('body').toggleClass('cui--headermargins');
    });
    $('main #global-spacing').change(function() {
        $('body').toggleClass('cui--compressed');
    });
    $('main #global-wide').change(function() {
        $('body').toggleClass('cui--wide');
    });
    $('main #global-sticky').change(function() {
        $('body').toggleClass('cui--sticky');
    });

    // Load the changelog
    $.get('changelog.md', function(markdownContent) {
        var converter = new Markdown.Converter();
        $("#changelog-content").html(converter.makeHtml(markdownContent));
    });

    // Load the broadcast file (if it exists)
    $.getJSON('broadcast.json', function(data) {
        if (data && data.text && data.text.length) {
            $("#broadcast-msg").html(data.text);
            $("#broadcast").toggleClass('hide');
        }
    });

    window.addEventListener('hashchange', function (event) {
        checkUrlAndSetupPage(event.newURL);
    }, false);

    // Check for anchor link in the URL
    checkUrlAndSetupPage(window.location.href);

    // Listen of window changes and close the sidebar if necessary
    $(window).resize(function() {
        shouldHideSidebar();
        calcSearchWindowHeight();
    });

    shouldHideSidebar();
    populateSearchIcons();
    populateSearchEntries();
    calcSearchWindowHeight();
    checkTheme();
});
