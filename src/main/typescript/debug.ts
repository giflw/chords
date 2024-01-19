export enum DebugLevel {
    OFF = 0, ERROR = 20, INFO = 50, ALL = 100
}

export class Debug {

    public level: DebugLevel = DebugLevel.ERROR;

    debugMatchers(regex: RegExp, line: string, found: boolean, value: string | undefined) {
        if (this.level >= DebugLevel.INFO || (this.level >= DebugLevel.ERROR && !found)) {
            console.table(
                [{ line, regex, found, value }],
                ["line", "regex", "found", "value"]
            );
        }
    }
}

export const DEBUG: Debug = new Debug();
export default DEBUG;