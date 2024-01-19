
let _debug = true;
export function debug(debug: boolean = true) {
    _debug = debug;
}

export abstract class Node {
    constructor(public readonly value: string) {
    }

    public isBlock(): boolean {
        return false;
    }

    public toString(): string {
        return this.value;
    }
}

export class EmptyNode extends Node { 
    public static readonly INSTANCE: EmptyNode = new EmptyNode(); 
    private constructor() {
        super("");
    }
}

export class MetaNode extends Node { }

export class AnnotationNode extends Node { }

export class BlockNode extends Node {

    readonly blocks: Node[];

    constructor(name: string) {
        super(name);
        this.blocks = [];
    }

    public isBlock(): boolean {
        return true;
    }
}

export class RootNode extends Node {
    readonly source: string;
    readonly nodes: Node[];

    constructor(source: string, nodes: Node[]) {
        super(source);
        this.source = source;
        this.nodes = nodes;
    }
}

interface NodeRegexPair {
    clazz: (value: string) => Node;
    regex: RegExp;
}

export const REGEXES: NodeRegexPair[] = [
    { clazz: () => EmptyNode.INSTANCE, regex: /^(?<value>\s*)$/m },
    { clazz: (value: string) => new BlockNode(value), regex: /^\[(?<value>[\p{L}\p{M}\p{Zs}0-9: -]+)\]$/um }
];

// FIXME move to Debug object, add logger
function debugMatchers(regex: RegExp, line: string, found: boolean, value: string | undefined) {
    if (_debug) {
        console.log(`"${line}"`, regex, found, `"${value}"`);
    }
}

export function parseLine(line: string): Node {
    let value: string | undefined = undefined;
    const pair: NodeRegexPair | undefined = REGEXES.find(pair => {
        value = pair.regex.exec(line)?.groups?.value;
        const found = value !== undefined;
        debugMatchers(pair.regex, line, found, value);
        return found;
    });
    if (!pair || value === undefined) {
        throw `Line matched no node: ${line}`;
    }
    const node = pair.clazz(value);
    console.log("NODE", node);
    return node;
}

export default function parse(source: string): RootNode {
    source.split(/[\r\n]/).map(parseLine);
    return new RootNode(source, []);
}