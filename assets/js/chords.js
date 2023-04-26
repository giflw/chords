const chords = document.querySelector('.chords')
if (chords) {
    const content = chords.textContent
    chords.innerHTML = ''

    const lines = content.split('\n')
    let section = document.createElement('div')
    let sections = 0;
    let blanks = 0;
    for(let i = 0; i < lines.length; i++) {
        let text = lines[i]
        // console.log(text)
        let line = document.createElement('p')
        line.textContent = text

        if (text.trim() === '') {
            blanks++;
            if (blanks == 1 && sections > 0) {
                section.appendChild(document.createElement('br'));
            }
            continue;
        }
        blanks = 0;

        if (/^ *\[[A-Za-zÀ-ÖØ-öø-ÿ0-9 ]+\]$/.test(text)) {
            // console.log('section', text)
            sections++;
            if (section.children.length > 0) {
                chords.appendChild(section)
            }

            line.textContent = text.trim()
            section = document.createElement('div')
            section.dataset.name = line.textContent.substring(1, line.textContent.length - 1)
            line.classList.add('has-text-weight-bold')
            line.classList.add('my-5')
        } else if (/^[A-H1-9Mm#bdisu°+\%()*~v^| ><\[\]/]+$/.test(text)) {
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
}

const strummings = document.querySelectorAll('.batida .content pre')
strummings.forEach(strumming => {
    const signs = document.createElement('div')
    strumming.textContent.split('').forEach(sign => {
        const node = document.createElement('i')
        switch(sign){
            case 'V':
                node.className = "fa-fw fal fa-long-arrow-down fa-2x"
                node.style = "width: .5em"
                break
            case 'v':
                node.className = "fa-fw far fa-long-arrow-down"
                break
            case 'A':
                node.className = "fa-fw fal fa-long-arrow-up fa-2x"
                node.style = "width: .5em"
                break
            case '^':
                node.className = "fa-fw far fa-long-arrow-up"
                break
            case 'x':
                node.className = "fa-fw fal fa-times"
                break
            case 'X':
                node.className = "fa-fw fas fa-times"
                break
            case '.':
            case ' ':
                node.className = "fad fa-dot-circle"
                node.style = "--fa-secondary-opacity: 0"
                break
        }
        signs.appendChild(node)
    })
    const parent = strumming.parentNode
    parent.removeChild(strumming)
    parent.appendChild(signs)
})
