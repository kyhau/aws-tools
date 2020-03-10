# Troubleshooting

### Runtime error "slice bounds out of range" on WSL
```
$ ./saml2aws
panic: runtime error: slice bounds out of range [308:282]
goroutine 1 [running]:
github.com/aulanov/go%2edbus.sessionBusPlatform(0xb2941e, 0x18, 0x0)
        /Users/markw/Code/go/pkg/mod/github.com/aulanov/go.dbus@v0.0.0-20150729231527-25c3068a42a0/conn_other.go:26 +0x1e9
github.com/aulanov/go%2edbus.SessionBusPrivate(0xd0, 0xabdb00, 0x760f498ce30b6501)
        /Users/markw/Code/go/pkg/mod/github.com/aulanov/go.dbus@v0.0.0-20150729231527-25c3068a42a0/conn.go:99 +0xa7
github.com/aulanov/go%2edbus.SessionBus(0x0, 0x0, 0x0)
        /Users/markw/Code/go/pkg/mod/github.com/aulanov/go.dbus@v0.0.0-20150729231527-25c3068a42a0/conn.go:76 +0xae
github.com/99designs/keyring.init.1()
        /Users/markw/Code/go/pkg/mod/github.com/99designs/keyring@v0.0.0-20190110203331-82da6802f65f/kwallet.go:18 +0x26
```

Solution:
`sudo apt-get remove dbus-x11`
