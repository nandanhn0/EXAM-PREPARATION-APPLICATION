document.addEventListener("DOMContentLoaded", function () {
    // Semester handling
    const semesterButtons = document.querySelectorAll("#semester-selection button");
    semesterButtons.forEach(button => {
        button.addEventListener("click", function () {
            const semester = button.textContent.split(' ')[1];
            showSubjects(semester);
        });
    });

    // Function to dynamically show subjects based on semester
    function showSubjects(semester) {
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

        const subjects = semesterSubjects[semester];
        let subjectHTML = `<h3>Subjects for Semester ${semester}</h3>`;

        subjects.forEach(subject => {
            subjectHTML += `<button class="subject-button" data-subject="${subject}">${subject}</button>`;
        });

        document.getElementById("subject-selection").innerHTML = subjectHTML;

        // Scroll to the subject selection section
        document.getElementById('subject-selection').scrollIntoView({ behavior: 'smooth' });

        const subjectButtons = document.querySelectorAll(".subject-button");
        subjectButtons.forEach(button => {
            button.addEventListener("click", function () {
                const subject = button.dataset.subject;
                showModules(subject);
            });
        });
    }

    // Function to dynamically show modules based on the subject
    function showModules(subject) {
        const subjectModules = {
            "Mathematical Foundation for Computing Sciences": ["Module 1", "Module 2", "Module 3", "Module 4", "Module 5"],
            "Digital Logic Design": ["Module 1", "Module 2", "Module 3", "Module 4", "Module 5"],
            "Problem Solving Using Data Structures": ["Module 1", "Module 2", "Module 3", "Module 4", "Module 5"]
            // Extend this for all subjects
        };

        const modules = subjectModules[subject] || ["No Modules Available"];
        let moduleHTML = `<h3>Modules for ${subject}</h3>`;

        modules.forEach(module => {
            moduleHTML += `<button class="module-button" data-module="${module}">${module}</button>`;
        });

        document.getElementById("module-selection").innerHTML = moduleHTML;

        // Scroll to the module selection section
        document.getElementById('module-selection').scrollIntoView({ behavior: 'smooth' });

        const moduleButtons = document.querySelectorAll(".module-button");
        moduleButtons.forEach(button => {
            button.addEventListener("click", function () {
                const module = button.dataset.module;
                showModuleDetails(subject, module);
            });
        });
    }

    // Function to display module details and YouTube link
    function showModuleDetails(subject, module) {
        const youtubeLinks = {
            "Mathematical Foundation for Computing Sciences Module 1": "https://youtube.com/playlist?list=PLsptxgQdqTVfS_6tg6DpbOqHlI0JLIpOj",
            "Digital Logic Design Module 1": "https://youtube.com/playlist?list=PLxCzCOWd7aiGmXg4NoX6R31AsC5LeCPHe",
            "Problem Solving Using Data Structures Module 1": "https://youtube.com/playlist?list=PLV7MgHu4-vg2nPMDVdNkkbdDQNQwRAcPC"
            // Extend this for all subjects and modules
        };

        const moduleName = `${subject} ${module}`;
        const youtubeLink = youtubeLinks[moduleName] || "#";

        document.getElementById("module-name").textContent = moduleName;
        document.getElementById("youtube-link").innerHTML = youtubeLink !== "#"
            ? `<a href="${youtubeLink}" target="_blank">Watch on YouTube</a>`
            : `<p>No video link available.</p>`;

        // Scroll to the module details section
        document.getElementById('module-name').scrollIntoView({ behavior: 'smooth' });
    }
});
