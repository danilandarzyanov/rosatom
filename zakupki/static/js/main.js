$("#filter").keyup(function() {

    // Retrieve the input field text and reset the count to zero
    var filter = $(this).val(),
      count = 0;

    // Loop through the comment list
    $('.list-company .list-company-block').each(function() {


      // If the list item does not contain the text phrase fade it out
      if ($(this).text().search(new RegExp(filter, "i")) < 0) {
        $(this).hide();  // MY CHANGE

        // Show the list item if the phrase matches and increase the count by 1
      } else {
        $(this).show(); // MY CHANGE
        count++;
      }

    });

  });


  $('.fa-heart').click(function() {
      alert('Спасибо! Рейтинг компании повышен');
  })


  $('.fa-heart-broken').click(function() {
    alert('Спасибо! Рейтинг компании понижен, мы будем рекомендовать их реже');
})


$( "#btnPlusFormAdd" ).on( "click", function() {
    event.preventDefault();
    $('#form-table-add tr:last').after('<tr><td><input type="text"></td><td><input type="text"></td><td><input type="text"></td><td></td></tr>');
  });

