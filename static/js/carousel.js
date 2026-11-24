document.addEventListener("DOMContentLoaded", () => {
  const track = document.getElementById("work-carousel");
  if (!track) return;

  const slides = track.querySelectorAll(".carousel-slide");
  let currentIndex = 0;
  let intervalId;
  let isInView = false;
  let isHovered = false;
  let userInteracted = false;

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function updateCarousel() {
    // Calculate the offset to center the active slide
    const slideWidth = slides[0].offsetWidth;
    const offset = -(currentIndex * slideWidth);
    
    // Apply the transform (translate3d for GPU acceleration)
    track.style.transform = `translate3d(${offset}px, 0, 0)`;
    
    // Reset loop
    if (currentIndex >= slides.length) {
       // It's handled inside the loop logic
    }
  }

  function advanceSlide() {
    if (userInteracted || !isInView || isHovered || document.hidden || prefersReducedMotion) return;

    currentIndex++;
    if (currentIndex >= slides.length) {
      // Reached the end, jump back to start instantly
      track.style.transition = 'none';
      currentIndex = 0;
      updateCarousel();
      
      // Force reflow and restore transition
      void track.offsetWidth;
      track.style.transition = 'transform 850ms cubic-bezier(0.65, 0, 0.35, 1)';
    } else {
      track.style.transition = 'transform 850ms cubic-bezier(0.65, 0, 0.35, 1)';
      updateCarousel();
    }
  }

  function startCarousel() {
    if (intervalId) clearInterval(intervalId);
    intervalId = setInterval(advanceSlide, 4000); // 4 seconds pause
  }

  function stopCarousel() {
    clearInterval(intervalId);
  }

  // 1. IntersectionObserver: Start/Stop when in view
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      isInView = entry.isIntersecting;
      if (isInView && !userInteracted) {
        startCarousel();
      } else {
        stopCarousel();
      }
    });
  }, { threshold: 0.3 }); // Trigger when 30% visible
  observer.observe(track);

  // 2. Visibility Change (Tab hidden)
  document.addEventListener("visibilitychange", () => {
    if (document.hidden) stopCarousel();
    else if (isInView && !userInteracted) startCarousel();
  });

  // 3. Pause on Hover/Touch
  track.addEventListener("mouseenter", () => { isHovered = true; stopCarousel(); });
  track.addEventListener("mouseleave", () => { isHovered = false; if(isInView) startCarousel(); });
  track.addEventListener("touchstart", () => { isHovered = true; stopCarousel(); }, { passive: true });
  track.addEventListener("touchend", () => { isHovered = false; if(isInView) startCarousel(); }, { passive: true });

  // Initial setup
  track.style.display = 'flex';
  track.style.width = '100%';
  track.style.overflow = 'hidden';
  
  // Wrap slides in a flex container for translation
  const wrapper = document.createElement('div');
  wrapper.style.display = 'flex';
  wrapper.style.transition = 'transform 850ms cubic-bezier(0.65, 0, 0.35, 1)';
  wrapper.style.width = '100%';
  wrapper.style.willChange = 'transform';

  slides.forEach(slide => {
    slide.style.flex = '0 0 100%';
    slide.style.width = '100%';
    wrapper.appendChild(slide);
  });
  
  track.innerHTML = '';
  track.appendChild(wrapper);
});