import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import '../components/hi';

@Component({
  selector: 'itq-root',
  standalone: true,
  imports: [RouterOutlet],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
  template: `
    <div class="p-2">
      <h1 class="text-3xl font-bold underline">Welcome to {{ title }}!</h1>
      <itq-hi></itq-hi>
      <router-outlet />
    </div>
  `,
  styles: [],
})
export class AppComponent {
  title = 'chordapp';
}
