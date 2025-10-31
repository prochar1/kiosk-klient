class Config:
    ServerReceivePort = 9001
    ServerSendPort = 9002
    TotalTime = 3600
    RemainingTime = 3600

class AppFlags:
    debug = False
    frameless = True
    on_top = True

class Data:
    class GameModes:
        Individual = 'Individual'
        Group = 'Group'
    GameMode = GameModes.Individual

def parse_arguments(args):
    i = 0
    while i < len(args):
        arg = args[i].lower()
        try:
            if arg == '-inport' and i + 1 < len(args):
                Config.ServerReceivePort = int(args[i + 1])
                i += 1
            elif arg == '-outport' and i + 1 < len(args):
                Config.ServerSendPort = int(args[i + 1])
                i += 1
            elif arg == '-totaltime' and i + 1 < len(args):
                Config.TotalTime = int(args[i + 1])
                i += 1
            elif arg == '-remainingtime' and i + 1 < len(args):
                Config.RemainingTime = int(args[i + 1])
                i += 1
            elif arg == '-groupmode' and i + 1 < len(args):
                if args[i + 1].lower() == 'true':
                    Data.GameMode = Data.GameModes.Group
                i += 1
            elif arg == '-debug':
                AppFlags.debug = True
                AppFlags.frameless = False
                AppFlags.on_top = False
        except Exception as e:
            print(f"Chyba při zpracování argumentu {arg}: {e}")
        i += 1
