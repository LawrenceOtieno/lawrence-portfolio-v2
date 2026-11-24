document.addEventListener('DOMContentLoaded', () => {
  // --- 1. Scroll Reveal ---
  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('active');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

  // --- 2. Sticky About Timeline ---
  const chapters = document.querySelectorAll('.about-chapter');
  const progressBar = document.getElementById('timeline-progress');
  if (chapters.length > 0 && progressBar) {
    const chapterObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          chapters.forEach(c => c.classList.remove('active'));
          entry.target.classList.add('active');
          
          const index = Array.from(chapters).indexOf(entry.target);
          const progress = ((index + 1) / chapters.length) * 100;
          progressBar.style.height = progress + '%';
        }
      });
    }, { threshold: 0.6, rootMargin: '-10% 0px -40% 0px' });

    chapters.forEach(chapter => chapterObserver.observe(chapter));
  }

  // --- 3. Gallery Filters & Lightbox ---
  const filterChips = document.querySelectorAll('.filter-chip');
  const galleryItems = document.querySelectorAll('.gallery-item');
  const dialog = document.getElementById('gallery-dialog');

  if (filterChips.length > 0 && galleryItems.length > 0) {
    filterChips.forEach(chip => {
      chip.addEventListener('click', () => {
        filterChips.forEach(c => {
          c.classList.remove('active', 'bg-teal-900', 'text-white');
          c.classList.add('bg-white', 'dark:bg-white/5', 'text-ink-500', 'dark:text-paper-100', 'border', 'border-line', 'dark:border-white/10');
        });
        chip.classList.add('active', 'bg-teal-900', 'text-white');
        chip.classList.remove('bg-white', 'dark:bg-white/5', 'text-ink-500', 'dark:text-paper-100', 'border', 'border-line', 'dark:border-white/10');

        const filter = chip.dataset.filter;

        galleryItems.forEach(item => {
          if (filter === 'all' || item.dataset.tag === filter) {
            item.style.display = 'block';
            setTimeout(() => item.style.opacity = '1', 50);
          } else {
            item.style.opacity = '0';
            setTimeout(() => item.style.display = 'none', 300);
          }
        });
      });
    });

    galleryItems.forEach(item => {
      item.addEventListener('click', () => {
        document.getElementById('dialog-img').src = item.dataset.img;
        document.getElementById('dialog-title').textContent = item.dataset.title;
        document.getElementById('dialog-tag').textContent = item.dataset.tag;
        if (typeof dialog.showModal === "function") {
          dialog.showModal();
        } else {
          alert("The dialog API is not supported in this browser.");
        }
      });
    });

    document.getElementById('close-dialog').addEventListener('click', () => dialog.close());
    
    dialog.addEventListener('click', (e) => {
      if (e.target === dialog) {
        dialog.close();
      }
    });
  }

  // --- 4. Testimonials Center Focus Carousel ---
  const testTrack = document.getElementById('testimonials-track');
  const testCards = document.querySelectorAll('.testimonial-card');
  const testCounter = document.getElementById('test-counter');
  
  if (testTrack && testCards.length > 0) {
    const updateTestimonialFocus = () => {
      const trackCenter = testTrack.scrollLeft + testTrack.offsetWidth / 2;
      let closestCard = null;
      let minDistance = Infinity;

      testCards.forEach(card => {
        const cardCenter = card.offsetLeft + card.offsetWidth / 2;
        const distance = Math.abs(trackCenter - cardCenter);
        
        if (distance < minDistance) {
          minDistance = distance;
          closestCard = card;
        }
        
        card.classList.remove('focused', 'dimmed');
        card.classList.add('dimmed');
      });

      if (closestCard) {
        closestCard.classList.remove('dimmed');
        closestCard.classList.add('focused');
        const index = closestCard.dataset.index;
        if (testCounter) testCounter.textContent = `${parseInt(index) + 1} / ${testCards.length}`;
      }
    };

    let scrollTimeout;
    testTrack.addEventListener('scroll', () => {
      clearTimeout(scrollTimeout);
      scrollTimeout = setTimeout(updateTestimonialFocus, 50);
    }, { passive: true });

    setTimeout(updateTestimonialFocus, 100);

    document.getElementById('prev-test').addEventListener('click', () => {
      testTrack.scrollBy({ left: -380, behavior: 'smooth' });
    });
    document.getElementById('next-test').addEventListener('click', () => {
      testTrack.scrollBy({ left: 380, behavior: 'smooth' });
    });

    testCards.forEach(card => {
      card.addEventListener('click', () => {
        const offset = card.offsetLeft - (testTrack.offsetWidth / 2) + (card.offsetWidth / 2);
        testTrack.scrollTo({ left: offset, behavior: 'smooth' });
      });
    });
  }
});