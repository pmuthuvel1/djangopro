$(window).load(function() {

    $(function() {

        $('footer').delay(5000).slideToggle('slow');
        $('#info').click(function() {
            $('footer').slideToggle('slow');
        });
        $('h2').parent('div').children('ul').hide();
        $('h2').click(function() {
            //$(this)+$('ul').slideToggle('slow');
            $(this).parent('div').children('ul').slideToggle('slow');
            $(this).children('i').toggleClass('fa-plus-square fa-minus-square');
        });

    });

});

