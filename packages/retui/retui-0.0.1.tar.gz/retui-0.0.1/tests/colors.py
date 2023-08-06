#!/usr/bin/env python3
import time

import retui


def test(handle_sigint=True, demo_time_s=None, title=None) -> int:
    print(title)
    cv = retui.App()
    if cv.color_mode() is False:
        print("Abort")
        return -1

    print("\x1B[34m" + "TEST 8bit ANSII Codes" + "\x1B[0m")
    retui.Test.ColorLine(0, 8, use_color=True, width=2)
    retui.Test.ColorLine(8, 16, use_color=True, width=2)
    for red in range(0, 6):
        start = 16 + 6 * 6 * red
        end = start + 36
        retui.Test.ColorLine(start, end, use_color=True, width=3)

    retui.Test.ColorLine(232, 256, use_color=True, width=4)

    brush = retui.Brush()

    test_color = retui.ConsoleColor(retui.Color(14, retui.ColorBits.Bit8), retui.Color(4, retui.ColorBits.Bit8))

    brush.SetBgColor(test_color.bgcolor)
    brush.SetFgColor(test_color.fgcolor)
    print("TEST", end="")
    brush.Reset()
    print()

    brush.print("TEST2", color=test_color, end="\n")
    if demo_time_s:
        time.sleep(demo_time_s)


if __name__ == "__main__":
    test()
