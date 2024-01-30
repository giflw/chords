export class Node {
    isBlock() {
        return false;
    }
}
export class SimpleNode extends Node {
    _value;
    constructor(_value) {
        super();
        this._value = _value;
    }
    parse(text) {
        this.value = this._parse(text);
        return this;
    }
    get value() {
        if (this._value) {
            return this._value;
        }
        throw "Value not set";
    }
    set value(value) {
        this._value = value;
    }
    toString() {
        return `${this.value}`;
    }
}
export class BlockNode extends Node {
    isBlock() {
        return true;
    }
}
export class TitleNode extends SimpleNode {
    static REGEX = /^(?<value>= .*)$/m;
    constructor(value) {
        super(value);
    }
    _parse(text) {
        return (text.startsWith("=") ? text.substring(1) : text).trim();
    }
}
export class ArtistNode extends SimpleNode {
    static REGEX = /^(?<value>[\p{L}\p{M}\p{Zs}0-9:?!&,. _-]+)$/mu;
    constructor(value) {
        super((value.startsWith("=") ? value.substring(1) : value).trim());
    }
    _parse(text) {
        return text.trim();
    }
}
export class DateTimeNode extends SimpleNode {
    static REGEX = /^(?<value>[0-9:/.Tz -]+)$/mu;
    constructor(value) {
        super(value);
    }
    _parse(text) {
        return new Date(text.trim());
    }
}
export class AttributeNode extends Node {
}
/*
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
*/
function foo() {
    const newInstance = Object.create(ArtistNode.prototype);
    newInstance.constructor.apply(newInstance);
    return newInstance;
}
foo();
