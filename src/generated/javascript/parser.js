export class AbstractNode {
    constructor() {
    }
    isBlock() {
        return false;
    }
}
export class SimpleNode extends AbstractNode {
    _value;
    constructor(value) {
        super();
        this._value = value;
    }
    parse(text) {
        return this.constructor(this._parse(text));
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
        return `${this._value}`;
    }
}
export class BlockNode extends AbstractNode {
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
        super(value);
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
/**
 * :name: value
 *
 * :name: value
 * value
 */
export class AttributeNode extends SimpleNode {
    static REGEX = /^(?<value>:[a-zA-Z0-9_-]:.*)$/m;
    _name;
    constructor(name, value) {
        super(value);
        this._name = name;
    }
    _parse(text) {
        // skip first : and split on second
        const parts = text.substring(1).replaceAll(/[\r\n][ ]*[|]/, " ").split(":", 2);
        this._name = parts[0];
        return this._parse(parts[1]?.trim() ?? "");
    }
    get name() {
        if (this._name) {
            return this._name;
        }
        throw "Name not set";
    }
    set name(name) {
        this._name = name;
    }
    toString() {
        return `${this._name}${this._value ? ": " + this._value : ""}`;
    }
    /**
     *
     * @returns value splitted by "," or given separator
     */
    asList(separator = ",") {
        return this._value?.split(separator) ?? [];
    }
    /**
     *
     * @returns true if stringTrue ("true") or "" or undefined
     */
    asBoolean(stringTrue = "true") {
        return this._value === stringTrue || this._value === "" || this._value === undefined;
    }
    /**
     *
     * @param defaultIfUndefined default number to return if undefined value
     * @returns value as number if not undefined or default otherwise
     */
    asNumber(defaultIfUndefined = 0) {
        return this._value !== undefined ? (this._value.includes(".") ? Number.parseFloat(this._value) : Number.parseInt(this._value)) : defaultIfUndefined;
    }
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
