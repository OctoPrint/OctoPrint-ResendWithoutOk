# OctoPrint-ResendWithoutOk

This plugin add support for firmwares that do not send an `ok` after
sending a resend request.

With such firmwares, OctoPrint 1.2.10 will wait for a `ok` that never
comes and run into one communication timeout after the other, instead
of just resending the requested line.

Sadly, while most firmwares do send an `ok` after a resend request,
some don't (and in fact, since a resend request does actually constitute
a communication error, not sending one makes more sense). OctoPrint is
very strict when it comes to sending lines to the printer without it
signaling to be ready for that (through an `ok`) and hence by default
therefore has issues with firmwares that do not have an `ok` following
a resend request.

This plugin solves that by simply monkey patching OctoPrint resend
processing method to also simulate an `ok` after each received resend
request, solving the issue that way.

## So when do I need this again?

If you see something like this in the Terminal tab:

```
Recv: Error:Line Number is not Last Line Number+1, Last Line: 11983
Recv: Resend: 11984
Communication timeout while printing and during an active resend,
resending same line again to trigger response from printer. Configure
long running commands or increase communication timeout if that happens
regularly on specific commands or long moves.
```

it means your firmware is not sending an `ok` after a resend and
OctoPrint therefore runs into a timeout and can't proceed.

In such a case, installing this plugin will solve the issue:

```
Recv: Error:Line Number is not Last Line Number+1, Last Line: 11983
Recv: Resend: 11984
Send: N11984 M27*19
Recv: SD printing byte 7374208/12773026
Recv: ok
...
```

## Setup

Install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/OctoPrint/OctoPrint-ResendWithoutOk/archive/master.zip

