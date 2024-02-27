import { LitElement, html } from 'lit';
import { customElement, property } from 'lit/decorators.js';

@customElement('itq-hi')
export class HiElement extends LitElement {
  @property({ type: Number })
  aNumber: number = 5;

  override render(){
    return html`<p>Hi ${this.aNumber}.</p>`;
  }
}

declare global {
  interface HTMLElementTagNameMap {
    "itq-hi": HiElement;
  }
}
