$(function() {
    // TODO: update every 10 secs and after submit

    // spinner after click
    var base_url = 'http://stratakazika.pl/';
    $('.increase').submit(function() {
        var name = this.counter_name.value;
        alert(name);
        var here_url = base_url + '?i=' + encodeURIComponent(name);
        base_url = encodeURIComponent(base_url);
        here_url = encodeURIComponent(here_url);
        var description = "Powiększam Stratę Kazika, kopiując płytę „" +
                name + "”. Dorzuć się i Ty!"
        var blip = encodeURIComponent(description + " #StrataKazika http://stratakazika.pl");
        var description = encodeURIComponent(description);

        var $form = $(this);
        var $button = $('button', this);
        $(this).ajaxSubmit({
            success: function() {
                $button.html('Dzięki!');
                var $share = $('#share-stub').clone();
                $share.removeAttr('id');

                $('.facebook', $share).attr('href',
                    'https://www.facebook.com/sharer.php?u=' + here_url);
                $('.google', $share).attr('href',
                    'https://plus.google.com/share?url=' + here_url);
                $('.diaspora', $share).attr('href',
                    'http://sharetodiaspora.github.com/?title=' + description +
                    '&url=' + base_url);
                $('.twitter', $share).attr('href',
                    'https://twitter.com/intent/tweet?url='+ base_url +
                    '&text=' + description + '&hashtags=stratakazika');
                $('.blip', $share).attr('href',
                    'http://blip.pl/dashboard?body=' + blip);
                $('.nk', $share).attr('href',
                    'http://nk.pl/#sledzik?shout=' + blip);

                $('.share', $form).remove();
                $form.append($share);
                $share.show('fast');
            }
        }); 
        return false;
    });
});
