const this_file_text = `{{ this_file_text }}`; // TODO: rename
const source_file_text = `{{ source_file_text }}`; // TODO: rename

const rawIndices = `{{ indices }}`; // TODO: rename

let this_file_container = undefined; // TODO: rename
let source_file_container = undefined; // TODO: rename
let this_file_similarLines = []; // TODO: rename
let source_file_similarLines = []; // TODO: rename

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
    printLines(text, this_file_container, this_file_similarLines, fragment.this_file);
    printLines(text, source_file_container, source_file_similarLines, fragment.source_file);
};

$(document).ready(() => {
    let indices = [];
    try {
        indices = JSON.parse(rawIndices);
    } catch(e) {
        console.log(e);
    }

    this_file_container = $("div.code > .left > pre");
    source_file_container = $("div.code > .right > pre");

    renderFragments(indices);

    for (let i = 0; i < indices.length; i++) {
        this_file_similarLines.push(indices[i].this_file);
        source_file_similarLines.push(indices[i].source_file);
    }

    printLines(this_file_text, this_file_container, this_file_similarLines, {});
    printLines(source_file_text, source_file_container, source_file_similarLines, {});
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
