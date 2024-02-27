import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NotSoSimpleChordsComponent } from './not-so-simple-chords.component';

describe('NotSoSimpleChordsComponent', () => {
  let component: NotSoSimpleChordsComponent;
  let fixture: ComponentFixture<NotSoSimpleChordsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NotSoSimpleChordsComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(NotSoSimpleChordsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
