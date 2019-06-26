const currentText = `{{ current.text }}`;
const sourceText = `{{ source.text }}`;

// To avoid JS parse errors, we inject indices as text and then convert to JSON
// array
const rawIndices = `{{ indices }}`; 

// Init placeholder values, to be initialized after document has finished 
// loading.
let currentContainer = undefined;
let sourceContainer = undefined;
let currentSimilarLines = [];
let sourceSimilarLines = [];

/**
 * @function printLines
 * Function prints lines of source code into specified target element. Lines 
 *      have formatting applied that can highlight them as similar or focus the 
 *      specific similarity matches.
 * @param  {String} source {The source code of the file to display}
 * @param  {jQuery element} targetElement {jQuery selected element that will 
 *      contain the formatted text}
 * @param  {Array} similarLines {Array of all matching fragments among both 
 *      files. This array should include the indices for file to display, each 
 *      value should have the structure `{from: {line: Int}, to: {line: Int}}`}
 * @param  {Object} hihghlightedLines {The highlighted match, if such exists. 
 *      Should have the structure `{from: {line: Int}, to: {line: Int}}`}
 * @return {void} {Function does not return anything}
 */
let printLines = (source, targetElement, similarLines, hihghlightedLines) => {
    // Clear any existing content
    targetElement.empty();

    let lines = source.split('\n');
    for(let i = 0; i < lines.length; i++) {
        let l = $("<span></span>").addClass("line").text(lines[i]);

        // Check for similar lines
        if (inRange(i+1, similarLines)) {
            l.addClass("similar");

            // Check for highlighted segment, highlighting only possible for 
            // similar lines
            if (inRange(i+1, [hihghlightedLines])) {
                l.addClass("focus");
            }
        }

        targetElement.append(l);
    }
};

/**
 * @function renderFragments
 * Function renders list of similar fragments. Upon click on such fragment, it 
 *      will be highlighted in code containers.
 * @param  {Array} fragments {All similar fragments among both files. The line 
 *      numbers shown are based on the current target file, not the possible 
 *      source file. Each entry of the array should have the following 
 *      structure: `{this_file: {from: {line: Int}, to: {line: Int}}}`}
 * @return {void} {Function does not return anything}
 */
let renderFragments = (fragments) => {
    let container = $(".fragment-links");
    // Clear out any content, if there is any
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

/**
 * @function loadFragment
 * Function higlights a specific matching fragments of code. 
 * @param  {Object} fragment {The fragment to highlight. Should have a structure 
 *      `{this_file: {from: {line: Int}, to: {line: Int}}, source_file: {..}}`}
 * @return {Function} {Function returns a function of no parameters}
 */
let loadFragment = fragment => () => {
    // Re-render both code containers with new highlighted fragment
    printLines(text, currentContainer, currentSimilarLines, fragment.this_file);
    printLines(text, sourceContainer, sourceSimilarLines, fragment.source_file);
};

$(document).ready(() => {
    let indices = [];
    try {
        // To avoid JS parse errors, we inject indices as text and then convert 
        // to JSON array
        indices = JSON.parse(rawIndices);
    } catch(e) {
        console.log(e);
    }

    // Init code fragment container selectors
    currentContainer = $("div.code > .left > pre");
    sourceContainer = $("div.code > .right > pre");

    // Render list of similarity fragments
    renderFragments(indices);

    // Create individual lists of matching indices for each file
    for (let i = 0; i < indices.length; i++) {
        currentSimilarLines.push(indices[i].this_file);
        sourceSimilarLines.push(indices[i].source_file);
    }

    // Render initial file source codes. This will have no highlighted segments
    printLines(currentText, currentContainer, currentSimilarLines, {});
    printLines(sourceText, sourceContainer, sourceSimilarLines, {});
});


/**
 * @function inRange
 * Function checks if given line number is within the ranges specified.
 * @param  {Int} value {Line number to lookup}
 * @param  {Array} range {Range of lines that are within target scope. Each 
 *      array value should have the structure 
 *      `{from: {line: Int}, to: {line: Int}}`}
 * @return {Boolean} {Returns true if given value is in the range of lines}
 */
let inRange = (value, range) => {
    for (let i = 0; i < range.length; i++) {
        const { from, to } = range[i];

        // If structure is not appropriate, assume no match
        if (from === undefined || to === undefined) return false;
        // If target value is within line range, return true
        if (value >= from.line && value <= to.line) {
            return true;
        }
    }

    // We did not manage to find a valid range, return false by default
    return false;
};
