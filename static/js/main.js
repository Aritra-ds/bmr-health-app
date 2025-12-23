/* =========================================================
   BMR HEALTH APP - MAIN JAVASCRIPT
   Connects all HTML pages for interactivity
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
    // -------------------- FORM VALIDATIONS --------------------
    const forms = document.querySelectorAll(".form-card");
    forms.forEach((form) => {
        form.addEventListener("submit", (e) => {
            const inputs = form.querySelectorAll("input, select");
            let valid = true;

            inputs.forEach((input) => {
                if (!input.value.trim()) {
                    valid = false;
                    input.classList.add("input-error");
                } else {
                    input.classList.remove("input-error");
                }
            });

            if (!valid) {
                e.preventDefault();
                alert("Please fill in all required fields.");
            }
        });
    });

    // -------------------- ADD INPUT HIGHLIGHT --------------------
    const allInputs = document.querySelectorAll("input, select");
    allInputs.forEach((input) => {
        input.addEventListener("focus", () => {
            input.style.borderColor = "#00b4d8";
        });
        input.addEventListener("blur", () => {
            input.style.borderColor = "#ccc";
        });
    });

    // -------------------- SMOOTH SCROLL FOR LINKS --------------------
    const navLinks = document.querySelectorAll("a[href^='#']");
    navLinks.forEach((link) => {
        link.addEventListener("click", (e) => {
            e.preventDefault();
            const target = document.querySelector(link.getAttribute("href"));
            if (target) {
                target.scrollIntoView({ behavior: "smooth" });
            }
        });
    });

    // -------------------- BUTTON INTERACTIVE EFFECT --------------------
    const buttons = document.querySelectorAll(".btn");
    buttons.forEach((btn) => {
        btn.addEventListener("mouseenter", () => {
            btn.style.transform = "translateY(-2px)";
            btn.style.boxShadow = "0 4px 10px rgba(0,0,0,0.2)";
        });
        btn.addEventListener("mouseleave", () => {
            btn.style.transform = "translateY(0)";
            btn.style.boxShadow = "none";
        });
    });

    // -------------------- RESULT CARD ANIMATION --------------------
    const resultCards = document.querySelectorAll(".result-card");
    resultCards.forEach((card) => {
        card.style.opacity = 0;
        card.style.transform = "translateY(20px)";
        setTimeout(() => {
            card.style.transition = "all 0.6s ease";
            card.style.opacity = 1;
            card.style.transform = "translateY(0)";
        }, 100);
    });

    // -------------------- PASSWORD TOGGLE FOR LOGIN/REGISTER --------------------
    const passwordFields = document.querySelectorAll('input[type="password"]');
    passwordFields.forEach((field) => {
        const toggleBtn = document.createElement("span");
        toggleBtn.textContent = "👁️";
        toggleBtn.style.cursor = "pointer";
        toggleBtn.style.marginLeft = "5px";
        toggleBtn.title = "Show/Hide Password";
        field.parentNode.appendChild(toggleBtn);

        toggleBtn.addEventListener("click", () => {
            if (field.type === "password") {
                field.type = "text";
            } else {
                field.type = "password";
            }
        });
    });

    // -------------------- TOAST NOTIFICATIONS FOR MESSAGES --------------------
    const messages = document.querySelectorAll(".result-card p, .form-card p");
    messages.forEach((msg) => {
        msg.style.transition = "all 0.5s ease";
        setTimeout(() => {
            msg.style.backgroundColor = "#00b4d8";
            msg.style.color = "#fff";
            msg.style.padding = "0.5rem";
            msg.style.borderRadius = "6px";
        }, 100);
    });

    // -------------------- OPTIONAL: SMOOTH FADE-IN FOR SECTIONS --------------------
    const sections = document.querySelectorAll(".main-content section");
    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = 1;
                    entry.target.style.transform = "translateY(0)";
                    entry.target.style.transition = "all 0.8s ease-out";
                } else {
                    entry.target.style.opacity = 0;
                    entry.target.style.transform = "translateY(20px)";
                }
            });
        },
        { threshold: 0.1 }
    );

    sections.forEach((section) => {
        section.style.opacity = 0;
        section.style.transform = "translateY(20px)";
        observer.observe(section);
    });
});
