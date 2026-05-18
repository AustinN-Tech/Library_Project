import * as pdfjsLib from "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/5.4.149/pdf.mjs";

pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/5.4.149/pdf.worker.mjs'; // handles heavy PDF work in the background, necessary for smooth viewing

// Defining Page/PDF Variables:
let pdf_doc = null;
let page_counter = 1; // keeps track of current page number
const min_page = 1;
let max_page = 1;
let scale = 1.25; // controls zoom of PDF

let canvas = document.querySelector("canvas"); // html drawing surface, pdf.js draws pdfs onto canvas
const context = canvas.getContext('2d'); // "drawing tool" for the canvas

let page_num = document.querySelector(".page_number") // shows current page num on webpage
let page_max = document.querySelector(".page_max");
const previous_button = document.querySelector(".previous");
const next_button = document.querySelector(".next");


pdfjsLib.getDocument({ url: pdf_URL}).promise.then((pdf) => { // loading PDF doc takes time, must be a promise
    console.log("PDF loaded.");

    pdf_doc = pdf; // load pdf into variable to reuse
    max_page = pdf.numPages;
    load_page(page_counter);
});

function load_page(page_number) {
    pdf_doc.getPage(page_number).then((page) => { // loading page takes time, must be a promise
        console.log("PDF loaded.");

        let viewport = page.getViewport( {scale: scale}); // viewport defines how PDF should appear

        // set canvas dimensions to page viewport: canvas matches page size
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        let renderContext = { // tells PDF.js to draw on the canvas using appropriate context, matching viewport
            canvasContext: context,
            viewport: viewport
        };
        let renderTask = page.render(renderContext); // draws PDF page on canvas
        renderTask.promise.then(() => { // render takes time, must be a promise
            console.log('Page rendered.');
            page_num.placeholder = `${page_number}`; // updates page counter
            page_max.textContent = `/ ${max_page}`;
        });
    }); 
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

page_num.addEventListener("keydown", () => { // allows users to jump to requested page number
    if (event.key === "Enter") {
        let entered_page = Number(page_num.value);

        if ((entered_page >= 1) && (entered_page <= max_page)) {
            load_page(entered_page);
            page_num.placeholder = `${entered_page}`;
            page_counter = entered_page; // update page_counter
        }
    }
})