// ========================================
// AI RESUME ANALYZER - JAVASCRIPT
// ========================================


// ================================
// FILE UPLOAD
// ================================

const resumeFile = document.getElementById("resumeFile");
const fileName = document.getElementById("fileName");

resumeFile.addEventListener("change", function () {

    if (resumeFile.files.length > 0) {

        const file = resumeFile.files[0];

        fileName.textContent = file.name;
        fileName.style.color = "#42d392";

    } else {

        fileName.textContent = "No file selected";
        fileName.style.color = "#8495aa";

    }

});


// ================================
// ANALYZE BUTTON
// ================================

const analyzeBtn =
    document.getElementById("analyzeBtn");


analyzeBtn.addEventListener("click", async function () {

    const file =
        resumeFile.files[0];


    const jobDescription =
        document
        .getElementById("jobDescription")
        .value
        .trim();


    // ----------------------------
    // CHECK RESUME
    // ----------------------------

    if (!file) {

        alert(
            "Please upload your resume first."
        );

        return;
    }


    // ----------------------------
    // CHECK FILE TYPE
    // ----------------------------

    const fileNameLower =
        file.name.toLowerCase();


    if (
        !fileNameLower.endsWith(".pdf") &&
        !fileNameLower.endsWith(".docx")
    ) {

        alert(
            "Please upload a PDF or DOCX file."
        );

        return;
    }


    // ----------------------------
    // CHECK FILE SIZE
    // ----------------------------

    const maxSize =
        5 * 1024 * 1024;


    if (file.size > maxSize) {

        alert(
            "File size must be less than 5 MB."
        );

        return;
    }


    // ----------------------------
    // CHECK JOB DESCRIPTION
    // ----------------------------

    if (!jobDescription) {

        alert(
            "Please enter the job description."
        );

        return;
    }


    // ----------------------------
    // CREATE FORM DATA
    // ----------------------------

    const formData =
        new FormData();


    formData.append(
        "resume",
        file
    );


    formData.append(
        "job_description",
        jobDescription
    );


    // ----------------------------
    // BUTTON LOADING
    // ----------------------------

    analyzeBtn.textContent =
        "Analyzing...";

    analyzeBtn.disabled = true;


    try {

        // ----------------------------
        // SEND RESUME TO FLASK
        // ----------------------------

        const response =
            await fetch("/analyze", {

                method: "POST",

                body: formData

            });


        // ----------------------------
        // CONVERT RESPONSE TO JSON
        // ----------------------------

        const result =
            await response.json();


        // ----------------------------
        // CHECK RESULT
        // ----------------------------

        if (!result.success) {

            alert(
                result.message ||
                "Analysis failed."
            );

            analyzeBtn.textContent =
                "Analyze Resume";

            analyzeBtn.disabled = false;

            return;
        }


        // ----------------------------
        // DISPLAY RESULTS
        // ----------------------------

        displayResults(result);


        // ----------------------------
        // BUTTON SUCCESS
        // ----------------------------

        analyzeBtn.textContent =
            "Analysis Complete ✓";

        analyzeBtn.style.background =
            "#42d392";


    } catch (error) {

        console.error(
            "Error:",
            error
        );


        alert(
            "Something went wrong while analyzing the resume."
        );


        analyzeBtn.textContent =
            "Analyze Resume";

        analyzeBtn.style.background =
            "";

    }


    analyzeBtn.disabled = false;

});


// ========================================
// DISPLAY ANALYSIS RESULTS
// ========================================

