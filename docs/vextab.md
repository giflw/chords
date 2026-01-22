
# VexTab usage

This project supports embedding VexTab notation blocks via the `vextab` fenced block.

```vextab
tabstave notation=true
notes :q C/4
```

The rendered HTML will include an embedded container and an initialization script that will load the local VexTab file and render the notation. If the vendor file is missing, the block will fall back to showing the raw VexTab source and log an error to the console.

If you want the site to ship the vendor file under the generated `site/` directory, ensure your static site build step copies `chordsmd/assets/vendor/vextab.min.js` into `site/assets/chordsmd/vendor/` (the extension expects the file to be available under `/assets/chordsmd/vendor/`).
