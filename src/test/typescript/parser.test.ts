import parser from "../../main/typescript/parser";
import { describe, expect, test } from "@jest/globals";

const nsscText = `
= Song Title!
Artist Name
2020-12-20 23:58:59
:bpm: 140

// just a comment
@live Live version
@radio Radio Versio

[Intro]
G9 * A4  D
@!radio
G9 * A4  D

[Verse]
G              D
Lorem ipsum dolor sit amet,
              D
consectetur adipiscing elit,
                   Bm7
sed do eiusmod tempor incididunt
                 A4 >   Bm7 v~
ut labore et dolore magna aliqua.

[FooBar-Ção]
( G9 * A4  D > )
`;

const nssc = parser(nsscText);

describe("chords parser tests", () => {
    test("root node has text", () => {
        expect(nssc.source).toBe(nsscText);
    });
});
