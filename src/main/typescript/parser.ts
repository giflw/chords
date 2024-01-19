import DEBUG from "./debug";

export interface NodeRegexPair {
    factory: (value: string) => Node;
    regex: RegExp;
}

export abstract class Node {

    public isBlock(): boolean {
        return false;
    }

    public abstract toString(): string;
}

export abstract class SimpleNode<T> extends Node {

    constructor(readonly value: T) {
        super();
    }

    public toString(): string {
        return `${this.value}`;
    }
}

export abstract class BlockNode extends Node {
    protected abstract parseChildren(): void;

    public isBlock(): boolean {
        return true;
    }
}

export class TitleNode extends SimpleNode<string> {
    public static readonly REGEX: RegExp = /^(?<value>= .*)$/m;

    public constructor(readonly value: string) {
        super(value);
    }

    public static parse(value: string): TitleNode {
        value = value.startsWith("=") ? value.substring(1) : value;
        return new TitleNode(value.trim());
    }
}

export class ArtistNode extends Node {
    public static readonly REGEX: RegExp = /^(?<value>[\p{L}\p{M}\p{Zs}0-9:?!&,. _-]+)$/mu;

    public constructor(value: string) {
        super(value);
    }

    public static parse(value: string, index: number, array: string[]): ArtistNode {
        if (!array[index - 1].startsWith("=")) {
            throw "Artist name must come after Title";
        }
        return new ArtistNode(value.trim());
    }
}

export class DateTimeNode extends Node {
    public static readonly REGEX: RegExp = /^(?<value>[0-9:/.Tz -]+)$/mu;

    public constructor(value: string) {
        super(value);
    }

    public static parse(value: string, index: number, array: string[]): DateTimeNode {
        if (!array[index - 2].startsWith("=")) {
            throw "Date/Time must come after Artist";
        }
        return new DateTimeNode(value.trim());
    }
}

export abstract class AttributeNode extends Node { }

export class HeaderNode extends BlockNode {

    public static readonly REGEXES: NodeRegexPair[] = [
        { factory: DateTimeNode.parse, regex: DateTimeNode.REGEX },
        { factory: TitleNode.parse, regex: TitleNode.REGEX },
        { factory: ArtistNode.parse, regex: ArtistNode.REGEX }
    ];

    constructor(readonly title: string, readonly artist: string, readonly datetime: Date, readonly attributes: AttributeNode[]) {
        super();
    }

    static parse(header: string): HeaderNode {
        throw new Error("Method not implemented.");
    }
}

export class ContentNode extends Node {
    static parse(content: string): ContentNode {
        throw new Error("Method not implemented.");
    }
}


export class DocumentNode extends Node {
    readonly source: string;
    readonly header: HeaderNode;
    readonly content: ContentNode;

    constructor(source: string, header: HeaderNode | string, content: ContentNode | string) {
        super(source);
        this.source = source;
        this.header = typeof header === "string" ? HeaderNode.parse(header) : header;
        this.content = typeof content === "string" ? ContentNode.parse(content) : content;
    }

    public static parse(source: string): DocumentNode {
        source = source.trim().replaceAll(/[\r\n]+/, "\n");
        const [header, content] = source.split("\n\n", 1);
        return new DocumentNode(source, header, content);
    }
}

export function parseLine(line: string, index: number, array: string[]): Node {
    console.log(line, index, array);
    let value: string | undefined = undefined;
    const pair: NodeRegexPair | undefined = REGEXES.find(pair => {
        value = pair.regex.exec(line)?.groups?.value;
        const found = value !== undefined;
        DEBUG.debugMatchers(pair.regex, line, found, value);
        return found;
    });
    if (!pair || value === undefined) {
        throw `Line matched no node: ${line}`;
    }
    const node = pair.factory(value, index, array);
    return node;
}

export default function parse(source: string): DocumentNode {
    return DocumentNode.parse(source);
}