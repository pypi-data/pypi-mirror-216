#!/usr/bin/env python3


import threed_optix.api as opt


def main():
    api = opt.ThreedOptixAPI('e31aeeae-e9b0-436c-abba-735ee10cee8e')

    setups = api.get_setups()
    print("setups:")
    for s in setups:
        print(f"\t{s}")
    print("\n")

    s = setups[0]
    api.fetch(s)
    print(f"parts in setup '{s}'")
    for p in s.parts:
        print(f"\t{p}")

    p = s.parts[0]
    api.fetch(p)
    p.pose.position.x += 33.66
    api.update(p)

    r = api.run(s)
    api.fetch(r)
    print(r.data)


if __name__ == '__main__':
    main()
