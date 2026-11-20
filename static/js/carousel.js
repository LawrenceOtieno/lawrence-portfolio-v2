document.addEventListener("DOMContentLoaded", () => {
  const track = document.getElementById("work-carousel");
  if (!track) return;

  const slides = track.querySelectorAll(".carousel-slide");
  let currentIndex = 0;
  let intervalId;

  // Function to advance to the next slide
  const advanceSlide = () => {
    // If we are on the final slide (the End marker)
    if (currentIndex === slides.length - 1) {
      currentIndex = 0;
      
      // Temporarily disable scroll snap and smooth scrolling to snap instantly
      track.style.scrollSnapType = "none";
      track.style.scrollBehavior = "auto";
      
      // Instantly jump to the first slide
      track.scrollLeft = slides[0].offsetLeft - track.offsetLeft;
      
      // Restore scroll snap and smooth scrolling for the next cycles
      setTimeout(() => {
        track.style.scrollSnapType = "x mandatory";
        track.style.scrollBehavior = "smooth";
      }, 50);
      return;
    }

    // Otherwise, move to the next slide smoothly
    currentIndex++;
    track.scrollTo({
      left: slides[currentIndex].offsetLeft - track.offsetLeft,
      behavior: "smooth"
    });
  };

  // Start the auto-play timer (4 seconds)
  const startCarousel = () => {
    intervalId = setInterval(advanceSlide, 4000);
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