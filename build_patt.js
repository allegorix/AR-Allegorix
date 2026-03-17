const { createCanvas, loadImage } = require('canvas');
const fs = require('fs');

// Mock browser objects
global.document = {
    createElement: (tag) => {
        if (tag === 'canvas') return createCanvas(16, 16);
        return {};
    }
};
global.Image = function () { }; // Dummy for THREEx

// Include THREEx
eval(fs.readFileSync('./threex-arpatternfile.js', 'utf8'));

async function generate() {
    const img = await loadImage('./card-inner.png');
    // We can't use encodeImageURL because it uses onload which we mocked poorly.
    // Use encodeImage directly since we already loaded the image.
    const patternString = THREEx.ArPatternFile.encodeImage(img);
    fs.writeFileSync('./card.patt', patternString);
    console.log("Successfully generated card.patt");
}

generate().catch(console.error);
