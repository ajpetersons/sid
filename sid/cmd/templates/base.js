let text = `?
this is a very long line, much much longer than a line of code should ever be. Maybe I am overdoing this? probably, I wouldnt be speaking with myself otherwise
is 
multiple
lines
this is a very long line, much much longer than a line of code should ever be. Maybe I am overdoing this? probably, I wouldnt be speaking with myself otherwise
is 
multiple
lines
this is a very long line, much much longer than a line of code should ever be. Maybe I am overdoing this? probably, I wouldnt be speaking with myself otherwise
is 
multiple
lines
this is a very long line, much much longer than a line of code should ever be. Maybe I am overdoing this? probably, I wouldnt be speaking with myself otherwise
is 
multiple
lines
this is a very long line, much much longer than a line of code should ever be. Maybe I am overdoing this? probably, I wouldnt be speaking with myself otherwise
is 
multiple
lines
`; // TODO: Init properly

let indices = [
    {
        "this_file": {
            "from": { "line": 2, "col": 4 },
            "to": { "line": 2, "col": 4 }
        },
        "source_file": {
            "from": { "line": 4, "col": 4 },
            "to": { "line": 5, "col": 4 }
        }
    },
    {
        "this_file": {
            "from": { "line": 3, "col": 4 },
            "to": { "line": 4, "col": 4 }
        },
        "source_file": {
            "from": { "line": 6, "col": 17 },
            "to": { "line": 6, "col": 4 }
        }
    },
    {
        "this_file": {
            "from": { "line": 10, "col": 4 },
            "to": { "line": 14, "col": 4 }
        },
        "source_file": {
            "from": { "line": 10, "col": 17 },
            "to": { "line": 14, "col": 4 }
        }
    }
]; // TODO: Init properly

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
        let from = fragments[i].this_file.from.line;
        let to = fragments[i].this_file.to.line;
        let fragment = $("<div></div>").addClass("fragment");
        let link = $("<a></a>").click(loadFragment(fragments[i]))
            .text(`Fragment ${i+1}  [Lines ${from} - ${to}]`);
        fragment.append(link);
        container.append(fragment);
    }
};

let loadFragment = fragment => () => {
    printLines(text, this_file_container, this_file_similarLines, fragment.this_file);
    printLines(text, source_file_container, source_file_similarLines, fragment.source_file);
};

$(document).ready(() => {
    this_file_container = $("div.code > .left > pre");
    source_file_container = $("div.code > .right > pre");

    renderFragments(indices);

    for (let i = 0; i < indices.length; i++) {
        this_file_similarLines.push(indices[i].this_file);
        source_file_similarLines.push(indices[i].source_file);
    }

    printLines(text, this_file_container, this_file_similarLines, {});
    printLines(text, source_file_container, source_file_similarLines, {});
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
