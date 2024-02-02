const chords = document.querySelector(".chords");
if (chords) {
    const content = chords.textContent;
    chords.innerHTML = "";

    const lines = content.split("\n");
    let section = document.createElement("div");
    let sections = 0;
    let blanks = 0;
    let lastWasSection = false;

    for (let i = 0; i < lines.length; i++) {
        let text = lines[i];
        // console.log(text)
        let line = document.createElement("p");
        line.textContent = text;

        if (text.trim() === "") {
            blanks++;
            if (!lastWasSection && blanks == 1 && sections > 0) {
                section.appendChild(document.createElement("br"));
            }
            continue;
        }
        blanks = 0;
        lastWasSection = false;
        console.log('line', text)

        if (/^ *\[[A-Za-zÀ-ÖØ-öø-ÿ0-9?{} -]+\] *$/.test(text)) {
            lastWasSection = true;
            console.log('section', text)
            sections++;
            if (section.children.length > 0) {
                chords.appendChild(section);
            }

            line.textContent = text.trim();
            section = document.createElement("div");
            section.dataset.name = line.textContent.substring(1, line.textContent.length - 1);
            line.classList.add("has-text-weight-bold");
            line.classList.add("my-5");
        } else if (/^[A-H1-9Mm#bdisu°+\%()*~v^| ><\[\]/ mpf-]+$/.test(text)) {
            console.log('chords', text)
            //line.innerHTML = text.replace('v', '&#x2193;').replace('^', '&#x2191;')
            line.classList.add("mt-2");
            line.classList.add("has-text-primary");
            line.classList.add("has-text-weight-bold");
        }
        console.log("end", line)
        section.appendChild(line);
    }

    if (sections == 0) {
        while (section.childNodes.length > 0) {
            chords.appendChild(section.childNodes[0]);
        }
    } else {
        chords.appendChild(section);
    }

    chords.classList.remove("cloak");
}

let strummings = document.querySelectorAll(".batida .content pre");
strummings = strummings.length > 0 ? strummings : document.querySelectorAll(".batida");
console.log("strummings", strummings);
strummings.forEach(strumming => {
    const text = strumming.textContent.trim();
    if (text === "N/I") {
        return;
    }
    const signs = text.split("").map(sign => {
        switch (sign) {
            case "V":
                return "&#x2193;";
            // '&#x21a1;'
            case "v":
                return "&#x21e3;";
            case "A":
                return "&#x2191;";
            // '&#x219f;'
            case "^":
                return "&#x21e1";
            case "x":
                return "&#x2093;";
            case ".":
                return "&#x2e;";
            default:
                return "?";
        }
    }).join("");
    strumming.style.fontFamily = "'MesloLGSDZ Nerd Font Mono', monospace";
    strumming.style.fontSize = "2em";
    strumming.style.letterSpacing = "-.25em";
    strumming.style.lineHeight = "0.4em";
    strumming.style.verticalAlign = "text-top";
    strumming.innerHTML = signs;
});



const bpmNote = document.querySelectorAll(".bpm");
bpmNote.forEach(node => {
    const text = node.textContent;
    const parts = text.split(" ");
    if (/[0-9\/ \.]+/.test(text) && parts.length == 2) {
        note = parts[0];
        bpm = parts[1];
        switch (note) {
            case "1":
                note = "&#x1d15d;";
                break;
            case "1/2":
                note = "&#x1d15e;";
                break;
            case "1/4":
                note = "&#x1d15f;";
                break;
            case "1/8":
                note = "&#x1d160;";
                break;
            case "1/16":
                note = "&#x1d161;";
                break;
        }
        node.innerHTML = `<span style="letter-spacing: .5em">${note}</span> ${bpm}`;
    }
});


// print preview
if (location.search.includes("print=true")) {
    console.log("PRINT MODE");
    document.querySelectorAll("head>link[rel=stylesheet]").forEach(css => {
        /*if ("screen" == css.media) {
            console.log("PRINT MODE :: Removing", css)
            css.remove()
        } else*/ if ("print" == css.media) {
            let link = document.createElement("link");
            link.media = "screen";
            link.href = css.href;
            link.rel = css.rel;
            document.querySelector("head").appendChild(link);
            console.log("PRINT MODE :: adding print link to screen", css);
        } else {
            console.log("PRINT MODE :: skipping", css);
        }
    });
} else {
    console.log("SCREEN MODE");
}