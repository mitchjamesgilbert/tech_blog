document.addEventListener("DOMContentLoaded", function () {
    const text = "Te amo Laura!"; // Text to type out
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

document.addEventListener("DOMContentLoaded", function () {
    const searchBar = document.getElementById("search-bar");
    const postsList = document.getElementById("posts-list");
    const posts = Array.from(postsList.getElementsByClassName("post-item"));

    searchBar.addEventListener("input", function () {
        const query = searchBar.value.toLowerCase();

        posts.forEach((post) => {
            const title = post.dataset.title; // Title of the post
            const content = post.dataset.content; // Content snippet of the post

            // Check if query matches title or content
            if (title.includes(query) || content.includes(query)) {
                post.style.display = ""; // Show matching posts
            } else {
                post.style.display = "none"; // Hide non-matching posts
            }
        });
    });
});
