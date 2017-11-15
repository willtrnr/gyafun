gyafun
======

A little experiment with making a simple stack based virtual machine (kinda of
like the JVM) because I do whatever I want.

Since its implemented on Python it kind of inherits the dynamic typing features
as an unintended feature, kind of frees me from writing typed opcodes.

Right now there's only a pretty cheapo assembler available to craft bytecode,
but the idea is to eventually have a compiler (a basic one at least).

The goal is just to have something barely functional just for fun, there's no
real plan for this.

Design
------

Uses 1 byte opcodes with a variable amount of 2 bytes arguments little-endian
encoded. This makes parsing the bytecode very easy and consistent.

"Native" types are (same as Python really):

  * int
  * float (needs better support, can't even set as constant)
  * string (needs better support, mostly cheating with native calls)
  * list
  * map
  * *set* (in consideration)

A constant pool is used to store int and string values and all opcode arguments
refer to an index in it except for `INC` and `DEC` which uses the argument as a
literal value and `IVK` which is using the loaded code pool instead.

There is also a symbol map whose current purpose is only to find the `main`
procedure, but could be extended to support dynamic linking like features.

As mentionned before the code pool stores the executable bytecode, but also
links to native functions (which are currently used as "cheats", but also for
real native IO operations).

Using
-----

This needs Python 3.2+ since it uses the `from/to_bytes` stuff on `int`, also
the `regex` lib as in the `requirements.txt`.

Wanna-be assembly files can be "assembled" using (multiple files can be passed)

    python assembler.py files...

And the `a.out` can be executed with

    python main.py a.out args...

Be aware that the opcode values are changed a lot to keep related things
together and binary compatibility is pretty much useless right now since no
executables are kept long enough for that.
