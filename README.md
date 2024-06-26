<h1>Vex SnipFuzz</h1>
<p><em>Houdini shelf tool (assigned to Alt+f in this demo)</em><br>
fuzzy search a text file containing VEX snippets and paste into selected wrangle node<br>
Keys:<br>
- <code>up</code> next snippet <br>
- <code>down</code> previous snippet <br>
- <code>ctrl/enter</code> paste into wrangle's textfield / or copy to clipboard (CLI version)<br>
- <code>alt</code> switch to hashtag mode search mode<br>
- <code>shift</code> switch to case sensitive search (default is OFF)<br>

- <code>left</code> jump to first snippet (CLI only)<br>
- <code>right</code> jump to last snippet (CLI only)<br>

Installation (Houdini)
----------------------
- copy <code>snipfuzz.ui</code> and <code>vex.c</code> to a directory on your computer (install_dir)
- edit snipfuzz_hou.py and change the <code>install_dir</code> path at the top of the file
- in Houdini create a new shelf tool and paste the content of the updated snipfuzz_hou.py
- select any wrangle node and click on the shelf tool or assign a keyboard shortcut, for example: Alt+f

![](https://github.com/jdvfx/vex_snipfuzz/blob/main/gif/snipfuzz.gif)


note: CLI versions require X.org, does not work with Wayland!
![](https://github.com/jdvfx/vex_snipfuzz/blob/main/gif/snipfuzz_cli.gif)
