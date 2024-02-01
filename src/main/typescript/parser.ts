export interface NodeRegexPair<T> {
    factory: (value: string) => AbstractNode<T>;
    regex: RegExp;
}

export interface Entry<T> {
    name: string
    value: T | undefined
}

export abstract class AbstractNode<T> {

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    constructor(protected type: { new(...args: any): T }) {
    }

    public isBlock(): boolean {
        return false;
    }

    public abstract toString(): string;
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

export abstract class BlockNode extends AbstractNode<BlockNode> {
    protected abstract parseChildren(): void;

    public override isBlock(): boolean {
        return true;
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
        } throw new Error("Date is not set");
    }
}

/**
 * :name: value
 * 
 * :name: value
 * value
 */
export class AttributeNode extends SimpleNode<Entry<string>, AttributeNode> {

    public static readonly REGEX: RegExp = /^(?<value>:[a-zA-Z0-9_-]:.*)$/m;

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
        throw new Error(`Line matched no node: ${line}`);
    }
    const node = pair.factory(value, index, array);
    return node;
}

export default function parse(source: string): DocumentNode {
    return DocumentNode.parse(source);
}
*/
