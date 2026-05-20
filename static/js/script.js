document.addEventListener("DOMContentLoaded", () => {
    const semesterSubjects = {
        1: ["Common Subjects for All Departments"],
        2: ["Common Subjects for All Departments"],
        3: ["Mathematical Foundation for Computing Sciences", "Digital Logic Design", "Problem Solving Using Data Structures", "Bio-Inspired Design and Innovation"],
        4: ["Discrete Mathematics and Graph Theory", "Computer Architecture with ARM", "Object-Oriented Programming", "Operating System"],
        5: ["Software Engineering and Project Management", "Design and Analysis of Algorithms", "Database Management Systems", "Professional Elective Course-I", "Research Methodology and IPR", "Critical and Creative Thinking Skills", "Environmental Studies"],
        6: ["Data Mining and Machine Learning", "Computer Networks", "Cyber Security Essentials", "Professional Elective Course-II"],
        7: ["Update Soon..."],
        8: ["Update Soon..."]
    };

    const subjectModules = {
        "Mathematical Foundation for Computing Sciences": ["Module 1", "Module 2", "Module 3", "Module 4", "Module 5"],
        "Digital Logic Design": ["Module 1", "Module 2", "Module 3", "Module 4", "Module 5"],
        "Problem Solving Using Data Structures": ["Module 1", "Module 2", "Module 3", "Module 4", "Module 5"]
    };

    const youtubeLinks = {
        "Mathematical Foundation for Computing Sciences Module 1": "https://youtube.com/playlist?list=PLsptxgQdqTVfS_6tg6DpbOqHlI0JLIpOj",
        "Digital Logic Design Module 1": "https://youtube.com/playlist?list=PLxCzCOWd7aiGmXg4NoX6R31AsC5LeCPHe",
        "Problem Solving Using Data Structures Module 1": "https://youtube.com/playlist?list=PLV7MgHu4-vg2nPMDVdNkkbdDQNQwRAcPC"
    };

    const interactionRoot = document.querySelector(".container");
    const subjectSelection = document.getElementById("subject-selection");
    const moduleSelection = document.getElementById("module-selection");
    const moduleName = document.getElementById("module-name");
    const youtubeLink = document.getElementById("youtube-link");
    const searchInput = document.getElementById("search-query");
    const searchSuggestions = document.getElementById("search-suggestions");

    if (interactionRoot) {
        interactionRoot.addEventListener("click", (event) => {
            const target = event.target.closest(".semester-button, .subject-button, .module-button");
            if (!target) return;

            if (target.classList.contains("semester-button")) {
                showSubjects(target.dataset.semester);
            } else if (target.classList.contains("subject-button")) {
                showModules(target.dataset.subject);
            } else if (target.classList.contains("module-button")) {
                showModuleDetails(target.dataset.subject, target.dataset.module);
            }
        });
    }

    function showSubjects(semester) {
        const subjects = semesterSubjects[semester] || [];
        subjectSelection.innerHTML = `<h3>Subjects for Semester ${semester}</h3>${subjects
            .map((subject) => `<button type="button" class="subject-button" data-subject="${subject}">${subject}</button>`)
            .join("")}`;
        moduleSelection.innerHTML = "";
        moduleName.textContent = "";
        youtubeLink.innerHTML = "";
        subjectSelection.scrollIntoView({ behavior: "smooth" });
    }

    function showModules(subject) {
        const modules = subjectModules[subject] || ["No Modules Available"];
        moduleSelection.innerHTML = `<h3>Modules for ${subject}</h3>${modules
            .map((module) => `<button type="button" class="module-button" data-subject="${subject}" data-module="${module}">${module}</button>`)
            .join("")}`;
        moduleSelection.scrollIntoView({ behavior: "smooth" });
    }

    function showModuleDetails(subject, module) {
        const selectedModuleName = `${subject} ${module}`;
        const selectedYoutubeLink = youtubeLinks[selectedModuleName] || "#";
        moduleName.textContent = selectedModuleName;
        youtubeLink.innerHTML = selectedYoutubeLink !== "#"
            ? `<a href="${selectedYoutubeLink}" target="_blank" rel="noopener noreferrer">Watch on YouTube</a>`
            : "<p>No video link available.</p>";
        moduleName.scrollIntoView({ behavior: "smooth" });
    }

    const debounce = (fn, delay) => {
        let timerId;
        const debounced = (...args) => {
            clearTimeout(timerId);
            timerId = setTimeout(() => fn(...args), delay);
        };
        debounced.cancel = () => clearTimeout(timerId);
        return debounced;
    };

    const loadSuggestions = debounce(async (query) => {
        if (!query || query.length < 2) {
            searchSuggestions.innerHTML = "";
            return;
        }

        try {
            const response = await fetch(`/api/search_suggestions?query=${encodeURIComponent(query)}`);
            if (!response.ok) return;
            const suggestions = await response.json();
            if (!suggestions.length) {
                searchSuggestions.innerHTML = "";
                return;
            }
            searchSuggestions.innerHTML = suggestions
                .map((name) => `<p><button type="button" class="suggestion-button" data-value="${name}">${name}</button></p>`)
                .join("");
        } catch (error) {
            console.error("Failed to fetch suggestions:", error);
            searchSuggestions.innerHTML = "";
        }
    }, 250);

    if (searchInput && searchSuggestions) {
        searchInput.addEventListener("input", () => loadSuggestions(searchInput.value.trim()));
        searchSuggestions.addEventListener("click", (event) => {
            const target = event.target.closest(".suggestion-button");
            if (!target) return;
            searchInput.value = target.dataset.value;
            searchSuggestions.innerHTML = "";
            searchInput.focus();
        });
        window.addEventListener("pagehide", () => loadSuggestions.cancel());
    }
});
