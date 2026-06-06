import * as pdfjsLib from "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/5.4.149/pdf.mjs";

pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/5.4.149/pdf.worker.mjs'; // handles heavy PDF work in the background, necessary for smooth viewing

// Defining Page/PDF Variables:
let pdf_doc = null;
let page_counter = 1; // keeps track of current page number
const min_page = 1;
let max_page = 1;
let unscaled_viewport = null;
let scaled_viewport = null;

let canvas = document.querySelector("canvas"); // html drawing surface, pdf.js draws pdfs onto canvas
const context = canvas.getContext('2d'); // "drawing tool" for the canvas

let page_num = document.querySelector(".page_number") // shows current page num on webpage
let page_max = document.querySelector(".page_max");
const previous_button = document.querySelector(".previous");
const next_button = document.querySelector(".next");

const canvas_container = document.querySelector(".canvas_container");

const mobile_query = window.matchMedia("(max-width: 1024px)");

pdfjsLib.getDocument({ url: pdf_URL}).promise // loading PDF doc takes time, must be a promise
    .then(
        (pdf) => { 
            console.log("PDF loaded.");

            pdf_doc = pdf; // load pdf into variable to reuse
            max_page = pdf.numPages;
            load_page(page_counter);
        },
    )
    .catch( // error handling
        (error) => {
            console.log("PDF loading failed.");
            console.error(error);
            // update HTML to show "PDF loading failed..."
        }
    );

function load_page(page_number) {
    pdf_doc.getPage(page_number) // returns a promise
    .then(
        (page) => {
            console.log("PDF loaded.");

            let unscaled_viewport = page.getViewport({scale: 1}); // viewport defines how PDF should appear

            if (mobile_query.matches) scaled_viewport = scale_viewport_mobile(canvas_container, unscaled_viewport, page);
            else scaled_viewport = scale_viewport_desktop(canvas_container, unscaled_viewport, page);

            canvas.width = scaled_viewport.width;
            canvas.height = scaled_viewport.height;

            let renderContext = { // tells PDF.js to draw on the canvas using appropriate context, matching viewport
                canvasContext: context,
                viewport: scaled_viewport
            };
            let renderTask = page.render(renderContext); // draws PDF page on canvas
            renderTask.promise.then(() => { // render takes time, must be a promise
                console.log('Page rendered.');
                page_num.placeholder = `${page_number}`; // updates page counter
                page_max.textContent = `/ ${max_page}`;
            });
        },
    )
    .catch( // error handling
        (error) => {
            console.log("Page loading failed.");
            console.error(error);
            // update HTML to show "Page loading failed..."
        }
    );
}

window.addEventListener("resize", () => { // Dynamically rerenders upon window resizing
    load_page(page_counter);
})

function scale_viewport_mobile(canvas_container, unscaled_viewport, page) {
    console.log("Scaling mobile...")
    // Scaling PDF viewport to make pdf viewing consistent across different PDFs and screens
    let container_height = canvas_container.clientHeight; // container height = 70% of user viewport (on mobile)
    let scale = container_height/unscaled_viewport.height; // update scale based on container
    scaled_viewport = page.getViewport( {scale: scale}); // scale pdf viewport (pdf display size) scaled to container
    return scaled_viewport;
}

function scale_viewport_desktop(canvas_container, unscaled_viewport, page) {
    console.log("Scaling desktop...")
    // Scaling PDF viewport to make pdf viewing consistent across different PDFs and screens
    let container_width = canvas_container.clientWidth; // container width = 60% of user viewport (on desktop)
    let scale = container_width/unscaled_viewport.width; // update scale based on container
    scaled_viewport = page.getViewport( {scale: scale}); // scale pdf viewport (pdf display size) scaled to container
    return scaled_viewport;
}

previous_button.addEventListener("click", () => {
    if (page_counter > min_page) {
        load_page(--page_counter);
        page_num.value = ""; // get rid of inputted value so placeholder (which tracks the page counter) is visible
    }
});

next_button.addEventListener("click", () => {
    if (page_counter < max_page) {
        load_page(++page_counter);
        page_num.value = "";
    }
});

// Arrow Key Navigation
document.addEventListener("keydown", () => {
    if (event.key === "ArrowRight") {
        if (page_counter < max_page) {
            load_page(++page_counter);
            page_num.value = "";
        }
    }
    else if (event.key === "ArrowLeft") {
        if (page_counter > min_page) {
            load_page(--page_counter);
            page_num.value = ""; 
        }
    }
});

/*
NOTE: bug found if input contains letters and numbers, it will default to NaN and break the PDF page loading via previous/next buttons.
*/
page_num.addEventListener("keydown", () => { // allows users to jump to requested page number
    if (event.key === "Enter") {
        let entered_page = Number(page_num.value);

        // Bounds checking
        if (entered_page < 1) entered_page = 1;
        else if (entered_page > max_page) entered_page = max_page;
        page_num.value = entered_page; // update page number (for if entered_page was adjusted because it was out of bounds)

        load_page(entered_page);
        page_num.placeholder = `${entered_page}`;
        page_counter = entered_page; // update page_counter
    }
})