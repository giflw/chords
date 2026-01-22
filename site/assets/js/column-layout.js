class ColumnLayoutManager {
    constructor(container) {
        this.container = container;
        this.chordSheet = container.querySelector('.chords-sheet');
        this.currentColumns = 1;

        this.init();
    }

    init() {
        // Find column control buttons
        const col1Btn = this.container.querySelector('.col-1');
        const col2Btn = this.container.querySelector('.col-2');
        const col3Btn = this.container.querySelector('.col-3');

        if (col1Btn) col1Btn.addEventListener('click', () => this.setColumns(1));
        if (col2Btn) col2Btn.addEventListener('click', () => this.setColumns(2));
        if (col3Btn) col3Btn.addEventListener('click', () => this.setColumns(3));

        // Set initial state
        this.setColumns(1);
    }

    setColumns(count) {
        if (!this.chordSheet) return;

        this.currentColumns = count;

        // Update active button state
        this.container.querySelectorAll('.col-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        const activeBtn = this.container.querySelector(`.col-${count}`);
        if (activeBtn) activeBtn.classList.add('active');

        // Apply CSS column layout
        if (count === 1) {
            this.chordSheet.style.columnCount = '';
            this.chordSheet.style.columnGap = '';
        } else {
            this.chordSheet.style.columnCount = count;
            this.chordSheet.style.columnGap = '20px';
        }
    }
}

// Auto-initialize
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.chords-sheet-container').forEach(container => {
        new ColumnLayoutManager(container);
    });
});
