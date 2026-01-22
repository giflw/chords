# Fountain Screenplay Format

**Extension:** `FountainExtension`  
**Syntax:** ` ```fountain `  
**Config Option:** `fountain` (enabled by default)

## Overview

Complete implementation of the [Fountain screenplay format](https://fountain.io/syntax/) specification for writing screenplays in plain text.

## Format Specification

### Scene Headings

**Automatic Detection:**
Lines starting with: `INT`, `EXT`, `EST`, `INT./EXT`, `INT/EXT`, `I/E` (case insensitive)

```fountain
INT. COFFEE SHOP - DAY
EXT. PARK - NIGHT
INT./EXT. CAR - CONTINUOUS
```

**Forced Scene Heading:**
Prefix with a period (`.`)

```fountain
.SNIPER SCOPE POV
.FLASHBACK
```

**Scene Numbers:**
Append with `#number#` (automatically stripped)

```fountain
INT. HOUSE - DAY #1#
INT. HOUSE - DAY #1A#
INT. HOUSE - FLASHBACK (1944) #110A#
```

### Characters

**Automatic Detection:**
- Line in ALL CAPS
- Preceded by blank line
- NOT followed by blank line

```fountain
JOHN
Hello there.

SARAH
(smiling)
You're late.
```

**Character Extensions:**
Parenthetical notations after character name

```fountain
MOM (O.S.)
Luke! Come down for supper!

HANS (on the radio)
What was it you said?
```

**Forced Character:**
Prefix with `@` to preserve mixed case

```fountain
@McCLANE
Yippie ki-yay!
```

### Dialogue

Text following a Character or Parenthetical element.

```fountain
SANBORN
A good 'ole boy. You know, loves the Army,
blood runs green. Country boy. Seems solid.
```

### Parentheticals

Wrapped in parentheses, between Character and Dialogue.

```fountain
STEEL
(starting the engine)
So much for retirement!
```

### Dual Dialogue

Add `^` after second character name for simultaneous dialogue.

```fountain
BRICK
Screw retirement.

STEEL ^
Screw retirement.
```

### Action

Any paragraph that doesn't meet other element criteria.

```fountain
They drink long and well from the beers.

And then there's a long beat.
Longer than is funny.
```

**Forced Action:**
Prefix with `!` when action is in uppercase

```fountain
!BRICK THROWS THE BOOK
```

### Transitions

**Automatic Detection:**
- ALL CAPS
- Ends with `TO:`
- Preceded and followed by blank line

```fountain
CUT TO:

FADE TO:

DISSOLVE TO:
```

**Forced Transition:**
Prefix with `>`

```fountain
>Burn to White.
```

### Lyrics

Lines starting with `~`

```fountain
~Willy Wonka! Willy Wonka!
~The amazing chocolatier!
```

### Centered Text

Wrapped in `>` and `<`

```fountain
>THE END<

> **TITLE CARD** <
```

### Page Breaks

Three or more equals signs

```fountain
===
```

### Title Page

Key-value pairs at document start

```fountain
Title: BRICK & STEEL
Subtitle: FULL RETIRED
Credit: Written by
Author: Stu Maschwitz
Draft date: 1/20/2012
Contact:
    Next Level Productions
    1588 Mission Dr.
    Solvang, CA 93463
```

**Supported Keys:**
- `Title`, `Subtitle`, `Credit`, `Author(s)`
- `Source`, `Draft date`, `Contact`
- `Copyright`, `Notes`

### Notes

Enclosed in double brackets (stripped from output)

```fountain
INT. TRAILER HOME - DAY

This is the home of THE BOY BAND, AKA DAN and JACK[[Or did we think of actual names for these guys?]].
```

### Emphasis

Following Markdown conventions:

```fountain
*italic*
**bold**
***bold italic***
_underline_
```

**Combined emphasis:**

```fountain
From what seems like only INCHES AWAY. _Steel's face FILLS the *Leupold Mark 4* scope_.
```

**Escaping:**

```fountain
Steel enters the code on the keypad: **\*9765\***
```

## Complete Example

```fountain
Title: My Screenplay
Author: John Doe
Draft date: 1/22/2026

INT. COFFEE SHOP - DAY

The morning rush is over. A few patrons sit scattered about.

JOHN enters, looking around nervously.

SARAH sits at a corner table, coffee in hand. She waves.

SARAH
(smiling)
You're late.

JOHN
Traffic was terrible.

He sits down across from her.

SARAH
I ordered for you.

She slides a coffee across the table.

JOHN
Thanks. Listen, about last night...

SARAH
(interrupting)
We don't have to talk about it.

JOHN
But I want to.

A long beat. They look at each other.

>**TITLE CARD: THREE YEARS LATER**<

FADE TO:

EXT. PARK - DAY

===
```

## CSS Classes

- `.fountain-screenplay` - Main container
- `.title-page` - Title page container
- `.title-*` - Title page elements (title, author, etc.)
- `.scene-heading` - Scene headings
- `.character` - Character names
- `.character.dual` - Dual dialogue character
- `.dialogue` - Dialogue text
- `.parenthetical` - Parentheticals
- `.action` - Action/description
- `.transition` - Transitions
- `.centered` - Centered text
- `.lyrics` - Lyrics
- `.page-break` - Page breaks
- `.blank-line` - Blank lines

## Styling

Fountain output uses Courier New font and standard screenplay formatting:
- **Scene headings**: Bold, uppercase
- **Character names**: Bold, uppercase, indented 2in
- **Dialogue**: Indented 1.5in left, 1.5in right
- **Parentheticals**: Indented 1.8in left
- **Transitions**: Bold, uppercase, right-aligned
- **Centered text**: Center-aligned
- **Lyrics**: Italic, indented 2in
