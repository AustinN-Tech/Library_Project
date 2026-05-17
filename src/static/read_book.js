import * as pdfjsLib from "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/5.4.149/pdf.mjs";

pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/5.4.149/pdf.worker.mjs';

let loading_task = pdfjsLib.getDocument({ url: pdf_URL});
loading_task.promise.then((pdf) => {
    console.log("PDF loaded.");

    let page_number = 1;
    pdf.getPage(page_number).then((page) => {
        console.log("Page loaded.");

        let scale = 1.5;
        let viewport = page.getViewport( {scale: scale});

        let canvas = document.querySelector("canvas");
        let context = canvas.getContext('2d');
        canvas.height = viewport.height;
        canvas.width = viewport.width

        let renderContext = {
            canvasContext: context,
            viewport: viewport
        };
        let renderTask = page.render(renderContext);
        renderTask.promise.then(() => {
            console.log('Page rendered.')
        });
    });
});