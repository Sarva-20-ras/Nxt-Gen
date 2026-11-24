const menuBtn = document.querySelector('.menu-btn');
const navLinks = document.querySelector('.nav-links');
const holidayDecorationsStart = new Date(2026, 10, 25);
const holidayDecorationsEnd = new Date(2026, 11, 31);
const currentDate = new Date();

function scheduleHolidayEnd(callback) {
    const remainingTime = holidayDecorationsEnd - new Date();
    if (remainingTime <= 0) {
        callback();
        return;
    }

    window.setTimeout(function() {
        scheduleHolidayEnd(callback);
    }, Math.min(remainingTime, 2147483647));
}

if (currentDate >= holidayDecorationsStart && currentDate < holidayDecorationsEnd) {
    document.documentElement.classList.add('holiday-decorations');
    scheduleHolidayEnd(function() {
        document.documentElement.classList.remove('holiday-decorations');
    });
}

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

function addChristmasSnowfall() {
    if (
        !document.documentElement.classList.contains('holiday-decorations')
        || window.matchMedia('(prefers-reduced-motion: reduce)').matches
    ) return;

    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    if (!context) return;

    canvas.className = 'christmas-snow';
    canvas.setAttribute('aria-hidden', 'true');
    document.body.appendChild(canvas);

    const flakes = [];
    const flakeCount = 48;
    let width = 0;
    let height = 0;
    let animationFrame;

    function resizeCanvas() {
        const pixelRatio = Math.min(window.devicePixelRatio || 1, 1.5);
        width = window.innerWidth;
        height = window.innerHeight;
        canvas.width = width * pixelRatio;
        canvas.height = height * pixelRatio;
        context.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    }

    for (let i = 0; i < flakeCount; i++) {
        flakes.push({
            x: Math.random() * window.innerWidth,
            y: Math.random() * window.innerHeight,
            radius: Math.random() * 1.8 + 0.8,
            speed: Math.random() * 0.7 + 0.35,
            drift: Math.random() * 0.5 - 0.25,
            opacity: Math.random() * 0.45 + 0.3,
        });
    }

    function drawSnowfall() {
        context.clearRect(0, 0, width, height);
        flakes.forEach(function(flake) {
            context.beginPath();
            context.fillStyle = 'rgba(255, 255, 255, ' + flake.opacity + ')';
            context.arc(flake.x, flake.y, flake.radius, 0, Math.PI * 2);
            context.fill();

            flake.y += flake.speed;
            flake.x += flake.drift;
            if (flake.y > height + flake.radius) {
                flake.y = -flake.radius;
                flake.x = Math.random() * width;
            }
            if (flake.x < -flake.radius) flake.x = width + flake.radius;
            if (flake.x > width + flake.radius) flake.x = -flake.radius;
        });
        animationFrame = window.requestAnimationFrame(drawSnowfall);
    }

    function stopSnowfall() {
        window.cancelAnimationFrame(animationFrame);
        window.removeEventListener('resize', resizeCanvas);
        document.removeEventListener('visibilitychange', handleVisibilityChange);
        canvas.remove();
    }

    function handleVisibilityChange() {
        if (document.hidden) {
            window.cancelAnimationFrame(animationFrame);
        } else {
            drawSnowfall();
        }
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    drawSnowfall();
    document.addEventListener('visibilitychange', handleVisibilityChange);
    scheduleHolidayEnd(stopSnowfall);
}

addChristmasSnowfall();

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
