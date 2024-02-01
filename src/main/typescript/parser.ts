export interface Node {
    // FIXME add source: string property
    toString(): string
}

export interface NodeRegexPair {
    factory: (line: string) => Node;
    regex: RegExp;
}

export interface Entry<T> {
    name: string
    value: T | undefined
}

export abstract class AbstractNode<N> implements Node {

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    constructor(protected type: { new(...args: any): N }) {
    }

    public abstract parse(text: string): N;

    public isBlock(): boolean {
        return false;
    }

    public abstract toString(): string;
}

export class EmptyNode implements Node {

    public static readonly REGEX: RegExp = /^(?<value>\s*)$/m;
    public static readonly INSTANCE: EmptyNode = new EmptyNode();

    private constructor() {
    }

    public toString(): string {
        return "";
    }
}

export class SeparatorNode implements Node {

    public static readonly REGEX: RegExp = /^(?<value>[\s]*[-]{4}[\s]*)$/m;
    public static readonly INSTANCE: SeparatorNode = new SeparatorNode();

    public toString(): string {
        return "----";
    }
}

export abstract class SimpleNode<T, S extends SimpleNode<T, S>> extends AbstractNode<S> {

    protected _content: T | undefined;

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    constructor(type: { new(...args: any): S }, content?: T) {
        super(type);
        this._content = content;
    }

    public parse(text: string): S {
        return new this.type(this._parse(text));
    }

    protected abstract _parse(text: string): T;

    public get content(): T {
        if (this._content) {
            return this._content;
        }
        throw new Error("Value not set");
    }
    protected set content(content: T) {
        this._content = content;
    }

    public toString(): string {
        return `${this._content}`;
    }
}

export class CommentNode extends SimpleNode<string, CommentNode> {

    public static readonly REGEX: RegExp = /^(?<value>\s*\/\/.*)$/m;

    constructor(content?: string) {
        super(CommentNode, content);
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    public override _parse(text: string): string {
        return text.split("//", 2)[1]?.trim() ?? "";
    }

    public override toString(): string {
        return `// ${this._content}`;
    }
}

export abstract class BlockNode<T extends BlockNode<T>> extends AbstractNode<T> {

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    constructor(type: { new(...args: any): T }, readonly nodes?: Node[]) {
        super(type);
    }

    public override isBlock(): boolean {
        return true;
    }

    public override toString(): string {
        return this.nodes?.map(n => n.toString()).reduce((p, c) => p + "\n" + c) ?? "";
    }
}

export class TitleNode extends SimpleNode<string, TitleNode> {

    public static readonly REGEX: RegExp = /^(?<value>= .*)$/m;

    public constructor(value?: string) {
        super(TitleNode, value);
    }

    protected _parse(text: string): string {
        return (text.startsWith("=") ? text.substring(1) : text).trim();
    }
}

export class ArtistNode extends SimpleNode<string, ArtistNode> {
    public static readonly REGEX: RegExp = /^(?<value>[\p{L}\p{M}\p{Zs}0-9:?!&,. _-]+)$/mu;

    public constructor(value?: string) {
        super(ArtistNode, value);
    }

    protected _parse(text: string): string {
        return text.trim();
    }
}

export class DateTimeNode extends SimpleNode<string, DateTimeNode> {
    public static readonly REGEX: RegExp = /^(?<value>[0-9:/.TZz -]+)$/mu;

    public constructor(value?: string) {
        super(DateTimeNode, value);
    }

    protected _parse(text: string): string {
        return text.trim();
    }

