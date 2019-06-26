const currentText = `{{ current.text }}`;
const sourceText = `{{ source.text }}`;

const rawIndices = `{{ indices }}`; 

let currentContainer = undefined;
let sourceContainer = undefined;
let currentSimilarLines = [];
let sourceSimilarLines = [];

let printLines = (source, targetElement, similarLines, hihghlightedLines) => {
    targetElement.empty();

    let lines = source.split('\n');
    for(let i = 0; i < lines.length; i++) {
        let l = $("<span></span>").addClass("line").text(lines[i]);

        if (inRange(i+1, similarLines)) {
            l.addClass("similar");

            if (inRange(i+1, [hihghlightedLines])) {
                l.addClass("focus");
            }
        }

        targetElement.append(l);
    }
};

let renderFragments = (fragments) => {
    let container = $(".fragment-links");
    container.empty();

    for (let i = 0; i < fragments.length; i++) {
        let { from, to } = fragments[i].this_file || {};

        let fragment = $("<div></div>").addClass("fragment");
        let link = $("<a></a>").click(loadFragment(fragments[i]))
            .text(`Fragment ${i+1}  [Lines ${from.line} - ${to.line}]`);
        fragment.append(link);
        container.append(fragment);
    }
};

let loadFragment = fragment => () => {
    printLines(text, currentContainer, currentSimilarLines, fragment.this_file);
    printLines(text, sourceContainer, sourceSimilarLines, fragment.source_file);
};

$(document).ready(() => {
    let indices = [];
    try {
        // To avoid JS parse errors, we inject indices as text and then convert to JSON array
        indices = JSON.parse(rawIndices);
    } catch(e) {
        console.log(e);
    }

    currentContainer = $("div.code > .left > pre");
    sourceContainer = $("div.code > .right > pre");

    renderFragments(indices);

    for (let i = 0; i < indices.length; i++) {
        currentSimilarLines.push(indices[i].this_file);
        sourceSimilarLines.push(indices[i].source_file);
    }

    printLines(currentText, currentContainer, currentSimilarLines, {});
    printLines(sourceText, sourceContainer, sourceSimilarLines, {});
});

let inRange = (value, range) => {
    for (let i = 0; i < range.length; i++) {
        const { from, to } = range[i];

        if (from === undefined || to === undefined) return false;
        if (value >= from.line && value <= to.line) {
            return true;
        }
    }

    return false;
};
