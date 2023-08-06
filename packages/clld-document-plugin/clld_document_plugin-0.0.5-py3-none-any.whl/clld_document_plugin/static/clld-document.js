function numberExamples() {
    var examples = document.querySelectorAll("li.example"); // select all examples
    for (var exc = 0; exc < examples.length; exc++) {
        ex = examples[exc]
        ex.setAttribute("value", exc + 1) // number each example
        var subexamplesol = ex.querySelector("ol.subexample");
        if (subexamplesol) { // if there are subexamples, number them example-internally
            subexamples = subexamplesol.children
            for (var subexc = 0; subexc < subexamples.length; subexc++) {
                subexamples[subexc].setAttribute("value", subexc + 1)
            }
        }
    }

    var exrefs = document.querySelectorAll("a.exref"); // get all links that are references to examples
    exrefs.forEach(function(x, i) {
        example_id = x.getAttribute("example_id")
        x.setAttribute("href", "#" + example_id) // point the link to the example
        x.textContent = getExampleLabel(example_id) // getExampleLabel returns labels like 1 or 2b
        if (x.hasAttribute("end")) { // for exrefs of the form (10-12)
            end = x.getAttribute("end")
            x.textContent += "-" + getExampleLabel(end)
        }
        if (x.hasAttribute("suffix")) { // for exrefs of the form (10a-b)
            x.textContent += x.getAttribute("suffix")
        }
        if (!x.hasAttribute("bare")) {
            x.textContent = "(" + x.textContent + ")" // wrap it up in parentheses (or not!)
        }
    });
}


function getExampleLabel(example_id) {
    ex = document.getElementById(example_id)
    if (ex == null){
        console.log("Could not find example with ID " + example_id);
        return "undefined"
    }
    parent = ex.parentElement
    if (parent.getAttribute("class") == "subexample") {
        return parent.parentElement.value + String.fromCharCode(96 + ex.value) // convert to alphabetical labels
    }
    return ex.value
}

// returns strings like 3. or 4.3.2
function getNumberLabel(counters, level) {
    output = []
    for (var i = 2; i <= level; i++) {
        output.push(counters["h"+i])
    }
    return output.join(".")
}

//used for storing both section labels and float counters
var stored = {}

function numberSections(){
    var toc = document.getElementById("toc") // get the table of contents
    var counters = {}; // initialize counters for every heading level except h1 (below)
    var levels = ["h2", "h3", "h4", "h5", "h6"];
    levels.forEach(function(x, i) {
        counters[x] = 0
    })
    
    // there is only supposed to be one h1; get a potential chapter number and format it
    h1 = document.querySelectorAll("h1")[0];
    if (h1.hasAttribute("number")) {
        prefix = h1.getAttribute("number") + "."
    } else {
        prefix = ""
    }
    h1.textContent = prefix+" " + h1.textContent

    // insert title into TOC
    toctitle = document.createElement("b")
    toctitle.textContent = h1.textContent
    toc.appendChild(toctitle)

    // iterate all headings
    var headings = document.querySelectorAll("h2, h3, h4, h5, h6");
    headings.forEach(function(heading, i) {
        var level = heading.tagName.toLowerCase();
        counters[level] += 1
        number = getNumberLabel(counters, level.charAt(level.length - 1)) // the formatted X.Y.Z counter
        heading.textContent = prefix + number + ". " + heading.textContent

        toclink = document.createElement('a') // insert links into the TOC
        toclink.textContent = '\xa0\xa0'.repeat(level.charAt(level.length - 1)-2)+heading.textContent
        toclink.href = "#"+heading.id
        tocdiv = document.createElement('div')
        tocdiv.appendChild(toclink);
        toc.appendChild(tocdiv);

        stored[heading.id] = prefix + number // for crossref resolution

        // reset the smaller counters
        reached = false;
        levels.forEach(function(level_comp, j) {
            if (reached){
                counters[level_comp] = 0
            };
            if (level==level_comp){
                reached = true;
            }
        });
    });
}


function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function numberCaptions(){
    var captions = document.querySelectorAll("div.caption"); // get all captions
    var figcaptions = document.querySelectorAll("figcaption"); // get all captions
    var kinds = ["table", "figure"] // only these two types for now
    var counters = {"table": 0, "figure": 0}
    captions.forEach(function(caption, i) {
        kinds.forEach(function(kind, j) {
            if (caption.classList.contains(kind)){
                counters[kind] += 1
                ref_counter = capitalizeFirstLetter(kind) + " " + counters[kind];
                caption.textContent = ref_counter + ": " + caption.textContent
                stored[caption.id] = ref_counter // store the value for resolveCrossrefs below
            }
        });
    });
    figcaptions.forEach(function(caption, i) {
        counters["figure"] += 1
        ref_counter = capitalizeFirstLetter("figure") + " " + counters["figure"];
        if (!caption.textContent.startsWith(ref_counter + ": ")){
            caption.textContent = ref_counter + ": " + caption.textContent
        }
        stored[caption.id] = ref_counter // store the value for resolveCrossrefs below
    })
}

// iterate all a.crossref and insert the calculated values; for floats and sections
function resolveCrossrefs(){
    var refs = document.querySelectorAll("a.crossref");
    refs.forEach(function(ref, i) {
        ref.textContent = stored[ref.name]
        if (ref.hasAttribute("end")) { // for ranges
            end = ref.getAttribute("end")
            ref.textContent += "–" + stored[end]
        }
    })
}