    public asDate(): Date {
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
export class AttributeNode extends SimpleNode<Entry<string>, AttributeNode> {

    public static readonly REGEX: RegExp = /^(?<value>:[a-zA-Z0-9_-]+:.*)$/s;

    public constructor(nameOrEntry?: string | Entry<string>, value?: string) {
        super(AttributeNode, nameOrEntry ? ((typeof nameOrEntry === "string") ? { name: nameOrEntry, value } : nameOrEntry) : undefined);
    }

    protected _parse(text: string): Entry<string> {
        // skip first : and split on second
        const parts = text.substring(1).replaceAll(/[ ]*[\r\n]+[ ]*[|][ ]*/g, " ").split(":", 2);
        return { name: parts[0], value: parts[1]?.trim() ?? "" };
    }

    public get name(): string {
        if (this._content?.name) {
            return this._content.name;
        }
        throw new Error("Content/name not set");
    }
    protected set name(name: string) {
        this._content = this._content?.name !== undefined ?
            { name, value: this._content.value }
            : { name, value: undefined };
    }

    public get value(): string | undefined {
        return this._content?.value;
    }
    protected set value(value: string | undefined) {
        if (this._content) {
            this._content.value = value;
        }
        throw new Error("Content/name not set");
    }

    public override toString(): string {
        return `${this.name}${this.value ? ": " + this.value : ""}`;
    }

    /**
     * 
     * @returns value splitted by "," or given separator
     */
    public asList(separator: string = ","): string[] {
        return this._content?.value?.split(separator).map(s => s.trim()) ?? [];
    }

    /**
     * 
     * @returns true if stringTrue ("true") or if not strict accept "" or undefined as true
     */
    public asBoolean(stringTrue: string = "true", strict: boolean = false): boolean {
        return this._content?.value === stringTrue || (
            !strict && (this._content?.value === "" || this._content?.value === undefined)
        );
    }

    /**
     * 
     * @param defaultIfUndefined default number to return if undefined value
     * @returns value as number if not undefined or default otherwise
     */
    public asNumber(defaultIfUndefined: number = 0): number {
        return this._content?.value !== undefined ? (
            this._content.value.includes(".") ? Number.parseFloat(this._content.value) : Number.parseInt(this._content.value)
        ) : defaultIfUndefined;
    }

}

export class HeaderNode extends BlockNode<HeaderNode> {

    public static readonly REGEXES: NodeRegexPair[] = [
        { factory: l => new CommentNode().parse(l), regex: CommentNode.REGEX },
        { factory: () => SeparatorNode.INSTANCE, regex: SeparatorNode.REGEX },
        { factory: l => new AttributeNode().parse(l), regex: AttributeNode.REGEX },
        { factory: l => new DateTimeNode().parse(l), regex: DateTimeNode.REGEX },
        { factory: l => new TitleNode().parse(l), regex: TitleNode.REGEX },
        { factory: () => EmptyNode.INSTANCE, regex: EmptyNode.REGEX },
        { factory: l => new ArtistNode().parse(l), regex: ArtistNode.REGEX }
    ];

    constructor(nodes?: Node[]) {
        super(HeaderNode, nodes);
    }

    public split(text: string): string[] {
        return text.split(/(?![\s]*[|]+)[\r\n]+/);
    }

    public override parse(text: string): HeaderNode {
        const nodes: Node[] = this.split(text).map(text => {
            const pair: NodeRegexPair | undefined = HeaderNode.REGEXES.find(pair => pair.regex.test(text));
            if (pair === undefined) {
                throw new Error(`Could not parse "${text}"`);
            }
            return pair.factory(text);
        });
        return new this.type(nodes);
    }

}

export class ContentNode extends BlockNode<ContentNode> {

    constructor() {
        super(ContentNode);
    }

    // eslint-disable-next-line @typescript-eslint/no-unused-vars
    public override parse(text: string): ContentNode {
        throw new Error("Method not implemented.");
    }

}


export class DocumentNode extends BlockNode<DocumentNode> {

    constructor(nodes?: Node[], readonly source?: string) {
        super(DocumentNode, nodes);
    }

    public parse(source: string): DocumentNode {
        const [header,] = source.split(SeparatorNode.REGEX, 2);
        return new DocumentNode(
            [new HeaderNode().parse(header), SeparatorNode.INSTANCE, new ContentNode()],
            source
        );
    }
}

/*
export default function parse(source: string): DocumentNode {
    return DocumentNode.parse(source);
}
*/