import * as pdfjsLib from "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/5.4.149/pdf.mjs";

pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/5.4.149/pdf.worker.mjs'; // handles heavy PDF work in the background, necessary for smooth viewing

// Defining Page/PDF Variables:
let pdf_doc = null;
let page_number = 1;
const min_page = 1;
let max_page = 1;
let scale = 1.5; // controls zoom of PDF

let canvas = document.querySelector("canvas"); // html drawing surface, pdf.js draws pdfs onto canvas
const context = canvas.getContext('2d'); // "drawing tool" for the canvas

let page_text = document.querySelector(".page_number");
const previous_button = document.querySelector(".previous");
const next_button = document.querySelector(".next");


pdfjsLib.getDocument({ url: pdf_URL}).promise.then((pdf) => { // loading PDF doc takes time, must be a promise
    console.log("PDF loaded.");

    pdf_doc = pdf; // load pdf into variable to reuse
    max_page = pdf.numPages;
    load_page(page_number);
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
            page_text.innerHTML = `Page ${page_number} of ${max_page}`; // updates page counter
        });
    }); 
}

previous_button.addEventListener("click", () => {
    if (page_number > min_page) {
        load_page(--page_number);
    }
});

next_button.addEventListener("click", () => {
    if (page_number < max_page) {
        load_page(++page_number);
    }
});