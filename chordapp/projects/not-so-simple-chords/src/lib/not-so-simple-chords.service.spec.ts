import { TestBed } from '@angular/core/testing';

import { NotSoSimpleChordsService } from './not-so-simple-chords.service';

describe('NotSoSimpleChordsService', () => {
  let service: NotSoSimpleChordsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NotSoSimpleChordsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
