prex
====
Python regular expression file transformer.

If you know `sed` or `awk` – or even `vim`'s search & replace functionality,
`prex` should feel familiar, but simpler and easier to use.

Usage
-----
By default `prex` will take input from _standard in_ and output the transformed text to _standard out_

```bash
$ echo 'Hello World!' | prex /World/Universe/
Hello Universe
```
    
File input and output is of course also supported

```bash
$ cat in.txt
I like command line tools!
$ prex /like/love/ in.txt -o out.txt
$ cat out.txt
I love command line tools!
```

Files can be transformed in-place (use `-f` or `--force` to skip the confirmation)

```bash
$ prex -p /like/love/ in.txt
Do you really want to replace the contents of `in.txt`,
-- the content will permanently and irrevocably be changed!
Type `in.txt` to replace the file: in.txt (user input)
$ cat in.txt
I love command line tools!
```
