// Bootstrap carosel
document.addEventListener('DOMContentLoaded', function() {
    var myCarousel = document.querySelector('#carouselExampleCaptions');
    var carousel = new bootstrap.Carousel(myCarousel, {
      interval: 3000,
      ride: 'carousel'
    });
  });

document.addEventListener("DOMContentLoaded", function() {
    // JavaScript code for blinking text
    function blinkText() {
        var blinkingText = document.querySelector('.blinking-text');
        if (blinkingText) {
            blinkingText.style.opacity = (blinkingText.style.opacity == '0' ? '1' : '0');
        }
    
    // Set interval for blinking
    var blinkInterval = setInterval(blinkText, 500); 
}});