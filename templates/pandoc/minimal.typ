// Minimal typst template for CV / cover letter PDFs
// Used via: pandoc input.md -o output.pdf --pdf-engine=typst --template=templates/pandoc/minimal.typ

#let (
  title: title = none,
  date: date = none,
  author: author = none,
) = {}

#set document(title: title, author: author)

#set page(
  paper: "a4",
  margin: (top: 0.75in, bottom: 0.75in, left: 0.85in, right: 0.85in),
)

#set text(
  font: "Helvetica Neue",
  size: 10.5pt,
  lang: "en",
)

#set par(
  leading: 0.65em,
  justify: false,
  spacing: 0.8em,
)

#show heading.where(level: 1): it => {
  set text(size: 18pt, weight: "bold")
  set par(leading: 0.4em, spacing: 0.4em)
  it
}

#show heading.where(level: 2): it => {
  set text(size: 12pt, weight: "bold")
  set par(spacing: 0.4em)
  it
}

#show heading.where(level: 3): it => {
  set text(size: 11pt, weight: "bold")
  set par(spacing: 0.3em)
  it
}

#show heading.where(level: 4): it => {
  set text(size: 10.5pt, weight: "bold", style: "italic")
  it
}

#set list(indent: 0.5em, body-indent: 0.5em, spacing: 0.4em)

#show link: set text(fill: rgb("#0066cc"))

#align(left)[
  #if title != none [
    #text(size: 20pt, weight: "bold")[#title]
    #v(0.2em)
  ]
  #if author != none [
    #text(size: 12pt)[#author]
    #v(0.2em)
  ]
  #if date != none [
    #text(size: 10pt, fill: gray.darken(20%))[#date]
    #v(0.6em)
  ]
]

#if title != none or author != none or date != none [
  #line(length: 100%, stroke: 0.5pt + gray.darken(30%))
  #v(0.4em)
]

#doc
