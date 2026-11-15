document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("contact-form");
  const btn = document.getElementById("send-btn");
  const toast = document.getElementById("contact-toast");

  if (!form) return;

  function showToast(message, isSuccess) {
    // Set colors based on success/error
    const bgColor = isSuccess ? "bg-teal-500" : "bg-red-500";
    const icon = isSuccess 
      ? `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg>`
      : `<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path></svg>`;

    // Inject HTML
    toast.innerHTML = `
      <div class="${bgColor} text-white px-6 py-4 rounded-xl shadow-2xl flex items-center gap-3 font-medium">
        ${icon}
        <span>${message}</span>
      </div>
    `;

    // Slide in
    toast.classList.remove("translate-y-20", "opacity-0");
    toast.classList.add("translate-y-0", "opacity-100");

    // Slide out after 4 seconds
    setTimeout(() => {
      toast.classList.remove("translate-y-0", "opacity-100");
      toast.classList.add("translate-y-20", "opacity-0");
    }, 4000);
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Native browser validation check
    if (!form.checkValidity()) {
      form.reportValidity();
      return;
    }

    // Disable button & show loading state
    const originalBtnText = btn.textContent;
    btn.disabled = true;
    btn.textContent = "Sending...";

    // Gather data
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());

    try {
      const response = await fetch("/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      const data = await response.json();

      if (response.ok && data.ok) {
        showToast("Message sent successfully! I'll be in touch soon.", true);
        form.reset();
      } else {
        showToast(data.error || "Something went wrong. Please try again.", false);
      }
    } catch (error) {
      showToast("Network error. Please email me directly at lawrenceit38@gmail.com", false);
    } finally {
      // Re-enable button
      btn.disabled = false;
      btn.textContent = originalBtnText;
    }
  });
});