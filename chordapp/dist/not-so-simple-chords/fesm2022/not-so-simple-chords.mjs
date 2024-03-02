import * as i0 from '@angular/core';
import { Injectable, Component } from '@angular/core';
import { __decorate } from 'tslib';
import { LitElement, html } from 'lit';
import { customElement } from 'lit/decorators.js';

class NotSoSimpleChordsService {
    constructor() { }
    static { this.ɵfac = i0.ɵɵngDeclareFactory({ minVersion: "12.0.0", version: "17.2.2", ngImport: i0, type: NotSoSimpleChordsService, deps: [], target: i0.ɵɵFactoryTarget.Injectable }); }
    static { this.ɵprov = i0.ɵɵngDeclareInjectable({ minVersion: "12.0.0", version: "17.2.2", ngImport: i0, type: NotSoSimpleChordsService, providedIn: 'root' }); }
}
i0.ɵɵngDeclareClassMetadata({ minVersion: "12.0.0", version: "17.2.2", ngImport: i0, type: NotSoSimpleChordsService, decorators: [{
            type: Injectable,
            args: [{
                    providedIn: 'root'
                }]
        }], ctorParameters: () => [] });

class NotSoSimpleChordsComponent {
    static { this.ɵfac = i0.ɵɵngDeclareFactory({ minVersion: "12.0.0", version: "17.2.2", ngImport: i0, type: NotSoSimpleChordsComponent, deps: [], target: i0.ɵɵFactoryTarget.Component }); }
    static { this.ɵcmp = i0.ɵɵngDeclareComponent({ minVersion: "14.0.0", version: "17.2.2", type: NotSoSimpleChordsComponent, isStandalone: true, selector: "lib-not-so-simple-chords", ngImport: i0, template: `
    <p>
      not-so-simple-chords works!
    </p>
  `, isInline: true, styles: [""] }); }
}
i0.ɵɵngDeclareClassMetadata({ minVersion: "12.0.0", version: "17.2.2", ngImport: i0, type: NotSoSimpleChordsComponent, decorators: [{
            type: Component,
            args: [{ selector: 'lib-not-so-simple-chords', standalone: true, imports: [], template: `
    <p>
      not-so-simple-chords works!
    </p>
  ` }]
        }] });

let NSSCHelloWorldElement = class NSSCHelloWorldElement extends LitElement {
    render() {
        return html `<p>Hello from NSSC.</p>`;
    }
};
NSSCHelloWorldElement = __decorate([
    customElement('nssc-hello-world')
], NSSCHelloWorldElement);

/*
 * Public API Surface of not-so-simple-chords
 */

/**
 * Generated bundle index. Do not edit.
 */

export { NotSoSimpleChordsComponent, NotSoSimpleChordsService };
//# sourceMappingURL=not-so-simple-chords.mjs.map
