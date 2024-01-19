export var AST;
(function (AST) {
    AST.debug = true;
    class Node {
        static of(type, args) {
            let instance = Object.create(type.prototype);
            instance.constructor.call(instance, args);
            return instance;
        }
    }
    AST.Node = Node;
    class EmptyNode extends Node {
    }
    AST.EmptyNode = EmptyNode;
    class MetaNode extends Node {
    }
    AST.MetaNode = MetaNode;
    class AnnotationNode extends Node {
    }
    AST.AnnotationNode = AnnotationNode;
    class BlockNode extends Node {
        name;
        blocks;
        constructor(name, blocks) {
            super();
            this.name = name;
            this.blocks = blocks;
        }
    }
    AST.BlockNode = BlockNode;
    class RootNode extends Node {
        source;
        blocks;
        constructor(text, blocks) {
            super();
            this.source = text;
            this.blocks = blocks;
        }
    }
    AST.RootNode = RootNode;
    AST.REGEXES = [
        { clazz: EmptyNode, regex: /^(?<value>\s*)$/m },
        { clazz: BlockNode, regex: /^\[(?<value>[\p{L}\p{M}\p{Zs}0-9: -]+)\]$/um }
    ];
    // FIXME move to Debug object, add logger
    function debugMatchers(regex, line, found, value) {
        if (AST.debug) {
            console.log(`"${line}"`, regex, found, `"${value}"`);
        }
    }
    function parseLine(line) {
        let value = undefined;
        let pair = AST.REGEXES.find(pair => {
            value = pair.regex.exec(line)?.groups?.value;
            const found = value !== undefined;
            debugMatchers(pair.regex, line, found, value);
            return found;
        });
        if (!pair) {
            throw `Line matched no node: ${line}`;
        }
        return Node.of(pair.clazz, [line]);
    }
    AST.parseLine = parseLine;
})(AST || (AST = {}));
export default function parse(source) {
    source.split(/[\r\n]/).map(AST.parseLine);
    return new AST.RootNode(source, []);
}
