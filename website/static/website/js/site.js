const menuBtn = document.querySelector('.menu-btn');
const navLinks = document.querySelector('.nav-links');

function updateMenuButton(isOpen) {
    menuBtn.setAttribute('aria-expanded', String(isOpen));
    menuBtn.setAttribute('aria-label', isOpen ? 'Close navigation menu' : 'Open navigation menu');
    menuBtn.textContent = isOpen ? '×' : '☰';
}

function setMenuState() {
    const isMobile = window.innerWidth <= 900;
    menuBtn.style.display = isMobile ? 'block' : 'none';
    if (!isMobile) {
        navLinks.classList.remove('active');
        navLinks.style.display = 'flex';
    } else {
        navLinks.style.display = navLinks.classList.contains('active') ? 'flex' : 'none';
    }
    updateMenuButton(isMobile && navLinks.classList.contains('active'));
}

function toggleMenu() {
    if (window.innerWidth > 900) return;
    navLinks.classList.toggle('active');
    navLinks.style.display = navLinks.classList.contains('active') ? 'flex' : 'none';
    updateMenuButton(navLinks.classList.contains('active'));
}

window.addEventListener('resize', setMenuState);
setMenuState();

document.querySelectorAll('.nav-links a').forEach(function(link) {
    link.addEventListener('click', function() {
        if (window.innerWidth <= 900) {
            navLinks.classList.remove('active');
            navLinks.style.display = 'none';
            updateMenuButton(false);
        }
    });
});

function getLastSunday(year, month) {
    let date = new Date(year, month + 1, 0);
    while (date.getDay() !== 0) {
        date.setDate(date.getDate() - 1);
    }
    return date;
}

function getNextEventDate() {
    const eventDateElement = document.getElementById("event-date");
    if (!eventDateElement) return;

    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    let year = today.getFullYear();
    let month = today.getMonth();

    let eventDate = getLastSunday(year, month);

    if (today > eventDate) {
        month++;

        if (month > 11) {
            month = 0;
            year++;
        }

        eventDate = getLastSunday(year, month);
    }

    let day = eventDate.getDate();
    let suffix = day % 100 >= 11 && day % 100 <= 13
        ? "TH"
        : ["TH", "ST", "ND", "RD"][day % 10] || "TH";

    let months = [
        "JANUARY", "FEBRUARY", "MARCH",
        "APRIL", "MAY", "JUNE",
        "JULY", "AUGUST", "SEPTEMBER",
        "OCTOBER", "NOVEMBER", "DECEMBER"
    ];

    eventDateElement.textContent =
        day + suffix + " OF " + months[eventDate.getMonth()] + " " + year;
}

function scheduleEventDateUpdate() {
    if (!document.getElementById("event-date")) return;

    const now = new Date();
    const tomorrow = new Date(now.getFullYear(), now.getMonth(), now.getDate() + 1);

    window.setTimeout(function() {
        getNextEventDate();
        scheduleEventDateUpdate();
    }, tomorrow - now);
}

document.addEventListener("visibilitychange", function() {
    if (!document.hidden) {
        getNextEventDate();
    }
});

getNextEventDate();
scheduleEventDateUpdate();
