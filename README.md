repx
====
Python regular expression file transformer.

If you know `sed` or `awk` – or even `vim`'s search & replace functionality,
`repx` should feel familiar, but simpler and easier to use.

`repx` is similar to [sd](https://github.com/chmln/sd).

Usage
-----
By default `repx` will take input from _standard in_ and output the transformed text to _standard out_

```ShellSession
$ echo 'Hello World!' | repx /World/Universe/
Hello Universe!
```
    
File input is of course also supported

```ShellSession
$ cat in.txt
I like command line tools!
$ repx /like/love/ in.txt
I love command line tools!
```

Files can be transformed in-place with `-i`/`--in-place`

```ShellSession
$ cat in2.txt
I like turtles!
$ repx -i /like/love/ in.txt int2.txt
$ cat in.txt
I love command line tools!
$ cat in2.txt
I love turtles!
```

Backreferences are supported during substitution is supported, but backslash
escapes on the command line can be hard, so it can be helpful to use `\g<1>`
in place of `\1`:

```ShellSession
$ repx -i '/YAML(Reader|Writer)/JSON\1/' [files...] # Won't work
$ repx -i '/YAML(Reader|Writer)/JSON\g<1>/' [files...] # Will work
```


Typical use
-----------
Typical use is within a git repository and using the `-i` option.
`-i` will irreversibly change the files passed on the command line so
be sure to commit previous changes before running the command.
Usually you will use `repx`  in tandem with `git grep -l` like
so:

```ShellSession
$ repx -i /YAMLReader/JSONReader/ $(git grep -l YAML)
# All files in the git repository containing "YAML"
```
