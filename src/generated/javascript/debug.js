export var DebugLevel;
(function (DebugLevel) {
    DebugLevel[DebugLevel["OFF"] = 0] = "OFF";
    DebugLevel[DebugLevel["ERROR"] = 20] = "ERROR";
    DebugLevel[DebugLevel["INFO"] = 50] = "INFO";
    DebugLevel[DebugLevel["ALL"] = 100] = "ALL";
})(DebugLevel || (DebugLevel = {}));
export class Debug {
    level = DebugLevel.ERROR;
    debugMatchers(regex, line, found, value) {
        if (this.level >= DebugLevel.INFO || (this.level >= DebugLevel.ERROR && !found)) {
            console.table([{ line, regex, found, value }], ["line", "regex", "found", "value"]);
        }
    }
}
export const DEBUG = new Debug();
export default DEBUG;
