$(function() {
    var update_counts_from_text = function(text) {
        var count = $.parseJSON(text);
        $("#the_count").html(count['the_count']);
        $("#the_money").html(count['the_money']);
    };
    
    var update_counts = function() {
        $.ajax('/update', {
            dataType: 'text',
            success: update_counts_from_text
        });
    };

    window.setInterval(update_counts, 10000);

    // TODO: spinner after click
    var base_url = 'http://stratakazika.pl/';
    $('.increase').submit(function() {
        var name = this.counter_name.value;
        var here_url = base_url + '?i=' + encodeURIComponent(name);
        base_url = encodeURIComponent(base_url);
        here_url = encodeURIComponent(here_url);
        var description = "Powiększam Stratę Kazika, kopiując płytę „" +
                name + "”. Dorzuć się i Ty!"
        var blip = encodeURIComponent(description + " #StrataKazika http://stratakazika.pl");
        var diaspora = encodeURIComponent(description + " #StrataKazika");
        var description = encodeURIComponent(description);

        var $form = $(this);
        $('.share').hide("fast", function() {$(this).remove()});
        var $button = $('button', this);
        $button.html("...");
        $(this).ajaxSubmit({
            dataType: 'text',
            success: function(text) {
                update_counts_from_text(text);
                var $share = $('#share-stub').clone();
                $share.removeAttr('id');
                $share.addClass('share');

                $('.facebook', $share).attr('href',
                    'https://www.facebook.com/sharer.php?u=' + here_url);
                $('.google', $share).attr('href',
                    'https://plus.google.com/share?url=' + here_url);
                $('.diaspora', $share).attr('href',
                    'http://sharetodiaspora.github.com/?title=' + diaspora +
                    '&url=' + base_url);
                $('.twitter', $share).attr('href',
                    'https://twitter.com/intent/tweet?url='+ base_url +
                    '&text=' + description + '&hashtags=stratakazika');
                $('.blip', $share).attr('href',
                    'http://blip.pl/dashboard?body=' + blip);
                $('.nk', $share).attr('href',
                    'http://nk.pl/#sledzik?shout=' + blip);

                $form.append($share);
                $share.show('fast');
                $button.html('Ja też!');
            }
        }); 
        return false;
    });

    $("#search").autocomplete({
        source: '/hint',
        minLength: 1,
    });

    $(".share .close").live("click", function() {
        $('.share').hide("fast", function() {$(this).remove()});
    });

});
