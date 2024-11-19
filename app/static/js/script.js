document.addEventListener("DOMContentLoaded", function () {
    const text = "Hello, World!"; // Text to type out
    const typingSpeed = 200; // Milliseconds per character
    const cursorBlinkSpeed = 500; // Milliseconds for cursor blink

    const textElement = document.getElementById("typewriter-text");
    const cursorElement = document.getElementById("cursor");

    let index = 0;

    // Function to type out the text
    function typeText() {
        if (index < text.length) {
            textElement.textContent += text.charAt(index);
            index++;
            setTimeout(typeText, typingSpeed);
        } 
    }

    // Function to make the cursor blink
    function blinkCursor() {
        cursorElement.style.visibility =
            cursorElement.style.visibility === "hidden" ? "visible" : "hidden";
    }

    // Start typing and cursor blinking
    setTimeout(typeText, 100); // Delay before typing starts
    setInterval(blinkCursor, cursorBlinkSpeed);
});
