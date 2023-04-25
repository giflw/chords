const chords = document.querySelector('.chords')
const content = chords.textContent
chords.innerHTML = ''

const lines = content.split('\n')
let section = document.createElement('div')
let sections = 0;
for(let i = 0; i < lines.length; i++) {
    let text = lines[i]
    // console.log(text)
    let line = document.createElement('p')
    line.textContent = text

    if (text.trim() === '') {
        continue
    }

    if (/^ *\[[A-Za-zÀ-ÖØ-öø-ÿ0-9]+\]$/.test(text)) {
        // console.log('section', text)
        sections++;
        if (section.children.length > 0) {
            chords.appendChild(section)
        }

        line.textContent = text.trim()
        section = document.createElement('div')
        section.dataset.name = line.textContent.substring(1, line.textContent.length - 1)
        line.classList.add('has-text-weight-bold')
        line.classList.add('my-2')
    } else if (/^[A-H1-9m#b()*~v^| ></]+$/.test(text)) {
        // console.log('chords', text)
        line.classList.add('mt-2')
        line.classList.add('has-text-primary')
        line.classList.add('has-text-weight-bold')
    }
    section.appendChild(line)
}

if (sections == 0) {
    while (section.childNodes.length > 0) {
        chords.appendChild(section.childNodes[0])
    }
} else {
    chords.appendChild(section)
}

chords.classList.remove('cloak')