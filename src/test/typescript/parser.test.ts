import { SimpleNode, ArtistNode, TitleNode } from "../../main/typescript/parser";
import { describe, expect, test } from "@jest/globals";

interface StandardVsParsed<T> {
    standard: string
    parsed: string
    node: SimpleNode<T>
}

function of<T>(node: (standard: string) => SimpleNode<T>, standard: string, parsed: string): StandardVsParsed<T> {
    return {
        standard, parsed, node: node(standard)
    };
}

const title: StandardVsParsed<string> = of(std => new TitleNode().parse(std), "= Song Title!", "Song Title!");
const artist: StandardVsParsed<string> = of(std => new ArtistNode().parse(std), "Artist Name", "Artist Name");
const nsscSource = `
${title.standard}
${artist.standard}
2020-12-20 23:58:59
:bpm: 140

----
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

----
`;

/*
const nssc = parser(nsscSource);

const nsscAst: DocumentNode = new DocumentNode(
    nsscSource,
    new HeaderNode(
        "Song Title!",
        "Artist Name",
        new Date("2020-12-20 23:58:59"),
        []
    ),
    new ContentNode()
);*/

// FIXME delete
function foo(bar: unknown) {
    `${bar}`;
}
foo(nsscSource);

describe("chords parser tests", () => {

    test("parse title line", () => {
        expect(title.node.value).toEqual(title.parsed);
    });
    test("parse artist line", () => {
        expect(artist.node.value).toEqual(artist.parsed);
    });

    /*test("full parser", () => {
        expect(nssc.source).toEqual(nsscSource);
        expect(nssc).toEqual(nsscAst);
    });*/
});
