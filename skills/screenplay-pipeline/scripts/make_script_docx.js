const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat,
  HeadingLevel, BorderStyle,
} = require("docx");

const FONT = { ascii: "Arial", hAnsi: "Arial", eastAsia: "Malgun Gothic" };
const inPath = process.argv[2];
if (!inPath || !fs.existsSync(inPath)) {
  console.error("usage: node make_script_docx.js <입력.md> [<출력.docx>]");
  if (inPath) console.error("not found: " + inPath);
  process.exit(1);
}
const outPath = process.argv[3] || inPath.replace(/\.md$/, ".docx");
const md = fs.readFileSync(inPath, "utf8");

function inlineRuns(text, extra = {}) {
  const parts = text.split(/(\*\*[^*]+\*\*)/g).filter(Boolean);
  return parts.map(p => {
    if (p.startsWith("**") && p.endsWith("**")) {
      return new TextRun({ text: p.slice(2, -2), bold: true, ...extra });
    }
    return new TextRun({ text: p, ...extra });
  });
}

const children = [];
let titleCount = 0;
const lines = md.split("\n");

for (let i = 0; i < lines.length; i++) {
  const line = lines[i].trimEnd();
  if (line.trim() === "") continue;

  // title (first = cover title; subsequent = part dividers on a new page)
  if (line.startsWith("# ")) {
    children.push(new Paragraph({
      style: "Title",
      pageBreakBefore: titleCount > 0,
      children: [new TextRun(line.slice(2))],
    }));
    titleCount++;
    continue;
  }

  // scene heading
  if (line.startsWith("## ")) {
    children.push(new Paragraph({
      heading: HeadingLevel.HEADING_2,
      children: inlineRuns(line.slice(3)),
    }));
    continue;
  }

  // montage sub-heading
  if (line.startsWith("### ")) {
    children.push(new Paragraph({
      spacing: { before: 200, after: 120 },
      children: [new TextRun({ text: line.slice(4), bold: true, color: "7030A0" })],
    }));
    continue;
  }

  // divider
  if (line.trim() === "---") {
    children.push(new Paragraph({
      spacing: { before: 120, after: 240 },
      border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: "BBBBBB", space: 1 } },
      children: [],
    }));
    continue;
  }

  // bullet (montage items)
  if (line.startsWith("- ")) {
    children.push(new Paragraph({
      numbering: { reference: "bullets", level: 0 },
      spacing: { after: 60, line: 300 },
      children: inlineRuns(line.slice(2), { color: "595959" }),
    }));
    continue;
  }

  // dialogue: **이름:** 대사
  const dlg = line.match(/^\*\*([^*]+):\*\*\s*(.*)$/);
  if (dlg) {
    children.push(new Paragraph({
      spacing: { after: 100, line: 320 },
      indent: { left: 400, hanging: 0 },
      children: [
        new TextRun({ text: dlg[1], bold: true }),
        new TextRun({ text: "   " }),
        ...inlineRuns(dlg[2]),
      ],
    }));
    continue;
  }

  // ending marker
  const endMark = line.trim().match(/^\*\*(— .+ —)\*\*$/);
  if (endMark) {
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 320, after: 200 },
      children: [new TextRun({ text: endMark[1], bold: true, size: 26 })],
    }));
    continue;
  }

  // stage direction (지문) — gray italic
  children.push(new Paragraph({
    spacing: { after: 80, line: 300 },
    children: inlineRuns(line, { color: "595959", italics: true }),
  }));
}

const doc = new Document({
  styles: {
    default: { document: { run: { font: FONT, size: 21 } } },
    paragraphStyles: [
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 25, bold: true, font: FONT, color: "1F3864" },
        paragraph: {
          spacing: { before: 360, after: 160 },
          outlineLevel: 1,
          border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "1F3864", space: 2 } },
        } },
      { id: "Title", name: "Title", basedOn: "Normal", next: "Normal",
        run: { size: 36, bold: true, font: FONT },
        paragraph: { spacing: { after: 240 }, alignment: AlignmentType.CENTER } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets",
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT,
            style: { paragraph: { indent: { left: 540, hanging: 300 } } } },
        ] },
    ],
  },
  sections: [{
    properties: {
      page: {
        size: { width: 11906, height: 16838 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 },
      },
    },
    children,
  }],
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync(outPath, buffer);
  console.log("done: " + outPath);
});
