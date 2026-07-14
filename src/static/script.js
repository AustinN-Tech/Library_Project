const ext_buttons = document.querySelectorAll(".extra_actions_button"); // returns static list of buttons
ext_buttons.forEach(button => { // "forEach", essentially iterates through list and applies a function
    button.addEventListener("click", () => { // function being applied (listener for clicks)
        const card = button.closest(".book_card"); // gets relative parent container ()
        const dropdown = card.querySelector(".extra_actions_dropdown"); // obtain dropdown to local card

        dropdown.classList.toggle("hidden"); // toggle hidden class to hide or show dropdown
    });
});

const dropdowns = document.querySelectorAll(".extra_actions_dropdown");
// Adding functionality that if clicked off from dropdown or dropdown button, dropdown automatically closes
document.querySelector("body").addEventListener("click", (event) => {
    const target = event.target; // obtain element that was clicked
    const close_dropdown = target.closest(".extra_actions_dropdown"); // get local dropdown
    const button = target.closest(".extra_actions_button"); // get local button

    if (close_dropdown===null && button===null) { // if button or dropdown was NOT clicked
        dropdowns.forEach(dropdown => {
            dropdown.classList.add("hidden"); // hide all dropdowns
        }); 
    }
})


const cover_button = document.querySelectorAll(".cover_button");
// To make it so clicking button opens file manager
cover_button.forEach(button => {
    button.addEventListener("click", () => {
        const form = button.closest(".change_cover"); // obtain local form
        const input = form.querySelector(".cover_file"); // get file input
        
        input.click(); // clicks input, which opens the file manager to submit a cover file
    })
})

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