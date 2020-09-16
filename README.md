# LSP-flow

This is a helper package that sets up the correct configuration for starting
flow automatically. This package doesn't download any binaries. It expects
one of your folders in your window to contain:

- a .flowconfig file
- a node_modules/.bin/flow file (or symbolic link)

If there exists a folder where both of these conditions are met, only then is
your flow language server started.
