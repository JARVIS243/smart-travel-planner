// NAVBAR SCROLL EFFECT
window.addEventListener("scroll", function () {

    const navbar = document.querySelector(".custom-navbar");

    if (window.scrollY > 50) {

        navbar.style.background =
            "linear-gradient(90deg,#000814,#023e8a)";

        navbar.style.boxShadow =
            "0 5px 20px rgba(0,0,0,0.3)";

        navbar.style.padding = "10px 0";

    }

    else {

        navbar.style.background =
            "linear-gradient(90deg,#001f3f,#0077b6)";

        navbar.style.boxShadow = "none";

        navbar.style.padding = "15px 0";

    }

});


// CARD ANIMATION
const cards = document.querySelectorAll(
    ".destination-card, .feature-box, .booking-card, .itinerary-box, .update-box"
);

window.addEventListener("scroll", revealCards);

function revealCards() {

    const triggerBottom = window.innerHeight * 0.85;

    cards.forEach(card => {

        const cardTop = card.getBoundingClientRect().top;

        if (cardTop < triggerBottom) {

            card.style.opacity = "1";
            card.style.transform = "translateY(0px)";

        }

    });

}


// INITIAL STYLE
cards.forEach(card => {

    card.style.opacity = "0";
    card.style.transform = "translateY(50px)";
    card.style.transition = "all 0.8s ease";

});


// HERO TEXT ANIMATION
window.addEventListener("load", () => {

    const heroTitle = document.querySelector(".hero-title");
    const heroText = document.querySelector(".hero-text");

    if(heroTitle){

        heroTitle.style.opacity = "0";
        heroTitle.style.transform = "translateY(40px)";

        heroText.style.opacity = "0";
        heroText.style.transform = "translateY(40px)";

        setTimeout(() => {

            heroTitle.style.transition = "1s";
            heroTitle.style.opacity = "1";
            heroTitle.style.transform = "translateY(0px)";

        }, 300);

        setTimeout(() => {

            heroText.style.transition = "1s";
            heroText.style.opacity = "1";
            heroText.style.transform = "translateY(0px)";

        }, 700);

    }

});