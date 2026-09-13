/* ==========================================
   PREDICTSITE JAVASCRIPT
   ========================================== */

document.addEventListener("DOMContentLoaded", function () {

    /* ==========================================
       ELEMENTS
       ========================================== */

    const symptomForm = document.getElementById("symptomForm");
    const searchInput = document.getElementById("searchSymptoms");
    const clearSearch = document.getElementById("clearSearch");
    const clearAll = document.getElementById("clearAll");
    const selectedCount = document.getElementById("selectedCount");
    const resultText = document.getElementById("resultText");
    const noResults = document.getElementById("noResults");
    const predictBtn = document.getElementById("predictBtn");

    const symptomCards = document.querySelectorAll(".symptom-card");


    /* ==========================================
       UPDATE SELECTED COUNT
       ========================================== */

    function updateCount() {

        const checkedSymptoms =
            document.querySelectorAll(
                ".symptom-card input[type='checkbox']:checked"
            );

        if (selectedCount) {
            selectedCount.textContent = checkedSymptoms.length;
        }

        if (predictBtn) {

            if (checkedSymptoms.length > 0) {

                predictBtn.style.opacity = "1";
                predictBtn.style.cursor = "pointer";

            } else {

                predictBtn.style.opacity = "0.75";
                predictBtn.style.cursor = "pointer";

            }
        }
    }


    /* ==========================================
       CHECKBOX CARD SELECTION
       ========================================== */

    symptomCards.forEach(function (card) {

        const checkbox =
            card.querySelector("input[type='checkbox']");

        checkbox.addEventListener("change", function () {

            if (checkbox.checked) {

                card.classList.add("selected");

            } else {

                card.classList.remove("selected");

            }

            updateCount();

        });

    });


    /* ==========================================
       SEARCH SYMPTOMS
       ========================================== */

    if (searchInput) {

        searchInput.addEventListener("input", function () {

            const searchValue =
                searchInput.value.toLowerCase().trim();

            let visibleCount = 0;

            symptomCards.forEach(function (card) {

                const symptomName =
                    card.getAttribute("data-name");

                if (
                    symptomName &&
                    symptomName.includes(searchValue)
                ) {

                    card.style.display = "flex";
                    visibleCount++;

                } else {

                    card.style.display = "none";

                }

            });


            /* SEARCH BUTTON */

            if (clearSearch) {

                if (searchValue.length > 0) {

                    clearSearch.style.display = "block";

                } else {

                    clearSearch.style.display = "none";

                }

            }


            /* RESULT TEXT */

            if (resultText) {

                if (searchValue.length === 0) {

                    resultText.textContent =
                        "Showing all symptoms";

                } else {

                    resultText.textContent =
                        "Found " +
                        visibleCount +
                        " symptom" +
                        (visibleCount === 1 ? "" : "s");

                }

            }


            /* NO RESULTS */

            if (noResults) {

                if (visibleCount === 0) {

                    noResults.style.display = "block";

                } else {

                    noResults.style.display = "none";

                }

            }

        });

    }


    /* ==========================================
       CLEAR SEARCH
       ========================================== */

    if (clearSearch) {

        clearSearch.addEventListener("click", function () {

            searchInput.value = "";

            symptomCards.forEach(function (card) {
                card.style.display = "flex";
            });

            clearSearch.style.display = "none";

            if (resultText) {
                resultText.textContent =
                    "Showing all symptoms";
            }

            if (noResults) {
                noResults.style.display = "none";
            }

            searchInput.focus();

        });

    }


    /* ==========================================
       CLEAR ALL SYMPTOMS
       ========================================== */

    if (clearAll) {

        clearAll.addEventListener("click", function () {

            symptomCards.forEach(function (card) {

                const checkbox =
                    card.querySelector(
                        "input[type='checkbox']"
                    );

                checkbox.checked = false;

                card.classList.remove("selected");

            });

            updateCount();

        });

    }


    /* ==========================================
       FORM VALIDATION
       ========================================== */

    if (symptomForm) {

        symptomForm.addEventListener("submit", function (event) {

            const checkedSymptoms =
                document.querySelectorAll(
                    ".symptom-card input[type='checkbox']:checked"
                );

            if (checkedSymptoms.length === 0) {

                event.preventDefault();

                alert(
                    "Please select at least one symptom before predicting."
                );

                return;

            }


            /* Loading state */

            if (predictBtn) {

                predictBtn.disabled = true;

                predictBtn.innerHTML =
                    `
                    <span>
                        Analyzing Symptoms...
                    </span>
                    <span class="arrow">
                        ⏳
                    </span>
                    `;

            }

        });

    }


    /* ==========================================
       INITIAL COUNT
       ========================================== */

    updateCount();


    /* ==========================================
       CONFIDENCE BAR ANIMATION
       ========================================== */

    const confidenceFill =
        document.querySelector(".confidence-fill");

    if (confidenceFill) {

        const targetWidth =
            confidenceFill.style.width;

        confidenceFill.style.width = "0%";

        setTimeout(function () {

            confidenceFill.style.width =
                targetWidth;

        }, 300);

    }


});