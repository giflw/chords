export class AbstractNode {
    type;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    constructor(type) {
        this.type = type;
    }
    isBlock() {
        return false;
    }
}
export class EmptyNode {
    static REGEX = /^(?<value>\s*)$/m;
    static INSTANCE = new EmptyNode();
    constructor() {
    }
    toString() {
        return "";
    }
}
export class SeparatorNode {
    static REGEX = /^(?<value>[\s]*[-]{4}[\s]*)$/m;
    static INSTANCE = new SeparatorNode();
    toString() {
        return "----";
    }
}
export class SimpleNode extends AbstractNode {
    _content;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    constructor(type, content) {
        super(type);
        this._content = content;
    }
    parse(text) {
        return new this.type(this._parse(text));
    }
    get content() {
        if (this._content) {
            return this._content;
        }
        throw new Error("Value not set");
    }
    set content(content) {
        this._content = content;
    }
    toString() {
        return `${this._content}`;
    }
}
export class CommentNode extends SimpleNode {
    static REGEX = /^(?<value>\s*\/\/.*)$/m;
    constructor(content) {
        super(CommentNode, content);
    }
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    _parse(text) {
        return text.split("//", 2)[1]?.trim() ?? "";
    }
    toString() {
        return `// ${this._content}`;
    }
}
export class BlockNode extends AbstractNode {
    nodes;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    constructor(type, nodes) {
        super(type);
        this.nodes = nodes;
    }
    isBlock() {
        return true;
    }
    toString() {
        return this.nodes?.map(n => n.toString()).reduce((p, c) => p + "\n" + c) ?? "";
    }
}
export class TitleNode extends SimpleNode {
    static REGEX = /^(?<value>= .*)$/m;
    constructor(value) {
        super(TitleNode, value);
    }
    _parse(text) {
        return (text.startsWith("=") ? text.substring(1) : text).trim();
    }
}
export class ArtistNode extends SimpleNode {
    static REGEX = /^(?<value>[\p{L}\p{M}\p{Zs}0-9:?!&,. _-]+)$/mu;
    constructor(value) {
        super(ArtistNode, value);
    }
    _parse(text) {
        return text.trim();
    }
}
export class DateTimeNode extends SimpleNode {
    static REGEX = /^(?<value>[0-9:/.TZz -]+)$/mu;
    constructor(value) {
        super(DateTimeNode, value);
    }
    _parse(text) {
        return text.trim();
    }
    asDate() {
        if (this._content !== undefined) {
            return new Date(this._content);
        }
        throw new Error("Date is not set");
    }
}
/**
 * :name: value
 *
 * :name: value
 * value
 */
export class AttributeNode extends SimpleNode {
    static REGEX = /^(?<value>:[a-zA-Z0-9_-]+:.*)$/s;
    constructor(nameOrEntry, value) {
        super(AttributeNode, nameOrEntry ? ((typeof nameOrEntry === "string") ? { name: nameOrEntry, value } : nameOrEntry) : undefined);
    }
    _parse(text) {
        // skip first : and split on second
        const parts = text.substring(1).replaceAll(/[ ]*[\r\n]+[ ]*[|][ ]*/g, " ").split(":", 2);
        return { name: parts[0], value: parts[1]?.trim() ?? "" };
    }
    get name() {
        if (this._content?.name) {
            return this._content.name;
        }
        throw new Error("Content/name not set");
    }
    set name(name) {
        this._content = this._content?.name !== undefined ?
            { name, value: this._content.value }
            : { name, value: undefined };
    }
    get value() {
        return this._content?.value;
    }
    set value(value) {
        if (this._content) {
            this._content.value = value;
        }
        throw new Error("Content/name not set");
    }
    toString() {
        return `${this.name}${this.value ? ": " + this.value : ""}`;
    }
    /**
     *
     * @returns value splitted by "," or given separator
     */
    asList(separator = ",") {
        return this._content?.value?.split(separator).map(s => s.trim()) ?? [];
    }
    /**
     *
     * @returns true if stringTrue ("true") or if not strict accept "" or undefined as true
     */
    asBoolean(stringTrue = "true", strict = false) {
        return this._content?.value === stringTrue || (!strict && (this._content?.value === "" || this._content?.value === undefined));
    }
    /**
     *
     * @param defaultIfUndefined default number to return if undefined value
     * @returns value as number if not undefined or default otherwise
     */
    asNumber(defaultIfUndefined = 0) {
        return this._content?.value !== undefined ? (this._content.value.includes(".") ? Number.parseFloat(this._content.value) : Number.parseInt(this._content.value)) : defaultIfUndefined;
    }
}
export class HeaderNode extends BlockNode {
    static REGEXES = [
        { factory: l => new CommentNode().parse(l), regex: CommentNode.REGEX },
        { factory: () => SeparatorNode.INSTANCE, regex: SeparatorNode.REGEX },
        { factory: l => new AttributeNode().parse(l), regex: AttributeNode.REGEX },
        { factory: l => new DateTimeNode().parse(l), regex: DateTimeNode.REGEX },
        { factory: l => new TitleNode().parse(l), regex: TitleNode.REGEX },
        { factory: () => EmptyNode.INSTANCE, regex: EmptyNode.REGEX },
        { factory: l => new ArtistNode().parse(l), regex: ArtistNode.REGEX }
    ];
    constructor(nodes) {
        super(HeaderNode, nodes);
    }
    split(text) {
        return text.split(/(?![\s]*[|]+)[\r\n]+/);
    }
    parse(text) {
        const nodes = this.split(text).map(text => {
            const pair = HeaderNode.REGEXES.find(pair => pair.regex.test(text));
            if (pair === undefined) {
                throw new Error(`Could not parse "${text}"`);
            }
            return pair.factory(text);
        });
        return new this.type(nodes);
    }
}
export class ContentNode extends BlockNode {
    constructor() {
        super(ContentNode);
    }
    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    parse(text) {
        throw new Error("Method not implemented.");
    }
}
export class DocumentNode extends BlockNode {
    source;
    constructor(nodes, source) {
        super(DocumentNode, nodes);
        this.source = source;
    }
    parse(source) {
        const [header,] = source.split(SeparatorNode.REGEX, 2);
        return new DocumentNode([new HeaderNode().parse(header), SeparatorNode.INSTANCE, new ContentNode()], source);
    }
}
/*
export default function parse(source: string): DocumentNode {
    return DocumentNode.parse(source);
}
*/ 
