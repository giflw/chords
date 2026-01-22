class ChordTransposer {
    constructor(container) {
        this.container = container;
        this.semitones = 0;
        this.scale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B'];
        this.flat_scale = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B'];

        this.init();
    }

    init() {
        // Find controls
        const downBtn = this.container.querySelector('.transpose-down');
        const upBtn = this.container.querySelector('.transpose-up');
        const display = this.container.querySelector('.key-display');

        if (downBtn) downBtn.addEventListener('click', () => this.transpose(-1));
        if (upBtn) upBtn.addEventListener('click', () => this.transpose(1));

        this.display = display;

        // Cache original chords to avoid drifting errors
        this.chordElements = this.container.querySelectorAll('.chord .root, .chord .bass');
        this.originalNotes = Array.from(this.chordElements).map(el => el.innerText);
    }

    transpose(steps) {
        this.semitones += steps;
        this.updateDisplay();

        this.chordElements.forEach((el, index) => {
            const original = this.originalNotes[index];
            const newNote = this.getNewNote(original, this.semitones);
            el.innerText = newNote;
        });
    }

    updateDisplay() {
        if (this.display) {
            const sign = this.semitones > 0 ? '+' : '';
            this.display.innerText = this.semitones === 0 ? 'Original' : `${sign}${this.semitones}`;
        }
    }

    getNewNote(note, semitones) {
        if (!note) return note;

        // Normalize Note
        let noteIndex = this.scale.indexOf(note);
        if (noteIndex === -1) noteIndex = this.flat_scale.indexOf(note);

        if (noteIndex === -1) return note; // Unknown note

        let newIndex = (noteIndex + semitones) % 12;
        if (newIndex < 0) newIndex += 12;

        // Return sharp version by default for simplicity
        return this.scale[newIndex];
    }
}

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.chords-sheet-container').forEach(container => {
        new ChordTransposer(container);
    });
});
