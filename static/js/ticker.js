// Duplicate the ticker's children so the -50% keyframe loops seamlessly.
(function () {
  const track = document.getElementById('trust-ticker');
  if (!track) return;
  track.innerHTML += track.innerHTML;
})();