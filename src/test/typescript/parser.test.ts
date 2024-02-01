import { SimpleNode, ArtistNode, TitleNode, AttributeNode, DateTimeNode, HeaderNode, EmptyNode, CommentNode } from "../../main/typescript/parser";
import { describe, expect, test } from "@jest/globals";

interface StandardVsParsed<S, T extends SimpleNode<S, T>> {
    standard: string
    toString: string
    node: T
}

function of<S, T extends SimpleNode<S, T>>(type: { new(value?: S): T }, standard: string, parsed: string): StandardVsParsed<S, T> {
    return {
        standard, toString: parsed, node: new type().parse(standard)
    };
}

const title = of(TitleNode, "= Song Title!", "Song Title!");
const artist = of(ArtistNode, "Artist Name", "Artist Name");
const dateTime = of(DateTimeNode, "2020-12-20 23:58:59 ", "2020-12-20 23:58:59");
const date = of(DateTimeNode, "2020-12-20", "2020-12-20");
const attrFlag = of(AttributeNode, ":attr-name:", "attr-name");
const attrNum = of(AttributeNode, ":attr-name-num: 5", "attr-name-num: 5");
const attrText = of(AttributeNode, `:attr-name-text: foo
                                              |bar 
                                              ||baz`, "attr-name-text: foo bar |baz");
const attrList = of(AttributeNode, `:attr-name-list: foo, 
                                             | bar`, "attr-name-list: foo, bar");

const nsscHeaderSource = `
${title.standard}
${artist.standard}
2020-12-20 23:58:59

${attrFlag.standard}
${attrNum.standard}
${attrText.standard}
${attrList.standard}
// comment
`;

const nsscSource = `
${nsscHeaderSource}
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

console.log(nsscSource);

describe("chords parser tests", () => {

    test("parse title line", () => {
        expect(title.node.toString()).toEqual(title.toString);
    });
    test("parse artist line", () => {
        expect(artist.node.toString()).toEqual(artist.toString);
    });
    test("parse date/time line", () => {
        expect(dateTime.node.toString()).toEqual(dateTime.toString);
        expect(date.node.toString()).toEqual(date.toString);
    });
    test("parse attributes lines", () => {
        expect(attrFlag.node.toString()).toEqual(attrFlag.toString);
        expect(attrNum.node.asNumber()).toEqual(Number.parseInt(attrNum.toString.split(":")[1]));
        expect(attrText.node.toString()).toEqual(attrText.toString);
        expect(attrList.node.toString()).toEqual(attrList.toString);
        expect(attrList.node.asList()).toEqual(["foo", "bar"]);
    });
    test("parse header", () => {
        expect(new HeaderNode().split(nsscHeaderSource)[1]).toEqual("= Song Title!");
        expect(new HeaderNode().parse(nsscHeaderSource).nodes).toEqual([
            EmptyNode.INSTANCE, title.node,
            artist.node,
            dateTime.node,
            attrFlag.node,
            attrNum.node,
            attrText.node,
            attrList.node,
            new CommentNode().parse("// comment"),
            EmptyNode.INSTANCE
        ]);
    });
});
