$(document).ready(function() {
      //SMOOTH SCROLL 
      $('.menu li a[href^="#"]').on('click', function(e){
          e.preventDefault();
  
          let target = $(this.hash);
  
          if (target.length) {
              $('html, body').stop().animate({
                  scrollTop: target.offset().top -60
              }, 1000);
          }
  
      });
  
      $(' a[href^="#"]').on('click', function(e){
        e.preventDefault();
  
        let target = $(this.hash);
  
        if (target.length) {
            $('html, body').stop().animate({
                scrollTop: target.offset().top -60
            }, 1000);
        }
  
    });

  });
  

mediumZoom('.zoom', {
    margin: 50,
    // background: '#BADA55',
    // scrollOffset: 0,
    // container: '#zoom-container',
    // template: '#zoom-template',
  })
