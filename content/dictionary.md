# Chord Dictionary
2023-11-10
:jbake-type: page


++++
&lt;div class="container m-3 p-3">
    &lt;form class="columns">
        &lt;fieldset class="column box">
            &lt;legend class="title is-4 mb-2">Instrumento&lt;/legend>
            &lt;div class="columns">
                &lt;label class="column">
                    &lt;input type="radio" checked name="tuning" value="guitar.standard" />
                    Violão/Guitarra
                &lt;/label>
                &lt;label class="column">
                    &lt;input type="radio" name="tuning" value="ukulele.standard"/>
                    Ukulele
                &lt;/label>
                &lt;label class="column">
                    &lt;input type="radio" name="tuning" value="bass.standard"/>
                    Baixo
                &lt;/label>
            &lt;/div>
        &lt;/fieldset>
        &lt;fieldset class="column box">
            &lt;legend class="title is-4 mb-2">Acorde&lt;/legend>
            &lt;div class="columns">
                &lt;label class="column is-two-thirds">
                    Nome do acorde:
                    &lt;input type="text" id="chord-name" />
                &lt;/label>
                &lt;div class="column is-one-third">
                    &lt;button class="button" type="button" onclick="showChords()">Visualizar&lt;/button>
                &lt;/div>
            &lt;/div>
        &lt;/fieldset>
    &lt;/form>
    &lt;div id="chords-list">
    &lt;/div>
&lt;/div>

&lt;script>
function showChords() {
    document.querySelector('#chords-list').innerHTML = '';

    const name = document.querySelector('#chord-name').value;

    const instrumentTuning = [...document.querySelectorAll('*[name="tuning"]')].filter(el => el.checked)[0].value.split('.');

    let tuning = chordictionary.tuning;
    for (const insTun of instrumentTuning) {
        tuning = tuning[insTun];
    }

    const instrument = new chordictionary.Instrument(tuning.join(''), 12, 5, 4);
    let tabs = instrument.getChordsList(name).chordList;

    //console.log(tabs)
    
    tabs.sort((a, b) => {
        let ax = a.tab.filter(f => f == "x").length;
        let bx = b.tab.filter(f => f == "x").length;
        const byXCount = ax > bx ? 1 : (ax &lt; bx ? -1 : 0);
        ax = a.tab.map((el, idx) => el == "x" ? idx : 0).reduce((p, c) => p + c);
        bx = b.tab.map((el, idx) => el == "x" ? idx : 0).reduce((p, c) => p + c);
        const byXCountAndXString = byXCount != 0 ? byXCount : (ax > bx ? 1 : (ax &lt; bx ? -1: 0));
        ax = a.tab.map((el, idx) => el == "x" ? idx : el).reduce((p, c) => p + c);
        bx = b.tab.map((el, idx) => el == "x" ? idx : el).reduce((p, c) => p + c);
        const byXCountAndXStringAndHandProcimity = byXCountAndXString != 0 ? byXCountAndXString : (ax > bx ? 1 : (ax &lt; bx ? -1: 0));
        return byXCountAndXStringAndHandProcimity;
    });
    
    tabs = tabs.filter( tab => {
        const freqs = tab.tab.reduce(function (acc, curr) {
            return acc[curr] ? ++acc[curr] : acc[curr] = 1, acc;
        }, {0: 0, x: 0});
        // probably impossible bars
        if (freqs[1] > 2 && freqs[0] > 0 && (freqs["x"] == 0 || tab.tab[0] != "x")) {
            return false;
        }
        if (freqs[0] == 0 && freqs[1] >= 2) {
            return true;
        }
        if (tab.tab.filter(f => f != "x" && f != 0).length &lt;= 4) {
            return true;
        }
        return false;
    });
    tabs.forEach(tab => {
        tab.info = instrument.getChordInfo(tab).first();
    });
    if (instrumentTuning[0] == 'guitar') {
        tabs.sort((a, b) => {
            if (a.info.name == b.info.name) {
                return 0;
            }
            if (a.info.name == name) {
                return -1;
            }
            if (b.info.name == name) {
                return 1;
            }
            if (a.info.name.startsWith(name)) {
                return -1;
            }
            if (b.info.name.startsWith(name)) {
                return 1;
            }
            return a.info.name.localeCompare(b.info.name);
        });
    }
    if (tabs?.length > 0) {
        let diagrams = '';
        tabs.forEach(tab => {
            diagrams += '&lt;div class="m-1 p-1" style="display: inline-block">' + instrument.getChordLayout(tab.tab, tab.info) + '&lt;/div>';
        });
        document.querySelector('#chords-list').innerHTML = diagrams;
    }

}
&lt;/script>
