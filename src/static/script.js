const ext_buttons = document.querySelectorAll(".extra_actions_button"); // returns static list of buttons


ext_buttons.forEach(button => { // "forEach", essentially iterates through list and applies a function
    button.addEventListener("click", () => { // function being applied (listener for clicks)
        const card = button.closest(".book_card"); // gets parent container ()
        const dropdown = card.querySelector(".extra_actions_dropdown"); // obtain dropdown to local card

        dropdown.classList.toggle("hidden"); // toggle hidden class to hide or show dropdown
    });
});

const cover_uploads = document.querySelectorAll(".cover_file"); // selecting all cover file inputs across change cover forms

// To submit cover file automatically, without upload button:
cover_uploads.forEach(file_upload => {
    file_upload.addEventListener("change", () => {
        const form = file_upload.closest(".change_cover"); // get local change_cover form

        const file = form.cover_file.files[0]; // files always returns a list, accessing first element (only element)
        if (!file) { // check if file is there
            return;
        }
        form.requestSubmit(); // automatically submits form
    })
})