function displayResults(result) {


    // ----------------------------
    // SHOW RESULTS SECTION
    // ----------------------------

    const resultsSection =
        document.getElementById("results");


    if (resultsSection) {

        resultsSection.style.display =
            "block";

    }


    // ----------------------------
    // ATS SCORE
    // ----------------------------

    const atsScoreElement =
        document.getElementById("atsScore");


    if (atsScoreElement) {

        atsScoreElement.textContent =
            result.ats_score + "%";

    }


    // ----------------------------
    // JOB MATCH
    // ----------------------------

    const matchScoreElement =
        document.getElementById("matchScore");


    if (matchScoreElement) {

        matchScoreElement.textContent =
            result.matching_percentage + "%";

    }


    // ----------------------------
    // SKILLS COUNT
    // ----------------------------

    const skillsCountElement =
        document.getElementById("skillsCount");


    if (skillsCountElement) {

        skillsCountElement.textContent =
            result.skills.length;

    }


    // ========================================
    // UPDATE DASHBOARD
    // ========================================

    const dashboardATS =
        document.getElementById("dashboardATS");


    if (dashboardATS) {

        dashboardATS.textContent =
            result.ats_score + "%";

    }


    const dashboardMatch =
        document.getElementById("dashboardMatch");


    if (dashboardMatch) {

        dashboardMatch.textContent =
            result.matching_percentage + "%";

    }


    const dashboardSkills =
        document.getElementById("dashboardSkills");


    if (dashboardSkills) {

        dashboardSkills.textContent =
            result.skills.length;

    }


    const dashboardSuggestions =
        document.getElementById(
            "dashboardSuggestions"
        );


    if (dashboardSuggestions) {

        dashboardSuggestions.textContent =
            result.suggestions.length;

    }
    

    // ========================================
    // DETECTED SKILLS
    // ========================================

    const skillsList =
        document.getElementById(
            "skillsList"
        );


    if (skillsList) {

        skillsList.innerHTML = "";


        if (
            !result.skills ||
            result.skills.length === 0
        ) {

            skillsList.innerHTML =
                '<span class="empty-result">No skills detected.</span>';

        } else {

            result.skills.forEach(
                function (skill) {

                    const tag =
                        document.createElement(
                            "span"
                        );


                    tag.className =
                        "skill-tag";


                    tag.textContent =
                        skill;


                    skillsList.appendChild(
                        tag
                    );

                }
            );

        }

    }


    // ========================================
    // MISSING SKILLS
    // ========================================

    const missingSkillsList =
        document.getElementById(
            "missingSkillsList"
        );


    if (missingSkillsList) {

        missingSkillsList.innerHTML =
            "";


        if (
            !result.missing_skills ||
            result.missing_skills.length === 0
        ) {

            missingSkillsList.innerHTML =
                '<span class="empty-result">No missing skills detected.</span>';

        } else {

            result.missing_skills.forEach(
                function (skill) {

                    const tag =
                        document.createElement(
                            "span"
                        );


                    tag.className =
                        "skill-tag missing-tag";


                    tag.textContent =
                        skill;


                    missingSkillsList.appendChild(
                        tag
                    );

                }
            );

        }

    }


    // ========================================
    // MATCHED SKILLS
    // ========================================

    const matchedSkillsList =
        document.getElementById(
            "matchedSkillsList"
        );


    if (matchedSkillsList) {

        matchedSkillsList.innerHTML =
            "";


        if (
            !result.matched_skills ||
            result.matched_skills.length === 0
        ) {

            matchedSkillsList.innerHTML =
                '<span class="empty-result">No matching skills found.</span>';

        } else {

            result.matched_skills.forEach(
                function (skill) {

                    const tag =
                        document.createElement(
                            "span"
                        );


                    tag.className =
                        "skill-tag matched-tag";


                    tag.textContent =
                        skill;


                    matchedSkillsList.appendChild(
                        tag
                    );

                }
            );

        }

    }


    // ========================================
    // SUGGESTIONS
    // ========================================

    const suggestionsList =
        document.getElementById(
            "suggestionsList"
        );


    if (suggestionsList) {

        suggestionsList.innerHTML =
            "";


        if (
            !result.suggestions ||
            result.suggestions.length === 0
        ) {

            suggestionsList.innerHTML =
                '<li class="empty-result">No suggestions available.</li>';

        } else {

            result.suggestions.forEach(
                function (suggestion) {

                    const item =
                        document.createElement(
                            "li"
                        );


                    item.textContent =
                        suggestion;


                    suggestionsList.appendChild(
                        item
                    );

                }
            );

        }

    }


    // ========================================
    // UPDATE SUGGESTIONS COUNT
    // ========================================

    const suggestionsCountElement =
        document.getElementById(
            "dashboardSuggestions"
        );


    if (suggestionsCountElement) {

        suggestionsCountElement.textContent =
            result.suggestions.length;

    }


    // ========================================
    // SCROLL TO RESULTS
    // ========================================

    if (resultsSection) {

        resultsSection.scrollIntoView({

            behavior: "smooth"

        });

    }

}