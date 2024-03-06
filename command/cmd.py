from command import operation

cmds = {
    "/help": lambda: operation.help(),
    "/exit": lambda: "exit",
    "/cls": lambda: operation.cls(),
    "/add": lambda: operation.add(),
    "/get": lambda: operation.get(),
    "/delete": lambda: operation.delete(),

}
