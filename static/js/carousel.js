document.addEventListener("DOMContentLoaded", () => {
  const track = document.getElementById("work-carousel");
  if (!track) return;

  const slides = track.querySelectorAll(".carousel-slide");
  let currentIndex = 0;
  let intervalId;

  // Function to advance to the next slide
  const advanceSlide = () => {
    // Move to next index, loop back to 0 if at the end
    currentIndex = (currentIndex + 1) % slides.length;
    
    const slide = slides[currentIndex];
    
    // Scroll the track to center the active slide
    track.scrollTo({
      left: slide.offsetLeft - track.offsetLeft,
      behavior: "smooth"
    });
  };

  // Start the auto-play timer (3 seconds)
  const startCarousel = () => {
    intervalId = setInterval(advanceSlide, 3000);
  };

  // Stop the timer (so users can read/click)
  const stopCarousel = () => {
    clearInterval(intervalId);
  };

  // Pause on hover (desktop) or touch (mobile)
  track.addEventListener("mouseenter", stopCarousel);
  track.addEventListener("mouseleave", startCarousel);
  track.addEventListener("touchstart", stopCarousel, { passive: true });
  track.addEventListener("touchend", startCarousel, { passive: true });

  // Start it up
  startCarousel();
});