function translate(srcElement, destElement, destLang) {
    $(destElement).html('<img src="/static/imgs/loading.gif">')
    $.post('/translate',
        {
            text: $(srcElement).text(),
            dest_language: destLang
        }
    ).done(function (response) {
            $(destElement).text(response['text'])
        }
    ).fail(function () {
            $(destElement).text("{{ _('Erro: Não foi possível acessar o servidor.') }}");
        }
    );
}

$(function () {
    let timer = null;
    const DELAY = 1000;
    $('.user_popup').hover(
        function (event) {
            // on mouse in
            let el = $(event.currentTarget);
            timer = setTimeout(() => {
                timer = null;
                xhr = $.ajax(
                    '/user/' + el.first().text().trim() + '/popup').done(
                    (data) => {
                        xhr = null;
                        el.popover(
                            {
                                trigger: 'manual',
                                html: true,
                                animation: false,
                                container: el,
                                content: data
                            }).popover('show');
                        flask_moment_render_all();
                    }
                );
            }, DELAY);
        },
        function (event) {
            // on mouse out
            let el = $(event.currentTarget);
            if (timer) {
                clearTimeout(timer);
                timer = null;
            } else if (xhr) {
                xhr.abort();
                xhr = null;
            } else {
                el.popover('destroy');
            }
        }
    );
});

function set_message_count(n) {
    $('#message_count').text(n);
    $('#message_count').css('visibility', n ? 'visible' : 'hidden');
}

function update_notifications(endpoint) {
    let since = 0;
    setInterval(() => {
        $.ajax(endpoint + '?since=' + since).done(
            (notifications) => {
                for (let i = 0; i < notifications.length; i++) {
                    switch (notifications[i].name) {
                        case 'unread_message_count':
                            set_message_count(notifications[i].data);
                            break;
                        case 'task_progress':
                            set_task_progress(notifications[i].data.task_id,
                                notifications[i].data.progress);
                            break;
                    }
                    since = notifications[i].timestamp;
                }
            }
        );
    }, 10000)
}

function set_task_progress(task_id, progress) {
    $('#' + task_id + '-progress').text(progress);
}